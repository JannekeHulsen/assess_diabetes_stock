import streamlit as st
import pandas as pd
from utils.functions import get_item_info

st.markdown("# Diabetes supplies")

"""
In the table below, you can find the items for which you can check your stock.

"""

item_info = get_item_info()
item_info

"""
At some point, I want to extend this table with:

- insulin
- pump batteries
- blood glucose meter batteries
- blood glucose meter test strips
"""