from compress import compress
from pathlib import Path
import json
import math
import pprint
import sys
import zipfile

cwd = Path.cwd()
work = cwd / 'work'
out = cwd / 'out'

pp = pprint.PrettyPrinter(indent=2)

def writeInfo(fileStem, info, verbose):
  if verbose:
    pp.pprint(info)
  try:
    xmlData = f'''<?xml version="1.0"?>
<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Title><![CDATA[{info['Title']}]]></Title>
  <Series><![CDATA[{info['series']}]]></Series>
  <Number><![CDATA[{info['issue']}]]></Number>
  <Summary><![CDATA[{info['Comments']}]]></Summary>
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
  <ScanInformation><![CDATA[{info['Comments']}]]></ScanInformation>
</ComicInfo>''' # <Characters><![CDATA[{info['Characters']}]]></Characters>
    xmlDataPath = work / fileStem / 'ComicInfo.xml'
    xmlDataPath.write_text(xmlData, encoding='UTF-8')

    cr = compress(fileStem, verbose)
    if(not cr[0]):
      return [False, cr[1]]
    
    jsonData = json.loads('{"ComicBookInfo/1.0": {}}')

    jsonData['ComicBookInfo/1.0']['comments'] = info['Comments']
    jsonData['ComicBookInfo/1.0']['credits'] = list(map(lambda x: {'person': x, 'role': 'Writer'}, info['writer']))
    jsonData['ComicBookInfo/1.0']['genre'] = info['Genre']
    jsonData['ComicBookInfo/1.0']['issue'] = info['issue']
    jsonData['ComicBookInfo/1.0']['language'] = info['LanguageISO']
    jsonData['ComicBookInfo/1.0']['publicationMonth'] = info['Month']
    jsonData['ComicBookInfo/1.0']['publicationYear'] = info['Year']
    jsonData['ComicBookInfo/1.0']['publisher'] = info['Publisher']
    jsonData['ComicBookInfo/1.0']['rating'] = math.floor(info['Rating']*2) or 1
    jsonData['ComicBookInfo/1.0']['series'] = info['series']
    jsonData['ComicBookInfo/1.0']['tags'] = info['tags']
    jsonData['ComicBookInfo/1.0']['title'] = info['Title']

    zipNote = json.dumps(jsonData, ensure_ascii=False, sort_keys=True).encode('utf-8')
    print(f'zip note size: {len(zipNote)} bytes/65535 bytes')
    f = out / f'{fileStem}.zip'
    fzip = zipfile.ZipFile(f, 'a', compression=zipfile.ZIP_DEFLATED, compresslevel=6)
    fzip.comment = zipNote
    fzip.close()
    newName = out / f'{fileStem}.cbz'
    f.rename(newName)
  except:
    return [False, sys.exc_info()]
  return [True]