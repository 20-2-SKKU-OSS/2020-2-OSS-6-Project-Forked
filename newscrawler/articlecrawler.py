#!/usr/bin/env python
# -*- coding: euc-kr -*-

from time import sleep
from bs4 import BeautifulSoup
from exceptions import *
from multiprocessing import Process
import os
import calendar
import requests
import csv
import re


class ArticleCrawler:
    def __init__(self):
        self.category = {'��ġ': 100, '����': 101, '��ȸ': 102, '��Ȱ��ȭ': 103, '����': 104, 'IT����': 105}
        self.selected_category = []
        self.date = {'startyear': 0, 'endyear': 0, 'endmonth': 0}

    def set_category(self, *args):
        for key in args:
            if self.category.get(key) is None:
                raise InvalidCategory(key)
            else:
                self.selected_category = args

    def set_date_range(self, startyear, endyear, endmonth):
        args = [startyear, endyear, endmonth]
        if startyear > endyear:
            raise InvalidYear(startyear, endyear)
        if endmonth < 1 or endmonth > 12:
            raise InvalidMonth(endmonth)
        for key, date in zip(self.date, args):
            self.date[key] = date
        print(self.date)

    def clearcontent(self, text):
        special_symbol_removed_content = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n�㢺�ߢ���\\\=\(\'\"]', '', text)
        end_phrase_removed_content = re.sub(
            '���� ����|TV�÷��̾�| ������ ����|flash ������ ��ȸ�ϱ� ���� �Լ� �߰�fuctio flashremoveCallback|tt|t|��Ŀ ��Ʈ|xa0', '',
            special_symbol_removed_content)
        blank_removed_content = end_phrase_removed_content.strip().replace('   ', '')  # ���� ���� ����
        reversed_content = ''.join(reversed(blank_removed_content))  # ��� ������ reverse �Ѵ�.
        content = ''
        for i in range(0, len(blank_removed_content)):
            if reversed_content[
               i:i + 2] == '.��':  # reverse �� ��� ������, ".��"�� ������ ��� ��� ������ ���� ���̱� ������ ��� ������ ���� ���� ����, ���� ���� ������ �� �����.
                content = ''.join(reversed(reversed_content[i:]))
                break
        return content

    def clearheadline(self, text):
        special_symbol_removed_headline = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n�㢺�ߢ���\\\=\(\'\"]', '', text)
        return special_symbol_removed_headline

    def find_news_totalpage(self, url):
        try:
            totlapage_url = url
            request_content = requests.get(totlapage_url)
            document_content = BeautifulSoup(request_content.content, 'html.parser')
            headline_tag = document_content.find('div', {'class': 'paging'}).find('strong')
            regex = re.compile(r'<strong>(?P<num>\d+)')
            match = regex.findall(str(headline_tag))
            return int(match[0])
        except Exception:
            return 0

    def make_news_page_url(self, category_url, startyear, lastyear, startmonth, lastmonth):
        maked_url = []
        final_startmonth = startmonth
        final_lastmonth = lastmonth
        for year in range(startyear, lastyear + 1):
            if year != lastyear:
                startmonth = 1
                lastmonth = 12
            else:
                startmonth = final_startmonth
                lastmonth = final_lastmonth
            for month in range(startmonth, lastmonth + 1):
                for month_day in range(1, calendar.monthrange(year, month)[1] + 1):
                    url = category_url
                    if len(str(month)) == 1:
                        month = "0" + str(month)
                    if len(str(month_day)) == 1:
                        month_day = "0" + str(month_day)
                    url = url + str(year) + str(month) + str(month_day)
                    final_url = url  # page ��¥ ������ �ְ� page ������ ���� url �ӽ� ����
                    totalpage = self.find_news_totalpage(
                        final_url + "&page=1000")  # totalpage�� ���̹� ������ ������ �̿��ؼ� page=1000���� ������ totalpage�� �˾Ƴ� ( page=1000�� �Է��� ��� �������� �������� �ʱ� ������ page=totalpage�� �̵� ��)
                    for page in range(1, totalpage + 1):
                        url = final_url  # url page �ʱ�ȭ
                        url = url + "&page=" + str(page)
                        maked_url.append(url)
        return maked_url

    def parse(self, category_name):
        print(category_name + " pid: " + str(os.getpid()))

        file = open('Article_' + category_name + '.csv', 'w', encoding='euc_kr', newline='')
        wcsv = csv.writer(file)

        url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(
            self.category.get(category_name)) + "&date="
        final_urlday = self.make_news_page_url(url, self.date['startyear'], self.date['endyear'], 1, self.date[
            'endmonth'])  # startyear�� 1�� ~ endyear�� endmonth ��¥���� ��縦 �����մϴ�.
        print(category_name + " Urls are generated")
        print("The crawler starts")

        for URL in final_urlday:

            regex = re.compile("date=(\d+)")
            news_date = regex.findall(URL)[0]

            request = requests.get(URL)
            document = BeautifulSoup(request.content, 'html.parser')
            tag_document = document.find_all('dt', {'class': 'photo'})

            post = []
            for tag in tag_document:
                post.append(tag.a.get('href'))  # �ش�Ǵ� page���� ��� ������ URL�� post ����Ʈ�� ����

            for content_url in post:  # ��� URL
                sleep(0.01)
                request_content = requests.get(content_url)
                document_content = BeautifulSoup(request_content.content, 'html.parser')

                try:
                    tag_headline = document_content.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                    text_headline = ''  # ���� ��� ���� �ʱ�ȭ
                    text_headline = text_headline + self.clearheadline(str(tag_headline[0].find_all(text=True)))
                    if not text_headline:  # ������ ��� ��� ���� ó��
                        continue

                    tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                    text_sentence = ''  # ���� ��� ���� �ʱ�ȭ
                    text_sentence = text_sentence + self.clearcontent(str(tag_content[0].find_all(text=True)))
                    if not text_sentence:  # ������ ��� ��� ���� ó��
                        continue

                    tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                    text_company = ''  # ��л� �ʱ�ȭ
                    text_company = text_company + str(tag_company[0].get('content'))
                    if not text_company:  # ������ ��� ��� ���� ó��
                        continue

                    wcsv.writerow([news_date, category_name, text_company, text_headline, text_sentence, content_url])

                except Exception as ex:  # UnicodeEncodeError ..
                    print(ex)
                    pass
        file.close()

    def start(self):
        for category_name in self.selected_category:
            proc = Process(target=self.parse, args=(category_name,))
            proc.start()


if __name__ == "__main__":
    Crawler = ArticleCrawler()
    Crawler.set_category("��ġ", "����")  # ��ġ, ����, ��Ȱ��ȭ, IT����, ��ȸ ī�װ� ��� ����
    Crawler.set_date_range(2017, 2018, 4)  # 2017�� 1������ 2018�� 4������ ũ�Ѹ� ����
    Crawler.start()
