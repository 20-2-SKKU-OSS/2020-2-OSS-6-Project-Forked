#!/usr/bin/env python
# -*- coding: euc-kr -*-

import calendar
import requests
from time import sleep
from bs4 import BeautifulSoup
import csv
import re

def Clearcontent(text):
    first = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n�㢺�ߢ���\\\=\(\'\"]','', text)
    second = re.sub('���� ����|TV�÷��̾�| ������ ����|flash ������ ��ȸ�ϱ� ���� �Լ� �߰�fuctio flashremoveCallback|tt|t|��Ŀ ��Ʈ|xa0', '', first)
    Third = second.strip().replace('   ', '')  # ���� ���� ����
    Four = ''.join(reversed(Third))  # ��� ������ reverse �Ѵ�.
    content = ''
    for i in range(0, len(Third)):
        if Four[i:i+2] == '.��':  # reverse �� ��� ������, ".��"�� ������ ��� ��� ������ ���� ���̱� ������ ��� ������ ���� ���� ����, ���� ���� ������ �� �����.
            content = ''.join(reversed(Four[i:]))
            break
    return content

def Clearheadline(text):
    first = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n�㢺�ߢ���\\\=\(\'\"]', '', text)
    return first

def html_totalpage(url):
    totlapage_url = url
    request_content = requests.get(totlapage_url)
    document_content = BeautifulSoup(request_content.content, 'html.parser')
    Tag_headline = document_content.find('div', {'class': 'paging'}).find('strong')
    regex = re.compile(r'<strong>(?P<num>\d+)')
    match = regex.findall(str(Tag_headline))
    return int(match[0])

def Make_url(URL, startyear, lastyear, startmonth, lastmonth):
    Maked_url = []
    final_startmonth = startmonth
    final_lastmonth = lastmonth
    for year in range(startyear, lastyear + 1):
        if year != lastyear:
            startmonth = 1
            lastmonth = 12
        else:
            startmonth = final_startmonth
            lastmonth = final_lastmonth
        for Month in range(startmonth, lastmonth + 1):
            for Month_Day in range(1, calendar.monthrange(year, Month)[1] + 1):
                url = URL
                if len(str(Month)) == 1:
                    Month = "0" + str(Month)
                if len(str(Month_Day)) == 1:
                    Month_Day = "0" + str(Month_Day)
                url = url + str(year) + str(Month) + str(Month_Day)
                final_url = url  # page ��¥ ������ �ְ� page ������ ���� url �ӽ� ����
                totalpage = html_totalpage(final_url+"&page=1000") # totalpage�� ���̹� ������ ������ �̿��ؼ� page=1000���� ������ totalpage�� �˾Ƴ� ( page=1000�� �Է��� ��� �������� �������� �ʱ� ������ page=totalpage�� �̵� ��)
                for page in range(1, totalpage + 1):
                    url = final_url # url page �ʱ�ȭ
                    url = url + "&page=" + str(page)
                    Maked_url.append(url)
    return Maked_url


# Main
url_list = [100, 101,102, 103, 104, 105]
Category = ["��ġ", "����" "��ȸ", "��Ȱ��ȭ", "����", "IT����"]

for url_num in url_list:  # URL ī�װ�
    category = Category[url_list.index(url_num)]  # URL �ε����� Category �ε����� ��ġ�� ��� �� ���� ��ġ
    file = open('Article_' + category + '.csv', 'w', encoding='euc-kr', newline='')
    wcsv = csv.writer(file)

    url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" +str(url_num)+"&date="
    final_urlday = Make_url(url, 2017, 2018, 1, 6) # 2017�� 1�� ~ 2018�� 6�� ������ ������ ��縦 �����մϴ�.
    print("url success")

    for URL in final_urlday:
        request = requests.get(URL)
        document = BeautifulSoup(request.content, 'html.parser')
        Tag = document.find_all('dt', {'class': 'photo'})

        post = []
        for tag in Tag:
            post.append(tag.a.get('href'))  # �ش�Ǵ� page���� ��� ������ URL�� post ����Ʈ�� ����

        for content_url in post:  # ��� URL
            sleep(0.01)
            request_content = requests.get(content_url)
            document_content = BeautifulSoup(request_content.content, 'html.parser')

            try:
                Tag_headline = document_content.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                text_headline = ''  # ���� ��� ���� �ʱ�ȭ
                text_headline = text_headline + Clearheadline(str(Tag_headline[0].find_all(text=True)))
                if not text_headline:  # ������ ��� ��� ���� ó��
                    continue

                Tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                text_sentence = ''  # ���� ��� ���� �ʱ�ȭ
                text_sentence = text_sentence + Clearcontent(str(Tag_content[0].find_all(text=True)))
                if not text_headline: # ������ ��� ��� ���� ó��
                    continue

                Tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                text_company = ''  # ��л� �ʱ�ȭ
                text_company = text_company + str(Tag_company[0].get('content'))
                if not text_headline: # ������ ��� ��� ���� ó��
                    continue

                wcsv.writerow([text_headline, text_sentence, text_company, category])

            except:  # UnicodeEncodeError ..
                pass
    file.close()
