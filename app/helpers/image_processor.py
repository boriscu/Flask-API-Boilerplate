import base64
import io
from typing import Optional
from PIL import Image
from werkzeug.datastructures import FileStorage


class ImageProcessor:
    @staticmethod
    def compress_image(file: FileStorage, max_dim: int = 512) -> bytes:
        """
        Compresses an image, resizing it to not exceed the given dimensions while maintaining aspect ratio.

        Args:
            file (FileStorage): The uploaded image file.
            max_dim (int): The maximum dimension (height or width) for the image.

        Returns:
            bytes: The compressed image data as a byte stream.
        """
        img = Image.open(file.stream)

        if img.height > max_dim or img.width > max_dim:
            img.thumbnail((max_dim, max_dim))

        byte_stream = io.BytesIO()
        img.save(byte_stream, format="PNG")
        return byte_stream.getvalue()

    @staticmethod
    def encode_image(image: bytes) -> Optional[str]:
        """
        Encodes a binary image to a base64 string suitable for JSON output.

        Args:
            image (bytes): The binary data of the image.

        Returns:
            Optional[str]: The base64-encoded string of the image, or None if the image is None.
        """
        if image:
            return base64.b64encode(image).decode("utf-8")
        return None
