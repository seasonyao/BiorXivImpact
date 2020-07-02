import requests
import pandas as pd
import seaborn as sns
import numpy as np
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
from tqdm import tqdm

output_name = "Path/to/output/CSVFile"

# Define the URL and start/stop years

url = "http://biorxiv.org/search/jcode%3Abiorxiv%20limit_from%3A2013-1-01%20limit_to%3A2020-2-27%20numresults%3A75%20format_result%3Astandard"

resp = requests.post(url)

# I'm not going to print this because it messes up the HTML rendering
# But you get the idea...probably better to look in Chrome anyway ;)
text = bs(resp.text)
total_num = int(str(text).split('window.googleanalytics_search_results = ')[1].split(";")[0])
total_pages = int(text.find('div', attrs={'class': 'pager-wrapper pager-full-pagination clearfix pager-no-first-items'}).text.strip().split('…')[1])

print("total papers num:", total_num)
print('total_pages num', total_pages)

# Now we'll do the scraping...
all_titles = []
all_authors = []
all_abstracts = []
all_date = []
for page in range(total_pages):
    print("now process page ", page, "    now paper num ", len(all_titles))
    this_page_url = url + "?page=" + str(page)
    resp = requests.post(this_page_url)
    html = bs(resp.text)
    # Collect the articles in the result in a list
    articles = html.find_all('li', attrs={'class': 'search-result'})
    for article in articles:
        # Pull the title, if it's empty then skip it
        title = article.find('span', attrs={'class': 'highwire-cite-title'})
        if title is None:
            continue
        title = title.text.strip()
        #---------------------------------------
        # Now collect author information
        this_paper_authors = []
        authors = article.find_all('span', attrs={'class': 'highwire-citation-author'})
        for author in authors:
            this_paper_authors.append((author.text))
        #---------------------------------------
        # Pull the title, if it's empty then skip it
        abstract = article.find('span', attrs={'class': 'highwire-cite-metadata-doi highwire-cite-metadata'})
        if abstract is None:
            continue
        abstract_url = abstract.text.split("doi:")[1].strip()
        resp = requests.post(abstract_url)

        text = bs(resp.text)
        abstract = text.find('div', attrs={'class': 'section abstract'})
        if abstract is None:
            continue
        try:
            abstract = abstract.text.split('Abstract')[1]
        except:
            pass
        #---------------------------------------
        date = text.find('div', attrs={'class': 'panel-pane pane-custom pane-1'}).text.strip().split('\xa0')[1].strip('.')
        all_date.append(date)
        all_authors.append(this_paper_authors)
        all_abstracts.append(abstract)
        all_titles.append(title)
print("get all data")
        
df = pd.DataFrame({'title':all_titles, 'authors':all_authors, 'date':all_date, 'abstract':all_abstracts})
df.to_csv(output_name)