import scrapy
import scrapy
import json
import time
import logging
import random
import yaml
from scrapy.utils.project import get_project_settings
from scrapy.http import Request
from bs4 import BeautifulSoup


class EbayspiderSpider(scrapy.Spider):
    name = "ebayspider"

    def __init__(self, *args, **kwargs):
        super(EbayspiderSpider, self).__init__(*args, **kwargs)
        self.load_config()
        self.failed_proxies = set()
        self.chunk_index = 0

    def load_config(self):
        with open("config.yaml", "r") as file:
            self.config = yaml.safe_load(file)
        self.chunk_size = self.config["chunk_size"]
        self.sleep_time = self.config["max_sleep_time"]
        self.max_retry_times = self.config["max_retry_times"]
        self.initial_sleep = self.config["initial_sleep"]
        self.use_proxies = self.config["use_proxies"]

    def start_requests(self):
        with open("input.json", "r") as file:
            json_dict = json.load(file)
            # flatten the json into urls
            links = [item["links"] for item in json_dict]
            urls = [link for sublist in links for link in sublist]

        for chunk in self.get_chunks(urls, self.chunk_size):
            for url in chunk:
                yield self.make_request(url)
            time.sleep(self.sleep_time)

    def get_chunks(self, data, size):
        for i in range(0, len(data), size):
            yield data[i : i + size]

    def make_request(self, url, retries=0):
        return Request(
            url,
            callback=self.parse,
            errback=self.errback,
            # meta={"proxy": proxy, "retries": retries, "url": url},
            meta={"retries": retries, "url": url},
        )

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        body_content = soup.body

        # If you want to get the body content as a string
        body_content_str = str(body_content)

        data = {
            "url": response.meta["url"],
            "body": body_content_str,
        }
        self.log_data(data, "success")
        yield data

    def errback(self, failure):
        request = failure.request
        retries = request.meta["retries"]
        if retries < self.retry_times:
            sleep_time = self.initial_sleep * (2**retries)
            time.sleep(sleep_time)
            retries += 1
            self.log_data(
                {
                    "url": request.meta["url"],
                    # "proxy": request.meta["proxy"],
                    "status": failure.value.response.status,
                },
                f"retrying_{retries}",
            )
            yield self.make_request(request.meta["url"], retries)
        else:
            self.log_data(
                {
                    "url": request.meta["url"],
                    # "proxy": request.meta["proxy"],
                    "status": "failed",
                },
                "failed after all retrying",
            )

    def log_data(self, data, comment):
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "url": data["url"],
            # "proxy": data["proxy"],
            # "status": data["status"],
            "comment": comment,
        }
        logging.info(json.dumps(log_entry))
