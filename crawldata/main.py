import bs4 as bs
import requests
import json
import os

books = [] #hold array of book 
rate ={
  "did not like it": 1,
  "it was ok": 2,
  "liked it": 3,
  "really liked it": 4,
  "it was amazing": 5
}

def get_info_book(link, bookModel, bookReviews):
  #load page by link 
  req = requests.get(link)
  soup = bs.BeautifulSoup(req.text, "lxml")

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
          
  bookModel['bookReviews'] = bookReviews
  return bookModel

if __name__ == '__main__':
  req1 = requests.get('https://www.goodreads.com/author/list/4634532.Nguy_n_Nh_t_nh?page=1&per_page=150')
  soup1 = bs.BeautifulSoup(req1.text, "lxml")
  links = soup1.find_all("a", class_='bookTitle')
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
    print(url)
    books.append(get_info_book(url, bookModel,bookReviews))

  with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=4)



