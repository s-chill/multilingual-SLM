import requests
from bs4 import BeautifulSoup
import os
import json

def scrape_wikipedia_page(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for unwanted in soup(['table', 'script', 'style', 'sup', 'ul', 'ol']):
        unwanted.decompose()
    
    for header in soup.find_all(['h2', 'h3']):
        if header.get_text(strip=True) in ['References', 'See also', 'External links']:
            for sibling in header.find_all_next():
                if sibling.name in ['h2', 'h3']:
                    break
                sibling.decompose()
            header.decompose()
    
    paragraphs = soup.find_all('p')
    
    text_content = '\n\n'.join(paragraph.get_text(separator=' ', strip=True) for paragraph in paragraphs if paragraph.get_text(strip=True))
    
    return text_content

def read_jsonl_and_scrape(jsonl_file):
    if not os.path.exists('data/textFiles'):
        os.makedirs('data/textFiles')
    
    with open(jsonl_file, 'r') as file:
        for line in file:
            entry = json.loads(line)
            link_text = entry['link_text']
            link_url = entry['link_url']
            
            print(f"Scraping: {link_text} from {link_url}")
            text_data = scrape_wikipedia_page(link_url)
            
            if text_data:
                filename = link_text.replace(' ', '_').replace('/', '_') + '.txt'
                filepath = os.path.join('data/textFiles', filename)
                
                with open(filepath, 'w', encoding='utf-8') as text_file:
                    text_file.write(text_data)
                print(f"Saved: {filepath}")

jsonl_file_path = "processedFinalLinks.jsonl"
read_jsonl_and_scrape(jsonl_file_path)

# url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
# text_data = scrape_wikipedia_page(url)

# if text_data:
#     print(text_data)