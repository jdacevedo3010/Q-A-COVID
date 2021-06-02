import os
import json
import os.path as op
import sys

sys.path.append(op.dirname(op.dirname(op.abspath(__file__))))
workspace = op.dirname(op.dirname(op.abspath(__file__)))
import pprint

import json
#from retrieval import information_retrieval
#from new_retrieval import search_similar_docs
from src import QaModule, print_answers_in_file#,  rankAnswersList#, rankAnswers
from typing import List, Tuple


pp = pprint.PrettyPrinter(indent=4)

#all_results, data_for_qa = information_retrieval("./dummy_data/task1_question.json")
#data_for_qa = format_es_response(q, search_similar_docs(q))

data_path = "../data/QA/2021-05-24"
paragraphs_path = f"{data_path}/paragraphs.jsonl"
questions_path = f"{data_path}/questions.txt"
answers_path = f"{data_path}/answers.jsonl"


with open(answers_path) as ans_file:

    data_for_qa = (
        json.loads(data)
        for data in ans_file
    )

    qa_model = QaModule(["mrqa", "biobert"], [f"{data_path}/HLTC-MRQA/exported-tf-model-1.15.2", f"{data_path}/BioBERT/exported-tf-model-1.15.2"], \
        f"{data_path}/HLTC-MRQA/spiece.model", f"{data_path}/BioBERT/bert_config.json", f"{data_path}/BioBERT/vocab.txt")

    print("Get Answers...")
    answers = qa_model.getAnswers(data_for_qa)
    for ans in answers:
        print(ans["data"]["answer"])
    #format_answer = qa_model.makeFormatAnswersList(answers)
    #ranked_answers = rankAnswersList(format_answer)

    '''
    Final output for synthesis
    List [{
            "question": "xxxx",
            "data": 
            {
                "answer": ["answer1", "answer2", ...],
                "confidence": [confidence1, confidence2, ...],
                "title": [title1, title2, ...],
                "doi": [doi1, doi2, ...]
                "sha": [sha1, sha2, ...]
            }
    }]
    '''