# Teachy AI Challenge

## Description

The goal is to extract relevant information from exam questions from PDF files,
including question number, statement, support text, alternatives and images.

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
