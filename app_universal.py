import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Universal Adaptive Coach", page_icon="🚀", layout="wide")

# --- INITIALISIERUNG DES SESSION STATE ---
if "onboarding_abgeschlossen" not in st.session_state:
    st.session_state.onboarding_abgeschlossen = False

if "profil" not in st.session_state:
    st.session_state.profil = {}

if "gewicht_historie" not in st.session_state:
    st.session_state.gewicht_historie = pd.DataFrame(columns=["Datum", "Gewicht"])

if "kraft_historie" not in st.session_state:
    st.session_state.kraft_historie = []


# --- ONBOARDING-WIZARD (ERWEITERTE GESUNDHEIT & BIOMETRIE) ---
if not st.session_state.onboarding_abgeschlossen:
    st.title("🚀 Universal Adaptive Coach — Erweitertes Onboarding")
    st.write("Lass uns ein präzises Profil erstellen, das medizinische und gesundheitliche Faktoren (wie Blutdruck, Diabetes & Vorerkrankungen) sicher berücksichtigt.")

    with st.form("onboarding_form"):
        st.subheader("1. Allgemeine Biometrie")
        col1, col2, col3 = st.columns(3)
        with col1:
            alter = st.number_input("Alter (Jahre)", min_value=15, max_value=90, value=57)
        with col2:
            gewicht_init = st.number_input("Aktuelles Gewicht (kg)", min_value=40.0, max_value=150.0, value=90.0, step=0.5)
        with col3:
            groesse = st.number_input("Größe (cm)", min_value=140, max_value=220, value=178)

        st.subheader("2. Erweiterter Gesundheits- & Medizin-Check")
        
        # Medikamente & Blutdruck
        blutdruck_meds = st.checkbox("Regelmäßige Einnahme von Blutdrucksenkern (z.B. Ramipril, Amlodipin)?", value=True)
        
        # Diabetes-Abfrage
        diabetes_status = st.selectbox(
            "Liegt eine Diabetes-Erdiagnose vor?", 
            ["Kein Diabetes", "Diabetes Typ 2", "Diabetes Typ 1", "Prädiabetes / Blutzucker-Regulation im Fokus"]
        )
        
        # Allgemeine Einschränkungen & Vorerkrankungen
        vorerkrankungen = st.multiselect(
            "Bekannte Vorerkrankungen oder Einflussfaktoren:",
            [
                "Herz-Kreislauf-System (z.B. Bluthochdruck)",
                "Stoffwechsel / Diabetes",
                "Orthopädische Gelenk- / Rückenprobleme",
                "Asthma / Atemwege",
                "Schilddrüse",
                "Keine nennenswerten Einschränkungen"
            ],
            default=["Herz-Kreislauf-System (z.B. Bluthochdruck)"]
        )

        allgemeines_befinden = st.slider(
            "Subjektives allgemeines Gesundheits- & Energieniveau im Alltag (1 = stark eingeschränkt, 10 = Top-fit)", 
            1, 10, 8
        )
        
        gesundheits_notiz = st.text_area("Details zu Medikamenten, Blutzuckermanagement oder Verletzungen (optional):", placeholder="z.B. Medikamenteneinnahme um 14:00 Uhr zum Essen; Blutzuckermessung vor dem Training...")

        st.subheader("3. Trainingserfahrung & Leistungsdaten")
        erfahrung = st.selectbox("Trainingstatus", ["Einsteiger", "Fortgeschrittener", "Ambitionierter Ausdauersportler / Athlet"])
        ftp_init = st.number_input("Aktuelle FTP (Watt) oder Schwellenwert", min_value=100, max_value=500, value=225, step=5)
        wochenstunden = st.slider("Geplante Trainingsstunden pro Woche", 2.0, 20.0, 8.0, 0.5)

        st.subheader("4. Zielsetzung & Event")
        ziel_typ = st.selectbox("Hauptziel", [
            "Langdistanz / Event-Vorbereitung (z.B. Gran Fondo / Radmarathon)", 
            "Gewichtsreduktion & Stoffwechseloptimierung", 
            "Allgemeine Fitness & Gesundheit",
            "Kraft- & Muskelaufbau"
        ])
        event_name = st.text_input("Name des Events (falls vorhanden)", value="Mallorca 312")
        event_datum = st.date_input("Datum des Hauptziels", value=datetime.date(2027, 4, 24))

        st.subheader("5. Ernährung & Präferenzen")
        ernaehrung = st.selectbox("Ernährungsform", [
            "Vegan (Fokus auf Linsen, Erbsen, Pilze)", 
            "Vegetarisch", 
            "Omnivor (Allesesser)", 
            "Low-Carb / Keto"
        ])
        fasten_aktiv = st.checkbox("Intervallfasten / Zeitfenster-Essen aktiv (z.B. Essen ab 14:00 Uhr)", value=True)

        submitted = st.form_submit_button("🚀 Profil speichern & Coach starten")

        if submitted:
            st.session_state.profil = {
                "alter": alter,
                "gewicht": gewicht_init,
                "groesse": groesse,
                "blutdruck_meds": blutdruck_meds,
                "diabetes_status": diabetes_status,
                "vorerkrankungen": vorerkrankungen,
                "befinden": allgemeines_befinden,
                "gesundheit_notiz": gesundheits_notiz,
                "erfahrung": erfahrung,
                "ftp": ftp_init,
                "wochenstunden": wochenstunden,
                "ziel_typ": ziel_typ,
                "event_name": event_name,
                "event_datum": event_datum,
                "ernaehrung": ernaehrung,
                "fasten": fasten_aktiv
            }
            heute_str = datetime.date.today().strftime("%Y-%m-%d")
            st.session_state.gewicht_historie = pd.DataFrame({"Datum": [heute_str], "Gewicht": [gewicht_init]})
            st.session_state.onboarding_abgeschlossen = True
            st.rerun()

