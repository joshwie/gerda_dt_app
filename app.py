import streamlit as st
import time
from PIL import Image


def store_parameter_combination():
    param_combination = {}

    st.session_state['erstellte_szenarien'].append(param_combination)


st.set_page_config(layout='wide')
st.title("Pandemie-Ausbrüche unter der Lupe")

if 'max_szenarien' not in st.session_state:
    st.session_state['max_szenarien'] = 3

if 'erstellte_szenarien' not in st.session_state:
    st.session_state['erstellte_szenarien'] = []

tab_inf, tab_sz_erstellen, tab_sz_analysieren, tab_sz_vergleichen = st.tabs(['Informationen', 'Szenario erstellen', 'Szenario analysieren', 'Szenarien vergleichen'])

with tab_inf:
   subtabs_ausgangssituation = st.tabs(['Ausgangssituation', 'Bedienungsanleitung', 'Vorab-Analyse'])

   with subtabs_ausgangssituation[0]:
       st.subheader('🧑‍💼 Versetzt euch in die Rolle eines/r Politikers/in')
       st.info('Stell dir vor du bist Mitglied des Stadtrats und musst morgen Entscheidungen über Pandemiemaßnahmen treffen.\n...')

       st.write('##')

       st.subheader('📊 Euch steht GERDA als Pandemie-Modell zur Verfügung')
       st.info('Bei GERDA handelt es sich um ein agentenbasiertes Modell (ABM), das auf der Grundlage von Geodaten...')

       st.write('##')

       st.subheader('🕵️‍♀️ Informationen über die Bevölkerungsgruppe')
       st.info('Nicht alle Personen in der Bevölkerung halten sich an die vorgegebenen Maßnahmen...')

       st.write('##')

       st.subheader('🦠 Angaben zum Virustyp')
       st.info('Der entdeckte Virus wurde bereits untersucht und weist eine starke/schwache Infektiösität auf.\n...')

   with subtabs_ausgangssituation[1]:
       st.subheader('🔎 So funktioniert die Nutzung des Simulationstools:')
       st.info('In den Reitern am oberen Bildrand kannst du den…\n\nUm ein Szenario zu erstellen…\n\nDeine erstellen Szenarien kannst du unter dem Reiter “Szenario analysieren” genauer unter die Lupe nehmen…\n\nDie Unterschiede in den Ergebnissen der verschiedenen Szenarien können am besten unter dem Reiter “Szenarien vergleichen” analysiert werden…\n...')

   with subtabs_ausgangssituation[2]:
       st.subheader('📈 Sensitivitätsanalyse')
       st.info('Unter einer Sensitivitätsanalyse versteht man …\n\nDas GERDA-Forschungsteam hat bereits zwei kleinere Sensitivitätsanalysen erstellt.\n\n'
               'Vielleicht können sie dabei helfen, ...')


