import requests
import string
from bs4 import BeautifulSoup
import csv
import pprint

TENLONG_URL = 'https://www.tenlong.com.tw/search'
BOOKS_URL = 'http://search.books.com.tw/search/query/key/<keyword>/cat/BKA'


# clear the punctuation for string
def strclear(text, newsign=''):
    signtext = string.punctuation + ' ' + '｜' + '、' + '：' + '－' + newsign
    signrepl = '@' * len(signtext)
    signtable = str.maketrans(signtext, signrepl)
    return text.translate(signtable).replace('@', '')


# search tenlong.com.tw by keyword
def get_tenlong_page(url, keyword, page_number):
    params = {
        'utf8': '%E2%9C%93',
        'authenticity_token': 'Tj68PmOdiG8LxEXu%2F%2FFvGJASIBgeIsP5t4ZMdUpq6%2B3lgIm3hqNz5AQmfDh7Nyf0ygtn1WEPgtZL3uI8samp7w%3D%3D',
        'keyword': keyword,
        'page': page_number,
        'top-search-btn': None
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    }

    resp = requests.get(url, params=params, headers=headers)

    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


# extract the title, author, price from tenlong search result
def get_book_list(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    books = soup.find_all('div', {'class': 'book-data'})

    result = []
    for book in books[:-1]:
        title = book.h3.text.split('(')[0].strip()
        title = strclear(title)
        author = book.find('span', {'class': 'author'}).text.strip()
        price = book.find('span', {'class': 'price'}
                          ).text.split('$')[1].strip()

        result.append([{'title': title, 'author': author, 'price': price}])

    return result


# search books.com.tw by keyword
def get_books_page(url, keyword):
    url = url.replace('<keyword>', keyword)
    resp = requests.get(url)

    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


# loop through books list to find the same book then extract title, author, price
def find_the_same_book(dom, target_book):
    soup = BeautifulSoup(dom, 'html.parser')
    books = soup.find_all('li', {'class': 'item'})
    print('searching ', target_book, ' ...')
    for book in books:
        title = book.a['title']
        title = strclear(title)
        author = []
        for e in book.find_all('a', {'rel': 'go_author'}):
            author.append(e.text)
        price = book.find('span', {'class': 'price'})('strong')[-1].b.text

        if title == target_book:
            print('find it')
            return {'title': title, 'author': author, 'price': price}

    return {None}


def output_to_csv(csvCursor, data, category):
    for entry in data:
        if entry[1] != {None}:
            csvCursor.writerow([
                category,
                entry[0]['title'],
                entry[0]['author'],
                entry[0]['price'],
                entry[1]['price']
            ])


def crawl_topic(topic, page_number):
    page = get_tenlong_page(TENLONG_URL, topic, page_number)
    if page:
        book_list = get_book_list(page)

    for book in book_list:
        page = get_books_page(BOOKS_URL, book[0]['title'])
        if page:
            book.append(find_the_same_book(page, book[0]['title']))
        else:
            book.append({None})

    return book_list


if __name__ == '__main__':
    # add keyword you want to search here
    keywords = ['Python', 'C', 'Java', 'C++', 'C#',
                'R', 'JavaScript', 'PHP', 'Go', 'Swift']

    file = open('./result.csv', 'w')
    csvCursor = csv.writer(file)
    csvHeader = ['category', 'title', 'author', 'tenlong', 'books']
    csvCursor.writerow(csvHeader)

    for keyword in keywords:
        for i in range(4):
            result = crawl_topic(keyword, i+1)
            output_to_csv(csvCursor, result, keyword)

    file.close()
