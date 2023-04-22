import streamlit as st

if 'max_szenarien' not in st.session_state:
    st.session_state['max_szenarien'] = 3

if 'erstellte_szenarien' not in st.session_state:
    st.session_state['erstellte_szenarien'] = 0

tab_inf, tab_sz_erstellen, tab_sz_analysieren, tab_sz_vergleichen = st.tabs(["Informationen", "Szenario erstellen", "Szenario analysieren", "Szenarien vergleichen"])

with tab_inf:
   subtabs_ausgangssituation = st.tabs(["Ausgangssituation", "Bedienungsanleitung", "Sensitivity Analysis"])

with tab_sz_erstellen:

    st.write("##")

    # FIX (+1 weg)
    # nicht mehr als 3!

    nr_sz_info_text = "Es wurden bisher " + str(st.session_state['erstellte_szenarien']) + " von " + str(st.session_state['max_szenarien']) + " Szenarien erstellt"

    st.info(nr_sz_info_text)

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

    dont_show = False
    if st.session_state['erstellte_szenarien'] >= 3:
        dont_show = True
        st.info("Du hast bereits die maximale Anzahl an Szenarien erstellt.")

    dummy_1, simulieren, dummy_1 = st.beta_columns(3)
    if simulieren.button('Simulieren', disabled=dont_show):
        st.session_state['erstellte_szenarien'] += 1
        st.write(st.session_state['erstellte_szenarien'])

with tab_sz_analysieren:
    if st.session_state['erstellte_szenarien'] == 0:
        st.info("Du musst für die Analyse mindestens ein Szenario erstellen")
    else:
        tab_names = []
        for i in range(0, st.session_state['erstellte_szenarien']):
            tab_name = "Szenario " + str(i+1)
            tab_names.append(tab_name)

        subtabs_analyse = st.tabs(tab_names)

        for i in range(0, st.session_state['erstellte_szenarien']):
            with tab_names[0]:
                st.info("Ausgewählte Parameter für Szenario" + (i+1))

