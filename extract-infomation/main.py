import os
import json
import numpy as np
from vncorenlp import VnCoreNLP
annotator = VnCoreNLP(address="http://127.0.0.1", port=9000)

with open('./comments.json') as f:
    data = json.loads(f.read())
    f.close()

names=[]
locations = []
for comment in data:
  ner_text = annotator.ner(comment)
  names+= [name[0] for name in ner_text[0] if name[1]=='B-PER']
  locations+= [name[0] for name in ner_text[0] if name[1]=='B-LOC']


names_list = list(np.unique(np.array(names)))
locations_list = list(np.unique(np.array(locations)))

with open('names.json', 'w', encoding='utf-8') as f:
  json.dump(names_list, f, ensure_ascii=False, indent=4)
with open('locations.json', 'w', encoding='utf-8') as f:
  json.dump(locations_list, f, ensure_ascii=False, indent=4)

















# vncorenlp -Xmx2g "/Users/ledat/CompSci/self_taught/intern/test1/extract-infomation/VnCoreNLP-1.1.1.jar" -p 9000 -a "wseg,pos,ner"