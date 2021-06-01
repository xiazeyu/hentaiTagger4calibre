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
  t1 = re.sub(u"\\「.*?\\」|\\(.*?\\)|\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】", "", st).strip()
  if t1 == '':
    t1 = re.sub(u"\\(.*?\\)|\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】", "", st).strip()
  if t1 == '':
    t1 = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】", "", st).strip()
  return t1

def getSeries(st):
  core = getCore(st)
  iss = 1.0
  ser = core

  # ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳
  replaceList = [
    ('①', 1),
    ('②', 2),
    ('③', 3),
    ('④', 4),
    ('⑤', 5),
    ('⑥', 6),
    ('⑦', 7),
    ('⑧', 8),
    ('⑨', 9),
    ('⑩', 10),
    ('⑪', 11),
    ('⑫', 12),
    ('⑬', 13),
    ('⑭', 14),
    ('⑮', 15),
    ('⑯', 16),
    ('⑰', 17),
    ('⑱', 18),
    ('⑲', 19),
    ('⑳', 20),
  ]
  for char in replaceList:
    core = core.replace(char[0], str(char[1]))

  # 2020年10月号
  # 2021月2号
  if '月' in core[-4:] and '号' in core[-4:]:
    while (ser[-1] != ' '):
      ser = ser[:-1]
    ser = ser.strip()
    return [ser, iss]

  # Artist Galleries :::
  if core[:16].lower() == 'artist galleries':
    ser = core[16:].strip().strip(':').strip()
    return [ser, iss]

  # 从本子了解汉化教程
  if core[:9] == '从本子了解汉化教程':
    ser = '从本子了解汉化教程'
    if core[9:][0].isdigit():
      iss = float(core[9:][0])
    return [ser, iss]

  # 美羽ちゃんとベランダXX
  if core == '美羽ちゃんとベランダXX':
    return [ser, iss]

  # 1階
  if core[-1] == '階' and core[-2].isdigit():
    count = -2
    while core[count - 1].isdigit():
      count = count - 1
    ser = core[:count].strip()
    iss = float(core[count:-1])
    return [ser, iss]
  # 1
  # 01
  # 1.5
  if core[-1].isdigit():
    count = -1
    while core[count - 1].isdigit() or (core[count - 1] == '.' and core[count - 2].isdigit()):
      count = count - 1
    ser = core[:count].strip()
    iss = float(core[count:])
    # 01
    # vol.1
    # Vol,01
    if ser[-1:] == '#' or ser[-1:] == '.' or ser[-1:] == ',':
      ser = ser[:-1].strip()
    # vol 1
    if ser[-3:].lower() == 'vol':
      ser = ser[:-3].strip()
    # LEVEL:1
    if ser[-6:].lower() == 'level:':
      ser = ser[:-6].strip()
    # 1+2
    # 1-2
    if ser[-1:] == '+' or ser[-1:] == '-':
      iss = 1.0
      ser = core

  # roman numerals
  # Ⅰ
  # Ⅱ
  # Ⅲ
  # Ⅳ
  # Ⅴ
  # Ⅵ
  # Ⅶ
  # Ⅷ
  # Ⅸ
  # Ⅹ
  # Ⅺ
  # Ⅻ
  # XIII
  # XIV
  # XV
  rn = [
    ['Ⅰ', 1.0],
    ['Ⅱ', 2.0],
    ['Ⅲ', 3.0],
    ['Ⅳ', 4.0],
    ['Ⅴ', 5.0],
    ['Ⅵ', 6.0],
    ['Ⅶ', 7.0],
    ['Ⅷ', 8.0],
    ['Ⅸ', 9.0],
    ['Ⅹ', 10.0],
    ['Ⅺ', 11.0],
    ['Ⅻ', 12.0],
    ['XIII', 13.0],
    ['VIII', 8.0],
    ['XIV', 14.0],
    ['XII', 12.0],
    ['VII', 7.0],
    ['III', 3.0],
    ['XV', 15.0],
    ['XI', 11.0],
    ['VI', 6.0],
    ['IX', 9.0],
    ['IV', 4.0],
    ['II', 2.0],
    ['X', 10.0],
    ['V', 5.0],
    ['I', 1.0],
  ]
  for r in rn:
    l = len(r[0])
    if core[-l:] == r[0]:
      ser = core[:-l].strip()
      iss = r[1]
      return [ser, iss]

  # 援助交配
  if core[:4] == '援助交配':
    ser = '援助交配'
    return [ser, iss]

  # ネコぱら01 おまけ本
  if core == 'ネコぱら01 おまけ本':
    ser = 'ネコぱら'
    return [ser, iss]

  # Arknights Character Fan Art Gallery
  if core[:35].lower() == 'arknights character fan art gallery':
    ser = 'Arknights Character Fan Art Gallery'
    return [ser, iss]

  return [ser, iss]

