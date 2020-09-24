import json
import glob
import shutil

allbooks = []

for file in sorted(glob.glob("*.json")):
  with open(file) as f:
    data = json.loads(f.read())
    allbooks += data

with open(f'allbooks.json', 'w', encoding='utf-8') as f:
  json.dump(allbooks, f, ensure_ascii=False, indent=4)
