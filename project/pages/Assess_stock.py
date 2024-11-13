import streamlit as st
import pandas as pd
import math
from utils.functions import get_item_info
st.sidebar.markdown("Hier bereken je hoeveel spullen er nodig zijn, of het huidige aantal spullen genoeg is, of hoeveel je voor je vakantie moet bestellen.")

st.markdown("# Assess diabetes stock")

"""
Fill in how many items you currently have, and, if applicable, the date until which you want to be covered by your next order.

#####

> Example:
> 
> Today, I'm going to place an order that has to cover me for the next three months.
>
> TODO finish example
"""

# TODO cache!
# TODO add Generate button

st.divider()

# st.text_input("Item", key="item")
item = st.selectbox(
    'Van welk diabetesonderdeel wil je je voorraad nagaan?',
     ['Infuusset', 'Sensor', 'Reservoir'])
stock = st.number_input('Wat is het aantal dat je nu hebt?', value=5, min_value=0, step=1)
order = st.number_input('Voor als je bestelling wilt checken: het aantal verpakkingen dat je bij bestelling hebt ingevuld. Als hier 0 staat, dan wordt de bestelling niet gecheckt.', value=0, min_value=0, step=1)
till_date = st.text_input('Tot aan welke datum wil je berekenen of je genoeg voorraad hebt? Geef als JJJJ-MM-DD.', None, placeholder='YYYY-MM-DD')
margin = st.number_input('Hoeveel marge wil je hebben voor de berekening? 0.2 staat voor 20%. 0.0 staat voor geen marge, oftewel, geen enkel onderdeel gaat verloren.',
value=0.2, min_value=0.0, step=0.1, format="%0.1f")

'Keuze: ', item

"""
---
"""

def main():
    verdict = assess_status(item = item,
                 till_date = till_date,
                 nr_of_days = 0,
                 stock = stock,
                 order = order,
                 margin = margin,
                 verbose = True,
                 item_info = None)
    st.write(verdict)

