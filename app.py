import streamlit as st
import time
from PIL import Image
import numpy as np

import firebase_admin
from firebase_admin import credentials, firestore

# initialize firebase db if not existing
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    })

    firebase_admin.initialize_app(cred, {
        'projectId': st.secrets["project_id"]
    })

# use Firestore
db = firestore.client()

# example 
doc_ref = db.collection("test").document("demo")
doc_ref.set({"abc": "def!"})
doc = doc_ref.get()

def toggle_lockdown():
    st.session_state["lockdown_disabled"] = lockdown_yes_no

# TODO
def check_aha_staerke():
    if abstand_checkbox or masken_checkbox:
        st.session_state["aha_staerke_disable"] = False
    else:
        st.session_state["aha_staerke_disable"] = True

def store_parameter_combination():
    param_combination = {
        "lockdown_yes_no": lockdown_yes_no,
        "lockdown_start": lockdown_start,
        "lockdown_dauer": lockdown_dauer,
        "lockdown_orte": lockdown_orte,
        "aha_staerke": aha_staerke,
        "masken": masken_checkbox,
        "abstand": abstand_checkbox,
        "ungehorsam": ungehorsam,
        #"impfstrategie": impfstrategie
    }
    st.session_state['erstellte_szenarien'].append(param_combination)

# Database
def speichere_szenario_in_firestore(code, image_urls):
    # Reihenfolge der Kategorien sicherstellen
    category_order = [
        "Infektionsverlauf (SIR)",
        "Infektions-Stati im Zeitverlauf",
        "Infektionen nach Ort",
        "Infektionen nach Alter",
        "Neue Diagnosen nach Alter"
    ]

    # Falls ein Mapping oder Metadaten verfügbar sind, hier sortieren (Platzhalter)
    # Aktuell wird angenommen, dass image_urls bereits korrekt sortiert ist:
    doc_ref = db.collection("szenarien").document(code)

    try:
        # make sure the urls are list
        if isinstance(image_urls, str):
            image_urls = [image_urls]
        st.write(image_urls)
        # access images if existing
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            existing_images = data.get("images", [])
            # Merge: flache Liste ohne Duplikate
            all_images = existing_images + image_urls
            doc_ref.update({"images": all_images})
        else:
            doc_ref.set({"images": image_urls})
            
        st.success("Szenario erfolgreich gespeichert.")
    except Exception as e:
        st.error(f"Fehler beim Speichern in Firestore: {e}")


