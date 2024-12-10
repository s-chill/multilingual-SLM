import scrapy
from urllib.parse import urljoin
from pathlib import Path
import json

class DomainSpider(scrapy.Spider):
    name = 'domain_spider'
    seenLinks = set()
    dataToSave = []

    topics_file = Path('topics.jsonl')
    start_urls = []
    
    with topics_file.open() as fileToRead:
        for line in fileToRead:
            topic = json.loads(line)
            link_url = urljoin('https://en.wikipedia.org', topic['link_url'])
            # print(link_url)
            start_urls.append(link_url)
            # print(start_urls)

    # print(start_urls)
    # start_urls = start_urls[:2]
    # print(start_urls)
    seenLinks = set()
    dataToSave = []

    def parse(self, response):
        bodyText = response.css("div#mw-content-text")
        # domainName = response.url.split('/')[-1]

        # filename = f"{domainName}.html"
        # Path(filename).write_text(bodyText.get())
        # self.log(f"Saved file {filename}")

        for heading in bodyText.css("div.mw-heading.mw-heading2"):
            title = heading.css("h2::text").get()
            content = heading.xpath("following-sibling::*[not(self::div[@class='mw-heading mw-heading2'])]")
            
            self.parse_section_helper(title, content)

        for item in self.dataToSave:
            yield item

    def parse_section_helper(self, title, content):
        if title not in ["References", "External links", "See also"]: #exclude these sections from being scraped
            for element in content:
                if element.root.tag == 'ul':
                    self.parse_list_helper(element)
                elif element.root.tag == 'div' and 'mw-heading mw-heading2' in element.attrib.get('class', ''):
                    break

    def parse_list_helper(self, ul_element, depth=0):
        for li in ul_element.css('li'):
            link = li.css('a:first-child')
            if link:
                link_title = link.css('::text').get()
                link_url = link.attrib.get('href')

                if "wiki/" in link_url and not any(x in link_url for x in ["Index", "List", "Glossary"]): #exclude non-article links and external links
                    full_url = urljoin(self.start_urls[0], link_url)
                    
                    if link_title and (link_title, link_url) not in self.seenLinks:
                        self.dataToSave.append({
                            'link_text': link_title,
                            'link_url': full_url
                        })
                        self.seenLinks.add((link_title, link_url))

            nested_ul = li.css('ul') #recurse for nested lists
            if nested_ul:
                self.parse_list_helper(nested_ul, depth + 1)