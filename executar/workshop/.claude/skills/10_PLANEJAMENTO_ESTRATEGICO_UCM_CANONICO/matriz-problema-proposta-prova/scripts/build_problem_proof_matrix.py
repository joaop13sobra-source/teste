#!/usr/bin/env python3
"""Build a problem-proposition-proof matrix from JSON."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


FIELDS = [
    "prioridade", "score", "problema", "impacto", "voz_cliente", "persona", "stage", "proposta",
    "mecanismo", "promessa", "objecao", "prova", "status_prova", "claim_pendente", "risco",
]


def load_payload(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def as_int(item: dict[str, Any], field: str) -> int:
    try:
        return int(item.get(field, 0) or 0)
    except ValueError:
        return 0


def score(item: dict[str, Any]) -> int:
    return (
        as_int(item, "impacto_score") * 2
        + as_int(item, "frequencia_score")
        + as_int(item, "evidencia_score")
        - as_int(item, "risco_score")
    )


def is_claim_pending(item: dict[str, Any]) -> bool:
    status = str(item.get("status_prova", "")).strip().lower()
    proof = str(item.get("prova", "")).strip()
    return status in {"ausente", "restrita"} or proof == ""


def build_rows(payload: dict[str, Any]) -> list[dict[str, str]]:
    problems = payload.get("problemas", [])
    if not isinstance(problems, list):
        raise ValueError("'problemas' must be a list.")
    rows = []
    for item in problems:
        if not isinstance(item, dict):
            continue
        rows.append({
            "prioridade": "",
            "score": str(score(item)),
            "problema": str(item.get("problema", "")),
            "impacto": str(item.get("impacto", "")),
            "voz_cliente": str(item.get("voz_cliente", "")),
            "persona": str(item.get("persona", "")),
            "stage": str(item.get("stage", "")),
            "proposta": str(item.get("proposta", "")),
            "mecanismo": str(item.get("mecanismo", "")),
            "promessa": str(item.get("promessa", "")),
            "objecao": str(item.get("objecao", "")),
            "prova": str(item.get("prova", "")),
            "status_prova": str(item.get("status_prova", "")),
            "claim_pendente": "sim" if is_claim_pending(item) else "nao",
            "risco": str(item.get("risco", "")),
        })
    rows.sort(key=lambda row: int(row["score"]), reverse=True)
    for index, row in enumerate(rows, start=1):
        row["prioridade"] = str(index)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def esc(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_markdown(path: Path, payload: dict[str, Any], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Matriz Problema Proposta Prova",
        "",
        f"- Cliente: {payload.get('cliente', '')}",
        f"- Oferta: {payload.get('oferta', '')}",
        f"- Fonte: {payload.get('fonte', '')}",
        "",
        "| prioridade | problema | proposta | mecanismo | promessa | prova | claim pendente |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        fields = ["prioridade", "problema", "proposta", "mecanismo", "promessa", "prova", "claim_pendente"]
        lines.append("| " + " | ".join(esc(row[field]) for field in fields) + " |")
    pending = [row for row in rows if row["claim_pendente"] == "sim"]
    if pending:
        lines.extend(["", "## Claims Pendentes", ""])
        for row in pending:
            lines.append(f"- `{row['promessa']}` precisa de prova para `{row['problema']}`.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build problem-proposition-proof matrix.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--md", dest="md_path", type=Path)
    parser.add_argument("--csv", dest="csv_path", type=Path)
    args = parser.parse_args()

    payload = load_payload(args.input_json)
    rows = build_rows(payload)
    if args.csv_path:
        write_csv(args.csv_path, rows)
    if args.md_path:
        write_markdown(args.md_path, payload, rows)
    if not args.csv_path and not args.md_path:
        for row in rows:
            print(f"{row['prioridade']}. {row['problema']} - claim pendente: {row['claim_pendente']}")


if __name__ == "__main__":
    main()
