from io import BytesIO
from pathlib import Path
from typing import List, Tuple

from PIL import Image
import pymupdf


MAX_WIDTH = 1000


def pdf_to_png(path: str | Path, pages: Tuple[int, int]) -> bytes:
    '''Receives a PDF file and returns its PNG image as a byte array'''
    with pymupdf.open(path) as pdf:
        # Calculate scale to transform the PDF, setting max width to 1000
        scales = [
            MAX_WIDTH / page.bound().width
            for page in pdf.pages(pages[0] - 1, pages[1])
        ]
        pixmaps: List[pymupdf.Pixmap] = [
            page.get_pixmap(matrix=pymupdf.Matrix(scales[i], scales[i]))
            for i, page in enumerate(pdf.pages(pages[0] - 1, pages[1]))
        ]
    images = [
        Image.open(BytesIO(pixmap.tobytes('png', jpg_quality=100)))
        for pixmap in pixmaps
    ]

    def concat_images(images: list[Image.Image]) -> Image.Image:
        '''Concatenates images vertically'''
        width = max(image.width for image in images)
        height = sum(image.height for image in images)
        result = Image.new('RGB', (width, height))
        y = 0
        for image in images:
            result.paste(image, (0, y))
            y += image.height
        return result

    image = concat_images(images)

    with BytesIO() as buffer:
        image.save(buffer, format='PNG')
        return buffer.getvalue()


if __name__ == '__main__':
    import sys

    path = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 \
        else Path(path).with_suffix('.png')

    png_data = pdf_to_png(path, (1, 3))
    with open(output, 'wb') as f:
        f.write(png_data)