def get_dynamic_paths_to_images(param_combination):
    # Kein Lockdown ausgewaehlt
    if param_combination["lockdown_yes_no"] == False:
        # infectivity
        prefix = 'https://medien.cedis.fu-berlin.de/pandemie_dt_media/gerda_output/nolockdown/'

        if (not param_combination['masken']) and (not param_combination['abstand']):
            suffix = 'FU__infectivity_0o14'
        elif param_combination['masken'] and param_combination['abstand']:
            suffix = 'FU__infectivity_0o078'
        elif param_combination['masken'] or param_combination['abstand']:
            suffix = 'FU__infectivity_0o106'


        trajectory_image_path = prefix + suffix + "/analysis/plots/" + suffix + "_statii.png"
        sub_image_path = prefix + suffix + "/analysis/plots/" + suffix + "_sub_statii.png"
        infections_per_loc_path = prefix + suffix + "/analysis/plots/" + "infections_per_time_per_loc_type.png"
        infectionspattern_per_age_group_path = prefix + suffix + "/analysis/plots/" + suffix + "_infectionpatterns.png"
        new_diagnoses_per_100000_path = prefix + suffix + "/analysis/plots/" + suffix + "_age_specific_diagnosis_incidence.png"
        new_deaths_per_100000_path = prefix + suffix + "/analysis/plots/" + suffix + "_age_specific_death_incidence.png"

    # Mit Lockdown
    else:
        # infectivity
        prefix = 'https://medien.cedis.fu-berlin.de/pandemie_dt_media/gerda_output/infectivity_'
        if param_combination['masken'] and param_combination['abstand']:
            if param_combination['aha_staerke'] == "Empfohlen":
                prefix += '0106/'
            else:
                prefix += '0078/'
        elif param_combination['masken'] and (not param_combination['abstand']):
            if param_combination['aha_staerke'] == "Empfohlen":
                prefix += '0118/'
            else:
                prefix += '0098/'
        elif (not param_combination['masken']) and param_combination['abstand']:
            if param_combination['aha_staerke'] == "Empfohlen":
                prefix += '0126/'
            else:
                prefix += '0112/'
        else:
            prefix += '014/'

        # lockdown start
        if param_combination['lockdown_start'] == 1:
            prefix += "start_168/"
        if param_combination['lockdown_start'] == 2:
            prefix += "start_336/"
        if param_combination['lockdown_start'] == 3:
            prefix += "start_504/"
        if param_combination['lockdown_start'] == 4:
            prefix += "start_672/"

        suffix = ""
        # disobedience
        if param_combination['ungehorsam'] == '0%':
            suffix += 'FU__disobedience_0_'
        if param_combination['ungehorsam'] == '10%':
            suffix += 'FU__disobedience_0o1_'
        if param_combination['ungehorsam'] == '20%':
            suffix += 'FU__disobedience_0o2_'
        if param_combination['ungehorsam'] == '40%':
            suffix += 'FU__disobedience_0o4_'

        # lockdown end
        lockdown_start_int = int(param_combination['lockdown_start']) * 168
        lockdown_dauer_int = int(param_combination['lockdown_dauer']) * 168
        start_3 = str(lockdown_start_int + lockdown_dauer_int)
        suffix += 'start_3_' + start_3 + "_"

        # closed locs
        suffix += 'closed_locs_'
        if param_combination['lockdown_orte'] == 'Arbeit': # TODO
            suffix += "['work']"
        if param_combination['lockdown_orte'] == 'Schulen': # TODO
            suffix += "['school', 'school_0', 'school_1', 'school_2']"
        if param_combination['lockdown_orte'] == 'Öffentliche Orte':
            suffix += "['public']"
        if param_combination['lockdown_orte'] == 'Arbeit & Öffentliche Orte':
            suffix += "['work', 'public']"
        if param_combination['lockdown_orte'] == 'Schulen & Öffentliche Orte':
            suffix += "['public', 'school', 'school_0', 'school_1', 'school_2']"
        if param_combination['lockdown_orte'] == 'Alles':
            suffix += "['work', 'public', 'school', 'school_0', 'school_1', 'school_2']"

        trajectory_image_path = prefix + suffix + "/analysis/plots/" + suffix + "_statii.png"
        sub_image_path = prefix + suffix + "/analysis/plots/" + suffix + "_sub_statii.png"
        infections_per_loc_path = prefix + suffix + "/analysis/plots/" + "infections_per_time_per_loc_type.png"
        infectionspattern_per_age_group_path = prefix + suffix + "/analysis/plots/" + suffix + "_infectionpatterns.png"
        new_diagnoses_per_100000_path = prefix + suffix + "/analysis/plots/" + suffix + "_age_specific_diagnosis_incidence.png"
        new_deaths_per_100000_path = prefix + suffix + "/analysis/plots/" + suffix + "_age_specific_death_incidence.png"

        trajectory_image_path = trajectory_image_path.replace(' ', "%20")
        sub_image_path = sub_image_path.replace(' ', "%20")
        infections_per_loc_path = infections_per_loc_path.replace(' ', "%20")
        infectionspattern_per_age_group_path = infectionspattern_per_age_group_path.replace(' ', "%20")
        new_diagnoses_per_100000_path = new_diagnoses_per_100000_path.replace(' ', "%20")
        new_deaths_per_100000_path = new_deaths_per_100000_path.replace(' ', "%20")

    dynamic_paths_to_images = [trajectory_image_path,
                               sub_image_path,
                               infections_per_loc_path,
                               infectionspattern_per_age_group_path,
                               new_diagnoses_per_100000_path,
                               new_deaths_per_100000_path]

    return dynamic_paths_to_images


# Wide-Mode
# st.set_page_config(layout='wide')

st.title("Pandemie-Ausbrüche unter der Lupe")

if 'max_szenarien' not in st.session_state:
    st.session_state['max_szenarien'] = 3

if 'erstellte_szenarien' not in st.session_state:
    st.session_state['erstellte_szenarien'] = []

tab_inf, tab_sz_erstellen, tab_sz_analysieren, tab_sz_vergleichen, about = st.tabs(
    ['ℹ️ Informationen', '🛠️ Szenario erstellen', '🔍 Szenarien analysieren', '🤔 Szenarien vergleichen', "💡Über's Projekt"])

