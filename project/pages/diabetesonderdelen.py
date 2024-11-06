import streamlit as st
import pandas as pd

st.markdown("# Diabetesonderdelen")
st.sidebar.markdown("Bekijk welke items in de tabel staan. Op deze pagina vind je een tabel waarin de onderdelen staan die zijn inbegrepen in de huidige app.")

"""
## Tabel met items


Dit wil ik nog uitbreiden met:

- insuline
- pompbatterijen
- meterbatterijen
- meetstrips
"""

def get_item_info():
    item_info=pd.DataFrame({'Item':['Sensor', 'Infuusset', 'Reservoir'],
                    'Days per unit':[7, 3, 3],
                    'Units in package':[5,10,10],
                    'Official name':['Guardian Sensor 4', 'Mio Advance 6mm 60cm', 'Medtr reservoir 3ml']
                   })
    return item_info


item_info = get_item_info()
item_info