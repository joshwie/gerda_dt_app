import streamlit as st

tab_inf, tab_sz_erstellen, tab_sz_analysieren, tab_sz_vergleichen = st.tabs(["Informationen", "Szenario erstellen", "Szenario analysieren", "Szenarien vergleichen"])

with tab_inf:
   st.header("Inf")
   st.tabs("Ausgangssituation")
