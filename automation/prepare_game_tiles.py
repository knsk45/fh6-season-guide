"""Prepare exact local FH6 game tiles for the two public card layouts.

The raw source stays next to the prepared asset.  This script only removes a
uniform outer frame introduced by the source export; it never crops into the
actual in-game card.  The report renderer then shows the prepared file without
overlays, darkening or a synthetic square backdrop.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parents[1]


def uniform_dark_row(image: Image.Image, y: int) -> bool:
    row = image.crop((0, y, image.width, y + 1)).convert("RGB")
    stat = ImageStat.Stat(row)
    # The FH6 export frame is the project dark teal (#081014), not pure black.
    return max(stat.mean) < 26 and max(stat.var) < 18


def uniform_dark_column(image: Image.Image, x: int) -> bool:
    column = image.crop((x, 0, x + 1, image.height)).convert("RGB")
    stat = ImageStat.Stat(column)
    return max(stat.mean) < 26 and max(stat.var) < 18


def trim_export_frame(image: Image.Image) -> Image.Image:
    """Trim only continuous, almost-uniform dark rows around an export."""
    top, bottom, left, right = 0, image.height, 0, image.width
    while top < image.height // 4 and uniform_dark_row(image, top):
        top += 1
    while bottom > image.height * 3 // 4 and uniform_dark_row(image, bottom - 1):
        bottom -= 1
    while left < image.width // 4 and uniform_dark_column(image, left):
        left += 1
    while right > image.width * 3 // 4 and uniform_dark_column(image, right - 1):
        right -= 1
    # A frame that is not clearly present is evidence, not a defect: keep it.
    if top < 12: top = 0
    if image.height - bottom < 12: bottom = image.height
    if left < 12: left = 0
    if image.width - right < 12: right = image.width
    return image.crop((left, top, right, bottom))


def prepare(asset_root: Path, source_name: str, output_name: str) -> tuple[int, int]:
    source = asset_root / source_name
    output = asset_root / output_name
    if not source.is_file():
        raise FileNotFoundError(source)
    with Image.open(source) as opened:
        image = trim_export_frame(opened)
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, format="WEBP", quality=86, method=6)
        return image.size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", default=ROOT / "data" / "current-season.json", type=Path)
    args = parser.parse_args()
    state = json.loads(args.state.read_text(encoding="utf-8-sig"))
    asset_root = ROOT / state["season"]["assetsDirectory"]
    for card in state["activities"]:
        visual = card["visual"]
        source_name = visual["sourceImage"]
        output_name = visual["image"]
        width, height = prepare(asset_root, source_name, output_name)
        actual = "horizontal" if width > height else "vertical"
        if visual["orientation"] != actual:
            raise ValueError(
                f"{card['id']}: {visual['orientation']} conflicts with prepared "
                f"{actual} tile {width}x{height}"
            )
        print(f"GAME_TILE={card['id']} {output_name} {width}x{height} {visual['orientation']}")
    print("GAME_TILE_PREPARATION=OK")


if __name__ == "__main__":
    main()
