import scrapy
from urllib.parse import urljoin
from pathlib import Path

class WikipediaTechSpider(scrapy.Spider):
    
    name = 'wiki_tech_outline_spider'
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Contents/Technology_and_applied_sciences']

    def parse(self, response):

        outlinesSection = response.css("div.contentsPage__section")[0]

        filename = f"contentsSection.html"
        Path(filename).write_text(outlinesSection.get())
        self.log(f"Saved file {filename}")

        seenLinks = set()

        for title in outlinesSection.css("li"):
            for link in title.css("a"):

                if not link.xpath('ancestor::sup'): # to remove citations

                    if (link.css('::text').get(), link.css('::attr(href)').get()) not in seenLinks: # prevent duplications of links added because of outer for loop over li tags

                        seenLinks.add((link.css('::text').get(), link.css('::attr(href)').get()))

                        yield {
                            'link_text': link.css('::text').get(),
                            'link_url': link.css('::attr(href)').get()
                        }
