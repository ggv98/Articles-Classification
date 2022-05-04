import requests
from bs4 import BeautifulSoup
import pandas as pd

ACCEPTED_CATEGORIES = ["Бизнес", "Имоти", "Технологии", "Култура"] #'Спорт', 'Любопитно', "Крими", "Авто"
DATA_ORDER = ['topic', 'title', 'text', 'author', 'date', 'visitors', 'rate', 'vote_count', 'key_words']
ARTICLES_PER_FILE = 500

def get_data(page_source):
    soup = BeautifulSoup(page_source, features="html.parser")
    topic = soup.find('span', class_="symbol-next").parent.next
    print(topic)
    if topic not in ACCEPTED_CATEGORIES:
        return False, dict()
    title = soup.find('title').contents[0].split(' ᐉ')[0]
    date = soup.find('span', class_="ndt").attrs['content']
    visitors = soup.find('span', class_="nv").text
    author = soup.find('span', class_="author_name").text

    if soup.find('span', class_="rate"):
        rate = soup.find('span', class_="rate").text
    else:
        rate = None

    if soup.find('span', class_="votesCount"):
        vote_count = soup.find('span', class_="votesCount").text
    else:
        vote_count = None
    if soup.find('ul', class_="tags no-print",):
        key_words = soup.find('ul', class_="tags no-print",).text.replace('-', '').replace('\t', '').replace('  ', ' ').strip().split(' ')
    else:
        key_words = None
    
    text = ""
    for p in soup.find('div', class_="news-text").find_all('p'):
        text += p.text

    data = {
        'topic': topic,
        'title': title,
        'text': text,
        'author': author,
        'date': date,
        'visitors': visitors,
        'rate': rate,
        'vote_count': vote_count,
        'key_words': key_words,
    }
    return True, data

def start_scraping():
    data_frame = pd.DataFrame(columns=DATA_ORDER)
    count = 0
    for article_index in range(468326, 100000, -1):
        if count == 10000:
            break
        print(count)
        url = "https://fakti.bg/imoti/" + str(article_index)
        print('Start Scraping: '+ url)
        try:
            result = requests.get(url)
        except:
            continue
        if result.status_code == 200:
            success, data = get_data(result.content)
            if success:
                count += 1
                data_frame = data_frame.append(data, ignore_index = True)
                print(data['topic'])
                if count%ARTICLES_PER_FILE == 0:
                    file_name = 'data'+ str(19 + int(count/ARTICLES_PER_FILE)) + '.csv'
                    data_frame.to_csv(file_name, index=False)
                    data_frame = pd.DataFrame(columns=DATA_ORDER)
            else:
                print("False")


start_scraping()
#394175