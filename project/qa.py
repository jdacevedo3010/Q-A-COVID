import os
import os.path as op
import sys

sys.path.append(op.dirname(op.dirname(op.abspath(__file__))))
workspace = op.dirname(op.dirname(op.abspath(__file__)))
import pprint

import json
from retrieval import information_retrieval
from new_retrieval import search_similar_docs
from src import QaModule, print_answers_in_file#,  rankAnswersList#, rankAnswers
from typing import List, Tuple


def format_es_response (q: str, res: List[Tuple[dict, float]]):
    return {
        "question": q,
        "data": {
            "answer": "",
            "context": [
                retreived["paragraph"]
                for retreived, _ in res
            ]
        },
        "doi": [],
        "titles": []
    }

pp = pprint.PrettyPrinter(indent=4)
q = "covid-19 microbiology bioinformatics"

#all_results, data_for_qa = information_retrieval("./dummy_data/task1_question.json")
data_for_qa = format_es_response(q, search_similar_docs(q))



qa_model = QaModule(["mrqa", "biobert"], ["PATH TO MRQA MODEL", "PATH TO BIOBERT MODEL"], \
    "./MRQA_FOLDER/spiece.model", "./BIOBERT_FOLDER/bert_config.json", "./BIOBERT_FOLDER/vocab.txt")

print("Get Answers...")
answers = qa_model.getAnswers(data_for_qa)
format_answer = qa_model.makeFormatAnswersList(answers)
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