# KoreaNewsCrawler 프로젝트 기여 - OSS 6조
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

네이버 포털의 올라오는 기사들을 크롤링 해주는 크롤러로, **(네이버 포털 외의 기사들을 크롤링하는 기능도 추가할 예정입니다.)**  
크롤링 가능한 기사 카테고리는 정치, 경제, 생활문화, IT과학, 사회, 세계, 오피니언, 연합뉴스속보 입니다.  
**(기사 카테고리를 더 명확히 하기 위해 병합/삭제/수정을 할 예정입니다.)**  

## 관련 외부링크

[KoreaNewsCrawler_github_홈페이지](https://github.com/lumyjuwon/KoreaNewsCrawler)  
[OSS_6조_static_page_](https://20-2-skku-oss.github.io/2020-2-OSS-6/)

## For comfortable

* **사용자가 카테고리/기간을 실행창에서 입력하는 기능**  

 **sample.py코드에 기간과 카테고리를 직접 바꿔야하는 번거로움을 제거했습니다.**

* **원하는 키워드가 포함된 제목의 기사들을 크롤링하는 기능**
 
 **사용자가 기간/카테고리/원하는 키워드를 입력하면 그 키워드가 포함된 제목의 기사들만 크롤링하는 기능을 추가하였습니다.**
 
* **원하는 키워드가 포함된 내용의 기사들을 크롤링하는 코드 추가**

 **파일명을 입력하고, 원하는 키워드를 입력하면 그 키워드가 포함된 기사가 csv파일의 몇 번째 줄에 있는지 출력하는 코드를 추가하였습니다.**

## Method

* **set_category(category_name)**
  
 이 메서드는 수집하려고자 하는 카테고리는 설정하는 메서드입니다.  
 파라미터에 들어갈 수 있는 카테고리는 '정치', '경제', '사회', '생활문화', 'IT과학', '세계', '오피니언','연합뉴스속보'입니다.  
 파라미터는 여러 개 들어갈 수 있습니다.  
 category_name: 정치, 경제, 사회, 생활문화, IT과학, 세계, 오피니언, 연합뉴스속보 or politics, economy, society, living_culture, IT_science, world, opinion, Yeonhap Newsflash
  
* **set_date_range(startyear, startmonth, endyear, endmonth)**
  
 이 메서드는 수집하려고자 하는 뉴스의 기간을 의미합니다. 기본적으로 startmonth월부터 endmonth월까지 데이터를 수집합니다.
  
* **start(isMultiProc)**
  
 이 메서드는 크롤링 실행 메서드입니다.
 > 2020-12-06 Edited : 실행 메서드에 멀티 프로세싱 여부를 선택할 수 있게 하는 argument를 추가했습니다. 멀티 프로세싱을 적용하고자 할 때, True Boolean을 전달하면 됩니다.
  
## Example
```
from korea_news_crawler.articlecrawler import ArticleCrawler

Crawler = ArticleCrawler()  
Crawler.set_category("정치", "IT과학", "economy")  
Crawler.set_date_range(2017, 1, 2018, 4)  
Crawler.start()
```
  2017년 1월 ~ 2018년 4월까지 정치, IT과학, 경제 카테고리 뉴스를 멀티프로세서를 이용하여 병렬 크롤링을 진행합니다.
  
## Multi Process 안내
  intel i5 9600 cpu로 테스트 해본 결과 1개의 카테고리 당 평균 **8%** 의 cpu 점유율을 보였습니다.  
  크롤러를 실행하는 컴퓨터 사양에 맞게 카테고리 개수를 맞추시거나 반복문을 이용하시기 바랍니다.
  
  ![ex_screenshot](./img/multi_process.PNG)
  
   > 2020-12-06 Edited : start() 메서드에 멀티 프로세싱 여부를 선택할 수 있게 하는 argument를 추가했습니다. 
   >    > 멀티 프로세싱을 적용하지 않으면, 크롤링 실행 도중 진행상황을 출력되는 csv파일에서 확인할 수 있습니다.
      
## Results
 ![ex_screenshot](./img/article_result.PNG)
 ![ex_screenshot](./img/sport_resultimg.PNG)
 
 Colum A: 기사 날짜  
 Colum B: 기사 카테고리  
 Colum C: 언론사  
 Colum D: 기사 제목  
 Colum E: 기사 본문  
 Colum F: 기사 주소  
 
 수집한 모든 데이터는 csv 확장자로 저장됩니다.  


# KoreaNewsCrawler (English version)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This crawler crawles news from portal Naver  
Crawlable article categories include politics, economy, lifeculture, global, IT/science, society.  
In the case of sports articles, that include Baseball, soccer, basketball, volleyball, golf, general sports, e-sports.  

**In the case of sports articles, you can't use sport article crawler because html form is changed. I will update sport article crawler 
as soon as possible.**

## User Python Installation
  * **KoreaNewsCrawler**

    ``` pip install KoreaNewsCrawler ```
    
## Method

* **set_category(category_name)**
 
 This method is setting categories that you want to crawl.  
 Categories that can be entered into parameters are politics, economy, society, living_culture, IT_science, and Yeonhap Newsflash. 
 Multiple parameters can be entered.
  
* **set_date_range(startyear, startmonth, endyear, endmonth)**
  
 This method represents the duration of the news you want to collect.  
 Data is collected from startmonth to endmonth.
  
* **start(isMultiProc)**
  
 This method is the crawl execution method.
 > 2020-12-06 Edited : MultiProcessing option is now added to exectution method. You should set 'isMultiProc' as True when it required.
  
## Example
```
from korea_news_crawler.articlecrawler import ArticleCrawler

Crawler = ArticleCrawler()  
Crawler.set_category("politics", "IT_science", "economy")  
Crawler.set_date_range(2017, 1, 2018, 4)  
Crawler.start()
```
 From January 2017 to April 2018, Parallel crawls will be conducted using multiprocessors for political, IT science, world, and economic category news.
  
## Multi Process Information
Testing with intel i5 9600 cpu showed an average ** 8% ** cpu share per category.  
Please adjust the number of categories to match the specifications of the computer running the crawler, or use a loop.
  
  ![ex_screenshot](./img/multi_process.PNG)
     
   > 2020-12-06 Edited : MultiProcessing option is now added to method 'start()'.
   >    > When multiprocessing turns off, you can check the csv file from ongoing crwaler's result.
      
## Results
 ![ex_screenshot](./img/article_result.PNG)
 ![ex_screenshot](./img/sport_resultimg.PNG)
 
 Colum A: Article Date  
 Colum B: Article Category  
 Colum C: Article Press  
 Colum D: Article headline  
 Colum E: Article Content  
 Colum F: Article URL  
 
 All collected data is saved as a csv.
 
## License
 Apache License 2.0
 
