import json
import pprint
import pycountry
import re
import sys
import urllib.parse

pp = pprint.PrettyPrinter(indent=2)

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
    
  info['tags'] = []
  for t in infoJson['gallery_info']['tags']:
    for tag in infoJson['gallery_info']['tags'][t]:
      info['tags'].append(tag)
  tagInTitle=re.findall(r'\[(.+?)\]|\((.+?)\)|【(.+?)】|（(.+?)）', infoJson['gallery_info']['title'])
  for x in tagInTitle:
    info['tags']+=list(x)
  info['tags'] = sorted(list(set(info['tags'])))
  if '' in info['tags']:
    info['tags'].remove('')

  info['writer'] = []
  if 'group' in infoJson['gallery_info']['tags']:
    for t in infoJson['gallery_info']['tags']['group']:
      info['writer'].append(t)
  if 'artist' in infoJson['gallery_info']['tags']:
    for t in infoJson['gallery_info']['tags']['artist']:
      info['writer'].append(t)
      
  info['characters'] = []
  if 'character' in infoJson['gallery_info']['tags']:
    for t in infoJson['gallery_info']['tags']['character']:
      info['characters'].append(t)

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
