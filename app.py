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

def get_dynamic_paths_to_images(param_combination):
    dynamic_paths_to_images = []

    # infectivity
    prefix = 'infectivity_'
    if param_combination['masken'] and param_combination['abstand']:
        prefix += '0078/'
    elif param_combination['masken'] or param_combination['abstand']:
        prefix += '0106/'
    else:
        prefix += '0140/' # stimmen die Ordner-Bezeichnungen?

    # lockdown start
    if param_combination['lockdown_start'] == 1:
        prefix += "start_168/"
    if param_combination['lockdown_start'] == 2:
        prefix += "start_336/"
    if param_combination['lockdown_start'] == 3:
        prefix += "start_504/"
    if param_combination['lockdown_start'] == 4:
        prefix += "start_672/"

    prefix += "analysis/plots/"

    suffix = ""
    # disobedience
    if param_combination['ungehorsam'] == '0%':
        suffix += 'FU__disobedience_0_'
    if param_combination['ungehorsam'] == '20%':
        suffix += 'FU__disobedience_0o2_'

    # lockdown end
    lockdown_start_int = int(param_combination['lockdown_start']) * 168
    lockdown_dauer_int = int(param_combination['lockdown_dauer']) * 168
    start_3 = str(lockdown_start_int + lockdown_dauer_int)
    suffix += 'start_3_' + start_3 + "_"

    # closed locs
    suffix += 'closed_locs_'
    if param_combination['lockdown_orte'] == 'Arbeit & Öffentliche Orte':
        suffix += "['work', 'public']"
    if param_combination['lockdown_orte'] == 'Schulen & Öffentliche Orte':
        suffix += "['public', 'school', 'school_0', 'school_1', 'school_2']"
    if param_combination['lockdown_orte'] == 'Schulen':
        suffix += "['school', 'school_0', 'school_1', 'school_2']"
    if param_combination['lockdown_orte'] == 'Alles':
        suffix += "['work', 'public', 'school', 'school_0', 'school_1', 'school_2']"


    trajectory_image_path = prefix + suffix + "/" + suffix + "_statii.png"
    sub_image_path = prefix + suffix + "/" + suffix + "_sub_statii.png"
    infections_per_loc_path = prefix + suffix + "/" + "infections_per_time_per_loc_type.png"
    infectionspattern_per_age_group = prefix + suffix + "/" + suffix + "_infectionpatterns.png"

    st.write(trajectory_image_path)
    st.write(sub_image_path)
    st.write(infections_per_loc_path)
    st.write(infectionspattern_per_age_group)

    # comment (just testing)
    dynamic_paths_to_images = ['test_plots/FirstChunk__infectivity_0o14_start_2_360_start_3_3023_closed_locs_work_disobedience_0o5_statii.png',
                       'test_plots/FirstChunk__infectivity_0o14_start_2_360_start_3_3023_closed_locs_work_disobedience_0o5_sub_statii.png',
                       'test_plots/infections_per_time_per_loc_type.png',
                       'test_plots/FirstChunk__infectivity_0o14_start_2_360_start_3_3023_closed_locs_work_disobedience_0o5_infectionpatterns.png']

    return dynamic_paths_to_images

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
               ' Darüber hinaus gibt es Hinweise auf einen schwereren Verlauf und eine höheren Letalitätsrate.\n\n...')

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
       st.info('In den Reitern am oberen Bildrand kannst du den Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.\n\n'
               'Um ein Szenario zu erstellen, Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.\n\n'
               'Deine erstellen Szenarien kannst du unter dem Reiter “Szenario analysieren” genauer unter die Lupe nehmen. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.\n\n'
               'Die Unterschiede in den Ergebnissen der verschiedenen Szenarien können am besten unter dem Reiter “Szenarien vergleichen” analysiert werden. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.')

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

        store_parameter_combination()

        time.sleep(2)
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
                param_combination = st.session_state['erstellte_szenarien'][i]

                masken_zusammenfassung = 'Nein'
                if param_combination['masken']:
                    masken_zusammenfassung = 'Ja'

                abstand_zusammenfassung = 'Nein'
                if param_combination['abstand']:
                    abstand_zusammenfassung = 'Ja'

                st.subheader('Ausgewählte Parameter für Szenario ' + str((i+1)))
                st.info('Lockdown-Start: nach ' + str(param_combination['lockdown_start']) + ' Woche(n)\n\n'
                        'Lockdown-Dauer: ' + str(param_combination['lockdown_dauer']) + ' Woche(n)\n\n'
                        'Lockdown-Orte: ' + str(param_combination['lockdown_orte']) + '\n\n'
                        'AHA-Regeln empfohlen oder verpflichtend: ' + '(DEAKTIVIERT)\n\n'
                        'Masken: ' + masken_zusammenfassung + '\n\n'
                        'Abstand: ' + abstand_zusammenfassung + '\n\n'
                        'Anteil der Bevölkerung, der sich nicht an die Maßnahmen hält: ' + str(param_combination['ungehorsam']) + "\n\n"
                        'Impfstrategie: ' + '(DEAKTIVIERT)')

                # get the (4?) images, based on the parameter combination
                dynamic_paths_to_images = get_dynamic_paths_to_images(param_combination)

                row1_col1, row1_col2 = st.columns(2)

                with row1_col1:
                    st.subheader("Infektionsverlauf")
                    image_trajectory = Image.open(dynamic_paths_to_images[0])
                    st.image(image_trajectory)

                with row1_col2:
                    st.subheader("Infektions-?")
                    image_ = Image.open(dynamic_paths_to_images[1])
                    st.image(image_)

                row2_col1, row2_col2 = st.columns(2)

                with row2_col1:
                    st.subheader("Infektionen pro Ort")
                    image_inf_per_loc = Image.open(dynamic_paths_to_images[2])
                    st.image(image_inf_per_loc)

                with row2_col2:
                    st.subheader("Infektionen nach Alter")
                    image_age_interactions = Image.open(dynamic_paths_to_images[3])
                    st.image(image_age_interactions)