with tab_inf:
    ausgangssituation, sensitivity_analysis, bedienungsanleitung = st.tabs(
        ['Ausgangssituation', 'Vorab-Analyse', 'Bedienungsanleitung'])

    with ausgangssituation:
        st.subheader('🧑‍💼 Versetzt euch in die Rolle eines/r Politikers/in')
        st.info(
            'Stellt euch vor, ihr seid Mitglieder des Stadtrats und müsst bereits morgen Entscheidungen über Maßnahmen zur Vermeidung eines unkontrollierten Infektionsausbruchs treffen.\n\n'
            'Es handelt sich dabei um die kleine Gemeinde Gangelt mit einer Bevölkerung von etwa 11.000 Menschen. '
            'Es ist davon auszugehen, dass es bereits erste Infizierte gibt. Wer und wie viele genau, ist allerdings nicht bekannt.')

        st.subheader('🦠 Angaben zum Virustyp')
        st.info(
            'Noch gibt es nicht allzu viele Informationen über das Virus. Es scheint jedoch deutlich ansteckender als ein Grippevirus zu sein.'
            ' Außerdem werden viele der Infizierten nach der Ansteckung grün.'
            ' Darüber hinaus gibt es Hinweise auf einen vergleichsweise schwereren Verlauf und eine höhere Sterberate.'
            )

        st.subheader('📊 Euch steht GERDA als Infektions-Modell zur Verfügung')
        st.info(
            'Für die Entscheidungsfindung stellt euch die Wissenschaft ein Infektionsmodell namens GERDA zur Verfügung.'
            ' Bei GERDA handelt es sich um ein agentenbasiertes Modell (ABM). Das bedeutet, dass die einzelnen Einwohner*innen von Gangelt im System synthetisch nachgebildet wurden,'
            ' um auf der Grundlage von echten Geodaten mögliche Zukunftsszenarien des Infektionsgeschehens zu simulieren. Damit kann getestet werden, wie sich verschiedene politische Maßnahmen auf den Infektionsverlauf möglicherweise auswirken könnten.\n\n'
            'Auch wenn bei der Entwicklung des Modells versucht wurde möglichst viele reale Gegebenheiten zu berücksichtigen, kann die Realität dennoch nie exakt abgebildet werden.'
            ' Das Modell soll somit lediglich als Entscheidungshilfe angesehen werden.'
            ' Denkt also auch an die verschiedenen Auswirkungen auf die Gesellschaft und andere/weitere Maßnahmen, die vom Modell nicht berücksichtigt werden.')

        st.subheader('⏳ Das Problem mit der Zeit')
        st.info(
            'Die Erstellung möglicher Zukunftsszenarien mit Hilfe des Modells nimmt einige Zeit in Anspruch. '
            ' Da bereits morgen über Maßnahmen entschieden werden muss, können (trotz Hochleistungsrechnern) lediglich drei Zukunftsszenarien erstellt werden. '
            ' Auf deren Grundlage könnt ihr dann eure Entscheidung für oder gegen bestimmte Maßnahmen stützen.')

        st.subheader('🕵️‍♀️ Informationen über die Bevölkerungsgruppe')
        st.info('Nicht alle Personen in der Bevölkerung halten sich an die vorgegebenen Maßnahmen. '
                'Es ist sogar davon auszugehen, dass strengere Maßnahmen mit einem erhöhten Anteil derer, die sich nicht an die Maßnahmen halten, einhergeht.'
                ' Auch diesen Faktor könnt ihr (je nach eurer Erwartung) bei der Erstellung von möglichen Szenarien Einstellen.')

    with sensitivity_analysis:
        st.subheader('📈 Sensitivitätsanalyse')
        st.info(
            'Das GERDA-Forschungsteam hat bereits etwas Vorarbeit geleistet und zwei sogenannte Sensitivitätsanalysen erstellt.'
            ' Bei einer Sensitivitätsanalyse wird geschaut, wie sich die Veränderung einer bestimmten Einflussgröße (z. B. Start oder Dauer eines Lockdowns) auf das Gesamtsystem auswirkt. Alle übrigen Einflussgrößen bleiben dabei unverändert.\n\n'
            ' Es steht zum einen eine Sensitivitätsanalye für den Start (oben) sowie eine für das Ende (unten) eines kompletten Lockdowns zur Verfügung.'
            ' Vielleicht können euch bei der Wahl der Parameter für die Erstellung der Szenarien helfen.')

        st.write('&nbsp;')

        st.subheader("Sensitivitätsanalyse für den Start des Lockdowns")
        image_sens_ana_s_20 = Image.open(
            'sensitivity_analysis/suppl_s_20.png')
        st.image(image_sens_ana_s_20)

        st.markdown(
            '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
            unsafe_allow_html=True)

        st.write('&nbsp;')

        st.subheader("Sensitivitätsanalyse für die Dauer des Lockdowns")
        image_sens_ana_s_21 = Image.open(
            'sensitivity_analysis/suppl_s_21.png')
        st.image(image_sens_ana_s_21)

    with bedienungsanleitung:
        st.subheader('🦠 Willkommen zur Pandemie-Simulations-App! 🦠')

        caption_black = '<p style="color:#30333f;font-size: 16px;">Hier könnt ihr verschiedene Szenarien erstellen und analysieren, um die Auswirkungen der Pandemie auf bestimmte Maßnahmen zu untersuchen. Zum Beispiel könnt ihr untersuchen, wie sich die Pandemie auswirkt, wenn ein Lockdown eingeführt wird oder Schulen geschlossen werden. In der oberen Leiste findet ihr 3 Reiter, zwischen denen ihr wählen könnt.</p>'
        st.markdown(caption_black, unsafe_allow_html=True)

        st.caption('')

        st.subheader('🛠️ Szenario erstellen')
        st.info(
            'Unter dem Reiter "Szenario erstellen", lassen sich durch die Auswahl verschiedener Parameter Szenarien erstellen, wobei pro Szenario 100 Simulationen durchgeführt werden. Ihr könnt jedoch insgesamt maximal 3 Szenarien erstellen.')

        st.subheader('🔍 Szenarien analysieren')
        st.info(
            'Unter dem Reiter "Szenario analysieren" könnt ihr Einblicke in die visualisierten Daten eurer erstellten Szenarien gewinnen. Hier könnt ihr im Zeitverlauf die Anzahl der Infizierten, Genesenen und Verstorbenen für jedes Szenario einsehen. Klickt in der oberen Leiste auf das gewünschte Szenario, um es genauer zu betrachten. Das hilft euch dabei den Pandemieverlauf zu bewerten und sinnvolle Schlüsse daraus zu ziehen.')

        st.subheader('🤔 Szenarien vergleichen')
        st.info(
            'Unter dem Reiter „Szenarien vergleichen" könnt ihr eure erstellten Szenarien im direkten Vergleich einsehen. Klickt dazu auf den Graph, der euch im Vergleich besonders interessiert, um sie direkt nebeneinander anzeigen zu lassen.')

