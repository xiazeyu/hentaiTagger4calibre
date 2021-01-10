from pathlib import Path
import json
import math
import pprint
import pycountry
import re
import urllib.parse
##import shutil

verbose = False

pp = pprint.PrettyPrinter(indent=2)

cwd = Path.cwd()

out = cwd / 'out'
work = cwd / 'work'
##if out.exists():
##  shutil.rmtree(out)

dirList = [x for x in work.iterdir() if x.is_dir()]
zipNote = {}

for curDirIndex in range(len(dirList)):
  curDir = dirList[curDirIndex]
  print(f'===== start processing {curDirIndex+1}/{len(dirList)} =====')
  print(f'  path: {curDir}')
  infoPath = curDir / 'info.json'
  infoText = infoPath.read_text(encoding='UTF-8')
  infoJson = json.loads(infoText)

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
  
  xmlData = f'''<?xml version="1.0"?>
<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Title><![CDATA[{info['Title']}]]></Title>
  <Series><![CDATA[{info['Title']}]]></Series>
  <Year><![CDATA[{info['Year']}]]></Year>
  <Month><![CDATA[{info['Month']}]]></Month>
  <Day><![CDATA[{info['Day']}]]></Day>
  <Writer><![CDATA[{info['Writer']}]]></Writer>
  <Publisher><![CDATA[{info['Publisher']}]]></Publisher>
  <Imprint><![CDATA[{info['Imprint']}]]></Imprint>
  <Genre><![CDATA[{info['Genre']}]]></Genre>
  <Web><![CDATA[{info['Web']}]]></Web>
  <PageCount><![CDATA[{info['PageCount']}]]></PageCount>
  <LanguageISO><![CDATA[{info['LanguageISO']}]]></LanguageISO>
  <AgeRating><![CDATA[{info['AgeRating']}]]></AgeRating>
  <Manga><![CDATA[{info['Manga']}]]></Manga>
  <Characters><![CDATA[{info['Characters']}]]></Characters>
  <ScanInformation><![CDATA[{info['Comments']}]]></ScanInformation>
</ComicInfo>
'''
  
  jsonData = json.loads('''
{
    "ComicBookInfo/1.0": {

    }
}
''')

  jsonData['ComicBookInfo/1.0']['title'] = info['Title']
  jsonData['ComicBookInfo/1.0']['publisher'] = info['Publisher']
  jsonData['ComicBookInfo/1.0']['publicationMonth'] = info['Month']
  jsonData['ComicBookInfo/1.0']['publicationYear'] = info['Year']
  jsonData['ComicBookInfo/1.0']['comments'] = info['Comments']
  jsonData['ComicBookInfo/1.0']['genre'] = info['Genre']
  jsonData['ComicBookInfo/1.0']['language'] = info['LanguageISO']
  jsonData['ComicBookInfo/1.0']['rating'] = math.floor(info['Rating']*2) or 1
  jsonData['ComicBookInfo/1.0']['credits'] = list(map(lambda x: {'person': x, 'role': 'Writer'}, info['writer']))
  jsonData['ComicBookInfo/1.0']['tags'] = info['tags']
  

  
  xmlDataPath = curDir / 'ComicInfo.xml'
  
  xmlDataPath.write_text(xmlData, encoding='UTF-8')  
  zipNote[curDir.name] = json.dumps(jsonData, ensure_ascii=False)
  
  
  print(f'===== finish processing {curDirIndex+1}/{len(dirList)} =====\n')

zipNotePath = cwd / 'zipNote.json'
zipNotePath.write_text(json.dumps(zipNote, ensure_ascii=False), encoding='UTF-8')
