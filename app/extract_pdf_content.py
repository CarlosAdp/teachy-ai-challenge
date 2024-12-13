from pathlib import Path
from typing import Tuple
import pymupdf
from PIL import Image
import io
import os
import json


def extract_content(
    path: str | Path,
    output_dir: str | Path,
    pages: Tuple[int, int] = (1, 10)
) -> dict:
    '''Extracts the PDF elements and their coordinates into a dictionary.

    This function identifies text and images. Text is extracted along with its
    coordinates. Images coordinates cannot be infered due tua a limitation in
    the library.

    The output of this function serves the purpose to feed GPT with context,
    and enable it to identify the area of each question in the PDF.
    '''
    pdf_content = []

    with pymupdf.open(path) as pdf:
        for page_number, page in enumerate(pdf[pages[0] - 1:pages[1]], start=1):
            page_content = []

            text_blocks = page.get_text('dict')['blocks']
            for block in text_blocks:
                if 'lines' in block:
                    block_text = '\n'.join([''.join(
                        span['text'] for span in line['spans']
                    ) for line in block['lines']])
                    page_content.append({
                        'type': 'text',
                        'content': block_text,
                        'coordinates': {
                            'x0': block['bbox'][0],
                            'y0': block['bbox'][1],
                            'x1': block['bbox'][2],
                            'y1': block['bbox'][3],
                        },
                    })

            # Extract images with positions
            images = page.get_images(full=True)
            for img_index, img_info in enumerate(images):
                xref = img_info[0]
                base_image = pdf.extract_image(xref)
                image_bytes = base_image['image']
                try:
                    # Get image position on the page
                    bbox = page.get_image_bbox(xref)
                except ValueError:
                    bbox = (None, None, None, None)

                page_content.append({
                    'type': 'image',
                    'content': None,  # No textual content for images
                    'coordinates': {
                        'x0': bbox[0],
                        'y0': bbox[1],
                        'x1': bbox[2],
                        'y1': bbox[3],
                    },
                })

            # Add the page content to the overall PDF content
            pdf_content.append({
                'page': page_number,
                'content': page_content
            })

    # Write the JSON file
    json_path = os.path.join(output_dir, 'pdf_content.json')
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(pdf_content, json_file, ensure_ascii=False)

    return pdf_content


# Usage
if __name__ == '__main__':
    import sys

    path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 \
        else Path(path).with_suffix('')

    output_dir.mkdir(exist_ok=True, parents=True)

    pdf_content = extract_content(path, output_dir, pages=(1, 3))
    print(len(pdf_content))