with tab_sz_erstellen:
    st.write('&nbsp;')

    nr_sz_info_text = 'Es wurden bereits ' + str(len(st.session_state['erstellte_szenarien'])) + '/' + str(
        st.session_state['max_szenarien']) + ' Szenarien erstellt.'
    st.info(nr_sz_info_text)

    st.write('&nbsp;')

    caption_black = '<p style="color:#30333f;font-size: 14px;">Welche AHA-Regeln sollten gelten?</p>'
    st.markdown(caption_black, unsafe_allow_html=True)

    masken, abstand = st.columns(2)
    with masken:
        masken_checkbox = st.checkbox('Masken', key="masken_checkbox", value=True)
    with abstand:
        abstand_checkbox = st.checkbox('Abstand', key="abstand_checkbox", value=True)

    st.write('&nbsp;')
    st.markdown(
        '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
        unsafe_allow_html=True)
    st.write('&nbsp;')

    aha_staerke = st.radio(
        'Sollen die AHA-Regeln empfohlen oder verpflichtend gelten?',
        ('Empfohlen', 'Verpflichtend'), horizontal=True, disabled=False)

    st.write('&nbsp;')
    st.markdown(
        '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
        unsafe_allow_html=True)
    st.write('&nbsp;')

    lockdown_yes_no = st.checkbox("Lockdown", key="lockdown_yes_no", value=True, on_change=toggle_lockdown)

    st.write('&nbsp;')
    st.markdown(
        '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
        unsafe_allow_html=True)
    st.write('&nbsp;')

    if st.session_state.get("lockdown_yes_no", True):
        st.session_state.lockdown_disabled = False
    else:
        st.session_state.lockdown_disabled = True

    lockdown_start = st.slider('Lockdown-Start (nach wie vielen Wochen?)', 1, 4, value=1, step=1,
                               disabled=st.session_state.get("lockdown_disabled", True))

    st.write('&nbsp;')
    st.markdown(
        '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
        unsafe_allow_html=True)
    st.write('&nbsp;')

    lockdown_dauer_options = np.array([2,3,4,6])
    lockdown_dauer = st.select_slider('Lockdown-Dauer (in Wochen?)', options=lockdown_dauer_options, value=2,
                               disabled=st.session_state.get("lockdown_disabled", True))

    st.write('&nbsp;')
    st.markdown(
        '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
        unsafe_allow_html=True)
    st.write('&nbsp;')

    lockdown_orte = st.radio(
        'Welche Orte sollen im Lockdown geschlossen werden?',
        ('Schulen', 'Öffentliche Orte', 'Arbeit & Öffentliche Orte', 'Schulen & Öffentliche Orte', 'Alles'), horizontal=True,
        disabled=st.session_state.get("lockdown_disabled", True))

    st.write('&nbsp;')
    st.markdown(
        '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
        unsafe_allow_html=True)
    st.write('&nbsp;')

    ungehorsam = st.radio(
        'Wie hoch schätzt ihr den Anteil der Bevölkerung ein, der sich NICHT an die Lockdown-Verordnung hält?',
        ('0%', '10%', '20%', '40%'), horizontal=True, disabled=st.session_state.get("lockdown_disabled", True))

    st.write('&nbsp;')
    st.markdown(
        '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
        unsafe_allow_html=True)
    st.write('&nbsp;')

    #impfstrategie = st.radio(
    #    'Welche Impfstrategie soll verfolgt werden?',
    #    ('Zufällig', 'Interaktion', 'Alter'), horizontal=True, disabled=True)

    #st.write('&nbsp;')
    #st.markdown(
    #    '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
    #    unsafe_allow_html=True)
    #st.write('&nbsp;')

    is_shown = False
    if len(st.session_state['erstellte_szenarien']) >= 3:
        is_shown = True
        st.warning(
            'Ihr habt nun die maximale Anzahl an Szenarien (' + str(st.session_state['max_szenarien']) + ') erstellt.')

    dummy_1, simulieren = st.columns(2)
    if simulieren.button('Simulieren', disabled=is_shown):

        # Progress-Bar
        progress_text = "Das Szenario wird erstellt..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)

        st.success('Fertig!')

        store_parameter_combination()

        time.sleep(1)
        st.rerun()

    st.markdown("[nach oben](#pandemie-ausbr-che-unter-der-lupe)")