def gett(index, st):
  if st.lower() in trans['data'][index]['data']:
    return trans['data'][index]['data'][st]['name']
  else:
    return None

def trasgroup(d):
  res = []
  for i in d:
    a = gett(i[0], i[1])
    if a != None:
      res.append(a)
  return res

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
  elif infoJson['gallery_info']['source']['site'] == 'acg18':
    info['Web'] = f'https://acg18.moe/{infoJson["gallery_info"]["source"]["gid"]}.html'

  info['Imprint'] = re.match(r'^(?:\()(.+?)(?:\))', infoJson['gallery_info']['title'])
  if(info['Imprint'] != None):
    info['Imprint'] = info['Imprint'].group(1)
  else:
    info['Imprint'] = infoJson['gallery_info_full']['source_site']

  # begin tags
  info['tags'] = []

  info['tags'].append(info['Genre'])
  transtags = [[1, info['Genre']]]

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
        transtags.append([typ[1], tag])

  rtagInTitle=re.findall(r'\[(.+?)\]|\((.+?)\)|【(.+?)】|（(.+?)）', infoJson['gallery_info']['title'])
  tagInTitle = []
  for x in rtagInTitle:
    tagInTitle += list(x)

  info['tags'] = trasgroup(transtags) + tagInTitle + info['tags']

  info['tags'] = list(dict.fromkeys(info['tags']))

  if '' in info['tags']:
    info['tags'].remove('')

  # end tags

  # begin writer
  info['writer'] = []
  transwris = []
  if 'group' in infoJson['gallery_info']['tags']:
    for t in infoJson['gallery_info']['tags']['group']:
      info['writer'].append(t)
      transwris.append([5, t])
  if 'artist' in infoJson['gallery_info']['tags']:
    for t in infoJson['gallery_info']['tags']['artist']:
      info['writer'].append(t)
      transwris.append([6, t])
  tg = trasgroup(transwris)
  ltg = [x.lower() for x in tg]
  awrite = []
  for x in info['writer']:
    if x.lower() not in ltg:
      awrite.append(x)
  info['writer'] = tg + awrite
  info['writer'] = list(dict.fromkeys(info['writer']))
  # end writer

  # begin characters
  info['characters'] = []
  transchars = []
  if 'character' in infoJson['gallery_info']['tags']:
    for t in infoJson['gallery_info']['tags']['character']:
      info['characters'].append(t)
      transchars.append([4, t])
  tg = trasgroup(transchars)
  ltg = [x.lower() for x in tg]
  achar = []
  for x in info['characters']:
    if x.lower() not in ltg:
      achar.append(x)
  info['characters'] = tg + achar
  info['characters'] = list(dict.fromkeys(info['characters']))
  # end characters

  # begin series
  info['coreTitle'] = getCore(info['Title'])
  info['series'], info['issue'] = getSeries(info['coreTitle'])
  # [Pixiv]
  # [pixiv]
  # [Pixiv Fanbox]
  if info['Title'][1:6].lower() == 'pixiv':
    info['series'], info['issue'] = ['Pixiv', 1.0]
  # [Twitter]
  if info['Title'][1:8].lower() == 'twitter':
    info['series'], info['issue'] = ['Twitter', 1.0]
  # Karorfulmix♥EX
  if info['series'] == 'Karorfulmix♥EX':
    info['series'] = 'KARORFUL MIX EX'

  cau = ['－', '-', ':', '：', '~', ']', '[', '(', ')', '「', '」', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+']
  cauFlag = False
  for c in cau:
    if c in info['series']:
      cauFlag = True
  if cauFlag:
    info['coreTitle']  = f"[CAUTION]{info['coreTitle']}"

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
