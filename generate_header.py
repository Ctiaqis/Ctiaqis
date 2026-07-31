"""
generate_header.py
Generates a GitHub Profile README banner (profile-header.png)
using the pink-cat.png mascot and Pillow.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BANNER_WIDTH: int = 1600
BANNER_HEIGHT: int = 420
CORNER_RADIUS: int = 24

BG_COLOR: str = "#0D1117"
BORDER_COLOR: str = "#30363D"
ACCENT_COLOR: str = "#FF8FB3"
TEXT_PRIMARY: str = "#E6EDF3"
TEXT_SECONDARY: str = "#8B949E"

FONT_BOLD: str = "DejaVuSans-Bold.ttf"
FONT_REGULAR: str = "DejaVuSans.ttf"

HEADLINE_MAX_FONT: int = 46
HEADLINE_MIN_FONT: int = 28
SUBTITLE_FONT_SIZE: int = 28
DESC_FONT_SIZE: int = 22

CAT_MIN_SIZE: int = 190
CAT_MAX_SIZE: int = 230

TEXT_LEFT_MARGIN: int = 80
TEXT_AREA_MAX_WIDTH: int = 940

ASSETS_DIR: Path = Path("./assets")
INPUT_CAT: Path = ASSETS_DIR / "pink-cat.png"
OUTPUT_BANNER: Path = ASSETS_DIR / "profile-header.png"

HEADLINE_TEXT: str = "Bonjour! I'm Dania Balqis Setyodhiyauddin"
SUBTITLE_TEXT: str = "Data Science & AI Enthusiast"
DESC_TEXT: str = "Exploring data, machine learning, deep learning, and intelligent applications."


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_font(filename: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a TrueType font by filename, falling back to the default if missing."""
    try:
        return ImageFont.truetype(filename, size)
    except OSError:
        # PIL default bitmap font (no size control, but always available)
        return ImageFont.load_default()


def fit_font_size(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_filename: str,
    max_size: int,
    min_size: int,
    max_width: int,
) -> ImageFont.FreeTypeFont:
    """Reduce font size until the text fits within max_width."""
    size = max_size
    while size >= min_size:
        font = load_font(font_filename, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            return font
        size -= 2
    return load_font(font_filename, min_size)


def draw_rounded_rectangle(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    radius: int,
    fill: str,
    outline: str,
    outline_width: int = 2,
) -> None:
    """Draw a rounded rectangle with an outline."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=outline_width)


def paste_cat(
    banner: Image.Image,
    cat_path: Path,
    min_size: int,
    max_size: int,
) -> None:
    """Load, resize (maintaining aspect ratio), and paste the cat onto the banner."""
    cat = Image.open(cat_path).convert("RGBA")

    # Scale so the longer side fits within max_size
    orig_w, orig_h = cat.size
    scale = min(max_size / orig_w, max_size / orig_h)
    new_w = max(min_size, int(orig_w * scale))
    new_h = max(min_size, int(orig_h * scale))
    cat = cat.resize((new_w, new_h), Image.LANCZOS)

    # Position: vertically centred, right-aligned with padding
    right_padding = 80
    x = BANNER_WIDTH - new_w - right_padding
    y = (BANNER_HEIGHT - new_h) // 2

    banner.paste(cat, (x, y), mask=cat)


def draw_accent_line(draw: ImageDraw.ImageDraw, x: int, y: int, length: int) -> None:
    """Draw a small vertical accent line to the left of the headline."""
    draw.rectangle([x, y, x + 5, y + length], fill=ACCENT_COLOR)


def render_text_block(
    draw: ImageDraw.ImageDraw,
    banner: Image.Image,
) -> None:
    """Render headline, subtitle, and description onto the banner."""
    # Accent line
    accent_x = TEXT_LEFT_MARGIN
    headline_top_estimate = BANNER_HEIGHT // 2 - 70
    draw_accent_line(draw, accent_x, headline_top_estimate, 90)

    text_x = TEXT_LEFT_MARGIN + 20

    # Headline (dynamic font size)
    headline_font = fit_font_size(
        draw, HEADLINE_TEXT, FONT_BOLD, HEADLINE_MAX_FONT, HEADLINE_MIN_FONT, TEXT_AREA_MAX_WIDTH
    )
    headline_bbox = draw.textbbox((0, 0), HEADLINE_TEXT, font=headline_font)
    headline_h = headline_bbox[3] - headline_bbox[1]

    # Subtitle
    subtitle_font = load_font(FONT_REGULAR, SUBTITLE_FONT_SIZE)
    subtitle_bbox = draw.textbbox((0, 0), SUBTITLE_TEXT, font=subtitle_font)
    subtitle_h = subtitle_bbox[3] - subtitle_bbox[1]

    # Description
    desc_font = load_font(FONT_REGULAR, DESC_FONT_SIZE)
    desc_bbox = draw.textbbox((0, 0), DESC_TEXT, font=desc_font)
    desc_h = desc_bbox[3] - desc_bbox[1]

    spacing = 18
    total_h = headline_h + spacing + subtitle_h + spacing + desc_h
    start_y = (BANNER_HEIGHT - total_h) // 2

    # Draw headline
    draw.text((text_x, start_y), HEADLINE_TEXT, font=headline_font, fill=TEXT_PRIMARY)

    # Draw subtitle
    subtitle_y = start_y + headline_h + spacing
    draw.text((text_x, subtitle_y), SUBTITLE_TEXT, font=subtitle_font, fill=ACCENT_COLOR)

    # Draw description
    desc_y = subtitle_y + subtitle_h + spacing
    draw.text((text_x, desc_y), DESC_TEXT, font=desc_font, fill=TEXT_SECONDARY)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def ensure_assets_dir() -> None:
    """Create the assets directory if it does not exist."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> None:
    """Check that required input files exist."""
    if not INPUT_CAT.exists():
        raise FileNotFoundError(
            f"[ERROR] Cat image not found: {INPUT_CAT}\n"
            "Please place 'pink-cat.png' inside the 'assets/' folder and try again."
        )


def generate_banner() -> None:
    """Create and save the profile header banner."""
    # Start with a transparent RGBA canvas
    banner = Image.new("RGBA", (BANNER_WIDTH, BANNER_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(banner)

    # Draw background rounded rectangle
    draw_rounded_rectangle(
        draw,
        (0, 0, BANNER_WIDTH - 1, BANNER_HEIGHT - 1),
        radius=CORNER_RADIUS,
        fill=BG_COLOR,
        outline=BORDER_COLOR,
        outline_width=2,
    )

    # Paste cat mascot (right side)
    paste_cat(banner, INPUT_CAT, CAT_MIN_SIZE, CAT_MAX_SIZE)

    # Render text (left side)
    render_text_block(draw, banner)

    # Save as PNG
    banner.save(OUTPUT_BANNER, format="PNG", optimize=True)
    print(f"[OK] Banner saved to: {OUTPUT_BANNER}")


def main() -> None:
    try:
        ensure_assets_dir()
        validate_inputs()
        generate_banner()
    except FileNotFoundError as e:
        print(e)
        raise SystemExit(1)
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
