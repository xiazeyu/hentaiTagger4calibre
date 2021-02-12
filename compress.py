import subprocess
import multiprocessing
import sys

corecount = multiprocessing.cpu_count()

def compress(dirName, verbose = False):
  command = f'7z a -r -scsUTF-8 -sccUTF-8 -mx6 -mmt{corecount} "out/{dirName}.zip" "./work/{dirName}/*"&&7z t "out/{dirName}.zip"'
  print(command)
  try:
    subprocess.run(command, shell=True, check=True)
  except:
    return [False, sys.exc_info()]
  return [True]
