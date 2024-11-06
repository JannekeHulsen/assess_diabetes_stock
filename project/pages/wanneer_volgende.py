import streamlit as st
import pandas as pd

st.markdown("# Besteldatum")
st.sidebar.markdown("Hier bereken je snel wanneer de volgende besteldatum is, of tot wanneer de huidige bestelling moet dekken.")

"""
## Wanneer volgende bestelling?
Vul in: datum laatste bestelling.

Berekening: datum plus kwartaal.

Uitkomst: verwachte datum volgende bestelling.

---

"""

last_date = st.date_input('Wat is de datum van je laatste bestelling?', format='DD-MM-YYYY')

last_date = pd.to_datetime(last_date)
st.write("Laatste bestelling was gedaan op: ", last_date)
next_date = last_date + pd.DateOffset(months=3)
st.write("Volgende bestelling zal worden gedaan rond: ", next_date)
