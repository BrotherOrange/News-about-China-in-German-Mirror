# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiegelItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    Erscheinungsdatum = scrapy.Field()
    Ueberschrift = scrapy.Field()
    Vorspann = scrapy.Field()
    Channel = scrapy.Field()
    Seite = scrapy.Field()
    Epaperkey = scrapy.Field()
    Score = scrapy.Field()
    Text = scrapy.Field()

    pass
