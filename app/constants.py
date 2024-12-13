from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / 'out'

MODEL = 'gpt-4o'
PRICE_PER_1M_TOKEN = 2.5

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

QUESTION_PARSER_SYSTEM_PROMPT = '''
You will receive a series of PNG images. The first batch consists of exam
questions and the second batch consists of images that might appear in the
questions. Each question has an question number and each image has an image
number.

Extract the following information from each question:

- "question_number": the question number.
- "question_type": "OpenEnded" if the question does not have alternatives and
    "MultipleChoice" if the question has alternatives.
- "statement": the actual question to the reader.
- "support_text": any observation, literary piece or reference that supports
    the question, but it is not its main statement.
- "alternatives": a list of alternatives to the question.
- "images": the list of image numbers that appear in the question.

Your answer must be a JSON object with the following schema:

- `questions`: a list of questions, each question is a dictionary with the
    following schema:

    - `question_number`: the question number
    - `question_type`: "OpenEnded" if the question does not have alternatives
        and "MultipleChoice" if the question has alternatives.
    - `statement`: the actual question to the reader.
    - `support_text`: any observation, literary piece or reference that supports
        the question, but it is not its main statement.
    - `alternatives`: a list of alternatives to the question.
    - `images`: the list of image numbers that appear in the question.

Important instructions:
1. If math equations are found, replace them with their LaTeX representation
enclosed in dollar signs ($), using the amsmath and amssymb packages.
2. If chemical formulas are found, replace them with their LaTeX representation
enclosed in dollar signs ($), using the chemmformula package.
3. If the question has images, the image number is the number of the image
in the batch of images that appears in the question.
'''
