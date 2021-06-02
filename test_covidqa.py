import json
import os
import os.path as op
import sys
from itertools import chain

sys.path.append(op.dirname(op.abspath(__file__)))
workspace = (op.dirname(op.abspath(__file__)))

questions_path = "./questions.txt"
review_path = f'{workspace}/kaggle-lit-review-0.2.json'

def write_questions (q_path: str):
    with open(review_path) as qa_file, open(q_path, "w") as q_file:
        covid_qa = json.load(qa_file)['categories']
        questions = chain.from_iterable(
            data["sub_categories"]
            for data in covid_qa
        )
        for q in questions:
            q_file.write(f"{q['nq_name']}\n")


write_questions(questions_path)

# with open (f'{workspace}/kaggle-lit-review-0.2.json') as file:
#     covid_qa = json.load(file)
#     for data in covid_qa:
#         sub_categories = data["sub_categories"]
#         q = sub_categories["nq_name"]
#         q_paraphrased = sub_categories["kq_name"]
#         answers = [
#             ans["exact_answer"]
#             for ans in sub_categories["answers"]
#         ]


test = 'this is a test'