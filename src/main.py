from bs4 import BeautifulSoup
import urllib.request
import os

questions = {};
categories_url = "https://jeopardyquestions.com/categories"

def get_html_from_url(url):
    uo = urllib.request.urlopen(url)
    data = uo.read()
    content = data.decode("utf8")

    return content


def get_link_to_answer(linkList):
    for link in linkList:
        if link.getText() == 'View Answer':
            return link['href']


def get_answer(link_to_answer):
    answer_html = get_html_from_url(link_to_answer)
    answer = BeautifulSoup(answer_html, 'html.parser').find('div', {"class": "answer"})

    return answer.getText().strip()


def get_questions_from_category(category):
    questions_html = get_html_from_url(category['link'])
    question_cards = BeautifulSoup(questions_html, 'html.parser').findAll('div', {"class": "card"})

    questions = []

    for question in question_cards:
        links = question.findAll('a')
        question = {
            'title': question.find('p').getText(),
            'answer': get_answer(get_link_to_answer(links))
        }

        questions.append(question)

        print(question)
        print()

    return questions


def get_categories(page):
    url = categories_url + "?page=" + str(page)
    content = get_html_from_url(url)
    category_cards = BeautifulSoup(content, 'html.parser').findAll("div", {"class": "category-card"})

    categories = [];

    for card in category_cards:
        category_data = {
            'title': card.find('h1').getText(),
            'link': card.find('a')['href']
        }

        category_data['questions'] = get_questions_from_category(category_data)
        categories.append(category_data)

    return categories
        


def execute_fetcher():
    page = 1
    if os.path.exists("lock"):
       file = open("lock", "r+")
       page = int(file.read());

    get_categories(page)

    f = open("lock", "w+")
    f.write(str(page + 1))
    f.close()


execute_fetcher()