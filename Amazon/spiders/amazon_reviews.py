# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response
from Amazon.middlewares import driver
from Amazon.items import AmazonItem
import logging
from datetime import datetime
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import re


class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"
    allowed_domains = ["amazon.com"]

    def __init__(self, url, *args, **kwargs):
        super(AmazonReviewsSpider, self).__init__(*args, **kwargs)
        if (
            re.match("^https\:\/\/www\.amazon\.com\/?.*\/dp\/[a-zA-Z0-9]*\/?.*$", url)
            is not None
        ):
            results = re.search(
                "^https\:\/\/www\.amazon\.com\/?.*\/dp\/([a-zA-Z0-9]*)\/?.*$", url
            )
            product_id = results.group(1)
            url = (
                "https://www.amazon.com/product-title/product-reviews/"
                + product_id
                + "/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"
            )
        else:
            driver.close()
            raise Exception("Invalid url!")
        self.start_urls = [url]

    def parse(self, response):
        logging.log(logging.INFO, "Good before parsing!!")

        for review_div in response.xpath("//div[@id='cm_cr-review_list']").xpath(
            "child::div[@class='a-section review aok-relative']"
        ):

            yield self.parse_review(review_div)

        if (
            "disabled"
            not in response.xpath("//div[@id='cm_cr-review_list']")
            .xpath(".//li[contains(@class, 'a-last')]/@class")
            .extract_first()
        ):
            next_page = (
                response.xpath("//div[@id='cm_cr-review_list']")
                .xpath(".//li[contains(@class, 'a-last')]/a/@href")
                .extract_first()
            )
            yield scrapy.Request(
                "https://www.amazon.com/" + next_page,
                dont_filter=True,
                callback=self.parse,
            )
        else:
            logging.log(logging.INFO, "Closing gecko driver!")
            driver.close()

    def parse_review(self, review_div):
        logging.log(logging.INFO, "Parsing a review!!!")
        amazon_item = AmazonItem()
        try:
            amazon_item["user_picture"] = review_div.xpath(
                ".//div[@class = 'a-profile-avatar']/img/@data-src"
            ).extract()[0]
            amazon_item["user_name"] = (
                review_div.xpath(".//div[@class = 'a-profile-content']/span/text()")
                .extract()[0]
                .strip()
            )
            amazon_item["review_title"] = (
                review_div.xpath(".//div[@class = 'a-row']")
                .xpath(".//a[contains(@class, 'review-title-content')]/span/text()")
                .extract()[0]
                .strip()
            )

            amazon_item["review_date"] = (
                review_div.xpath(".//span[contains(@class, 'review-date')]/text()")
                .extract()[0]
                .strip()
            )
            # logging.warning("review_date: ", amazon_item['review_date'])
            amazon_item["review_date"] = " ".join(
                amazon_item["review_date"].split()[-3:]
            )
            amazon_item["review_date"] = datetime.strptime(
                amazon_item["review_date"], "%B %d, %Y"
            )
            amazon_item["review_data"] = " ".join(
                review_div.xpath(
                    ".//span[@class='a-size-base review-text review-text-content']/span/text()"
                ).extract()
            ).strip()
            return amazon_item
        except:
            logging.log(logging.INFO, "Exception")
