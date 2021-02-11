from pathlib import Path
import json
import pprint
import pycountry
import re
import sys
import urllib.parse

pp = pprint.PrettyPrinter(indent=2)

cwd = Path.cwd()
utilsPath = cwd / 'utils'
transPath = utilsPath / 'db.text.json'
trans = json.loads(transPath.read_text(encoding='UTF-8'))

def getCore(st):
  return re.sub(u"\\(.*?\\)|\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】", "", st)

def gett(index, st):
  if st.lower() in trans['data'][index]['data']:
    return trans['data'][index]['data'][st]['name']
  else:
    return None

def genInfo(dir, verbose = False):
  try:
    infoPath = dir / 'info.json'
    infoText = infoPath.read_text(encoding='UTF-8')
    infoJson = json.loads(infoText)
  except:
    return [False, sys.exc_info()]
  
  info = {}
  info['Title'] = infoJson['gallery_info']['title_original'] or infoJson['gallery_info']['title']
  info['Genre'] = infoJson['gallery_info']['category']
  info['Language'] = infoJson['gallery_info']['language']
  info['UploadDate'] = infoJson['gallery_info']['upload_date']
  info['Year'] = info['UploadDate'][0]
  info['Month'] = info['UploadDate'][1]
  info['Day'] =  info['UploadDate'][2]
  info['PageCount'] = infoJson['gallery_info_full']['image_count']
  info['Rating'] = infoJson['gallery_info_full']['rating']['average']
  info['Publisher'] = urllib.parse.unquote(infoJson['gallery_info_full']['uploader'])

  if infoJson['gallery_info']['source']['site'] == 'exhentai':
    info['Web'] = f'https://exhentai.org/g/{infoJson["gallery_info"]["source"]["gid"]}/{infoJson["gallery_info"]["source"]["token"]}/'
  elif infoJson['gallery_info']['source']['site'] == 'e-hentai':
    info['Web'] = f'https://e-hentai.org/g/{infoJson["gallery_info"]["source"]["gid"]}/{infoJson["gallery_info"]["source"]["token"]}/'

  info['Imprint'] = re.match(r'^(?:\()(.+?)(?:\))', infoJson['gallery_info']['title'])
  if(info['Imprint'] != None):
    info['Imprint'] = info['Imprint'].group(1)
  else:
    info['Imprint'] = infoJson['gallery_info_full']['source_site']
 
  # begin tags
  info['tags'] = []

  info['tags'].append(info['Genre'])
  if gett(1, info['Genre']) != None:
    info['tags'].append(gett(1, info['Genre']))

  keywords = [
    ['language', 2],
    ['parody', 3],
    ['character', 4],
    ['male', 7],
    ['female', 8],
    ['misc', 9],
  ]

  for typ in keywords:
    if typ[0] in infoJson['gallery_info']['tags']:
      for tag in infoJson['gallery_info']['tags'][typ[0]]:
        info['tags'].append(tag)
        if gett(typ[1], tag) != None:
          info['tags'].append(gett(typ[1], tag))
  
  tagInTitle=re.findall(r'\[(.+?)\]|\((.+?)\)|【(.+?)】|（(.+?)）', infoJson['gallery_info']['title'])
  for x in tagInTitle:
    info['tags']+=list(x)
  
  info['tags'] = sorted(list(set(info['tags'])))
  if '' in info['tags']:
    info['tags'].remove('')

  # end tags

  # begin writer
  info['writer'] = []
  if 'group' in infoJson['gallery_info']['tags']:
    for t in infoJson['gallery_info']['tags']['group']:
      info['writer'].append(t)
      if gett(5, t) != None:
        info['writer'].append(gett(5, t))
  if 'artist' in infoJson['gallery_info']['tags']:
    for t in infoJson['gallery_info']['tags']['artist']:
      info['writer'].append(t)
      if gett(6, t) != None:
        info['writer'].append(gett(6, t))
  info['writer'] = sorted(list(set(info['writer'])))
  # end writer

  # begin characters
  info['characters'] = []
  if 'character' in infoJson['gallery_info']['tags']:
    for t in infoJson['gallery_info']['tags']['character']:
      info['characters'].append(t)
      if gett(4, t) != None:
        info['characters'].append(gett(4, t))
  info['characters'] = sorted(list(set(info['characters'])))
  # end characters

  # begin series
  info['series'] = getCore(info['Title'])
  info['issue'] = 1
  #end series

  if info['Genre'] == 'non-h':
    info['AgeRating'] = 'Teen'
  else:
    info['AgeRating'] = 'Adults Only 18+'

  if info['Genre'] in ['doujinshi', 'manga']:
    info['Manga'] = 'Yes'
  else:
    info['Manga'] = 'No'

  info['Writer'] = ', '.join(str(p) for p in info['writer'])
  info['Characters'] = ', '.join(str(p) for p in info['characters'])
  info['LanguageISO'] = pycountry.languages.get(name=info['Language']).alpha_2
  info['Comments'] = f'''<div><p>Web: <a href="{info['Web']}">{info['Web']}</a></p><p>Rating: {info['Rating']}, {infoJson['gallery_info_full']['rating']['count']}</p><p>PageCount: {info['PageCount']}</p><p>Genre: {info['Genre']}</p><p>Imprint: {info['Imprint']}</p><p>AgeRating: {info['AgeRating']}</p><p>UploadDate: {info['UploadDate']}</p></div>'''

  if verbose:
    pp.pprint(info)

  return [True, info]
