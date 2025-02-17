from PIL import Image, ImageDraw, ImageFont

from pypacks.scripts.scrapers.minecraft_font_scraper import get_minecraft_font

MINECRAFT_FONT_DATA = get_minecraft_font()


def add_text(image: Image.Image, text: str, x: int, y: int, font_size: int = 40, color: int = 0xCCCCCC) -> Image.Image:
    """Adds the default minecraft font to an image"""
    font = ImageFont.truetype(MINECRAFT_FONT_DATA, size=font_size)
    draw = ImageDraw.Draw(image)
    draw.text((x, y), text, font=font, fill=0x007700)
    # Convert the draw object back to an image
    # image.show()
    return image
