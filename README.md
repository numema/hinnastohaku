# Sök prislistor från lvisnet.fi/OpusCapita

## Funktion

Programmet körs i terminalen. Sökvägen för hämtning (url) och uppackningsmapp visas. Ifall något behöver ändras, stäng programmet och gör behövliga ändringar i filen `hinnastot.ini`.
I annat fall görs hämtningen och uppackningen av de hämtade zip-filerna.

## Installation

Klona repon eller ladda ner repons filer i huvudmappen (undermapparna behövs inte).

>[!TIP]
>>>>>>> 167721eb5f92c7373b36778fb803a5d22491ba02
>Använd UV för enkel hantering av python projekt

##### Med `uv` (rekommenderas):

Kör `uv sync` för att skapa en virtuell omgivning och installera alla beroenden.

##### Med `pip`:

Installera beroenden manuellt.

## Kör hämtning av listor och packa upp

Öppna skriptmappen och kör pythonskript (i venv):

`uv run haku.py`

Med shortcut-link: Gör en genväg för haku.py på arbetsbordet. Konfiguration:
```
Starta i: sökvägen ska vara filens sökväg
mål: `uv run haku.py`
```

## filformat

hinnastot.ini är en konfigurationsfil i python standardformat för configparser.

`hinnastohakemisto` anger lokala 

grossistvis kan väljas om prislistor hämtas med variabeln 'inUse' (1 / 0). Specifika filer kan utelämnas med # som första tecken.

## Versionshistoria

### 2.6.2025
Changed venv handler to uv

### v0.53 2.1.2025
Updated source URL in hinnasto.ini as it had changed

### v0.52 10.1.2025
Added check for existing zip file in request url as script terminated in error
when url was wrong.

### v0.51 1.11.2024
Added input line to keep terminal window open after running script
from shortcut etc

### v0.5 30.10.2024
Moved all code under 'if __name__ ='
Added check for existing inifile
Informative text if some files are not up-to-date

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
