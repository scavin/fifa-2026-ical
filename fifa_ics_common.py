from __future__ import annotations

import argparse
import urllib.request
from pathlib import Path


DEFAULT_URL = "https://ics.fixtur.es/v2/league/fifa-world-cup-2026.ics"
DEFAULT_OUTPUT = "fifa-world-cup-2026.zh.ics"
PLACEHOLDER = "..."
CALENDAR_NAME_EN = "FIFA World Cup 2026"
CALENDAR_NAME_ZH = "2026 世界杯"

# Current feed names plus a few common aliases used by English football feeds.
TEAM_TRANSLATIONS = {
    PLACEHOLDER: "待定",
    "Algeria": "阿尔及利亚",
    "Argentina": "阿根廷",
    "Australia": "澳大利亚",
    "Austria": "奥地利",
    "Belgium": "比利时",
    "Brazil": "巴西",
    "Cabo Verde": "佛得角",
    "Canada": "加拿大",
    "Cape Verde": "佛得角",
    "Colombia": "哥伦比亚",
    "Croatia": "克罗地亚",
    "Curacao": "库拉索",
    "Curaçao": "库拉索",
    "Czech Republic": "捷克",
    "Ecuador": "厄瓜多尔",
    "Egypt": "埃及",
    "England": "英格兰",
    "France": "法国",
    "Germany": "德国",
    "Ghana": "加纳",
    "Haiti": "海地",
    "IR Iran": "伊朗",
    "Iran": "伊朗",
    "Ivory Coast": "科特迪瓦",
    "Japan": "日本",
    "Jordan": "约旦",
    "Korea Republic": "韩国",
    "Mexico": "墨西哥",
    "Morocco": "摩洛哥",
    "Netherlands": "荷兰",
    "New Zealand": "新西兰",
    "Norway": "挪威",
    "Panama": "巴拿马",
    "Paraguay": "巴拉圭",
    "Portugal": "葡萄牙",
    "Qatar": "卡塔尔",
    "Saudi Arabia": "沙特阿拉伯",
    "Scotland": "苏格兰",
    "Senegal": "塞内加尔",
    "South Africa": "南非",
    "South Korea": "韩国",
    "Spain": "西班牙",
    "Switzerland": "瑞士",
    "Tunisia": "突尼斯",
    "Turkey": "土耳其",
    "Türkiye": "土耳其",
    "United States": "美国",
    "Uruguay": "乌拉圭",
    "USA": "美国",
    "Uzbekistan": "乌兹别克斯坦",
}

TRANSLATABLE_PROPERTIES = {
    "SUMMARY",
    "DESCRIPTION",
    "X-WR-CALNAME",
    "X-WR-CALDESC",
}

SORTED_NAMES = sorted(TEAM_TRANSLATIONS, key=len, reverse=True)


def build_argument_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"ICS URL to download. Default: {DEFAULT_URL}",
    )
    source.add_argument(
        "--input",
        type=Path,
        help="Read ICS content from a local file instead of downloading it.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(DEFAULT_OUTPUT),
        help=f"Output file path. Default: {DEFAULT_OUTPUT}",
    )
    return parser


def read_from_url(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "Cache-Control": "no-cache",
            "User-Agent": "fixtur.es-2026-fifa-translator/1.0",
        },
    )
    with urllib.request.urlopen(request) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def read_source(input_path: Path | None, url: str) -> str:
    if input_path:
        return input_path.read_text(encoding="utf-8")
    return read_from_url(url)


def translate_text(text: str) -> str:
    translated = text
    for english_name in SORTED_NAMES:
        translated = translated.replace(english_name, TEAM_TRANSLATIONS[english_name])
    return translated


def translate_property_value(property_name: str, value: str) -> str:
    base_name = property_name.split(";", 1)[0].upper()

    if base_name == "X-WR-CALNAME" and value == CALENDAR_NAME_EN:
        return CALENDAR_NAME_ZH
    if base_name == "X-WR-CALDESC" and value == "Games FIFA World Cup 2026":
        return "2026 FIFA 世界杯赛程"

    return translate_text(value)
