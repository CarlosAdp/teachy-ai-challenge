# Teachy AI Challenge

![](banner-teachy.png)

## General Instructions

1. Fork this repository and develop what is asked bellow.
2. Let us know when you are done.

## The Challenge


You'll create a Proof of Concept of a pipeline that extracts questions from entrance exams PDFs.
You should use the same pipeline for all input PDFs, but you can pass different parameters for each pdf if needed.
Write a script that given a folder with PDFs and optionally config files, read the PDFs and extract each question as a JSON object.

There are two types of questions. You should consider:
- Multiple Choice Questions:
    - These questions are composed of two elements:
      - Statement
      - Support Text (optional) // a literary piece or other text that is referenced in the question but is not a direct part of the statement
      - Alternatives
- Open Ended Questions:
    - These questions are composed of one elements:
      - Statement
      - Support Text (optional)

PoC's Specifications:

### MUST HAVEs:
- [x] Accept PDF inputs
- [ ] Extract the aforementioned components of each type of question
- [ ] Extract Support Text for questions
- [ ] Extract images and link them to their question(s) 
- [ ] Support exams that have a two-column layout
- [ ] Enumerate Questions correctly

### NICE TO HAVEs:
- [ ] Represent Equations correctly in LaTeX
- [ ] Represent Chemical Formulas correctly
- [ ] Support questions where the text is split between consecutive pages or consecutive columns

Example JSON of a question should look like this:

```json
{
  "question_number": "3",
  "question_type": "MultipleChoice",
  "statement": "...",
  "Alternatives": ["...", "...", "...", "..."],
  "image": "link to image, if there's an image associated with the question",
  "support_text": "Support Text if there's a support text associeated with the question"
}
```

## What You Should Deliver:

You'll receive 10 entrance exams PDFs. Your output should be:
1. The code that you wrote for extracting questions out of these PDFs
2. Your reasoning explained in the readme
3. 10 directories, one for each exam, each one with JSONs of questions for that exam

Feel free to reach out for any questions about the challenge!

Best of Luck!
