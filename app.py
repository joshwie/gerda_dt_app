import streamlit as st

erstellte_szenarien = 0
max_szenarien = 3

tab_inf, tab_sz_erstellen, tab_sz_analysieren, tab_sz_vergleichen = st.tabs(["Informationen", "Szenario erstellen", "Szenario analysieren", "Szenarien vergleichen"])

with tab_inf:
   subtab_ausgangssituation = st.tabs(["Ausgangssituation", "Bedienungsanleitung", "Sensitivity Analysis"])

with tab_sz_erstellen:
    counter_text = st.text("Es wurden bisher " + str(erstellte_szenarien) + " von " + str(max_szenarien) + " Szenarien erstellt")

    st.write("##")

    lockdown_start = st.slider('Lockdown-Start (nach wie vielen Wochen?)', 1, 4, step=1)

    st.markdown("""---""")

    lockdown_dauer = st.slider('Lockdown-Dauer (in Wochen?)', 2, 6, step=2)

    st.markdown("""---""")

    lockdown_orte = st.radio(
        "Welche Orte sollen im Lockdown geschlossen werden?",
        ('Arbeit & Öffentliche Orte', 'Schulen & Öffentliche Orte', 'Schulen', 'Alles'), horizontal=True)

    st.markdown("""---""")

    aha_staerke = st.radio(
        "Sollen die AHA-Regeln empfohlen oder verpflichtend gelten?",
        ('Keine', 'Empfohlen', 'Verpflichtend'), horizontal=True, disabled=True)

    st.markdown("""---""")

    caption_black = '<p style="color:#30333f;font-size: 14px;">Welche AHA-Regeln sollten gelten?</p>'
    st.markdown(caption_black, unsafe_allow_html=True)

    aha_regeln_art = checks = st.columns(2)
    with aha_regeln_art[0]:
        st.checkbox('Masken')
    with aha_regeln_art[1]:
        st.checkbox('Abstand')

    st.markdown("""---""")

    aha_staerke = st.radio(
        "Welcher Anteil der Bevölkerung hält sich nicht an die Lockdown-Verordnung?",
        ('0%', '20%'), horizontal=True)

    st.markdown("""---""")

    aha_staerke = st.radio(
        "Welche Impfstrategie soll verfolgt werden?",
        ('Zufällig', 'Interaktion', 'Alter'), horizontal=True, disabled=True)

    st.markdown("""""")

    st.write("##")

    dummy_1, simulieren, dummy_1 = st.beta_columns(3)
    if simulieren.button('Simulieren'):
        erstellte_szenarien += 1
