import streamlit as st

erstellte_szenarien = 0
max_szenarien = 3

tab_inf, tab_sz_erstellen, tab_sz_analysieren, tab_sz_vergleichen = st.tabs(["Informationen", "Szenario erstellen", "Szenario analysieren", "Szenarien vergleichen"])

with tab_inf:
   subtab_ausgangssituation = st.tabs(["Ausgangssituation", "Bedienungsanleitung", "Sensitivity Analysis"])

with tab_sz_erstellen:
    st.header("Es wurden bisher " + str(erstellte_szenarien) + " von " + str(max_szenarien) + " Szenarien erstellt")
    lockdown_start = st.slider('Lockdown-Start (nach wie vielen Wochen?)', 1, 4, step=1)

    lockdown_dauer = st.slider('Lockdown-Dauer (in Wochen?)', 2, 6, step=2)

    close_work_public = st.checkbox("Arbeit & Öffentliche Orte")
    close_school_public = st.checkbox("Schulen & Öffentliche Orte")
    close_school = st.checkbox("Schulen")
    close_all = st.checkbox("Alles")
