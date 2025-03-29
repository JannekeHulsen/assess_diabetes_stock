import streamlit as st

# TODO plaatje erbij om het wat begrijpelijker te maken.
# TODO wat als je maar 1 voedingsmiddel hebt?
# TODO toggle met keuze hoeveel voedingsmiddelen erin te gooien
# TODO kh-lijst van veelgebruikte voedingsmiddelen (lijst keuken)

st.markdown("# Hoeveel eten weeg ik af?")

"""
Voorbeelden:
- Ik ga rijst koken en wil op 50 gram koolhydraten uitkomen. Hoeveel gram rijst moet ik dan afwegen?
- Ik wil een mueslimix maken van rozijnen en havermoutvlokken. Ik wil op 50 gram koolhydraten uitkomen. Als ik 10 gram rozijnen toevoeg, hoeveel gram havermout moet ik dan nog toevoegen?
- Voor een mengsel van aardbeien en druiven wil ik voor eenderde aardbeien en tweederde druiven. Hoeveel gram moet ik van beide afwegen om op 30 gram koolhydraten te komen?
"""

st.image("images/kh_uitleg.jpg")

st.divider()
st.write("### Vul in!")

def calculate_mix_of_two(kh_food1:float = None,
                         kh_food2:float = None,
                         aim_kh:float = None,
                         fraction_food1 = None,
                        # m_food1:float = 0, # TODO should this be an option or not?
                         m_food2:float = 0,
                         name_food1:str = "First food item",
                         name_food2:str = "Second food item"):
    """
    Arguments:
    kh_food1: Carbohydrates per 100g in first food item that is to be mixed.
    kh_food2: Carbohydrates per 100g in second item.
    aim_kh: How much g carbohydrates do you want in the final mix?
    fraction_food1: Ratio of food item 1 and 2. What portion of total should be
        food item 1? If None, all carbs will be filled up by item 1.
    m_food2: How much grams of the second food item you already have.
    name_food1: Provide the name of the first food item if you want. Not required.
    name_food2: Name of second food item. Not required.
    """
    # Make sure all input is given
    assert aim_kh is not None, "Please fill in how much carbs should be in final mix."
    assert kh_food1 is not None, "Please provide amount of carbohydrates per 100g"
    assert kh_food2 is not None, "Please provide amount of carbohydrates per 100g"

    # Make it per gram
    kh_food1 = kh_food1/100
    kh_food2 = kh_food2/100

    m_food1 = 0 # TODO not sure if this should be an argument or not

    if fraction_food1 is None:
        aim_food1 = aim_kh - m_food1*kh_food1 - m_food2*kh_food2 # if no fraction, e.g. mueslimix
    else:
        aim_food1 = aim_kh * fraction_food1 - m_food1 * kh_food1

    print(f"Voor {aim_kh}g kh totaal:")
    m_food1 = int(round(aim_food1 / kh_food1, 0))
    print(f"{name_food1}: {m_food1} g")
    aim_food2 = aim_kh - aim_food1
    m_food2 = int(round(aim_food2 / kh_food2, 0))
    print(f"{name_food2}: {m_food2} g")

    return m_food1, m_food2


st.write("Hoeveel gram koolhydraten per 100 gram?")
col1, col2 = st.columns(2)
with col1:
    kh_food1 = st.number_input("Eerste voedingsmiddel:", min_value=0, max_value=100, step=1)
    name_food1 = st.text_input('Naam:', value="Eerste voedingsmiddel")

with col2:
    kh_food2 = st.number_input('Tweede voedingsmiddel:', min_value=0, max_value=100, step=1)
    name_food2 = st.text_input("Naam:", value="Tweede voedingsmiddel")

col1, col2 = st.columns(2)
with col1:
    aim_kh = st.number_input("Hoeveel gram koolhydraten in totaal?", min_value=0, step=1,
                         help="Hoeveel g kh moet er in het uiteindelijke mengsel zitten?")

keuze = st.radio("Wil je een ratio geven of hoeveel je extra bij het tweede voedingsmiddel moet toevoegen?", ["ratio", "hoeveel extra"],
         help="Ene is fractie van eerste voedingsmiddel, andere is hoeveel extra toe te voegen om bij het gewenste aantal koolhydraten te komen.")
if keuze == "ratio":
    fraction_food1 = st.number_input('Wat is de fractie van het totaal aan koolhydraten dat moet worden opgevuld door het eerste voedingsmiddel?',
                                value=0.5, min_value=0.0, step=0.1, max_value=1.0)
elif keuze == "hoeveel extra":
    m_food2 = st.number_input('Hoeveel gram van het tweede voedingsmiddel heb je al om toe te voegen?', value=0, min_value=0, step=1,
                          help="Bijvoorbeeld 10g rozijnen.")
else:
    fraction_food1 = None

st.write("#####")

if st.button('Bereken'):
    if kh_food1 == 0 or kh_food2 == 0:
        st.write("Vul waardes in voor koolhydraten per 100 gram.")
    else:
        m_food1, m_food2 = calculate_mix_of_two(kh_food1=kh_food1,
                            kh_food2=kh_food2,
                            fraction_food1=fraction_food1,
                            aim_kh=aim_kh,
                            m_food2=m_food2,
                            name_food1=name_food1,
                            name_food2=name_food2)
        st.write("#####")
        st.write(f"Voor {aim_kh}g kh totaal:")
        st.write(f"{name_food1}: {m_food1} g")
        st.write(f"{name_food2}: {m_food2} g")
