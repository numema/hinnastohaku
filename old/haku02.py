import requests
import os
import signal
from zipfile import ZipFile
from io import BytesIO
import configparser
from datetime import datetime
from dateutil import parser
from pathlib import Path
from rich import print
from rich.console import Console

'''
MN v0.3 4.3.2024

Changed terminal pretty printing from 'terminal-markup' to 'rich' and added
status indicator.
Added keyboard interrupt catcher (signal/SIGINT) that exits gracely without
interrupting file writing.
'''

ctrlExit = False

def handler(signum, frame): # Handler for keyboard interrupt and exit gracefully
    global ctrlExit
    ctrlExit = True
    console.print ('\n[red]Keyboard interrupt!\n')
    #exit (0)

signal.signal(signal.SIGINT, handler)

console = Console() # Use rich to pretty print terminal output

iniFile = 'hinnastot.ini'

config=configparser.ConfigParser(allow_no_value=True) # 
config.optionxform = str # keep case of config file options, otherwise all are lowercase
config.read(iniFile)

hinnasto_folder = Path(config['url']['hinnastohakemisto'])
url = config['url']['hinnastourl']


def fetch_external():
    with console.status("[magenta]Startar hämtning och uppackning") as status:

        for tukkuri in config.sections():
            if tukkuri != 'url' and config[tukkuri].getboolean('inUse'): # Skip first section with urls and folders
                                                                        # and 'tukkuri' sections not in use
                console.log(f'\n[grey15 on grey50]{tukkuri}:')

                for f in config[tukkuri]: # Read filenames
                    #print(f'file: {f}, value: {config[tukkuri].getboolean(f,True)}')
                    
                    if f != 'inUse': # Skip first row in section
                        status.update(status='Hämtar fil...')
                        req = requests.get(url+tukkuri+'/'+f)#, verify=False)
                        fileModTime = req.headers['Last-Modified'] # Take files original timestring from header
                        fileModTime = parser.parse(fileModTime) # parse to datetime
                        fileModTime = datetime.timestamp(fileModTime) # change to POSIX seconds

                        if ctrlExit: # If ctrl+C has been pressed
                            exit(0)

                        status.update(status='Packar upp fil...')
                        with ZipFile(BytesIO(req.content)) as zfile: # Extract zip file and write to folder
                            for txtFile in zfile.namelist():
                                zfile.extract(txtFile, hinnasto_folder/tukkuri)
                                # Change timestamp to original
                                os.utime(hinnasto_folder / tukkuri / txtFile, (fileModTime, fileModTime))
                                console.log(f'{f} -> [green]{txtFile}')
        console.print('[]\nPrislistor klara!\n')

if __name__ == "__main__":
    print(f'\n[bold grey70 on yellow]  Hämta prislistor v0.3  ')
    print(f'\nPrislistor hämtas från [blue]{url}')
    print(f'Prislistor packas upp i [green]{hinnasto_folder}')
    print(f'Inställningar hämtade från [dark_orange]{iniFile}\n')
    decision = (input('Hämta prislistor j/n: ')).lower()
    if decision != 'n':
         fetch_external()
    else:
         print('\n[reverse]Programmet avbrutet. Inga prislistor hämtades.\n')

