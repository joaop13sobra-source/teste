#!/usr/bin/env python3
"""Generate canonical Marketing OS IDs, names and UTM URLs from JSON."""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path
from typing import Any
from urllib.parse import urlencode


FIELDS = [
    "client_id",
    "campaign_id",
    "adgroup_id",
    "creative_id",
    "test_id",
    "campaign_name",
    "adgroup_name",
    "creative_name",
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
    "final_url",
]


def slugify(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = re.sub(r"[^a-z0-9_-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


def required(item: dict[str, Any], field: str, context: str) -> str:
    value = slugify(item.get(field))
    if not value:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return value


def seq(value: Any, context: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError(f"Missing sequencial in {context}.")
    if not raw.isdigit():
        raise ValueError(f"Sequencial must be numeric in {context}: {raw}")
    return raw.zfill(3)


def build_rows(payload: dict[str, Any]) -> list[dict[str, str]]:
    base_url = str(payload.get("base_url", "")).strip()
    if not base_url:
        raise ValueError("Missing 'base_url'.")

    client_slug = required(payload, "cliente", "root")
    year_month = str(payload.get("ano_mes", "")).strip()
    if not re.fullmatch(r"\d{6}", year_month):
        raise ValueError("'ano_mes' must use YYYYMM.")

    client_id = f"cli-{client_slug}"
    utm_source = required(payload, "utm_source", "root")
    utm_medium = required(payload, "utm_medium", "root")

    rows: list[dict[str, str]] = []
    campaigns = payload.get("campanhas")
    if not isinstance(campaigns, list):
        raise ValueError("'campanhas' must be a list.")

    for campaign in campaigns:
        if not isinstance(campaign, dict):
            raise ValueError("Each campaign must be an object.")
        campaign_id = f"cmp-{client_slug}-{year_month}-{seq(campaign.get('sequencial'), 'campaign')}"
        typ = required(campaign, "tipo_campanha", campaign_id)
        obj = required(campaign, "objetivo", campaign_id)
        mov = required(campaign, "movimento", campaign_id)
        campaign_slug = required(campaign, "slug", campaign_id)
        cohort = required(campaign, "cohort", campaign_id)
        segmento = required(campaign, "segmento", campaign_id)
        periodo = required(campaign, "periodo", campaign_id)
        campaign_name = f"{campaign_id} | {typ} | {obj} | {mov} | {campaign_slug}"
        utm_campaign = (
            f"{campaign_id}__typ-{typ}__obj-{obj}__mov-{mov}__slug-{campaign_slug}"
            f"__coh-{cohort}__seg-{segmento}__per-{periodo}"
        )

        adgroups = campaign.get("adgroups")
        if not isinstance(adgroups, list):
            raise ValueError(f"'adgroups' must be a list in {campaign_id}.")

        for adgroup in adgroups:
            if not isinstance(adgroup, dict):
                raise ValueError(f"Each adgroup in {campaign_id} must be an object.")
            adgroup_id = f"adg-{client_slug}-{year_month}-{seq(adgroup.get('sequencial'), 'adgroup')}"
            publico = required(adgroup, "publico", adgroup_id)
            temperatura = required(adgroup, "temperatura", adgroup_id)
            posicionamento = required(adgroup, "posicionamento", adgroup_id)
            adgroup_slug = required(adgroup, "slug", adgroup_id)
            placement = slugify(adgroup.get("placement")) or "na"
            geo = slugify(adgroup.get("geo")) or "na"
            keyword = slugify(adgroup.get("keyword"))
            match_type = slugify(adgroup.get("match_type"))
            adgroup_name = f"{adgroup_id} | {publico} | {temperatura} | {posicionamento} | {adgroup_slug}"
            if keyword:
                utm_term = f"{adgroup_id}__kw-{keyword}__match-{match_type or 'na'}__temp-{temperatura}__slug-{adgroup_slug}__geo-{geo}"
            else:
                utm_term = f"{adgroup_id}__pub-{publico}__temp-{temperatura}__pos-{posicionamento}__slug-{adgroup_slug}__plc-{placement}__geo-{geo}"

            creatives = adgroup.get("criativos")
            if not isinstance(creatives, list):
                raise ValueError(f"'criativos' must be a list in {adgroup_id}.")

            for creative in creatives:
                if not isinstance(creative, dict):
                    raise ValueError(f"Each creative in {adgroup_id} must be an object.")
                creative_id = f"crv-{client_slug}-{year_month}-{seq(creative.get('sequencial'), 'creative')}"
                test_id = f"tst-{client_slug}-{year_month}-{seq(creative.get('test_sequencial'), 'test')}"
                formato = required(creative, "formato", creative_id)
                hook = required(creative, "hook", creative_id)
                persona = required(creative, "persona", creative_id)
                creative_slug = required(creative, "slug", creative_id)
                dor = required(creative, "dor", creative_id)
                angulo = required(creative, "angulo", creative_id)
                etapa = required(creative, "etapa", creative_id)
                versao = required(creative, "versao", creative_id)
                creative_name = f"{creative_id} | {formato} | {hook} | {persona} | {creative_slug} | {versao}"
                utm_content = (
                    f"{creative_id}__fmt-{formato}__hook-{hook}__per-{persona}__slug-{creative_slug}"
                    f"__dor-{dor}__ang-{angulo}__stage-{etapa}__ver-{versao}"
                )
                query = {
                    "utm_source": utm_source,
                    "utm_medium": utm_medium,
                    "utm_campaign": utm_campaign,
                    "utm_content": utm_content,
                    "utm_term": utm_term,
                    "v4_client_id": client_id,
                    "v4_campaign_id": campaign_id,
                    "v4_adgroup_id": adgroup_id,
                    "v4_creative_id": creative_id,
                    "v4_test_id": test_id,
                }
                separator = "&" if "?" in base_url else "?"
                final_url = f"{base_url}{separator}{urlencode(query)}"
                rows.append({
                    "client_id": client_id,
                    "campaign_id": campaign_id,
                    "adgroup_id": adgroup_id,
                    "creative_id": creative_id,
                    "test_id": test_id,
                    "campaign_name": campaign_name,
                    "adgroup_name": adgroup_name,
                    "creative_name": creative_name,
                    "utm_source": utm_source,
                    "utm_medium": utm_medium,
                    "utm_campaign": utm_campaign,
                    "utm_content": utm_content,
                    "utm_term": utm_term,
                    "v4_client_id": client_id,
                    "v4_campaign_id": campaign_id,
                    "v4_adgroup_id": adgroup_id,
                    "v4_creative_id": creative_id,
                    "v4_test_id": test_id,
                    "final_url": final_url,
                })
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
        "# Matriz De UTMs E IDs",
        "",
        "| " + " | ".join(FIELDS) + " |",
        "| " + " | ".join("---" for _ in FIELDS) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_md(row[field]) for field in FIELDS) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Marketing OS UTM matrix from JSON.")
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--csv", dest="csv_path", type=Path)
    parser.add_argument("--md", dest="md_path", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    rows = build_rows(payload)
    if not args.csv_path and not args.md_path:
        for row in rows:
            print(row["final_url"])
        return
    if args.csv_path:
        write_csv(rows, args.csv_path)
    if args.md_path:
        write_markdown(rows, args.md_path)


if __name__ == "__main__":
    main()
