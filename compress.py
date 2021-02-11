import subprocess
import multiprocessing
import sys

corecount = multiprocessing.cpu_count()

def compress(dirName, verbose = False):
  command = f'7z a -r -bt -scsUTF-8 -sccUTF-8 -mx6 -mmt{corecount} "out/{dirName}.zip" "./work/{dirName}/*"'
  print(command)
  try:
    subprocess.run(command, shell=True, check=True)
  except:
    return [False, sys.exc_info()]
  return [True]
