import requests
from bs4 import BeautifulSoup
from donations.models import Goods
import re

category_list = {
    'foods': 'https://www.coupang.com/np/categories/393760',
    'cleaning': 'https://www.coupang.com/np/categories/469638?listSize=60&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=Y&selectedPlpKeepFilter=&sorter=bestAsc&filter=&component=469538&rating=0',
    'tissue': 'https://www.coupang.com/np/categories/464920?listSize=60&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=Y&selectedPlpKeepFilter=&sorter=bestAsc&filter=&component=464820&rating=0'
}



def crawl_items(category):
  # url='https://www.coupang.com/np/search?component=&q=%ED%9C%B4%EC%A7%80&channel=user'
  if (category=='foods'):
      item_url=category_list['foods']
  elif (category=='cleaning'):
      item_url=category_list['cleaning']
  elif (category=='tissue'):
      item_url=category_list['tissue']

  url=item_url
  headers = {
       "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
  }

  response = requests.get(url, headers=headers)
  if response.status_code != 200:
        print(f"Failed to retrieve the page: {response.status_code}")
        return
    
  soup = BeautifulSoup(response.text, "lxml") # 가져온 HTML 문서를 파서를 통해 BeautifulSoup 객체로 만듦

  # items = soup.find_all("li", attrs={"class":re.compile("^search-product")}) # li 태그 중에서 class 옵션이 search-product로 시작하는 요소들만 가져온다.
  items = soup.find_all("li", attrs={"class":re.compile("^baby-product")}) # li 태그 중에서 class 옵션이 search-product로 시작하는 요소들만 가져온다.
  print(items[0].find("div", attrs={"class":"name"}).get_text())
  print(items[1].find("div", attrs={"class":"name"}).get_text())
  temp=items[1].find("dt", attrs={"class":"image"})
  print(temp.find("img").get('src'))
  items_list=[]
  for item in items:

      name = item.find("div", attrs={"class":"name"}).get_text() # 제품명

      price = item.find("strong", attrs={"class":"price-value"}).get_text() # 가격

      rate = item.find("em", attrs={"class":"rating"}) # 평점

      img_tag = item.find("dt", attrs={"class":"image"})
      img = img_tag.find("img").get('src')
      img = "https:"+img
      if rate:
          rate = rate.get_text()
      else:
          rate = "평점 없음"

      rate_cnt = item.find("span", attrs={"class":"rating-total-count"}) # 평점 수
      if rate_cnt:
          rate_cnt = rate_cnt.get_text()
      else:
          rate_cnt = "평점 수 없음"
      items_list.append({
          'goods_id': 1234, 'goods_name': name.strip(), 'goods_price': int(price.replace(',','')),
          'goods_num': 1, 'item_url': "12435r",
          'item_img': img,
          'goods_category': 'tissue'})

  return(items_list)
