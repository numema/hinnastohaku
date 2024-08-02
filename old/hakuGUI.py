import requests
import os
from zipfile import ZipFile
from io import BytesIO
import configparser
from datetime import datetime
from dateutil import parser
from pathlib import Path
from nicegui import ui

iniFile = 'hinnastot.ini'

config=configparser.ConfigParser(allow_no_value=True) # 
config.optionxform = str # keep case of config file options, otherwise all are lowercase
config.read(iniFile)

hinnasto_folder = Path(config['url']['hinnastohakemisto'])
url = config['url']['hinnastourl']

def fetch_external():
    print('sub started')
    log = ui.log().classes('w-full h-20') #open a console window in gui for status updates

    for tukkuri in config.sections():
            if tukkuri != 'url' and config[tukkuri].getboolean('inUse'): # Skip first section with urls and folders
                                                                         # and 'tukkuri' sections not in use
                log.push(f'\n{tukkuri}:')

                for f in config[tukkuri]: # Read filenames
                    #print(f'file: {f}, value: {config[tukkuri].getboolean(f,True)}')
                    
                    if f != 'inUse': # Skip first row in section
                        req = requests.get(url+tukkuri+'/'+f)#, verify=False)
                        fileModTime = req.headers['Last-Modified'] # Take files original timestring from header
                        fileModTime = parser.parse(fileModTime) # parse to datetime
                        fileModTime = datetime.timestamp(fileModTime) # change to POSIX seconds

                        with ZipFile(BytesIO(req.content)) as zfile: # Extract zip file and write to folder
                            for txtFile in zfile.namelist():
                                zfile.extract(txtFile, hinnasto_folder/tukkuri)
                                # Change timestamp to original
                                os.utime(hinnasto_folder / tukkuri / txtFile, (fileModTime, fileModTime))
                                log.push(f'{f} -> {txtFile}')

    log.push('Hinnastot haettu ja purettu hakemistoihin')


# Define layout for nicegui
ui.aggrid({
    'defaultColDef': {'flex': 1},
    'columnDefs': [
        {'headerName': 'Description', 'field': 'desc'},
        {'headerName': 'File/URL', 'field': 'name'},
    ],
    'rowData': [
        {'desc': 'Asetustiedosto', 'name': iniFile},
        {'desc': 'Hinnastojen haku', 'name': url},
        {'desc': 'Tiedostojen purku', 'name': str(hinnasto_folder)},
    ],
    'rowSelection': 'none',
    }).classes('max-h-40')

# Add company and associated filenames as hierarcial tree 
rowData = []
rowData_temp = []
for key in config.sections(): # For each 'tukkuri'
    if key != 'url':
        for f in config[key]: # add filenames to temporary list as a id:filename dict
            if f != 'inUse': rowData_temp.append({'id' : f})
        # add to actual tree data as {'id': tukkuri, 'children': [{'id': file1}, {'id': file2}]}
        rowData.append({'id':key, 'children': rowData_temp})
        rowData_temp = []

ui.tree(rowData, label_key='id').expand().props("dense")

ui.button('Hämta prislistor', on_click=fetch_external)

ui.run(title='Hinnastohaku',native=False, reload=False, dark = True, window_size=(600, 800), fullscreen=False)
