import requests
from pathlib import Path
import json
import time
import zipfile
import pprint
from xml.dom.minidom import parseString
from cookie import cookie

cbzPath = Path('\\\\server\\share')
# cbzPath = Path('D:\\books')

cwd = Path.cwd()
chgPath = cwd / 'chg.json'
errPath = cwd / 'err.json'

cbzList = list(cbzPath.glob('**/*.cbz'))

print(f'Found {len(cbzList)} files.')

urls = []
changed = []
error = []

for filePath in cbzList:
  try:
    zipobj = zipfile.ZipFile(filePath)
    xmlobj = zipobj.read('ComicInfo.xml').decode()
    dom = parseString(xmlobj)
    urls.append(dom.getElementsByTagName('Web')[0].childNodes[0].data)
  except:
    print(f'err:{0}', filePath)
    error.append(filePath)

proxies = {
  'http': 'http://127.0.0.1:7890',
  'https': 'http://127.0.0.1:7890',
}

def getPage(url, s):
  r = s.get(url)#, proxies=proxies)
  # print(r.text)
  return r.text

def stillThere(url, s):
  return getPage(url, s).find('<tr><td class="gdt1">Visible:</td><td class="gdt2">Yes</td></tr>') != -1


counter = 0

s = requests.Session()
requests.utils.add_dict_to_cookiejar(s.cookies, cookie)
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'

for url in urls:
  try:
    counter += 1
    if counter < 0: # when error occured, change this to continue
      continue
    print(f'{counter}/{len(urls)}')
    if not stillThere(url, s):
      print(url)
      # print(stillThere(url))
      changed.append(url)
    # time.sleep(1)
  except:
    print(f'err:{0}', url)
    error.append(url)

print('changed:')
pprint.pprint(changed)
print('error:')
pprint.pprint(error)
chgPath.write_text(json.dumps(changed, ensure_ascii=False, indent=2), encoding='UTF-8')
errPath.write_text(json.dumps(error, ensure_ascii=False, indent=2), encoding='UTF-8')
