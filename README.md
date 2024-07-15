<!-- generate readme to install this repo (which is a scrapy project and run it on different platforms with installing requirements.txt in venv) -->
# Ebay Scraper

This is a simple ebay scraper that scrapes the URLs of search results for a given keyword and saves the results in an output file.

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install the requirements
4. Run the spider

```bash
git clone https://github.com/mahmoudamr512/Ebay-Scraper-Scrapy.git
cd ebay
python3 -m venv venv
source venv/bin/activate # for windows: venv\Scripts\activate
pip install -r requirements.txt
scrapy crawl ebayspider -o output.json
```

## Usage

To run the spider, use the following command:

```bash
scrapy crawl ebayspider -o output.json
```

This will save the search results in a file named `output.json`. You can change the URLs by modifying input.json in the main directory.

## Changing config

You can change the configuration of the spider by modifying the `settings.py` file in the `ebay` directory as well as the config.yaml file in the main directory.


