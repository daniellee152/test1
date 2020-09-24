import bs4 as bs
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

rate ={
  "did not like it": 1,
  "it was ok": 2,
  "liked it": 3,
  "really liked it": 4,
  "it was amazing": 5
}

def get_info_book(link, bookModel, bookReviews):

  # chrome_options = Options()
  # chrome_options.add_argument("--headless")
  driver = webdriver.Chrome(executable_path = f"{os.getcwd()}/chromedriver")
  driver.get(link)
  driver.maximize_window()

  # select all languages
  element = driver.find_element_by_xpath('//select[@id="language_code"]')
  all_options = element.find_elements_by_tag_name("option")
  all_options[0].click()  
  time.sleep(7)

  #get soup
  soup = bs.BeautifulSoup(driver.page_source, "lxml")
  bookModel['bookId'] = soup.link.get('href').split('show/')[1].split('-')[0]
  bookModel['bookLink'] = soup.link.get('href')
  bookModel['bookTitle'] = soup.find(id='bookTitle').text.strip()
  bookModel['bookRate'] = soup.find(itemprop = 'ratingValue').text.strip()

  #check description exits
  if(len(soup.find(id='descriptionContainer').contents)==1):
    bookModel['bookDescription'] = ""
  else:
    bookModel['bookDescription'] = soup.find(id='description').text.strip()
    
  #get reviews
  reviews = soup.find_all("div", class_="review")
  for review in reviews:
    bookReviews['userId'].append(review.find('a').get('href').split('show/')[1].split('-')[0]) 
    bookReviews['userName'].append(review.find("a", class_ = "user").text)
    bookReviews['datePost'].append(review.find("a", class_="reviewDate").text)

    #check if review is rated it
    if (review.find('div', class_ = "reviewHeader").contents[4].strip()=="rated it"):
      bookReviews['rate'].append(rate[review.find("span", class_ = "staticStars notranslate").get('title')])
    else:
      bookReviews['rate'].append(0)

    #check content review is empty
    if len(review.find("div", class_ = "left bodycol"))!= 7:
      bookReviews['contentReview'].append("")     
    else:
      bookReviews['contentReview'].append(review.find("div", class_="reviewText").text.strip())

    # check review is inapproriate
    if len(review.find("div", class_ = "left bodycol"))== 7:
      if (len(review.find('div', class_="updateActionLinks").contents)==7):
        routeReview = "https://www.goodreads.com/"+ review.find('div', class_="updateActionLinks").contents[5].get('href')
        bookReviews['commentList'].append(routeReview)  
    else:
      bookReviews['commentList'].append("")  

  #calculate total page for review 
  next_page = soup.find("a", class_="next_page")
  if (next_page):
    if next_page.find_previous_sibling().text == "…":
      total_page =10 
    else:
      total_page = int(next_page.find_previous_sibling().text)
  else:
    total_page = 1

  #go to next page
  if total_page>1:
    for _ in range(total_page-1):
      nextpage_btn = driver.find_element_by_xpath('(//*[@id="reviews"]/div[5]/div/a)[last()]')
      nextpage_btn.click()
      time.sleep(5)
      soup = bs.BeautifulSoup(driver.page_source, "lxml")

      reviews = soup.find_all("div", class_="review")
      for review in reviews:
        bookReviews['userId'].append(review.find('a').get('href').split('show/')[1].split('-')[0]) 
        bookReviews['userName'].append(review.find("a", class_ = "user").text)
        bookReviews['datePost'].append(review.find("a", class_="reviewDate").text)

        #check if review is rated it
        if (review.find('div', class_ = "reviewHeader").contents[4].strip()=="rated it"):
          bookReviews['rate'].append(rate[review.find("span", class_ = "staticStars notranslate").get('title')])
        else:
          bookReviews['rate'].append(0)

        #check content review is empty
        if len(review.find("div", class_ = "left bodycol"))!= 7:
          bookReviews['contentReview'].append("")     
        else:
          bookReviews['contentReview'].append(review.find("div", class_="reviewText").text.strip())
          
        # check review is inapproriate
        if len(review.find("div", class_ = "left bodycol"))== 7:
          if (len(review.find('div', class_="updateActionLinks").contents)==7):
            routeReview = "https://www.goodreads.com/"+ review.find('div', class_="updateActionLinks").contents[5].get('href')
            bookReviews['commentList'].append(routeReview)  
        else:
          bookReviews['commentList'].append("")
  
  driver.quit()
  bookModel['bookReviews'] = bookReviews 
  return bookModel

if __name__ == '__main__':
  for i in range(1, 76):
    reqs = requests.get(f'https://www.goodreads.com/author/list/4634532.Nguy_n_Nh_t_nh?page={i}&per_page=2')
    soups = bs.BeautifulSoup(reqs.text, "lxml")
    links = soups.find_all("a", class_='bookTitle')
    collections = []
    print(f'collections: {i}')
    for link in links:
      bookModel = {
        'bookId':  None,
        'bookLink':  None,
        'bookTitle': None,
        'bookRate' :  None,
        'bookDescription': None,
        'bookReviews':{}
      }

      bookReviews ={
        'userId' : [],
        'userName': [],
        'rate': [],
        'contentReview': [],
        'commentList': [],
        'datePost' : []
      }
      url ="https://www.goodreads.com"+link.get('href')
      print(f"url is: {url}")

      book = get_info_book(url, bookModel,bookReviews)
      collections.append(book)
    #export every two
    with open(f'./data/collections_{i}.json', 'w', encoding='utf-8') as f:
      json.dump(collections, f, ensure_ascii=False, indent=4)

  
  
    
    



