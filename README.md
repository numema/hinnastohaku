# Sök prislistor från lvisnet.fi (v0.4)

## Funktion

Programmet kör i terminalen. Sökvägen för hämtning (url) och uppackningsmapp visas. Ifall något behöver ändras, stäng programmet och gör behövliga ändringar i filen `hinnastot.ini`.
I annat fall görs hämtningen och uppackningen av de hämtade zip-filerna.

## Kör hämtning av listor och packa upp

Öppna skriptmappen och kör pythonskript (i venv):

`cd C:\Users\MagnusNumelin\OneDrive - LVIS-K.A.Stendahl-VVSEL Oy Ab\Documents\python\hinnastohaku>`

`poetry run python haku.py`

eller kör filen från `VS Code` eller annan IDE som kan hantera venv.

## filformat

hinnastot.ini är en konfigurationsfil i python standardformat för configparser.

grossistvis kan väljas om prislistor hämtas med variabeln 'inUse' med värdet 1 eller 0. Specifika filer kan utelämnas med # som första tecken.

## Versionshistoria

### v0.42 3.9.2024

Add '.txt' if missing from file

### v0.41 2.8.2024

Version number as variable

### v0.4 3.6.2024

Shows date of unzipped files in console and shows warning if file dates are not yet upddated for the month of retreival.

### 0.3 6.3.2024

- Changed venv handler to `poetry`. `Nicegui` is not working for some reason, so UI is moved back to terminal.
- Changed terminal pretty printing from `terminal-markup` to `rich` and added status indicator.
- Added keyboard interrupt catcher (signal/SIGINT).

### 0.2

- Script is made more interactive and graphical with `Nicegui` framework

### 0.1

- First release
- Uses `hinnastot.ini` to configure what to fetch
