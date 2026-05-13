#!/usr/bin/env python3
"""Consolida funil unificado A-2 a partir de JSON (playbook 17) e audita DoD."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def block(t: Any) -> str:
    s = "" if t is None else str(t).strip()
    return s if s else "_[preencher]_"


def is_placeholder(s: str) -> bool:
    t = s.strip().lower()
    if not t:
        return True
    if t.startswith("_[preencher]"):
        return True
    if t in ("[nome]", "yyyy-mm-dd"):
        return True
    return False


def filled(v: Any) -> bool:
    if v is None:
        return False
    if isinstance(v, bool):
        return True
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, str):
        return not is_placeholder(v)
    if isinstance(v, list):
        return len(v) > 0
    if isinstance(v, dict):
        return len(v) > 0
    return bool(v)


def default_document() -> dict[str, Any]:
    return {
        "meta": {
            "cliente_projeto": "[Nome]",
            "versao_funil": "v1",
            "data": "YYYY-MM-DD",
            "responsavel": "",
            "link_plano_midia": "",
            "link_deoc": "",
            "link_protocolo_handoff": "",
            "link_benchmark": "",
        },
        "concordancia": {
            "marketing_concorda": False,
            "vendas_concorda": False,
            "data_alinhamento": "",
        },
        "objetivo": {
            "conversao_final_que_importa": "",
            "lead_correto_definicao": "",
        },
        "as_is": {
            "marketing": "",
            "vendas": "",
            "ferramentas_resumo": "",
            "lacunas": "",
        },
        "to_be": {"notas_alinhamento": ""},
        "etapas": [
            {
                "ordem": 1,
                "nome": "",
                "definicao_passa": "",
                "evidencia_minima": "",
                "conversao_evento": "",
                "fonte_da_verdade": "",
                "dono_etapa": "",
                "handoff_protocolo_ref": "",
                "taxa_aceitavel": {
                    "verde": "",
                    "amarelo": "",
                    "vermelho": "",
                    "fonte_benchmark": "",
                },
                "campos_minimos": [
                    {"campo": "", "definicao_preenchimento": ""},
                ],
            },
            {
                "ordem": 2,
                "nome": "",
                "definicao_passa": "",
                "evidencia_minima": "",
                "conversao_evento": "",
                "fonte_da_verdade": "",
                "dono_etapa": "",
                "handoff_protocolo_ref": "",
                "taxa_aceitavel": {
                    "verde": "",
                    "amarelo": "",
                    "vermelho": "",
                    "fonte_benchmark": "",
                },
                "campos_minimos": [
                    {"campo": "", "definicao_preenchimento": ""},
                ],
            },
        ],
        "eventos_tracking": [
            {"evento": "", "etapa_relacionada": "", "nota": ""},
        ],
        "coerencia_operacao": {
            "capacidade_time": "",
            "ciclo_venda": "",
            "riscos_funil_impossivel": "",
        },
        "backlog": [
            {"item": "", "prioridade": "", "dono": ""},
        ],
        "gerenciado": {
            "kpis": [
                "% leads com status válido",
                "% campos mínimos preenchidos",
                "Tempo de ciclo por etapa",
            ],
            "cadencia_revisao": "Quinzenal até estabilizar; mensal após",
            "dono_funil": "",
            "thresholds_resumo": "Vermelho: discrepância entre fontes ou etapa sem dono. Amarelo: muitas etapas e baixa adesão. Verde: rastreio mínimo e aderência.",
        },
    }


def render_md(d: dict[str, Any]) -> str:
    m = d.get("meta") or {}
    conc = d.get("concordancia") or {}
    obj = d.get("objetivo") or {}
    as_is = d.get("as_is") or {}
    to_be = d.get("to_be") or {}
    co = d.get("coerencia_operacao") or {}
    ger = d.get("gerenciado") or {}

    parts: list[str] = []
    parts.append("# Funil unificado (A-2) — consolidado\n\n")
    parts.append("## Cabeçalho\n\n")
    parts.append(
        "| Campo | Valor |\n|---|---|\n"
        f"| Cliente/projeto | {block(m.get('cliente_projeto'))} |\n"
        f"| Versão | {block(m.get('versao_funil'))} |\n"
        f"| Data | {block(m.get('data'))} |\n"
        f"| Responsável | {block(m.get('responsavel'))} |\n"
        f"| Plano mídia | {block(m.get('link_plano_midia'))} |\n"
        f"| DEOC | {block(m.get('link_deoc'))} |\n"
        f"| Protocolo handoff | {block(m.get('link_protocolo_handoff'))} |\n"
        f"| Benchmark | {block(m.get('link_benchmark'))} |\n"
    )
    parts.append("\n## Concordância (DoD)\n\n")
    parts.append(
        f"- Marketing concorda: **{conc.get('marketing_concorda')}**\n"
        f"- Vendas concorda: **{conc.get('vendas_concorda')}**\n"
        f"- Data alinhamento: {block(conc.get('data_alinhamento'))}\n"
    )
    parts.append("\n## 1. Objetivo\n\n")
    parts.append(
        f"- **Conversão final que importa:** {block(obj.get('conversao_final_que_importa'))}\n"
        f"- **Lead correto:** {block(obj.get('lead_correto_definicao'))}\n"
    )
    parts.append("\n## 2. AS IS\n\n")
    parts.append(f"### Marketing\n\n{block(as_is.get('marketing'))}\n\n")
    parts.append(f"### Vendas\n\n{block(as_is.get('vendas'))}\n\n")
    parts.append(f"### Ferramentas\n\n{block(as_is.get('ferramentas_resumo'))}\n\n")
    parts.append(f"### Lacunas\n\n{block(as_is.get('lacunas'))}\n\n")
    parts.append("## 3. TO BE (vocabulário)\n\n")
    parts.append(f"{block(to_be.get('notas_alinhamento'))}\n\n")

    parts.append("## 4. Etapas\n\n")
    for et in d.get("etapas") or []:
        if not isinstance(et, dict):
            continue
        tax = et.get("taxa_aceitavel") or {}
        parts.append(f"### Etapa {block(et.get('ordem'))} — {block(et.get('nome'))}\n\n")
        parts.append(f"- **Definição de passou:** {block(et.get('definicao_passa'))}\n")
        parts.append(f"- **Evidência mínima:** {block(et.get('evidencia_minima'))}\n")
        parts.append(f"- **Evento conversão:** {block(et.get('conversao_evento'))}\n")
        parts.append(f"- **Fonte da verdade:** {block(et.get('fonte_da_verdade'))}\n")
        parts.append(f"- **Dono da etapa:** {block(et.get('dono_etapa'))}\n")
        parts.append(f"- **Handoff (protocolo):** {block(et.get('handoff_protocolo_ref'))}\n")
        parts.append("#### Taxas aceitáveis\n\n")
        parts.append(f"- **Verde:** {block(tax.get('verde'))}\n")
        parts.append(f"- **Amarelo:** {block(tax.get('amarelo'))}\n")
        parts.append(f"- **Vermelho:** {block(tax.get('vermelho'))}\n")
        parts.append(f"- **Fonte faixa:** {block(tax.get('fonte_benchmark'))}\n")
        parts.append("\n#### Campos mínimos\n\n")
        for cm in et.get("campos_minimos") or []:
            if isinstance(cm, dict):
                parts.append(
                    f"- **{block(cm.get('campo'))}:** {block(cm.get('definicao_preenchimento'))}\n"
                )
        parts.append("\n")

    parts.append("## 5. Eventos de tracking\n\n")
    for ev in d.get("eventos_tracking") or []:
        if isinstance(ev, dict):
            parts.append(
                f"- **{block(ev.get('evento'))}** → etapa {block(ev.get('etapa_relacionada'))} — {block(ev.get('nota'))}\n"
            )
    parts.append("\n## 6. Coerência operação\n\n")
    parts.append(f"- **Capacidade time:** {block(co.get('capacidade_time'))}\n")
    parts.append(f"- **Ciclo venda:** {block(co.get('ciclo_venda'))}\n")
    parts.append(f"- **Riscos:** {block(co.get('riscos_funil_impossivel'))}\n")
    parts.append("\n## 7. Backlog\n\n")
    for b in d.get("backlog") or []:
        if isinstance(b, dict):
            parts.append(
                f"- **{block(b.get('prioridade'))}** · {block(b.get('item'))} — dono: {block(b.get('dono'))}\n"
            )
    parts.append("\n## 8. Gerenciado\n\n")
    for k in ger.get("kpis") or []:
        parts.append(f"- KPI: {k}\n")
    parts.append(f"\n**Cadência:** {block(ger.get('cadencia_revisao'))}\n\n")
    parts.append(f"**Dono funil:** {block(ger.get('dono_funil'))}\n\n")
    parts.append(f"**Thresholds:** {block(ger.get('thresholds_resumo'))}\n")
    return "".join(parts)


def audit(d: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    m = d.get("meta") or {}
    if not filled(m.get("cliente_projeto")):
        issues.append("meta.cliente_projeto")
    obj = d.get("objetivo") or {}
    if not filled(obj.get("conversao_final_que_importa")):
        issues.append("objetivo.conversao_final_que_importa")
    if not filled(obj.get("lead_correto_definicao")):
        issues.append("objetivo.lead_correto_definicao")
    as_is = d.get("as_is") or {}
    for k in ("marketing", "vendas", "ferramentas_resumo"):
        if not filled(as_is.get(k)):
            issues.append(f"as_is.{k}")
    etapas = [e for e in (d.get("etapas") or []) if isinstance(e, dict)]
    if len(etapas) < 2:
        issues.append("etapas: mínimo 2 etapas end-to-end")
    for i, et in enumerate(etapas, 1):
        pr = f"etapa[{i}]"
        for k in (
            "nome",
            "definicao_passa",
            "evidencia_minima",
            "conversao_evento",
            "fonte_da_verdade",
        ):
            if not filled(et.get(k)):
                issues.append(f"{pr}.{k}")
        tax = et.get("taxa_aceitavel") or {}
        for tk in ("verde", "amarelo", "vermelho", "fonte_benchmark"):
            if not filled(tax.get(tk)):
                issues.append(f"{pr}.taxa_aceitavel.{tk}")
        cms = [c for c in (et.get("campos_minimos") or []) if isinstance(c, dict)]
        real = [
            c
            for c in cms
            if filled(c.get("campo")) and filled(c.get("definicao_preenchimento"))
        ]
        if not real:
            issues.append(f"{pr}.campos_minimos (≥1 campo com nome e regra)")

    has_handoff = filled(m.get("link_protocolo_handoff")) or any(
        filled(e.get("handoff_protocolo_ref")) for e in etapas
    )
    if not has_handoff:
        issues.append("handoff: meta.link_protocolo_handoff ou etapas[].handoff_protocolo_ref")

    evs = [e for e in (d.get("eventos_tracking") or []) if isinstance(e, dict) and filled(e.get("evento"))]
    if not evs:
        issues.append("eventos_tracking: ≥1 evento nomeado")

    co = d.get("coerencia_operacao") or {}
    if not filled(co.get("capacidade_time")):
        issues.append("coerencia_operacao.capacidade_time")
    if not filled(co.get("ciclo_venda")):
        issues.append("coerencia_operacao.ciclo_venda")

    backlog = [b for b in (d.get("backlog") or []) if isinstance(b, dict) and filled(b.get("item"))]
    if not backlog:
        issues.append("backlog: ≥1 item priorizado")

    conc = d.get("concordancia") or {}
    if not conc.get("marketing_concorda") or not conc.get("vendas_concorda"):
        issues.append("(aviso) concordancia: confirmar marketing_concorda e vendas_concorda no DoD")

    ger = d.get("gerenciado") or {}
    if not filled(ger.get("dono_funil")):
        issues.append("(aviso) gerenciado.dono_funil — canônico registra lacuna de dono")

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Funil unificado A-2 (playbook 17)")
    parser.add_argument("input_json", nargs="?", type=Path)
    parser.add_argument("--md", dest="md_path", type=Path)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--write-default", dest="out_json", type=Path)
    args = parser.parse_args()

    if args.out_json:
        args.out_json.write_text(
            json.dumps(default_document(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Escrito: {args.out_json}")
        return

    if not args.input_json:
        parser.error("informe input_json ou --write-default")

    d = load(args.input_json)
    if args.audit:
        xs = audit(d)
        print("Lacunas / avisos (funil A-2 / playbook 17):")
        for x in xs:
            print(f"  - {x}")
        return

    if args.md_path:
        args.md_path.write_text(render_md(d), encoding="utf-8")
        print(f"Escrito: {args.md_path}")
    else:
        print(render_md(d), end="")


if __name__ == "__main__":
    main()
