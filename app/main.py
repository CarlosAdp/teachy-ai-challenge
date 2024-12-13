# %%
import base64
import importlib
import json
import logging
import os
import pathlib

from dotenv import load_dotenv
from openai import OpenAI

from extract_pdf_content import extract_content
from extract_questions import crop_questions_to_png
import base64
import constants

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# %%
logger.info(
    'Extracting PDFs layouts and saving images to the %s folder' %
    constants.OUTPUT_DIR)

entrance_folder = pathlib.Path(__file__).parent.parent / 'entrance-exams'
exams = [{'path': f} for f in entrance_folder.glob('*.pdf')][:5]

for exam in exams:
    output_dir = constants.OUTPUT_DIR / exam['path'].stem
    output_dir.mkdir(exist_ok=True, parents=True)

    exam['content'] = extract_content(exam['path'], output_dir)

# %%
logger.info('For budget reasons, limiting our queries to one PDF only')
exam = next(exam for exam in exams if exam['path'].name == 'ime.pdf')

# %%
logger.info('Querying OpenAI for questions layout')
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = openai_client.chat.completions.create(
    model=constants.MODEL,
    messages=[
        {
            'role': 'system',
            'content': constants.QUERY_LAYOUT_SYSTEM_PROMPT
        },
        {
            'role': 'user',
            'content': constants.QUESTION_LAYOUT_PROMPT.format(
                content=json.dumps(exam['content'])
            )
        }
    ],
    response_format={'type': 'json_object'}
)
questions = json.loads(response.choices[0].message.content)

# %%
questions_dir = constants.OUTPUT_DIR / exam['path'].stem / 'questions'
question_images = crop_questions_to_png(
    exam['path'], questions_dir, questions['questions'])

# %%
