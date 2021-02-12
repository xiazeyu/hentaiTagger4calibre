from genInfo import genInfo
from pathlib import Path
from writeInfo import writeInfo
import json

verbose = False
infoOnly = True

succeeded = []
failed = []

cwd = Path.cwd()
work = cwd / 'work'
infPath = cwd / 'inf.json'
serPath = cwd / 'ser.json'

if infPath.exists():
  infStore = json.loads(infPath.read_text(encoding='UTF-8'))
else:
  infStore = {}

if serPath.exists():
  serStore = json.loads(serPath.read_text(encoding='UTF-8'))
else:
  serStore = {}

dirList = [x for x in work.iterdir() if x.is_dir()]

for curDirIndex in range(len(dirList)):
  curDir = dirList[curDirIndex]
  print(f'===== start processing {curDirIndex+1}/{len(dirList)} =====')
  print(f'  path: {curDir}')

  if curDir.name in infStore:
    print('from inf.json')
    info = infStore[curDir.name]
  else:
    gr = genInfo(curDir, verbose)
    if not gr[0]:
      print(f'===== fail generating {curDirIndex+1}/{len(dirList)} =====\n')
      failed.append([curDir.name, gr[1]])
      continue
    info = gr[1]

  if curDir.name in serStore:
    print('from ser.json')
    info['series'], info['issue'] = serStore[curDir.name][:2]
  
  serStore[curDir.name] = [info['series'], info['issue'], info['coreTitle'], info['Web']]
  infStore[curDir.name] = info

  if not infoOnly:
    wr = writeInfo(curDir.name, info, verbose)
    if(not wr[0]):
      print(f'===== fail writing {curDirIndex+1}/{len(dirList)} =====\n')
      failed.append([curDir.name, wr[1]])
      continue
  print(f'===== finish processing {curDirIndex+1}/{len(dirList)} =====\n')
  succeeded.append(curDir.name)

infPath.write_text(json.dumps(infStore, ensure_ascii=False, indent=2, sort_keys=True), encoding='UTF-8')
serPath.write_text(json.dumps(serStore, ensure_ascii=False, indent=2, sort_keys=True), encoding='UTF-8')

result = {
  'succeeded_count': len(succeeded),
  'failed_count': len(failed),
}
print(failed)
print(result)