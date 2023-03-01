from requests import get
from bs4 import BeautifulSoup
import os
import json


def scrape_one_page(topic):
    base_url="https://inshorts.com/en/read/"
    response=get("https://inshorts.com/en/read/"+topic)
    soup= BeautifulSoup(response.content, 'html.parser')
    titles=soup.find_all('span', itemprop='headline')
    summaries=soup.find_all('div', itemprop='articleBody')
    summary_list=[]
    
    for i in range(len(titles)):
        temp_dict={'title':titles[i].text, 'text':summaries[i].text, 'category': topic}
        summary_list.append(temp_dict)
    return summary_list


def get_blog_articles():
    link_list=['https://codeup.com/tips-for-prospective-students/coding-bootcamp-or-self-learning/',
              'https://codeup.com/codeup-news/codeup-best-bootcamps/',
              'https://codeup.com/events/black-excellence-in-tech-panelist-spotlight/',
              'https://codeup.com/events/black-excellence-in-tech-panelist-spotlight-james-cooper/',
              'https://codeup.com/events/black-excellence-in-tech-panelist-spotlight-stephanie-jones/']
    article_info = []
    file = 'blog_posts.json'
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
    headers = {'User-Agent': 'Codeup Data Science'}
    article_info = []
    for article in article_list:
        response = get(article, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        info_dict = {'title': soup.find('h1').text,
                     'date_published': soup.find('span', class_='published').text,
                     'content': soup.find('div', class_='entry-content').text}
        
        article_info.append(info_dict)
        with open(file, 'w') as f:
            json.dump(article_info, f)
    return article_info 


def get_news_articles(topic_list):
    file='news_articles.json'
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
    final_list=[]
    for topic in topic_list:
        final_list.extend(scrape_one_page(topic))
    with open(file, 'w') as f:
        json.dump(final_list, f)
    return final_list