def assess_status(item: str = ["Sensor", "Infuusset", "Reservoir"],
                 till_date: str = None,
                nr_of_days: float = 0,
                 stock: int = 0,
                 order: int = 0,
                 margin: float = 0.2,
                 verbose: bool = True,
                 item_info: pd.DataFrame = None):
    """
    Calculate how many packages I need to order of a specific item, or whether the current order is sufficient,
    or until what date the current stock or order provides.

    Parameters
    ----------
    item
        The diabetes item to check. One of ['Sensor', 'Infuusset', 'Reservoir'] for default item info.
    till_date
        Until what date do I want to make sure to have enough supply? Give in the form 'YYYY-MM-DD'.
    nr_of_days
        For how many days do I want to make sure to have enough supply?
    stock
        How many units do I've got in stock of this specific item?
    order
        If I want to check the current order amount: Fill in number of packages in the order.
    margin
        To prevent living on the edge: what's the margin to cover for item failings? As fraction.
    verbose
        Print output yes or no.
    item_info
        If I want to give a different dataframe than given in the function, give here.
        Must follow certain structure.
        Check the `item_info` dataframe in the function code for this structure.
    """
    
    # Check input
    assert margin >= 0, "Margin should be non-negative."
    assert stock >= 0, "Stock should be non-negative."
    assert nr_of_days >= 0, "Number of days should be non-negative."
    assert pd.to_datetime(till_date, errors='coerce') is not pd.NaT, "Invalid format for till_date. Should adhere to 'YYYY-MM-DD'."
    
    # Initialise output
    verdict = ""

    # Product info
    if item_info is None:
        item_info = get_item_info()
    assert item_info is not None and not item_info.empty, "Item info DataFrame must be provided and non-empty."

    # Get the item's specifics
    days_per_unit, units_in_package, official_name = get_specifics(item_info, item)

    # Determine assignment
    if till_date is None and nr_of_days == 0:
        option = 1
    elif till_date is not None or nr_of_days > 0:
        if order == 0:
            option = 2
        elif order > 0:
            option = 3
    else:
        # TODO break
        print("errorrr does not exist.")

    # Print item info + assignment
    if verbose:
        assignments = {1:"Checking until when diabetes needs are covered...\n\n",
                       2:"Calculating how many packages are needed...\n\n",
                       3:f"Checking if an order with {order} package(s) is enough...\n\n"}
        verdict += f'-- Item: {item} --\n\nOfficial name: {official_name}.\n\n{stock} units in stock.\n\n'
        lines='\n----------------------\n'
        # verdict += lines
        verdict += assignments[option]
        # verdict += lines

    if option == 1:
        # Calculate how many days are covered.
        date_stock, verdict = until_what_date_covered(stock=stock, days_per_unit=days_per_unit,
                                             units_in_package=units_in_package,
                                             order=0,
                                             verdict=verdict,
                                             margin=margin, verbose=verbose)
        verdict += f'\n\nCurrent stock covers until {date_stock}.'
            
        if order>0:
            date_order, verdict = until_what_date_covered(stock=stock, days_per_unit=days_per_unit,
                                             units_in_package=units_in_package, order=order,
                                             verdict=verdict,
                                                margin=margin, verbose=verbose)
            verdict += f'Including order, the items cover until {date_order}.'

    elif option in [2, 3]:
        # Calculate how many days need to be covered.
        if till_date is not None:
            till_date, today = pd.to_datetime(till_date), pd.to_datetime('today')
            days_needed = (till_date-today).days*(1+margin)
            if verbose:
                verdict += f'Starting date: {today.date()}\n\nCovering until date: {till_date.date()}\n\n{round(days_needed,1)} days to be covered.\n{lines}'
        if nr_of_days>0:
            days_needed = nr_of_days
    
        # Calculate.
        days_covered=stock*days_per_unit + order*units_in_package*days_per_unit
        days_lacking=days_needed-days_covered
        more_to_order=math.ceil(days_lacking/days_per_unit/units_in_package)
        
        if verbose:
            verdict += f'{int(days_covered)} days are covered.'
            if days_lacking<=0:
                verdict += f'Stock covers enough days with {abs(int(days_lacking))} extra days.\n'
            else:
                verdict += f'{int(days_lacking)} days are not covered in this order.\n' if order>0 else f'{int(days_lacking)} more days need to be covered.\n'
        
        # State how much more is needed.
        if order>0:
            verdict += '\n\nOrder is sufficient' if days_lacking<=0 else f'Not enough: {more_to_order} more package(s) needed.'
        else:
            verdict += f"{'Stock is sufficient' if days_lacking<=0 else f'Order must contain at least {more_to_order} package(s).'}"
    else:
        print("errorrorror smth's wrong")
    
    return verdict

# Utils
def get_specifics(item_info, item):
    specs = item_info.loc[item_info['Item'] == item].iloc[0]
    days_per_unit, units_in_package, official_name = specs['Days per unit'], specs['Units in package'], specs['Official name']
    
    assert days_per_unit > 0 and units_in_package > 0, "Days per unit and units in package should be positive."
    
    return days_per_unit, units_in_package, official_name

def until_what_date_covered(stock: int,
                            days_per_unit: float,
                            units_in_package: int,
                            verdict: str,
                            order: int = 0,
                            margin: float = 0.2,
                            verbose: bool = True):
    
    days_covered = (stock*days_per_unit + order*units_in_package*days_per_unit)*(1-margin)
    final_date = pd.to_datetime('today') + pd.DateOffset(days=days_covered)
    final_date = final_date.strftime("%d-%m-%Y")
    
    if verbose:
        addition = ' including order' if order>0 else ''
        verdict += f'{int(days_covered)} days are covered by stock{addition}.'
    return final_date, verdict

if __name__ == "__main__":
    main()