with tab_sz_analysieren:
    if len(st.session_state['erstellte_szenarien']) == 0:
        st.info('Du musst für die Analyse mindestens ein Szenario erstellen')
    else:
        tab_names = []
        for i in range(0, len(st.session_state['erstellte_szenarien'])):
            tab_name = 'Szenario ' + str(i + 1)
            tab_names.append(tab_name)

        subtabs_analyse = st.tabs(tab_names)

        all_dynamic_paths_to_images = []

        for i in range(0, len(st.session_state['erstellte_szenarien'])):
            with subtabs_analyse[i]:
                param_combination = st.session_state['erstellte_szenarien'][i]

                masken_zusammenfassung = 'Nein'
                if param_combination['masken']:
                    masken_zusammenfassung = 'Ja'

                abstand_zusammenfassung = 'Nein'
                if param_combination['abstand']:
                    abstand_zusammenfassung = 'Ja'

                st.subheader('Eure gewählten Parameter für Szenario ' + str((i + 1)))

                links, rechts = st.columns(2)

                lockdown_yes_no_value = 'Nein'
                if param_combination['lockdown_yes_no']:
                    lockdown_yes_no_value = 'Ja'

                lockdown_start_param_value = ' nach ' + str(param_combination['lockdown_start']) + ' Wochen'
                if not param_combination['lockdown_yes_no']:
                    lockdown_start_param_value = ' (kein Lockdown)'

                lockdown_ablehnende = str(param_combination['ungehorsam'])
                if not param_combination['lockdown_yes_no']:
                    lockdown_ablehnende = ' (kein Lockdown)'

                make_table_smaller = '<style scoped> table {font-size: 13px;} </style>'

                st.markdown(make_table_smaller, unsafe_allow_html=True)

                with links:
                    table_links = '''
                            | Parameter | Wert |
                            |---|---|
                            | Masken | :green[''' + masken_zusammenfassung + ''']|
                            | Lockdown | :green[''' + lockdown_yes_no_value + ''']|
                            | Lockdown-Start | :green[''' + lockdown_start_param_value + ''']|
                            | Lockdown-Verweigernde | :green[''' + lockdown_ablehnende + ''']|
                        '''

                    st.markdown(table_links)

                lockdown_dauer_param_value = str(param_combination['lockdown_dauer']) + ' Woche(n)'
                if not param_combination['lockdown_yes_no']:
                    lockdown_dauer_param_value = ' (kein Lockdown)'

                aha_regeln_param_value = str(param_combination['aha_staerke'])

                lockdown_orte_param_value = str(param_combination['lockdown_orte'])
                if not param_combination['lockdown_yes_no']:
                    lockdown_orte_param_value = ' (kein Lockdown)'

                with rechts:
                    st.markdown(
                        '''
                            | Parameter | Wert |
                            |---|---|
                            | Abstand: | :green[''' + abstand_zusammenfassung + ''']|
                            | "AHA" verpflichtend/empfohlen | :green[''' + aha_regeln_param_value + ''']|
                            | Lockdown-Dauer | :green[''' + lockdown_dauer_param_value + ''']|
                            | Lockdown-Orte | :green[''' + lockdown_orte_param_value + ''']|
                        ''')

                st.write('&nbsp;')

                # get the (4?) images, based on the parameter combination
                dynamic_paths_to_images = get_dynamic_paths_to_images(param_combination)
                all_dynamic_paths_to_images.append(dynamic_paths_to_images)

                row1_col1, row1_col2 = st.columns(2)

                with row1_col1:
                    st.subheader("Infektionsverlauf")
                    #st.write(dynamic_paths_to_images[0])
                    st.image(dynamic_paths_to_images[0])

                with row1_col2:
                    st.subheader("Infektions-Stati im Zeitverlauf")
                    #st.write(dynamic_paths_to_images[1])
                    st.image(dynamic_paths_to_images[1])

                row2_col1, row2_col2 = st.columns(2)

                with row2_col1:
                    st.subheader("Infektionen nach Ort")
                    #st.write(dynamic_paths_to_images[2])
                    st.image(dynamic_paths_to_images[2])

                with row2_col2:
                    st.subheader("Infektionen nach Alter")
                    #st.write(dynamic_paths_to_images[3])
                    st.image(dynamic_paths_to_images[3])

                st.subheader("Neue Diagnosen nach Alter")
                #st.write(dynamic_paths_to_images[4])
                st.image(dynamic_paths_to_images[4])

                #st.subheader("Neue Todesfälle nach Alter")
                #st.write(dynamic_paths_to_images[5])
                #st.image(dynamic_paths_to_images[5])

        # Eingabe eines Codes durch den Benutzer
        szenario_code = st.text_input("📌 Bitte hier deinen Gruppen-Code eingeben (z.B. B5)", key="szenario_code")

        # Button zum Speichern des Szenarios
        if st.button("Szenario für's Plenum speichern"):
            if szenario_code:
                active_index = tab_names.index(st.session_state.get("__tabs__", tab_names[0]))
                st.write(active_index)
                speichere_szenario_in_firestore(szenario_code, all_dynamic_paths_to_images[active_index])
            else:
                st.warning("Bitte einen Code eingeben!")



