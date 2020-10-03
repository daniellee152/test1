import json
comments = []

#read data
with open('../crawldata/data/allbooks.json') as f:
    data = json.loads(f.read())
    for  book in data:
        comments+= book['bookReviews']['contentReview']

# filter out empty string from comments
comments[:] = [x for x in comments if x]

#dump to json file
with open('comments.json', 'w', encoding='utf-8') as f:
  json.dump(comments, f, ensure_ascii=False, indent=4)







