#! /usr/bin/python3
import urllib.request
import json
import re
import os
import sys

scriptPath = os.path.dirname(os.path.realpath(sys.argv[0]))
url = "https://wiki.microfocus.com/index.php/SUSE/SLES/Kernel_versions"
kernelLists = {}
try:
  rawData = urllib.request.urlopen(url).read()
except:
  print("Something went wrong.. Failed to retrieve " + url)
  quit()
itemsList = re.findall(r"(?:(?:[0-9]+)(?:\.))+(?:(?:[0-9]+)(?:\-)(?:[0-9]+))(?:(?:\.)?(?:[0-9]+)?)+|<th>\sSLES(?:\s)?[0-9]+(?:\sSP[0-5])?(?:\s\-\sLTSS)?", str(rawData))


for number,item in enumerate(itemsList):
  itemsList[number] = re.sub("<th>\s", "", item)

for item in itemsList:
  if "S" in item:
    key = item
    kernelLists[item] = []
  else:
    try:
      kernelLists[key].append(item)
    except:
      print("Something went wrong.. Is " + url +  " displaying properly?")
      quit()

with open('%s/kernel_versions.json' % scriptPath, 'w') as document:
  try:
    document.write(json.dumps(kernelLists))
  except:
    print("Something went wrong.. Unable to write a kernel_versions.json file.")
    quit()

print("Json data collected.")

