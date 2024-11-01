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

version = "0.51"

'''
v0.51 1.11.2024
Added 'input' line to keep terminal open when calling script from shortcut etc

v0.5 30.10.2024
Moved all code under 'if __name__...'
Added check for existing inifile
Informative text if some files are not up-to-date

v0.42 3.9.2024
Add '.txt' if missing from file

v0.41 2.8.2024
Version number as variable

v0.4 3.6.2024
Shows date of unzipped files in console and shows warning if file dates 
are not yet upddated for the month of retreival.

v0.3 4.3.2024
Changed terminal pretty printing from 'terminal-markup' to 'rich' and added
status indicator.
Added keyboard interrupt catcher (signal/SIGINT) that exits gracely without
interrupting file writing.
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
                        status.update(status='Hämtar fil...')
                        req = requests.get(url+tukkuri+'/'+f)#, verify=False)
                        fileModTime = req.headers['Last-Modified'] # Take files original timestring from header
                        fileModTime = parser.parse(fileModTime) # parse to datetime
                        fileModTime = datetime.timestamp(fileModTime) # change to POSIX seconds

                        if ctrlExit: # If ctrl+C has been pressed
                            exit(0)

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
                                if fileDate > thisMonthFirst - timedelta (days = 4):
                                    console.log(f'{f} -> [green]{txtFile} {date.fromtimestamp(fileModTime)}')
                                else:
                                    console.log(f'{f} -> [green]{txtFile} [red]Gammal fil {date.fromtimestamp(fileModTime)}!')
                                    oldFileStatus = '[red] Alla filer inte up-to-date!'
                                    
        console.print(f'\n[green]Prislistor klara!{oldFileStatus}\n')

if __name__ == "__main__":

    ctrlExit = False
    signal.signal(signal.SIGINT, handler) #Keyboard EXIT handler

    console = Console() # Use rich to pretty print terminal output

    config=configparser.ConfigParser(allow_no_value=True) # 
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

    input('Tryck ENTER för att avsluta')

