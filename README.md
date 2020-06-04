[![Build Status](https://travis-ci.org/BioGeneTools/LmitJ.svg?branch=master)](https://travis-ci.org/BioGeneTools/LmitJ)

# LmitJ
LmitJ (Lernen mit Journal): learn German with journal

This tool helps to learn and practice German with a different strategy and motivation.

### Documentation
API [Documentation](https://documenter.getpostman.com/view/7764556/SztHWk5S). 

## Installation
1. 
```sh
>>> git clone https://github.com/BioGeneTools/LmitJ.git
>>> cd LmitJ
>>> python -m venv .env
>>> source .env/bin/activate
>>> pip install -r requirements.txt
```

2. 
```sh
>>> python lmitj.py
```
or
```sh
>>> export FLASK_ENV=development
>>> export FLASK_APP=lmitj.py
>>> flask run
```

### Info
The backend has the following main features: 
- Scraping a journal article (news link) and store the words in the database. 
- Regenerate the sentence that each word came from from the scrapped journal link.

Next step: 
- Increasing the backend ability to scrapping more journals. 
- Implementing more interesting ideas to practice the language (such as building more sentence for specific stored vocabularies, allowing to store a user's mother language and sentence, ... etc)
- **Frontend**: to make this tool available more easily and extending the functionality, the frontend will be developed with **Vue.js**, hopefully soon. 