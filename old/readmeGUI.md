# Sök prislistor från lvisnet.fi (v0.2)

## Hämta listor och packa upp

Öppna skriptmappen och aktivera venv, kör pythonskript:

`cd C:\Users\MagnusNumelin\OneDrive - LVIS-K.A.Stendahl-VVSEL Oy Ab\Documents\python\hinnastohaku>`

`.\venv\Scripts\Activate.ps1`

`python haku.py`

## Funktion

I det grafiska gränssnittet visas diverse sökvägar och vilka grossisters prislistor som ska hämtas. Ifall något behöver ändras, stängs programmet och behövliga förändringar görs i filen hinnastot.ini.

I annat fall görs hämtningen och uppackningen av de hämtade zip-filerna genom att trycka "Hämta prislistor".

### filformat

hinnastot.ini är en konfigurationsfil i python standardformat för configparser.

grossistvis kan väljas om prislistor hämtas med variabeln 'inUse' med värdet 1 eller 0. Specifika filer kan utelämnas med #.
