from typing import List
import pymupdf  # PyMuPDF
import os
from pathlib import Path

from extract_pdf_content import extract_content


MAX_WIDTH = 1000
MAX_HEIGHT = 1414


def crop_questions_to_png(
        pdf_path: str | Path,
        output_dir: str | Path,
        metadata: List[dict]
) -> List[dict]:
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    question_images = []

    # Open the PDF document
    pdf_document = pymupdf.open(pdf_path)

    # Loop through the metadata to crop and save each question
    for question in metadata:
        question_number = question["question"]
        coordinates = question["coordinates"]

        # Extract the page number (assuming all questions are on the same page)
        # Adjust if metadata includes specific pages
        page_number = question["page"] - 1  # Adjust for 0-based indexing
        page = pdf_document[page_number]

        # Define the rectangle for cropping
        rect = pymupdf.Rect(
            coordinates["x0"], coordinates["y0"], coordinates["x1"], coordinates["y1"]
        )

        if rect.width == 0 or rect.height == 0:
            print(f"Skipping question {
                  question_number} due to invalid dimensions")
            continue

        # Crop the specified region and save as PNG
        scale = min(MAX_WIDTH / rect.width, MAX_HEIGHT / rect.height)
        pix: pymupdf.Pixmap = page.get_pixmap(
            clip=rect, matrix=pymupdf.Matrix(scale, scale))
        output_path = os.path.join(output_dir, f"{question_number}.png")
        pix.save(output_path)

        question_images.append({
            'question': question_number,
            'path': output_path,
            'image': pix.tobytes('png', jpg_quality=100)
        })

        print(f"Saved {question_number} to {output_path}")

    # Close the PDF document
    pdf_document.close()

    return question_images


# Example metadata (replace with your actual metadata)
metadata = {'questions': [{'page': 2,
                           'question': 1,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 145.36880493164062,
                                           'x1': 559.2692260742188,
                                           'y1': 334.0941467285156}},
                          {'page': 2,
                           'question': 2,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 351.86578369140625,
                                           'x1': 559.27099609375,
                                           'y1': 497.6351623535156}},
                          {'page': 2,
                           'question': 3,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 515.40673828125,
                                           'x1': 559.27099609375,
                                           'y1': 678.0531616210938}},
                          {'page': 2,
                           'question': 4,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 695.8247680664062,
                                           'x1': 559.2789306640625,
                                           'y1': 781.8411865234375}},
                          {'page': 3,
                           'question': 5,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 39.549766540527344,
                                           'x1': 500.1841125488281,
                                           'y1': 221.94317626953125}},
                          {'page': 3,
                           'question': 6,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 244.06576538085938,
                                           'x1': 132.5396728515625,
                                           'y1': 771.817138671875}},
                          {'page': 4,
                           'question': 7,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 635.94775390625,
                                           'x1': 498.6347351074219,
                                           'y1': 778.794189453125}},
                          {'page': 4,
                           'question': 8,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 39.549766540527344,
                                           'x1': 500.1841125488281,
                                           'y1': 299.302978515625}},
                          {'page': 4,
                           'question': 9,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 315.5768127441406,
                                           'x1': 500.1841125488281,
                                           'y1': 466.3121643066406}},
                          {'page': 4,
                           'question': 10,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 487.1877746582031,
                                           'x1': 500.1841125488281,
                                           'y1': 612.1632080078125}},
                          {'page': 5,
                           'question': 11,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 633.0387573242188,
                                           'x1': 500.1841125488281,
                                           'y1': 778.3558959960938}},
                          {'page': 5,
                           'question': 12,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 39.549766540527344,
                                           'x1': 559.2753295898438,
                                           'y1': 286.1741943359375}},
                          {'page': 5,
                           'question': 13,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 310.4237976074219,
                                           'x1': 559.2759399414062,
                                           'y1': 417.7061767578125}},
                          {'page': 5,
                           'question': 14,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 438.8157958984375,
                                           'x1': 559.27685546875,
                                           'y1': 564.2471923828125}},
                          {'page': 5,
                           'question': 15,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 613.7037353515625,
                                           'x1': 559.2764892578125,
                                           'y1': 771.817138671875}},
                          {'page': 6,
                           'question': 16,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 145.17477416992188,
                                           'x1': 559.270751953125,
                                           'y1': 384.5888977050781}},
                          {'page': 6,
                           'question': 17,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 402.5307922363281,
                                           'x1': 559.2708129882812,
                                           'y1': 782.0521850585938}},
                          {'page': 7,
                           'question': 18,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 39.549766540527344,
                                           'x1': 500.1841125488281,
                                           'y1': 613.8221435546875}},
                          {'page': 8,
                           'question': 19,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 39.549766540527344,
                                           'x1': 559.27978515625,
                                           'y1': 714.3671875}},
                          {'page': 9,
                           'question': 20,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 39.549766540527344,
                                           'x1': 559.27978515625,
                                           'y1': 295.90716552734375}},
                          {'page': 9,
                           'question': 21,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 317.0167541503906,
                                           'x1': 559.274658203125,
                                           'y1': 750.1138916015625}},
                          {'page': 10,
                           'question': 22,
                           'coordinates': {'x0': 35.41600036621094,
                                           'y0': 39.549766540527344,
                                           'x1': 559.2744140625,
                                           'y1': 503.08917236328125}}]}

if __name__ == '__main__':
    import sys

    path = sys.argv[1]
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 \
        else Path(path).with_suffix('')

    output_dir.mkdir(exist_ok=True, parents=True)

    pdf_content = extract_content(path, output_dir, pages=(1, 3))

    questions_dir = output_dir / 'questions'
    question_images = crop_questions_to_png(
        path, questions_dir, metadata['questions'])

    print(question_images)
