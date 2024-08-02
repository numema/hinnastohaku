import configparser
from nicegui import ui

iniFile = 'hinnastot copy.ini'

config=configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
config.read(iniFile)
url='test url'
hinnasto_folder = 'test folder'

#ui.markdown(f'Asetustiedosto: **{iniFile}**')
#ui.markdown(f"Hinnastojen haku: **{config['url']['hinnastourl']}**")
#ui.markdown(F"Hinnastojen purku: **{config['url']['hinnastohakemisto']}**")

ui.aggrid({
    'defaultColDef': {'flex': 1},
    'columnDefs': [
        {'headerName': 'Description', 'field': 'desc', 'hide' : False},
        {'headerName': 'File/URL', 'field': 'name', 'hide' : False},
    ],
    'rowData': [
        {'desc': 'Asetustiedosto', 'name': iniFile},
        {'desc': 'Hinnastojen haku', 'name': url},
        {'desc': 'Tiedostojen purku', 'name': hinnasto_folder},
    ],
    'rowSelection': 'none',
}).classes('max-h-40')

rowData = []
rowData_temp = []
for key in config.sections():
    if key != 'url':
        for f in config[key]:
            if f != 'inUse': rowData_temp.append({'id' : f})
        rowData.append({'id':key, 'children': rowData_temp})
        rowData_temp=[]

print(rowData)

t = ui.tree(rowData, label_key='id').expand().props("dense")

t.add_slot('default-header ahlsell', '''
    <span :props="props"><strong>{{ props.node.id }}</strong></span>
''')

ui.run(title='Hinnastohaku', reload=False, dark = True, window_size=(400, 800), fullscreen=False)