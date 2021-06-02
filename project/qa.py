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

## Data Settings
settings_file = open("./config.json")
settings = json.load(settings_file)
data_path = settings["data_path"]
models_path = settings["models_path"]

settings_file.close()

#data_path = "../data/QA/2021-05-24"
#questions_path = f"{data_path}/questions.txt"
ir_path = f"{data_path}/ir.jsonl"
answers_path = f"{data_path}/qa.jsonl"


with open(ir_path) as ir_file, open(answers_path, "w") as ans_file:

    data_for_qa = (
        json.loads(data)
        for data in ir_file
    )

    qa_model = QaModule(["mrqa", "biobert"], [f"{models_path}/HLTC-MRQA/exported-tf-model-1.15.2", f"{models_path}/BioBERT/exported-tf-model-1.15.2"], \
        f"{models_path}/HLTC-MRQA/spiece.model", f"{models_path}/BioBERT/bert_config.json", f"{models_path}/BioBERT/vocab.txt")

    print("Get Answers...")
    answers = qa_model.getAnswers(data_for_qa)
    for ans in answers:
        q = ans["question"]
        answers = list(ans["data"]["answer"])
        print("Q: ", q)
        print(answers)
        json.dump({
            "question": q,
            "answers": answers
        }, ans_file)
        ans_file.write("\n")
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