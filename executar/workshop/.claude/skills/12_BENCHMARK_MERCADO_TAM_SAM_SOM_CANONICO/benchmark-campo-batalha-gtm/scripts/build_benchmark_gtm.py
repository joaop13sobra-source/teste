#!/usr/bin/env python3
"""Gera Markdown resumido do benchmark campo de batalha GTM a partir de JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def bullets(title: str, items: list[Any]) -> str:
    lines = [f"## {title}", ""]
    for item in items:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build benchmark GTM markdown from JSON.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--md", dest="md_path", type=Path, required=True)
    args = parser.parse_args()

    data = load(args.input_json)
    ctx = data.get("contexto") or {}
    if not isinstance(ctx, dict):
        ctx = {}

    lines = [
        "# Benchmark Campo De Batalha GTM",
        "",
        f"## Pergunta de negócio",
        "",
        str(data.get("pergunta_negocio", "")),
        "",
        "## Contexto",
        "",
        f"- Cliente: {ctx.get('cliente', '')}",
        f"- Segmento: {ctx.get('segmento', '')}",
        f"- Geografia: {ctx.get('geografia', '')}",
        f"- Produto foco: {ctx.get('produto_foco', '')}",
        f"- Ticket: {ctx.get('ticket', '')}",
        f"- ICP: {ctx.get('icp', '')}",
        f"- Canais: {', '.join(ctx.get('canais') or [])}",
        f"- Objetivo: {ctx.get('objetivo_aquisicao', '')}",
        "",
        "## Concorrentes",
        "",
        "| Player | Tipo | Anuncia | Formato | Mensagem | Gap | Evidência |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for c in data.get("concorrentes", []):
        if not isinstance(c, dict):
            continue
        lines.append(
            "| {player} | {tipo} | {anuncia} | {fmt} | {msg} | {gap} | {ev} |".format(
                player=c.get("player", ""),
                tipo=c.get("tipo", ""),
                anuncia="sim" if c.get("anuncia") else "nao",
                fmt=c.get("formato", ""),
                msg=str(c.get("mensagem", "")).replace("|", "\\|"),
                gap=str(c.get("gap", "")).replace("|", "\\|"),
                ev=str(c.get("evidencia", "")).replace("|", "\\|"),
            )
        )
    lines.append("")

    pads = data.get("padroes", [])
    if isinstance(pads, list) and pads:
        lines.append(bullets("Padrões dominantes", [str(p) for p in pads]))

    ruidos = data.get("ruidos", [])
    if isinstance(ruidos, list) and ruidos:
        lines.append(bullets("Ruído de mercado", [str(r) for r in ruidos]))

    ops = data.get("oportunidades", [])
    if isinstance(ops, list) and ops:
        lines.extend(["## Oportunidades", ""])
        for o in ops:
            if isinstance(o, dict):
                lines.append(f"- **{o.get('nome', '')}**: {o.get('implicacao', '')} (evidência: {o.get('evidencia', '')})")
        lines.append("")

    risks = data.get("riscos", [])
    if isinstance(risks, list) and risks:
        lines.extend(["## Riscos", ""])
        for r in risks:
            if isinstance(r, dict):
                lines.append(f"- **{r.get('nome', '')}**: mitigação {r.get('mitigacao', '')}")
        lines.append("")

    lines.extend([
        "## Baseline vs diferenciação",
        "",
        f"- Baseline: {data.get('baseline', '')}",
        f"- Diferenciação: {data.get('diferenciacao', '')}",
        "",
    ])

    impl = data.get("implicacoes") or {}
    if isinstance(impl, dict) and impl:
        lines.extend(["## Implicações", ""])
        for key, val in impl.items():
            lines.append(f"- **{key}**: {val}")
        lines.append("")

    args.md_path.parent.mkdir(parents=True, exist_ok=True)
    args.md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
