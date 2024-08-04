from bs4 import BeautifulSoup
import requests

#검색어
search = input("검색할 키워드를 입력해주세요")

url = "https://www.coupang.com/np/search?component=&q=" + search + "&channel=user"

headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

#html 불러오기
original_html = requests.get(url, headers=headers)
html = BeautifulSoup(original_html.text, "html.parser")

goods = html.select("div.search-content search-content-with-feedback > ul.search-product-list > li a")

print(goods)
print(len(goods),"개의 신발이 검색됨")