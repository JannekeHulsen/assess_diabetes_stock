import streamlit as st
import pandas as pd
from typing import Literal

st.markdown("# Wanneer moet ik de volgende bestelling plaatsen?")

"""

Hier bereken je snel wanneer de volgende besteldatum is, of tot wanneer de huidige bestelling moet dekken.

Vul in: datum laatste bestelling.

Berekening: datum plus kwartaal.

Uitkomst: verwachte datum volgende bestelling.

> Example:
> Last time I ordered was about two months ago. Maybe almost three? Let's check.
> 1. Find the date in your order history, mail or calendar.
> 2. Fill in date.
> 3. The app generates the next order date.
"""
st.divider()

def get_order_date(last_date, months: float | None = 3.0, weeks: float | None = None, days: int | None = None, verbose: bool = False):
    """
    Given an order date and the number of days, weeks or months that should be covered by this order, when is the next time to order?
    """
    if verbose:
        print(f"Provided order date is: {last_date}.")
    # if days is not None:
        #TODO add feature
    # if weeks is not None:
        # TODO add feature
    next_date = last_date + pd.DateOffset(months=months)
    if verbose:
        print(f"Next order date is: {next_date}.")
    return next_date

# TODO pandas date-time format, how to print only date and in nice format?
# TODO add assert

last_date = st.date_input('What is the date of your most recent order?', format='DD-MM-YYYY')

last_date = pd.to_datetime(last_date)
st.write("Most recent order on: ", last_date)
next_date = get_order_date(last_date) # TODO add period as input option
st.write("Given the standard three months, the next order has to be made on or around: ", next_date)
