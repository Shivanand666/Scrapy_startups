# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapStartupItem(scrapy.Item):
    Comp_Name = scrapy.Field()
    e27_url = scrapy.Field()
    comp_url = scrapy.Field()
    Description = scrapy.Field()
    Long_descr = scrapy.Field()
    Location = scrapy.Field()
    found_date = scrapy.Field()
    CEO = scrapy.Field()
    Tags = scrapy.Field()
    Phone = scrapy.Field()
    Email = scrapy.Field()
    Emp_range=scrapy.Field()
    
