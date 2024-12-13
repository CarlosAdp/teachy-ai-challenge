# Teachy AI Challenge

## Description

The goal is to extract relevant information from exam questions from PDF files,
including question number, statement, support text, alternatives and images.

## Installation and Execution

First, configure a `.env` file with your OpenAI API Key:

```
# .env
OPENAI_API_KEY=sk-...
```

To run the code locally, install the required Python packages

```bash
(env) $ python -m pip install -r app/requirements.txt
```

Then run the `app/main.py` script, informing which exam you are looking to parse:

```bash
(env) $ python app.main.py ime
```

## Results

All artifacts produced are stored in the `out/<exam>/`. There you'll find the
following subdirectories and files

- `images/`: contains all the PDF images
- `questions/`: contains clipped questions
- `<question_number>.json`: the questions data, as requested in the challenge
- `execution.metadata.json`: information about time and tokens spent, cost in dollars and data volume.

>
> 💡Tip: If you get the `openai.RateLimitError` exception, try removing logos
> and other spare images from the `out/<exam>/images/` directory.
>

## Proposed solution

Exams in the entrance collection are issued by different organizations and have
different layouts. They also cover multiple topics, and can contain complex
elements, such as math equations, chemical formulas and images.

For this reason, silver bullet OCR tools do not function properly.

Find below the proposed solution:

### Step 1: Extract the PDF content

Using the `PyMuPDF` Python library, all text and image elements in the PDF are
extracted into a JSON metadata, alongside the elements' coordinates.

### Step 2: Query OpenAI's GPT to extract only questions

The pipeline sends this metadata to OpenAI's GPT-4o model, asking it to
identify each question and it's coordinates. Metadata enables better precision
to the model, when compared to sending the PDF as PNG images, for example,
while also saving tokens (from ~1M to ~25K for a 24-pages PDF, a 97%
reduction).

GPT answers with a list of JSON objects, each containing the question number,
its page and its coordinates.

### Step 3: Clip questions into PNG images

With this information, the pipeline leverages `PyMuPDF` again, to clip each
question into a small image. These images will be sent over to GPT-4o for
parsing.

**Note**: Parsing can be done partially in Step 3, but it is imprecise in
collecting complex texts as math equations and chemical formulas.


### Step 4: QUery OpenAI's GPT to parse each question

The model responds with a list of JSON objects containing information about
each question:

- question_number
- `question_type`
- `statement`
- `support_text`
- `alternatives`
- `images`

## Costs

Find below how much was spent in OpenAI's API usage per exam:

| Exam      | Cost       |
|-----------|------------|
| ita       | $0.1205    |
| ufpr      | $0.1057    |
| unesp     | $0.1380    |
| fuvest    | $0.1319    |
| enem      | $0.1531    |
| uerj      | $0.0842    |
| ime       | $0.1318    |
| unicamp   | $0.1554    |
| obf       | $1.5281    |
| obmep     | $0.0779    |

OBF higher cost is justified by the large number of images the PDF contained.

More detailes can be found at `/out/<exam>/execution_metadata.json`.


## Next Steps

Find below some improvements that can be made to this pipeline

1. Handle exam layouts with two or more columns.
2. Remove icons and logos from the images folder, to reduce the number of
   tokens requested to the OpenAI API.
3. Give more context to the questions parser about the images pages, limiting
    the search to be made only in the page of the question.
4. Improve the quality of saved images.
5. Support multiple questions that reference one piece of support text.
5. Build a question visualizer for quick consultation (using Streamlit).