with tab_sz_vergleichen:
    if len(st.session_state['erstellte_szenarien']) < 2:
        st.info('Du musst für den Vergleich mindestens zwei Szenarien erstellen')
    else:
        szenarien = st.session_state['erstellte_szenarien']
        anzahl_szenarien = len(szenarien)

        paths_to_images = get_dynamic_paths_to_images(szenarien[0])
        anzahl_images = len(paths_to_images)

        image_chunks = []
        for i in range(anzahl_images):
            image_chunks.append([])

        for param_combination in szenarien:
            paths_to_images = get_dynamic_paths_to_images(param_combination)

            for i in range(len(paths_to_images)):
                image_chunks[i].append(paths_to_images[i])

        expander_sir = st.expander("Infektionsverlauf (SIR)")
        sir = expander_sir.columns(3)

        for i in range(len(image_chunks[0])):
            with sir[i]:
                st.image(image_chunks[0][i], caption="Szenario " + str((i + 1)))

        expander_stati = st.expander("Infektions-Stati im Zeitverlauf")
        statii = expander_stati.columns(3)
        for i in range(len(image_chunks[1])):
            with statii[i]:
                st.image(image_chunks[1][i], caption="Szenario " + str((i + 1)))

        expander_loc = st.expander("Ifektionen nach Ort")
        loc = expander_loc.columns(3)
        for i in range(len(image_chunks[2])):
            with loc[i]:
                st.image(image_chunks[2][i], caption="Szenario " + str((i + 1)))

        expander_inf_age_groups = st.expander("Infektionen nach Alter")
        inf_age_groups = expander_inf_age_groups.columns(3)
        for i in range(len(image_chunks[3])):
            with inf_age_groups[i]:
                st.image(image_chunks[3][i], caption="Szenario " + str((i + 1)))

        expander_new_diagn_age = st.expander("Neue Diagnosen nach Alter")
        diagnoses_age_group = expander_new_diagn_age.container()
        with diagnoses_age_group:
            for i in range(len(image_chunks[4])):
                if i > 0:
                    st.markdown(
                        '<iv data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
                        unsafe_allow_html=True)
                st.image(image_chunks[4][i], caption="Szenario " + str((i + 1)))


        #expander_new_deaths_age = st.expander("Neue Todesfälle nach Alter")
        #deaths_age_group = expander_new_deaths_age.container()
        #with deaths_age_group:
        #    for i in range(len(image_chunks[5])):
        #        if i > 0:
        #            st.markdown(
        #                '<div data-baseweb="tab-border" aria-hidden="true" role="presentation" class="st-cx st-bd st-cu"></div>',
        #                unsafe_allow_html=True)
        #        st.image(image_chunks[5][i], caption="Szenario " + str((i + 1)))

