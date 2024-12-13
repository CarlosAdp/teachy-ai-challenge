from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / 'out'

MODEL = 'gpt-4o'

QUERY_LAYOUT_SYSTEM_PROMPT = '''
Your main task is to assist on identifying exam questions in PDF files. All
your answers need to be in JSON format, according to the schema prompted to you
at each step.
'''

QUESTION_LAYOUT_PROMPT = '''
The following JSON object contains the content of a PDF file.
Each object corresponds to a page in the PDF with the attributes `page` (page
number) and `content`. Content is the list of elements in the page, each 
element having the following properties:

- `type`: either "text" or "image"
- `content`: if `type` is "text", it contains the text of the PDF file. If
    `type` is "image" it is blank
- `coordinates`: if `type` is "text", it contains the coordinates of the text
    in the PDF file. If `type` is "image" it is blank.

Important details:
1. Images in pages have unknown coordinates.
2. Text in pages have known coordinates.

Collect all questions in a JSON list, of objects with the schema:

- `page`: the page number where the question is located
- `question`: the question number
- `coordinates`: the coordinates of the question in the PDF file. Make sure the
    coordinates encompasse the whole question and any image that might be
    related to the question.
- `images`: a list of images related to the question. Each image is a
    dictionary with the following schema:

    - `page`: the page number where the image is located
    - `coordinates`: the coordinates of the image in the PDF file. Make sure the
        coordinates encompasse the whole image and any text that might be
        related to the image.

Your answer must be a JSON object with the following schema:

- `questions`: a list of questions, each question is a dictionary with the
    following schema:

    - `page`: the page number where the question is located
    - `question`: the question number
    - `coordinates`: the coordinates of the question in the PDF file. Make sure
        the coordinates encompasse the whole question and any image that might
        be related to the question.
    - `images`: a list of image paths related to the question.

{content}
'''
