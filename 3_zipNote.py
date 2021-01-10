from pathlib import Path
import json
import pprint
import zipfile

verbose = False

pp = pprint.PrettyPrinter(indent=2)

cwd = Path.cwd()
out = cwd / 'out'

fileList = list(out.glob('*.zip'))

zipNotePath = cwd / 'zipNote.json'
zipNoteStore = zipNotePath.read_text(encoding='UTF-8')
zipNote = json.loads(zipNoteStore)

for fileIndex in range(len(fileList)):
  file = fileList[fileIndex]
  print(f'===== start processing {fileIndex+1}/{len(fileList)} =====')
  print(f'  file: {file.name}')

  cmpJson = zipNote[file.stem]
  extJson = json.loads(cmpJson)
  #print(json.dumps(extJson, ensure_ascii=False, sort_keys=True))
  cmpJson = json.dumps(extJson, ensure_ascii=False, sort_keys=True).encode('utf-8')
  print(f'zip note size: {len(cmpJson)} bytes/65535 bytes')

  fzip = zipfile.ZipFile(file, 'a', compression=zipfile.ZIP_DEFLATED, compresslevel=6)
  fzip.comment = cmpJson

  fzip.close()

  newName = file.parent / f'{file.stem}.cbz'
  file.rename(newName)
 
  if verbose:
    pp.pprint(extJson)
  
  print(f'===== finish processing {fileIndex+1}/{len(fileList)} =====\n')
