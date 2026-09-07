"""Seed the permanent FH6 activity-overlay icon library from local, verified assets.

The current-season tiles are the evidence for the three activity variants that
do not have a standalone icon file.  This tool is intentionally run only when
the reusable library changes; weekly renders merely reference the resulting
files through data/project.json.activityIconLibrary.
"""
from pathlib import Path
import shutil

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
SPRING = ROOT / 'reports' / 'assets' / 'series-04-spring'
LIBRARY = ROOT / 'reports' / 'assets' / 'activity-icons'

NATIVE = {
    'photo-challenge': 'FH6_EventFP_PhotoChallenge_Icon.png',
    'treasure-hunt': 'FH6_EventFP_TreasureHunt_Icon.png',
    'speed-trap': 'FH6_EventFP_SpeedTrap_Icon.png',
    'drift-zone': 'FH6_EventFP_DriftZone_Icon.png',
    'trial': 'FH6_EventFP_Trial_Icon.png',
    'horizon-play': 'FH6_EventFP_HorizonPlay_Icon.png',
    'monthly-rivals': 'FH6_EventFP_MonthlyRivals_Icon.png',
}

# (current exact tile, crop around its upper-right in-game activity glyph)
CROPS = {
    'championship-cross-country': ('tile-unlimited-buddies.webp', (584, 84, 708, 208)),
    'championship-street': ('tile-hot-hatch.webp', (584, 84, 708, 208)),
    'time-attack': ('tile-time-attack.webp', (590, 86, 708, 210)),
}


def transparent_icon(source: Image.Image) -> Image.Image:
    """Remove a mostly black backing while retaining the original coloured glyph."""
    image = source.convert('RGBA')
    alpha = image.getchannel('A')
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a and max(r, g, b) < 22:
                pixels[x, y] = (r, g, b, 0)
    alpha = image.getchannel('A')
    bbox = alpha.getbbox()
    if not bbox:
        raise ValueError('Icon extraction produced an empty alpha channel')
    image = image.crop(bbox)
    image.thumbnail((128, 128), Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', (144, 144))
    canvas.alpha_composite(image, ((144 - image.width) // 2, (144 - image.height) // 2))
    return canvas


def extracted_tile_icon(source: Image.Image) -> Image.Image:
    """Keep red/white glyph pixels from an exact current tile, then make alpha."""
    image = source.convert('RGBA')
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, _ = pixels[x, y]
            bright = max(r, g, b)
            low = min(r, g, b)
            red = r > 105 and r > g * 1.28 and r > b * 1.28
            white = bright > 172 and bright - low < 74
            if not (red or white):
                pixels[x, y] = (r, g, b, 0)
    return transparent_icon(image)


def save(name: str, image: Image.Image) -> None:
    target = LIBRARY / f'{name}.png'
    image.save(target, format='PNG', optimize=True)
    print(f'ACTIVITY_ICON={target.relative_to(ROOT).as_posix()}')


def main() -> None:
    LIBRARY.mkdir(parents=True, exist_ok=True)
    for key, filename in NATIVE.items():
        with Image.open(SPRING / filename) as source:
            save(key, transparent_icon(source))
    for key, (filename, box) in CROPS.items():
        with Image.open(SPRING / filename) as source:
            save(key, extracted_tile_icon(source.crop(box)))
    print('ACTIVITY_ICON_LIBRARY=OK')


if __name__ == '__main__':
    main()
