#!/usr/bin/env python3
"""Compare expected URL tracking parameters against backup and CRM captures."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


FIELDS = [
    "camada",
    "campo",
    "esperado",
    "capturado",
    "status",
    "severidade",
]

REQUIRED_FIELDS = [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "v4_client_id",
    "v4_campaign_id",
    "v4_adgroup_id",
    "v4_creative_id",
    "v4_test_id",
]

RULE_LABELS = {
    "first_touch_preserved": "First-touch preservado",
    "last_touch_updates": "Last-touch atualiza",
    "dedupe_ok": "Dedupe ok",
    "conversion_event_ok": "Evento de conversão ok",
    "export_match_ok": "Export permite match",
}


def parse_url_params(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    values = parse_qs(parsed.query)
    return {key: value[0] for key, value in values.items() if value}


def compare_layer(expected: dict[str, str], captured: dict[str, Any], layer: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for field in REQUIRED_FIELDS:
        expected_value = expected.get(field, "")
        captured_value = str(captured.get(field, "")).strip()
        ok = expected_value == captured_value
        rows.append({
            "camada": layer,
            "campo": field,
            "esperado": expected_value,
            "capturado": captured_value,
            "status": "ok" if ok else "erro",
            "severidade": "baixo" if ok else ("bloqueador" if field.startswith("v4_") or field == "utm_content" else "alto"),
        })
    return rows


def compare_rules(rules: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for field, label in RULE_LABELS.items():
        value = bool(rules.get(field))
        rows.append({
            "camada": "rules",
            "campo": label,
            "esperado": "true",
            "capturado": str(value).lower(),
            "status": "ok" if value else "erro",
            "severidade": "baixo" if value else "bloqueador",
        })
    return rows


def decision(rows: list[dict[str, str]]) -> str:
    severities = {row["severidade"] for row in rows if row["status"] != "ok"}
    if "bloqueador" in severities:
        return "no-go"
    if "alto" in severities:
        return "go-com-risco"
    if "medio" in severities:
        return "go-com-risco"
    return "go"


def load_rows(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    url = str(payload.get("url", "")).strip()
    if not url:
        raise ValueError("JSON must contain 'url'.")
    expected = parse_url_params(url)
    missing = [field for field in REQUIRED_FIELDS if field not in expected]
    if missing:
        raise ValueError(f"URL is missing required params: {', '.join(missing)}")

    rows = []
    rows.extend(compare_layer(expected, payload.get("backup", {}), "backup"))
    rows.extend(compare_layer(expected, payload.get("crm", {}), "crm"))
    rows.extend(compare_rules(payload.get("rules", {})))
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_markdown(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# QA Tracking UTM CRM",
        "",
        f"- Decisão: `{decision(rows)}`",
        "",
        "| " + " | ".join(FIELDS) + " |",
        "| " + " | ".join("---" for _ in FIELDS) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_md(row[field]) for field in FIELDS) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare expected UTM params against backup and CRM captures.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--md", dest="md_path", type=Path)
    parser.add_argument("--csv", dest="csv_path", type=Path)
    args = parser.parse_args()

    rows = load_rows(args.input_json)
    if not args.md_path and not args.csv_path:
        print(decision(rows))
        return
    if args.md_path:
        write_markdown(rows, args.md_path)
    if args.csv_path:
        write_csv(rows, args.csv_path)


if __name__ == "__main__":
    main()
