# Welcome To TrustCrawler

## Demo

https://trustcrawler.streamlit.app/

The url scraped is : https://fr.trustpilot.com/review/{brand}?languages=all with brand in parameters

## Important if you run in local make sure to secret api key in .streamlit/secrets.toml

### To run the project:

1. Clone this repo
2. Run `pip install -r requirements.txt`
3. Run `streamlit run home.py`

### Usage example:

#### Home page:

1. Go to http://localhost:8501/
2. selects brands u want to get their reviews
3. Wait to the crawler to finish
4. Download the csv file

#### Reviews page:

1. Go to http://localhost:8501/reviews
2. Select the brand you want to see its reviews
3. Select the export u want to see the reviews in
4. Check the reviews
5. U can select the reviews u want to translate
6. Click on translate
7. Wait to the translation to finish


### Why this frameworks ?

#### Streamlit:

1. Easy to use
2. Fast to develop
3. Easy to deploy
4. Integrate fast with python frameworks scraping like scrapy here

#### Scrapy:

1. Dynamic scraping
2. Crawling and scraping lots of data fast
3. Good development experience with good infrastructure
4. Easy to deploy