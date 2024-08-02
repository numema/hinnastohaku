import requests
import os
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime
from dateutil import parser

hinnastourl = "https://hinnastot.lvisnet.fi/onninen/OTAHINTA.zip"
req=requests.get(hinnastourl)
lmod=req.headers['Last-Modified']
print(lmod)
lmod_dt=datetime.strptime(lmod,"%a, %d %b %Y %H:%M:%S %Z")
lmod_pt=parser.parse(lmod)
print(f'strptime {lmod_dt}, parsertime {lmod_pt}, ')
print(f'strpime stamp {datetime.timestamp(lmod_dt)}, parser stamp {datetime.timestamp(lmod_pt)}')
#zfile=ZipFile(BytesIO(req.content))
#zfile.extractall()

os.utime('otahinta.txt', (datetime.timestamp(lmod_pt), datetime.timestamp(lmod_pt)))