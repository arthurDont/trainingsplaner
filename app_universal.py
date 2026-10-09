import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Universal Adaptive Coach", page_icon="🚀", layout="wide")

# --- INITIALISIERUNG DES SESSION STATE FÜR ONBOARDING ---
if "onboarding_abgeschlossen" not in st.session_state:
    st.session_state.onboarding_abgeschlossen = False

if "profil" not in st.session_state:
    st.session_state.profil = {}

if "gewicht_historie" not in st.session_state:
    st.session_state.gewicht_historie = pd.DataFrame(columns=["Datum", "Gewicht"])

if "kraft_historie" not in st.session_state:
    st.session_state.kraft_historie = []


# --- ONBOARDING-WIZARD (WENN NOCH NICHT ABGESCHLOSSEN) ---
if not st.session_state.onboarding_abgeschlossen:
    st.title("🚀 Willkommen beim Adaptive Coaching System")
    st.write("Lass uns deinen individuellen Trainings- und Ernährungsplan aufbauen. Bitte furhe einmalig das Onboarding durch.")

    with st.form("onboarding_form"):
        st.subheader("1. Biometrie & Gesundheit")
        col1, col2, col3 = st.columns(3)
        with col1:
            alter = st.number_input("Alter (Jahre)", min_value=15, max_value=90, value=57)
        with col2:
            gewicht_init = st.number_input("Aktuelles Gewicht (kg)", min_value=40.0, max_value=150.0, value=90.0, step=0.5)
        with col3:
            groesse = st.number_input("Größe (cm)", min_value=140, max_value=220, value=178)

        medikamente_check = st.checkbox("Nehme ich regelmäßige Medikamente ein (z.B. Blutdrucksenker)?", value=True)
        gesundheits_notiz = st.text_input("Gesundheitliche Hinweise / Einschränkungen (optional)", value="Blutdruckmanagement unter Medikation")

        st.subheader("2. Trainingserfahrung & Leistungsdaten")
        erfahrung = st.selectbox("Trainingstatus", ["Einsteiger", "Fortgeschrittener", "Ambitionierter Ausdauersportler / Athlet"])
        ftp_init = st.number_input("Aktuelle FTP (Watt) oder Schwellenwert", min_value=100, max_value=500, value=225, step=5)
        wochenstunden = st.slider("Geplante Trainingsstunden pro Woche", 2.0, 20.0, 8.0, 0.5)

        st.subheader("3. Zielsetzung & Event")
        ziel_typ = st.selectbox("Hauptziel", [
            "Langdistanz / Event-Vorbereitung (z.B. Gran Fondo / Radmarathon)", 
            "Gewichtsreduktion & Stoffwechseloptimierung", 
            "Allgemeine Fitness & Gesundheit",
            "Kraft- & Muskelaufbau"
        ])
        event_name = st.text_input("Name des Events (falls vorhanden)", value="Mallorca 312")
        event_datum = st.date_input("Datum des Hauptziels", value=datetime.date(2027, 4, 24))

        st.subheader("4. Ernährung & Präferenzen")
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
                "medikamente": medikamente_check,
                "gesundheit": gesundheits_notiz,
                "erfahrung": erfahrung,
                "ftp": ftp_init,
                "wochenstunden": wochenstunden,
                "ziel_typ": ziel_typ,
                "event_name": event_name,
                "event_datum": event_datum,
                "ernaehrung": ernaehrung,
                "fasten": fasten_aktiv
            }
            # Initialisiere Startgewicht in Historie
            heute_str = datetime.date.today().strftime("%Y-%m-%d")
            st.session_state.gewicht_historie = pd.DataFrame({"Datum": [heute_str], "Gewicht": [gewicht_init]})
            st.session_state.onboarding_abgeschlossen = True
            st.rerun()

else:
    # --- HAUPT-APP (NACH ERFOLGREICHEM ONBOARDING) ---
    p = st.session_state.profil
    
    st.title(f"🚴‍♂️ Adaptives Coaching-Dashboard für: {p['event_name']}")
    st.success(f"Profil geladen: {p['ziel_typ']} | Zieltermin: {p['event_datum']} | Ernährung: {p['ernaehrung']}")

    # Sidebar für tägliches Tracking
    st.sidebar.header("Tägliches Monitoring")
    aktuelles_gewicht = st.sidebar.number_input("Gewicht heute (kg)", value=float(p['gewicht']), step=0.5)
    if st.sidebar.button("Gewicht eintragen"):
        heute_str = datetime.date.today().strftime("%Y-%m-%d")
        new_row = pd.DataFrame({"Datum": [heute_str], "Gewicht": [aktuelles_gewicht]})
        st.session_state.gewicht_historie = pd.concat([st.session_state.gewicht_historie, new_row]).drop_duplicates(subset=["Datum"], keep="last").reset_index(drop=True)
        st.sidebar.success("Gewicht aktualisiert!")

    coros_hrv = st.sidebar.selectbox("Tagesform / HRV", ["Gut / Stabil", "Müde / Erhöht"])
    
    if st.sidebar.button("🔄 Onboarding zurücksetzen / Profil bearbeiten"):
        st.session_state.onboarding_abgeschlossen = False
        st.rerun()

    # Tabs im Hauptbereich
    tab1, tab2, tab3 = st.tabs(["📊 Übersicht & Biometrie", "📉 Gewichtsverlauf", "⚙️ Profil-Daten"])
    
    with tab1:
        st.subheader("Dein individueller Status")
        col1, col2, col3 = st.columns(3)
        col1.metric("Aktuelle FTP", f"{p['ftp']} Watt")
        col2.metric("Gewicht", f"{aktuelles_gewicht} kg")
        col3.metric("Tage bis zum Event", f"{(p['event_datum'] - datetime.date.today()).days} Tage")
        
        st.info(f"**Gesundheits- & Sicherheitsmodus:** {'Aktiv (Blutdruck/Medikamente berücksichtigt)' if p['medikamente'] else 'Standard'}")
        st.write(f"**Ernährungs-Framework:** {p['ernaehrung']} | Intervallfasten: {'Ja (Essen ab 14:00 Uhr)' if p['fasten'] else 'Nein'}")

    with tab2:
        st.subheader("Gewichtsentwicklung")
        if not st.session_state.gewicht_historie.empty:
            st.line_chart(st.session_state.gewicht_historie.set_index("Datum"))
            st.dataframe(st.session_state.gewicht_historie)

    with tab3:
        st.subheader("Deine Onboarding-Parameter")
        st.json(p)