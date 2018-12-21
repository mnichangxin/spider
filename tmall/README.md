# Spider of tmall

## Introduction

Crawling [tmall](https://www.tmall.com).

## Enviroment:

* Python version: `Python 2.7.13`
* Depend modules: `requests`

## Usage

Setting enviroment of above when you use it. `main.py` is main entry of project. And run command:

```
    python main.py
```

Run prompt to enter the number of comment pages to be crawled. A csv file will be created locally and can be viewed directly in Excel.

## Philosophy

By observing, Tmall's product data is dynamically loaded and stored in a name `https://rate.tmall.com/list_detail_rate.htm?itemId=537734028319&spuId=696624585&sellerId=197232874&order=3&currentPage=` js file. So by crawling such a file and change `currentPage=` value to crawl comments.
