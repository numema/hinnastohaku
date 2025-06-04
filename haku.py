import requests
import os
import signal
from zipfile import ZipFile
from io import BytesIO
import configparser
from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil import parser
from pathlib import Path
from rich import print
from rich.console import Console


iniFile = 'hinnastot.ini'

version = "0.53"

'''
Fetch and extract price lists from a remote server.
This script reads a configuration file (hinnastot.ini) to determine which price lists to fetch.
It uses the requests library to download zip files containing the price lists,
and the zipfile library to extract them.   
It also uses the rich library to print status messages in a formatted way.
It handles keyboard interrupts gracefully, allowing the user to exit the script without leaving it in an inconsistent state.    
Keyboard interrupts are handled to allow graceful exit of the script.

Usage:
python haku.py 

'''


def handler(signum, frame): # Handler for keyboard interrupt and exit gracefully
    global ctrlExit
    ctrlExit = True
    console.print ('\n[red]Avslutat med ctrl+C!\n')
    #exit (0)

def fetch_external():
    with console.status("[magenta]Startar hämtning och uppackning") as status:

        for tukkuri in config.sections():
            # Skip first section with urls and folders and 'tukkuri' sections not in use
            if tukkuri != 'url' and config[tukkuri].getboolean('inUse'): 

                console.log(f'\n[grey15 on grey50]{tukkuri}:')

                for f in config[tukkuri]: # Read filenames
                    #print(f'file: {f}, value: {config[tukkuri].getboolean(f,True)}')
                    
                    if f != 'inUse': # Skip first row in section
                        status.update(status=f'Hämtar fil... ({f})')

                        req = requests.get(url+tukkuri+'/'+f)#, verify=False)
                        #print(req.headers)
                        if req.headers['Content-Type'] == 'application/zip':
                            fileModTime = req.headers['Last-Modified'] # Take files original timestring from header
                            fileModTime = parser.parse(fileModTime) # parse to datetime
                            fileModTime = datetime.timestamp(fileModTime) # change to POSIX seconds

                            oldFileStatus = ''

                            status.update(status='Packar upp fil...')
                            with ZipFile(BytesIO(req.content)) as zfile: # Extract zip file and write to folder
                                for txtFile in zfile.namelist():
                                    zfile.extract(txtFile, hinnasto_folder / tukkuri)

                                    # add extension if missing
                                    base, extension = os.path.splitext(txtFile)
                                    if extension == '':
                                        txtFileNew = txtFile + '.txt'
                                        os.replace(hinnasto_folder / tukkuri / txtFile, \
                                                hinnasto_folder / tukkuri / txtFileNew)
                                        txtFile = txtFileNew
                                                    
                                    # Change timestamp to original
                                    os.utime(hinnasto_folder / tukkuri / txtFile, (fileModTime, fileModTime))
                                    fileDate = date.fromtimestamp(fileModTime)
                                    thisMonthFirst = date(date.today().year, date.today().month, 1)
                                    if fileDate > thisMonthFirst - timedelta (days = 4): # Accept pricelist as valid if from end of month before
                                        console.log(f'{f} -> [green]{txtFile} {date.fromtimestamp(fileModTime)}')
                                    else:
                                        console.log(f'{f} -> [green]{txtFile} [red]Gammal fil {date.fromtimestamp(fileModTime)}!')
                                        oldFileStatus = '[red] En del filer inte up-to-date!'
                        else:
                            console.log(f'{f} [red]file not found!')

                    if ctrlExit: # If ctrl+C has been pressed
                        exit(0)
                                        
        console.print(f'\n[green]Prislistor klara!{oldFileStatus}\n')

if __name__ == "__main__":

    ctrlExit = False
    signal.signal(signal.SIGINT, handler) #Keyboard EXIT handler

    console = Console() # Use rich to pretty print terminal output

    config = configparser.ConfigParser(allow_no_value=True) # 
    config.optionxform = str # keep case of config file options, otherwise all are lowercase
    
    dataset = config.read(iniFile)

    if not dataset:
        console.print(f'[red]Hittar inte [grey50]{iniFile}[red] Programmet avslutas.\n')

    else:

        hinnasto_folder = Path(config['url']['hinnastohakemisto'])
        url = config['url']['hinnastourl']

        print(f'\n[bold grey70 on yellow]  Hämta prislistor v{version}  ')
        print(f'\nPrislistor hämtas från [blue]{url}')
        print(f'Prislistor packas upp i [green]{hinnasto_folder}')
        print(f'Inställningar hämtade från [dark_orange]{iniFile}\n')
        decision = (input('Hämta prislistor j/n: ')).lower()
        if decision != 'n':
            fetch_external()
        else:
            print('\n[reverse]Programmet avbrutet. Inga prislistor hämtades.\n')
    
    input('Press ENTER to exit')

