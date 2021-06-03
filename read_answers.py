import json
import os
import os.path as op
import sys
from itertools import chain
import jsonlines

sys.path.append(op.dirname(op.abspath(__file__)))
workspace = (op.dirname(op.abspath(__file__)))

#review_path = f'{workspace}/kaggle-lit-review-0.2.json'
qa_path =  f'{workspace}/qa.jsonl'

with jsonlines.open(qa_path) as qa_file:
    for line in qa_file.iter():
        print(line['question'], line['answers'])

test = 'this is a test'
'''
def write_questions (q_path: str):
    with open(review_path) as qa_file, open(q_path, "w") as q_file:
        covid_qa = json.load(qa_file)['categories']
        questions = chain.from_iterable(
            data["sub_categories"]
            for data in covid_qa
        )
'''
