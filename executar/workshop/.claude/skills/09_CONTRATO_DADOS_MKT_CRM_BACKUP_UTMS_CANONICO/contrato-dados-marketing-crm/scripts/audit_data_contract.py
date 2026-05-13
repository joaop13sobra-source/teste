#!/usr/bin/env python3
"""Audit marketing to CRM data contract coverage."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "lead_id",
    "first_utm_source",
    "first_utm_medium",
    "first_utm_campaign",
    "last_utm_source",
    "last_utm_medium",
    "last_utm_campaign",
    "v4_client_id",
    "v4_campaign_id",
    "v4_adgroup_id",
    "v4_creative_id",
    "v4_test_id",
}

REQUIRED_N2 = [
    "backup_padronizado",
    "utms_chegam_conversao",
    "ids_chegam_planilha",
    "crm_recebe_origem_ou_match",
    "first_last_touch_preservados",
    "dicionario_dados_existe",
    "teste_ponta_a_ponta_existe",
    "analise_pos_campanha_possivel",
]


def load_payload(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def field_names(payload: dict[str, Any]) -> set[str]:
    fields = payload.get("campos", [])
    if not isinstance(fields, list):
        raise ValueError("'campos' must be a list.")
    return {str(item.get("campo", "")).strip() for item in fields if isinstance(item, dict)}


def audit(payload: dict[str, Any]) -> list[dict[str, str]]:
    names = field_names(payload)
    n2 = payload.get("criterios_n2", {})
    if not isinstance(n2, dict):
        n2 = {}
    rows: list[dict[str, str]] = []

    for field in sorted(REQUIRED_FIELDS):
        rows.append({
            "tipo": "campo",
            "item": field,
            "status": "ok" if field in names else "gap",
            "severidade": "alta" if field not in names else "ok",
            "acao": "Adicionar ao dicionario e ao fluxo form/backup/CRM." if field not in names else "Manter.",
        })

    for criterion in REQUIRED_N2:
        ok = bool(n2.get(criterion))
        rows.append({
            "tipo": "criterio_n2",
            "item": criterion,
            "status": "ok" if ok else "gap",
            "severidade": "critica" if not ok else "ok",
            "acao": "Resolver antes de considerar contrato N2." if not ok else "Manter evidencia.",
        })
    return rows


def decision(rows: list[dict[str, str]]) -> str:
    critical = sum(1 for row in rows if row["severidade"] == "critica")
    high = sum(1 for row in rows if row["severidade"] == "alta")
    if critical:
        return "nao_n2"
    if high:
        return "n2_parcial"
    return "n2"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["tipo", "item", "status", "severidade", "acao"])
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, payload: dict[str, Any], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Auditoria Do Contrato De Dados",
        "",
        f"- Cliente: {payload.get('cliente', '')}",
        f"- Contrato: {payload.get('contrato', '')}",
        f"- Decisão: {decision(rows)}",
        "",
        "| tipo | item | status | severidade | ação |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['tipo']} | `{row['item']}` | {row['status']} | {row['severidade']} | {row['acao']} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit data contract coverage.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--md", dest="md_path", type=Path)
    parser.add_argument("--csv", dest="csv_path", type=Path)
    args = parser.parse_args()

    payload = load_payload(args.input_json)
    rows = audit(payload)
    if not args.md_path and not args.csv_path:
        print(decision(rows))
        return
    if args.csv_path:
        write_csv(args.csv_path, rows)
    if args.md_path:
        write_markdown(args.md_path, payload, rows)


if __name__ == "__main__":
    main()
