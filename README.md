# CU Research Faculty Scraper and Emailer

## What is this for?

Scrape CU's research faculty and send an email pertaining to: https://github.com/jrothrock/cu_grades. In order to get the scraper student to work, you have to go to linkedin and copy the 'li_at' cookie into the cookie variable found in the main.py. Then set the students variable in main to true, and change the amount in the scraper_students.py.

Credit to austinoboyle for his [linkedin scraping solution](https://github.com/austinoboyle/scrape-linkedin-selenium).

## How To Use
1. Create GMAIL Api following this (step 1), and move the client_secret.json to this folder
    - https://developers.google.com/gmail/api/quickstart/python
2. Build a virualenv
    - python 2: `virtualenv venv --distribute; source venv/bin/activate`
    - python 3: `python3 -m venv venv; . ./venv/bin/activate`
3. Install python packages
    - `pip install -r requirements.txt`
4. Run main.py
    - python 2: `python main.py`
    - python 3: `python3 main.py`


## Technologies Used
- Python
- Beautifulsoup
- Selenium Web Driver
- Pandas
- Google Mail API

## License 
    Released under MIT.