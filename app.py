import streamlit as st

st.title('Pandemie-Ausbrüche unter der Lupe:')
st.subheader('Ein Decision Theater zu Infektionsausbreitung')

tab_inf, tab_sz_erstellen, tab_sz_analysieren, tab_sz_vergleichen = st.tabs(["Informationen", "Szenario erstellen", "Szenario analysieren", "Szenarien vergleichen"])