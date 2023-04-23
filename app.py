import streamlit as st
import time
from PIL import Image


def store_parameter_combination():
    param_combination = {
        "lockdown_start": lockdown_start,
        "lockdown_dauer": lockdown_dauer,
        "lockdown_orte": lockdown_orte,
        "aha_staerke": aha_staerke,
        "masken": masken_checkbox,
        "abstand": abstand_checkbox,
        "ungehorsam": ungehorsam,
        "impfstrategie": impfstrategie

    }
    st.session_state['erstellte_szenarien'].append(param_combination)

st.set_page_config(layout='wide')
st.title("Pandemie-Ausbrüche unter der Lupe")

if 'max_szenarien' not in st.session_state:
    st.session_state['max_szenarien'] = 3

if 'erstellte_szenarien' not in st.session_state:
    st.session_state['erstellte_szenarien'] = []

tab_inf, tab_sz_erstellen, tab_sz_analysieren, tab_sz_vergleichen = st.tabs(['Informationen', 'Szenario erstellen', 'Szenario analysieren', 'Szenarien vergleichen'])

with tab_inf:
   ausgangssituation, bedienungsanleitung, sensitivity_analysis = st.tabs(['Ausgangssituation', 'Bedienungsanleitung', 'Vorab-Analyse'])

   with ausgangssituation:
       st.subheader('🧑‍💼 Versetzt euch in die Rolle eines/r Politikers/in')
       st.info('Stellt euch vor, ihr seid Mitglieder des Stadtrats und müsst bereits morgen Entscheidungen über Maßnahmen zur Vermeidung eines unkontrollierten Infektionsausbruchs treffen.\n\n'
               'Es handelt sich dabei um die kleine Gemeinde Gangelt mit einer Bevölkerung von etwa 11.000 Menschen. '
               'Es ist davon auszugehen, dass es bereits erste Infizierte gibt. Wer und wie viele genau, ist allerdings nicht bekannt.')

       st.write('##')

       st.subheader('🦠 Angaben zum Virustyp')
       st.info('Noch ist nicht alles über das Virus bekannt. Es scheint jedoch ansteckender als ein Grippevirus zu sein.'
               'Darüber hinaus gibt es Hinweise auf einen schwereren Verlauf und eine höheren Letalitätsrate.\n\n...')

       st.write('##')

       st.subheader('📊 Euch steht GERDA als Infektions-Modell zur Verfügung')
       st.info(
           'Für die Entscheidungsfindung stellt euch die Wissenschaft ein Infektionsmodell namens GERDA zur Verfügung.'
           ' Bei GERDA handelt es sich um ein agentenbasiertes Modell (ABM). Das bedeutet, dass die einzelnen Einwohner*innen von Gangelt im System synthetisch nachgebildet wurden,'
           ' um auf der Grundlage von echten Geodaten mögliche Zukunftsszenarien des Infektionsgeschehens zu simulieren. Damit kann getestet werden, wie sich verschiedene politische Maßnahmen auf den Infektionsverlauf möglicherweise auswirken könnten.\n\n'
           'Auch wenn bei der Entwicklung des Modells versucht wurde möglichst viele reale Gegebenheiten zu berücksichtigen, kann die Realität dennoch nie exakt abgebildet werden.'
           ' Das Modell soll somit lediglich als Entscheidungshilfe gesehen werden.'
           ' Denkt also auch an die verschiedenen Auswirkungen auf die Gesellschaft und andere/weitere Maßnahmen, die vom Modell nicht berücksichtigt werden.')

       st.write('##')

       st.subheader('⏳ Das Problem mit der Zeit')
       st.info(
           'Die Erstellung möglicher Zukunftsszenarien mit Hilfe des Modells nimmt einige Zeit in Anspruch. '
           ' Da bereits morgen über Maßnahmen entschieden werden muss, können (trotz Hochleistungsrechnern) lediglich 3 Zukunftsszenarien erstellt werden. '
           ' Auf deren Grundlage könnt ihr dann eure Entscheidung für oder gegen besetimmte Maßnahmen stützen.')

       st.write('##')

       st.subheader('🕵️‍♀️ Informationen über die Bevölkerungsgruppe')
       st.info('Nicht alle Personen in der Bevölkerung halten sich an die vorgegebenen Maßnahmen. '
               'Es ist sogar davon auszugehen, dass strengere Maßnahmen mit einem erhöhten Anteil derer, die sich nicht an die Maßnahmen halten, einhergeht.'
               ' Auch diesen Faktor könnt ihr bei der Erstellung von möglichen Szenarien berücksichtigen.')


   with bedienungsanleitung:
       st.subheader('🔎 So funktioniert die Nutzung des Simulationstools:')
       st.info('In den Reitern am oberen Bildrand kannst du den…\n\n'
               'Um ein Szenario zu erstellen…\n\n'
               'Deine erstellen Szenarien kannst du unter dem Reiter “Szenario analysieren” genauer unter die Lupe nehmen…\n\n'
               'Die Unterschiede in den Ergebnissen der verschiedenen Szenarien können am besten unter dem Reiter “Szenarien vergleichen” analysiert werden…\n...')

   with sensitivity_analysis:
       st.subheader('📈 Sensitivitätsanalyse')
       st.info('Das GERDA-Forschungsteam hat bereits etwas Vorarbeit geleistet und zwei sogenannte Sensitivitätsanalysen erstellt.'
               ' Bei einer Sensitivitätsanalyse wird geschaut, wie sich die Veränderung einer bestimmten Einflussgröße (z. B. Start oder Dauer eines Lockdowns) auf das Gesamtsystem auswirkt. Alle übrigen Einflussgrößen bleiben dabei unverändert.\n\n'
               ' Es steht zum einen eine Sensitivitätsanalye für den Start (oben) sowie eine für das Ende (unten) eines kompletten Lockdowns zur verfügung.'
               ' Vielleicht können euch bei der Wahl der Parameter für die Erstellung der Szenarien helfen.')

       st.write('##')

       st.subheader("Sensitivitätsanalyse für den Start des Lockdowns")
       st.write('##')
       image_sens_ana_s_20 = Image.open(
           'sensitivity_analysis/suppl_s_20.png')
       st.image(image_sens_ana_s_20)

       st.write('##')
       st.write('##')
       st.markdown(
           '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
           unsafe_allow_html=True)
       st.write('##')
       st.write('##')

       st.subheader("Sensitivitätsanalyse für die Dauer des Lockdowns")
       st.write('##')
       image_sens_ana_s_21 = Image.open(
           'sensitivity_analysis/suppl_s_21.png')
       st.image(image_sens_ana_s_21)



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

    masken, abstand = st.columns(2)
    with masken:
        masken_checkbox = st.checkbox('Masken')
    with abstand:
        abstand_checkbox = st.checkbox('Abstand')

    st.write('##')
    st.markdown('<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>', unsafe_allow_html=True)
    st.write('##')

    ungehorsam = st.radio(
        'Welcher Anteil der Bevölkerung hält sich nicht an die Lockdown-Verordnung?',
        ('0%', '20%'), horizontal=True)

    st.write('##')
    st.markdown('<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>', unsafe_allow_html=True)
    st.write('##')

    impfstrategie = st.radio(
        'Welche Impfstrategie soll verfolgt werden?',
        ('Zufällig', 'Interaktion', 'Alter'), horizontal=True, disabled=True)

    st.write('##')
    st.markdown('<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>', unsafe_allow_html=True)
    st.write('##')

    is_shown = False
    if len(st.session_state['erstellte_szenarien']) >= 3:
        is_shown = True
        st.error('Es wurde bereits die maximale Anzahl an Szenarien (' + str(st.session_state['max_szenarien']) + ') erstellt.')

    dummy_1, simulieren = st.columns(2)
    if simulieren.button('Simulieren', disabled=is_shown):

        # Progress-Bar
        progress_text = "Das Szenario wird erstellt..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1, text=progress_text)

        st.success('Done!')

        # TODO: on_click --> Parameter_Kombination speichern
        store_parameter_combination()

        # muss drin bleiben
        time.sleep(2) #change to 2
        st.experimental_rerun()

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
                    st.subheader("Infektionsverlauf")
                    image_trajectory = Image.open('test_test_plots/FirstChunk__infectivity_0o14_start_2_360_start_3_3023_closed_locs_work_disobedience_0o5_statii.png')
                    st.image(image_trajectory)

                with col2:
                    st.subheader("Infektionen pro Ort")
                    image_inf_per_loc = Image.open('test_test_plots/infections_per_time_per_loc_type.png')
                    st.image(image_inf_per_loc)

                with col3:
                    st.subheader("Infektionsverlauf")
                    image_ = Image.open('test_test_plots/FirstChunk__infectivity_0o14_start_2_360_start_3_3023_closed_locs_work_disobedience_0o5_sub_statii.png')
                    st.image(image_)

                with col4:
                    st.subheader("Infektionen nach Alter")
                    image_age_interactions = Image.open('test_test_plots/FirstChunk__infectivity_0o14_start_2_360_start_3_3023_closed_locs_work_disobedience_0o5_infectionpatterns.png')
                    st.image(image_age_interactions)


