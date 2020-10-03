## Crawl Data
 - Go to CrawlData folder
 - Run: python3 main.py. That will export data.json file, contains all books from this link https://www.goodreads.com/author/list/4634532.Nguy_n_Nh_t_nh?page=1&per_page=30
 
 ## Set up Database:
 - Go to database folder
 - Run: npm init to install node modules 
 - Run: node server.js --import to save all data to database or node server.js --delete to delete all data in database 
 
 ## Extract Information:
 - Run:  pip3 install vncorenlp
 - Start server: vncorenlp -Xmx2g <FULL-PATH-to-VnCoreNLP-jar-file> -p 9000 -a "wseg,pos,ner,parse" (PORT: 9000) 
 - Run: python3 main.py to extract names and locations 
 
For more information about the model and how to use VnCoreNLP, follow the link: https://github.com/vncorenlp/VnCoreNLP
 
