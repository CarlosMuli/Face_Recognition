import scrapy
from ..items import InsightCrawlerItem

class InsightSpider(scrapy.Spider):
    name = "InsightCrawler"
# DCU Only: https://www.insight-centre.org/about/team?field_user_fullname_value=&field_user_insight_institude_value=Dublin+City+University+%28DCU%29&field_user_unit_nid=All&field_user_job_title_value=All

# All of Insight: https://www.insight-centre.org/about/team?field_user_fullname_value=&field_user_insight_institude_value=All&field_user_unit_nid=All&field_user_job_title_value=All
    start_urls = ['https://www.insight-centre.org/about/team?field_user_fullname_value=&field_user_insight_institude_value=Dublin+City+University+%28DCU%29&field_user_unit_nid=All&field_user_job_title_value=All']

    def parse(self, response):
        PERSON_SELECTOR = 'li .institution'
        img_urls = []
        for person in response.css(PERSON_SELECTOR):    # Cycles through people
            item = InsightCrawlerItem()                 # VERY IMPORTANT, resets item list
            NAME_SELECTOR = 'a ::text'                  # Selects Name
            IMAGE_SELECTOR = 'img ::attr(src)'          # Selects Image
            POSITION_SELECTOR = ".//div[@class='views-field views-field-field-user-job-title']/div[@class='field-content']/text()"                     # Selects Position
         
            item["image_urls"] = [person.css(IMAGE_SELECTOR).extract_first()]   # Stores info in items
            item["first_name"] = person.css(NAME_SELECTOR).extract_first().split(' ')[1]
            item["last_name"] = person.css(NAME_SELECTOR).extract_first().split(' ')[2-3]
            item["position"] = person.xpath(POSITION_SELECTOR).extract_first()

            yield item                                  # Yields image url, name, etc.
        
        NEXT_PAGE_SELECTOR = '.pager__item--next a ::attr(href)'    # Selects next page
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:                                   # If there's a next page, go to next page
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse)                    # Recurse through function

