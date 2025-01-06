import io
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