with about:
    st.info("**Über Uns – Das Projekt Schule@DecisionTheatreLab**\n\nDie GERDA-WebApp wurde im Rahmen des Projekts Schule@DecisionTheatreLab entwickelt. Das Projekt bringt Schüler\*innen und Wissenschaftler\*innen zusammen und zielt darauf ab, ein tieferes Verständnis für die Bedeutung von Mathematik für unsere Gesellschaft und Zukunft zu entwickeln. In sogenannten Decision Theatres erleben die Schüler*innen, wie mathematische Modellierung Entscheidungsprozesse unterstützen kann. Weitere Informationen zu unserem Projekt und den Decision Theatres finden Sie auf unserer Webseite.(https://mathplus.de/schuledecisiontheatrelab/).")
    st.info("**Über das Modell hinter der GERDA-WebApp**\n\nGERDA (GEoReferenced Demographic Agent-based model) ist ein agentenbasiertes Modell zur Simulation der Ausbreitung von COVID-19 in einem realistischen Szenario. Das Modell wurde von der Arbeitsgruppe Theoretische Biophysik an der Humboldt-Universität zu Berlin entwickelt und integriert demografische Daten, Tagesabläufe sowie geographische Informationen. Es berücksichtigt die klinischen Phasen von Infektion, Krankheit und Genesung und ermöglicht die Simulation verschiedener nicht-pharmazeutischer Maßnahmen an Orten wie Arbeitsplätzen, Schulen und öffentlichen Räumen. GERDA wurde unter der GNU General Public License v3.0 veröffentlicht und ist kostenlos im GitLab-Repository (https://tbp-klipp.science/GERDA-model/) verfügbar.\n\n")
    st.info("**Förderungen von MATH+ und Berlin University Alliance**\n\nDas Projekt Schule@DecisionTheatreLab wird von Oktober 2021 bis Ende 2024 sowohl vom Exzellenzcluster MATH+ als auch von der Berlin University Alliance (BUA) gefördert. Darüber hinaus wird es bis Ende 2025 weiterhin durch MATH+ finanziert.\n\n")
    st.info("**Technische Umsetzung durch Joshua Wiebe**\n\n")
