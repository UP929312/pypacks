import io


def get_png_dimensions(file_path: str | None = None, image_bytes: bytes | None = None, enforce_square: bool = True,
                       enforce_factor_of_two: bool = True) -> tuple[int, int]:
    """Returns (width, height) of the image"""
    if file_path is not None:
        with open(file_path, 'rb', encoding="utf-8") as file:
            image_bytes = file.read()

    assert image_bytes is not None, "Must provide image bytes if not providing file_path"
    file_io = io.BytesIO(image_bytes)
    file_io.seek(16)  # Width and height start at byte 16
    width = int.from_bytes(file_io.read(4), 'big')
    height = int.from_bytes(file_io.read(4), 'big')
    if enforce_square:
        assert width == height, "Image must be square"
    if enforce_factor_of_two:
        assert width == 1 or width % 2 == 0, f"Image width must be divisible by 16, {width} is not"
        assert height == 1 or height % 2 == 0, f"Image height must be divisible by 16, {height} is not"
    assert 1 <= width <= 512, f"Image width must be between 1 and 512, {width} is not"
    assert 1 <= height <= 512, f"Image height must be between 1 and 512, {height} is not"
    # rint(file_path, width, height)
    return width, height


def get_png_height(file_path: str | None = None, image_bytes: bytes | None = None,
                   enforce_square: bool = False, enforce_factor_of_two: bool = False) -> int:
    """Returns the height of the image"""
    return get_png_dimensions(file_path=file_path, image_bytes=image_bytes, enforce_square=enforce_square, enforce_factor_of_two=enforce_factor_of_two)[1]