with tab_sz_erstellen:

    st.write('##')

    # FIX (+1 weg)
    # nicht mehr als 3!

    nr_sz_info_text = 'Es wurden bereits ' + str(len(st.session_state['erstellte_szenarien'])) + '/' + str(st.session_state['max_szenarien']) + ' Szenarien erstellt.'
    st.info(nr_sz_info_text)

    st.write('##')

    lockdown_start = st.slider('Lockdown-Start (nach wie vielen Wochen?)', 1, 4, step=1)

    st.write('##')
    st.markdown('<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>', unsafe_allow_html=True)
    st.write('##')

    lockdown_dauer = st.slider('Lockdown-Dauer (in Wochen?)', 2, 6, step=2)

    st.write('##')
    st.markdown('<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>', unsafe_allow_html=True)
    st.write('##')

    lockdown_orte = st.radio(
        'Welche Orte sollen im Lockdown geschlossen werden?',
        ('Arbeit & Öffentliche Orte', 'Schulen & Öffentliche Orte', 'Schulen', 'Alles'), horizontal=True)

    st.write('##')
    st.markdown('<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>', unsafe_allow_html=True)
    st.write('##')

    aha_staerke = st.radio(
        'Sollen die AHA-Regeln empfohlen oder verpflichtend gelten?',
        ('Keine', 'Empfohlen', 'Verpflichtend'), horizontal=True, disabled=True)

    st.write('##')
    st.markdown('<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>', unsafe_allow_html=True)
    st.write('##')

    caption_black = '<p style="color:#30333f;font-size: 14px;">Welche AHA-Regeln sollten gelten?</p>'
    st.markdown(caption_black, unsafe_allow_html=True)

    aha_regeln_art = st.columns(2)
    with aha_regeln_art[0]:
        st.checkbox('Masken')
    with aha_regeln_art[1]:
        st.checkbox('Abstand')

    st.write('##')
    st.markdown('<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>', unsafe_allow_html=True)
    st.write('##')

    aha_staerke = st.radio(
        'Welcher Anteil der Bevölkerung hält sich nicht an die Lockdown-Verordnung?',
        ('0%', '20%'), horizontal=True)

    st.write('##')
    st.markdown('<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>', unsafe_allow_html=True)
    st.write('##')

    aha_staerke = st.radio(
        'Welche Impfstrategie soll verfolgt werden?',
        ('Zufällig', 'Interaktion', 'Alter'), horizontal=True, disabled=True)

    st.write('##')
    st.markdown('<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>', unsafe_allow_html=True)
    st.write('##')

    dont_show = False
    if len(st.session_state['erstellte_szenarien']) >= 3:
        dont_show = True
        st.error('Es wurde bereits die maximale Anzahl an Szenarien (' + str(st.session_state['max_szenarien']) + ') erstellt.')

    dummy_1, simulieren = st.columns(2)
    if simulieren.button('Simulieren', disabled=dont_show):

        new_state = st.session_state['erstellte_szenarien'].append('dummy')
        #st.write(st.session_state['erstellte_szenarien'])

        # Uncomment for progress bar
        '''
        progress_text = "Das Szenario wird erstellt..."
        my_bar = st.progress(0, text=progress_text)
        
        
        for percent_complete in range(100):
            time.sleep(0.07)
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        st.success('Done!')
        time.sleep(2)
        '''

        st.experimental_rerun()
        # TODO: on_click --> Parameter_Kombination speichern
        store_parameter_combination()
        st.write("HI!")
        st.write(st.session_state['erstellte_szenarien'])

    st.markdown("[nach oben](#pandemie-ausbr-che-unter-der-lupe)")

with tab_sz_analysieren:
    if len(st.session_state['erstellte_szenarien']) == 0:
        st.info('Du musst für die Analyse mindestens ein Szenario erstellen')
    else:
        tab_names = []
        for i in range(0, len(st.session_state['erstellte_szenarien'])):
            tab_name = 'Szenario ' + str(i+1)
            tab_names.append(tab_name)

        subtabs_analyse = st.tabs(tab_names)

        for i in range(0, len(st.session_state['erstellte_szenarien'])):
            with subtabs_analyse[i]:
                st.info('Ausgewählte Parameter für Szenario ' + str((i+1)) + ':')

                # TODO: zusammenfassung Parameter..

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.header("Infektionsverlauf")
                    image_trajectory = Image.open('plots/FirstChunk__infectivity_0o14_start_2_360_start_3_3023_closed_locs_work_disobedience_0o5_statii.png')
                    st.image(image_trajectory)

                with col2:
                    st.header("Infektionen pro Ort")
                    image_inf_per_loc = Image.open('plots/infections_per_time_per_loc_type.png')
                    st.image(image_inf_per_loc)

                with col3:
                    st.header("Infektionsverlauf")
                    image_ = Image.open('plots/FirstChunk__infectivity_0o14_start_2_360_start_3_3023_closed_locs_work_disobedience_0o5_sub_statii.png')
                    st.image(image_)

                with col4:
                    image_age_interactions = Image.open('plots/FirstChunk__infectivity_0o14_start_2_360_start_3_3023_closed_locs_work_disobedience_0o5_infectionpatterns.png')
                    st.image(image_age_interactions)


