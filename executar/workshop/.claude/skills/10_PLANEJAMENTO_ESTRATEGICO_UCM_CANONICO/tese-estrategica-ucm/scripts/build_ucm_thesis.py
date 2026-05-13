#!/usr/bin/env python3
"""Build an initial UCM strategic thesis from JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_payload(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def list_text(values: Any) -> str:
    if isinstance(values, list):
        return ", ".join(str(value) for value in values)
    return str(values or "")


def build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Tese Estratégica UCM",
        "",
        "## Contexto",
        "",
        f"- Cliente: {payload.get('cliente', '')}",
        f"- Produto/oferta foco: {payload.get('produto', '')}",
        f"- Objetivo da campanha: {payload.get('objetivo', '')}",
        f"- Canal de conversão: {payload.get('canal_conversao', '')}",
        "",
        "## Batalha Estratégica",
        "",
        str(payload.get("batalha", "")),
        "",
        "## Problemas Priorizados",
        "",
        "| Problema | Impacto | Voz do cliente | Funil |",
        "| --- | --- | --- | --- |",
    ]
    for problem in payload.get("problemas", []):
        if isinstance(problem, dict):
            lines.append(f"| {problem.get('nome', '')} | {problem.get('impacto', '')} | {problem.get('voz_cliente', '')} | {problem.get('funil', '')} |")

    lines.extend([
        "",
        "## Personas E Papéis De Decisão",
        "",
        "| Persona | Papel | Dores | Objeções | Provas | CTA |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for persona in payload.get("personas", []):
        if isinstance(persona, dict):
            lines.append(
                f"| {persona.get('nome', '')} | {persona.get('papel', '')} | {list_text(persona.get('dores'))} | {list_text(persona.get('objecoes'))} | {list_text(persona.get('provas'))} | {persona.get('cta', '')} |"
            )

    narrative = payload.get("narrativa", {})
    if not isinstance(narrative, dict):
        narrative = {}
    lines.extend([
        "",
        "## Proposta De Valor E Mecanismo",
        "",
        str(payload.get("proposta_valor", "")),
        "",
        "## Inimigo / Status Quo",
        "",
        str(payload.get("inimigo", "")),
        "",
        "## Narrativa Central",
        "",
        f"- Contexto: {narrative.get('contexto', '')}",
        f"- Tensão: {narrative.get('tensao', '')}",
        f"- Inimigo: {narrative.get('inimigo', '')}",
        f"- Nova crença: {narrative.get('nova_crenca', '')}",
        f"- Mecanismo: {narrative.get('mecanismo', '')}",
        f"- Prova: {narrative.get('prova', '')}",
        f"- Convite: {narrative.get('convite', '')}",
        "",
        "## Tradução Para Ativos",
        "",
        "| Ativo | Direção |",
        "| --- | --- |",
        "| DCC/DEOC | Transformar tese, persona, dor e provas em documento estratégico. |",
        "| LP | Usar batalha, promessa, prova e objeções na sequência de seções. |",
        "| Criativos | Derivar hooks a partir de inimigo, tensão e nova crença. |",
        "| Plano de mídia | Separar públicos e mensagens por persona/funil. |",
        "| Comercial | Usar objeções e provas na qualificação. |",
        "| Tracking | Codificar persona, hook, dor, ângulo e stage. |",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build UCM thesis markdown from JSON.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--md", dest="md_path", type=Path, required=True)
    args = parser.parse_args()

    payload = load_payload(args.input_json)
    args.md_path.parent.mkdir(parents=True, exist_ok=True)
    args.md_path.write_text(build_markdown(payload), encoding="utf-8")


if __name__ == "__main__":
    main()
