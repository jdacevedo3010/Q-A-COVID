# CAiRE-COVID (FORKED)

This is a Fork of the [CAiRe COVID project](https://github.com/HLTCHKUST/CAiRE-COVID/blob/master/src/covidQA/qa_utils.py) and a continuation of our information retrieval module (https://github.com/slemus9/covid-ir). 

# Requirements

All libraries can be installed via `npm install -r requirements.txt`. It is **mandatory** to have Python 3.7 to run this project. We recommend to make a virtual environment with this Python version 

# Configurations
You need to specify the paths to the data within your system in the `config.json` file.

- **data_path**: Path to a file names `ir.jsonl`, which is the output of the [covid-ir](https://github.com/slemus9/covid-ir)module, which is Information Retreival performed over CORD-19 dataset
- **models_path**: Path to the pre-trained models available [here](https://drive.google.com/drive/folders/1yjzYN_KCz8uLobqaUddftBGPAZ6uSDDj). You should specify the path to the folder which is parent of both **BioBERT** and **HLTC-MRQA** folders

The entry point of the program is the file `project/qa.py`. When runned, it should output a file called `qa.jsonl` in the specified **data_path** field of `config.json`
