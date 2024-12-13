# %%
import base64
import base64
import itertools
import json
import logging
import os
import pathlib
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI

import extract_pdf_content
import extract_questions
import constants

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(stream_handler)

# %%
logger.info(
    'Extracting PDFs layouts and saving images to the %s folder' %
    constants.OUTPUT_DIR)

entrance_folder = pathlib.Path(__file__).parent.parent / 'entrance-exams'
exams = [{'path': f} for f in entrance_folder.glob('*.pdf')]

logger.info(
    'For budget reasons, limiting our queries to process only the first '
    'ten pages of each exam.'
)
for exam in exams:
    output_dir = constants.OUTPUT_DIR / exam['path'].stem
    output_dir.mkdir(exist_ok=True, parents=True)

    if (output_dir / 'pdf_content.json').is_file():
        with open(output_dir / 'pdf_content.json', 'r') as f:
            exam['content'] = json.load(f)
    else:
        exam['content'] = extract_pdf_content.extract_content(
            exam['path'], output_dir, pages=(1, 10))

# %%
exam = next(exam for exam in exams if exam['path'].stem == sys.argv[1])
two_columns = '--two-columns' in sys.argv
logger.info('Exam: %s%s', exam['path'].stem,
            ' (two columns)' if two_columns else '')

# %%
logger.info('Querying OpenAI for questions layout')
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

start_time = time.time()
response = openai_client.chat.completions.create(
    model=constants.MODEL,
    messages=[
        {
            'role': 'system',
            'content': constants.QUERY_LAYOUT_SYSTEM_PROMPT
            + 'The exam is formatted in two columns' if two_columns else ''
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
end_time = time.time()
query_layout_time = end_time - start_time
query_layout_tokens = response.usage.total_tokens
questions_coordinates = json.loads(response.choices[0].message.content)

# %%
logger.info('Cropping questions to PNG images')
questions_dir = constants.OUTPUT_DIR / exam['path'].stem / 'questions'
question_images = extract_questions.crop_questions_to_png(
    exam['path'], questions_dir, questions_coordinates['questions'])
for question_image in question_images:
    question_image['b64_png'] = base64.b64encode(
        question_image['image']).decode('utf-8')

# %%
pdf_image_paths = [
    element['image_path']
    for page in exam['content'] for element in page['content']
    if element['type'] == 'image'
    and pathlib.Path(element['image_path']).is_file()
]
pdf_images = []
for pdf_image_path in pdf_image_paths:
    with open(pdf_image_path, 'rb') as f:
        pdf_images.append(base64.b64encode(f.read()).decode('utf-8'))

# %%
logger.info('Querying OpenAI for questions parser')

time.sleep(max(0, 90 - query_layout_time))

start_time = time.time()
response = openai_client.chat.completions.create(
    model=constants.MODEL,
    messages=[
        {
            'role': 'system',
            'content': constants.QUESTION_PARSER_SYSTEM_PROMPT
        },
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': 'Questions Batch: '},
            ] + list(itertools.chain.from_iterable([[
                {'type': 'text', 'text': f'question_number={q["question"]}:'},
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': f'data:image/png;base64,{q["b64_png"]}'
                    }
                }
            ] for q in question_images]))
            + list(itertools.chain.from_iterable([[
                {'type': 'text', 'text': f'image_number={i}:'},
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': f'data:image/png;base64,{pdf_images[i]}'
                    }
                }
            ] for i in range(len(pdf_images))]))
        }
    ],
    response_format={'type': 'json_object'}
)
end_time = time.time()
query_parser_time = end_time - start_time
query_parser_tokens = response.usage.total_tokens
questions = json.loads(response.choices[0].message.content)['questions']

# %%
for question in questions:
    question['images'] = [
        pdf_image_paths[i]
        for i in question['images']
    ]

    question_json_path = constants.OUTPUT_DIR / \
        exam['path'].stem / f'{question["question_number"]}.json'

    with open(question_json_path, 'w') as f:
        json.dump(question, f, indent=2, ensure_ascii=False)

# %%
execution_metadata = {
    'model': constants.MODEL,
    'query_layout_time': query_layout_time,
    'query_parser_time': query_parser_time,
    'total_time': query_layout_time + query_parser_time,
    'query_layout_tokens': query_layout_tokens,
    'query_parser_tokens': query_parser_tokens,
    'total_tokens': query_layout_tokens + query_parser_tokens,
    'query_layout_cost ($)': query_layout_tokens * constants.PRICE_PER_1M_TOKEN / 1e6,
    'query_parser_cost ($)': query_parser_tokens * constants.PRICE_PER_1M_TOKEN / 1e6,
    'total_cost ($)': (query_layout_tokens + query_parser_tokens) * constants.PRICE_PER_1M_TOKEN / 1e6,
    'exam': exam['path'].name,
    'questions': len(questions),
}
with open(constants.OUTPUT_DIR / exam['path'].stem / 'execution_metadata.json', 'w') as f:
    json.dump(execution_metadata, f, indent=2, ensure_ascii=False)

# %%