else:
    # --- HAUPT-DASHBOARD ---
    p = st.session_state.profil
    
    st.title(f"🚴‍♂️ Adaptives Coaching-Dashboard: {p['event_name']}")
    st.success(f"Profil geladen | Ziel: {p['ziel_typ']} ({p['event_datum']}) | Diät: {p['ernaehrung']}")

    # Sidebar für tägliches Monitoring
    st.sidebar.header("Tägliches Monitoring")
    aktuelles_gewicht = st.sidebar.number_input("Gewicht heute (kg)", value=float(p['gewicht']), step=0.5)
    if st.sidebar.button("Gewicht eintragen"):
        heute_str = datetime.date.today().strftime("%Y-%m-%d")
        new_row = pd.DataFrame({"Datum": [heute_str], "Gewicht": [aktuelles_gewicht]})
        st.session_state.gewicht_historie = pd.concat([st.session_state.gewicht_historie, new_row]).drop_duplicates(subset=["Datum"], keep="last").reset_index(drop=True)
        st.sidebar.success("Gewicht aktualisiert!")

    coros_hrv = st.sidebar.selectbox("Tagesform / HRV / Erholung", ["Gut / Stabil", "Müde / Erhöht", "Eingeschränkt (Infekt/Krank)"])
    
    if st.sidebar.button("🔄 Profil bearbeiten / Onboarding neu starten"):
        st.session_state.onboarding_abgeschlossen = False
        st.rerun()

    # Tabs im Hauptbereich
    tab1, tab2, tab3 = st.tabs(["📊 Status & Sicherheits-Check", "📉 Gewichtsverlauf", "⚙️ Medizin- & Profil-Daten"])
    
    with tab1:
        st.subheader("Leistungs- & Gesundheits-Übersicht")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Aktuelle FTP", f"{p['ftp']} Watt")
        col2.metric("Gewicht", f"{aktuelles_gewicht} kg")
        col3.metric("Allg. Befinden", f"{p['befinden']}/10")
        col4.metric("Tage zum Event", f"{(p['event_datum'] - datetime.date.today()).days} Tage")
        
        # Dynamische Sicherheitswarnungen basierend auf den Onboarding-Daten
        if p['diabetes_status'] != "Kein Diabetes":
            st.warning(f"⚠️ **Diabetes-Hinweis aktiv ({p['diabetes_status']}):** Achte streng auf dein Blutzuckermanagement vor und während intensiver Intervalle. Halte schnelle Kohlenhydrate (Gels/Carb-Drinks) bereit.")
        if p['blutdruck_meds']:
            st.info("ℹ️ **Blutdruck-Medikation berücksichtigt:** Keine streng nüchternen High-Intensity-Einheiten; Intra-Workout-Carbs und zeitliche Entzerrung der Medikamente beachten.")
        if "Krank" in coros_hrv or p['befinden'] < 5:
            st.error("🛑 **Achtung:** Das subjektive Befinden oder die Tagesform meldet Einschränkungen. Reduziere das Training auf lockere Zone-2-Erholung oder lege einen Ruhetag ein!")

    with tab2:
        st.subheader("Gewichtsentwicklung")
        if not st.session_state.gewicht_historie.empty:
            st.line_chart(st.session_state.gewicht_historie.set_index("Datum"))
            st.dataframe(st.session_state.gewicht_historie)

    with tab3:
        st.subheader("Gespeicherte Profil- & Gesundheitsdaten")
        st.json(p)