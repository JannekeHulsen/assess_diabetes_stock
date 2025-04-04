import pandas as pd

def get_item_info():
    item_info=pd.DataFrame({'Item':['Sensor', 'Infuusset', 'Reservoir', 'Insuline'],
                    'Item (EN)':['Sensor', 'Infusion set', 'Reservoir', 'Insulin'],
                    'Days per unit':[7, 3, 3, 21],
                    'Units in package':[5,10,10,5],
                    'Official name':['Guardian Sensor 4', 'Mio Advance 6mm 60cm', 'Medtr reservoir 3ml', 'Novorapid flacon 10ml']
                   })
    return item_info

def get_regular_carbs():
    df = pd.DataFrame({'Product':['Gedroogde pruimen', 'Gedroogde abrikozen', 'Gedroogde mango', 'Gedroogde vijgen', 'Dadels, verse', 'Dadels, medjoul', 'Vlokken', 'Rijst'],
                       'Kh per 100g':[57, 56, 80, 48, 54, 62, 0, 0]
                       })
    return df