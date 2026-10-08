import streamlit as st
import pandas as pd
import datetime

st.title("🚴‍♂️ Norwegischer Adaptiver Smart-Trainer-Planer")
st.write("Dein tagesaktueller Coach mit Coros, Blutdruck-Sicherheit, Thermomix, Mallorca-Rechner & veganem Kraft-Futter!")

# --- Datenbank für Workouts & Thermomix-Verpflegung (inkl. Dr. Vegan inspirierten Rezepten) ---
if "rezept_datenbank" not in st.session_state:
    st.session_state.rezept_datenbank = {
        "regeneration": [
            {
                "titel": "Norwegische Zone-2 Grundlagenfahrt (Nüchtern möglich)",
                "typ": "Grundlagen / Aerobe Basis",
                "beschreibung": "Strikte Zone 2 (ca. 60-70% FTP). Perfekt für den Fettstoffwechsel im Vormittags-Fastenfenster.",
                "zutaten": ["100g Haferflocken", "350ml Sojamilch", "1 Banane", "1 EL Ahornsirup"],
                "tm_schritte": ["Porridge im Thermomix bei 90°C / Stufe 2.5 für 7 Minuten zubereiten (ab 14:00 Uhr essen)."]
            }
        ],
        "schwellen_intervalle": [
            {
                "titel": "High-Protein Power-Pasta: Pilz-Linsen-Erbsen-Pfanne",
                "typ": "Post-Intervalle / High Carb & Protein",
                "beschreibung": "Ideal nach harten Schwellentagen. Liefert komplexe Carbs und pflanzliches Protein für die Muskelregeneration.",
                "zutaten": ["200g Vollkornpasta", "150g rote Linsen", "150g Champignons (geviertelt)", "100g TK-Erbsen", "1 Zwiebel", "2 Knoblauchzehen", "400g passierte Tomaten", "1 TL Olivenöl"],
                "tm_schritte": [
                    "Zwiebel und Knoblauch im Mixtopf 5 Sek / Stufe 5 zerkleinern.",
                    "Olivenöl zugeben und 3 Min / 120°C / Stufe 1 dünsten.",
                    "Champignons zugeben und 4 Min / 100°C / Linkslauf / Stufe 1 anbraten.",
                    "Rote Linsen, Erbsen und passierte Tomaten zugeben. 15 Min / 100°C / Linkslauf / Stufe 1 garen (parallel Pasta auf dem Herd kochen)."
                ]
            }
        ],
        "lang_ausfahrt_verpflegung": [
            {
                "titel": "Mallorca 312 Carb-Boost: DIY Energy-Rice-Cakes & Drink",
                "typ": "Langdistanz- & Magen-Darm-Training",
                "beschreibung": "Fokus auf hohe Kohlenhydratzufuhr (60-90g/h) für Ausfahrten über 3 Stunden.",
                "zutaten": ["300g Rundkornreis", "500ml Kokoswasser", "4 Datteln", "Ahornsirup", "Maltodextrin-Pulver"],
                "tm_schritte": [
                    "Reis und Kokoswasser in den Mixtopf geben, 20 Min / 100°C / Linkslauf / Stufe 1 garen.",
                    "Datteln und Ahornsirup unterrühren, in eine Form drücken und auskühlen lassen.",
                    "Maltodextrin für die Trinkflaschen vorbereiten (Verhältnis 2:1 mit Fruktose)."
                ]
            }
        ]
    }

# --- Historie für Gewicht & Krafttraining in session_state ---
if "gewicht_historie" not in st.session_state:
    st.session_state.gewicht_historie = pd.DataFrame(columns=["Datum", "Gewicht"])

if "kraft_historie" not in st.session_state:
    st.session_state.kraft_historie = []

# --- Sidebar: Biometrie, Medikamente & Tracking ---
st.sidebar.header("1. Biometrie & Tagesform")
ftp = st.sidebar.number_input("Deine aktuelle FTP (Watt)", value=220, step=5)
gewicht = st.sidebar.number_input("Aktuelles Gewicht heute (kg, Smart-Waage)", value=90.0, step=0.5)

if st.sidebar.button("Gewicht für heute speichern"):
    heute_str = datetime.date.today().strftime("%Y-%m-%d")
    new_row = pd.DataFrame({"Datum": [heute_str], "Gewicht": [gewicht]})
    st.session_state.gewicht_historie = pd.concat([st.session_state.gewicht_historie, new_row]).drop_duplicates(subset=["Datum"], keep="last").reset_index(drop=True)
    st.sidebar.success(f"Gewicht {gewicht} kg gespeichert!")

st.sidebar.markdown("---")
st.sidebar.subheader("Coros Uhr & Medikation")
coros_hrv = st.sidebar.selectbox("Coros HRV-Status / Erholung", ["Gut / Im grünen Bereich", "Leicht erhöht / Stabil", "Niedrig / Müde"])
schlaf_stunden = st.sidebar.slider("Schlaf (Stunden)", 4.0, 10.0, 7.5, 0.5)
medikamente_aktiv = st.sidebar.checkbox("Blutdrucksenker (Ramipril/Amlodipin) aktiv", value=True)

trainings_fokus = st.sidebar.selectbox(
    "Was steht heute an?", 
    [
        "Normales Training / Intervalle", 
        "Lange Ausfahrt (Unter-Woche-Langdistanz / Magen-Training)", 
        "Doppelter Schwellentag (Double Threshold)",
        "Regeneration / Zone 2"
    ]
)
ausfahrt_stunden = st.sidebar.slider("Geplante Fahrtdauer (Stunden)", 1.0, 10.0, 3.5, 0.5)

st.sidebar.markdown("---")
st.sidebar.subheader("💪 Dein Rad-Kraft-Log")
kraft_gemacht = st.sidebar.checkbox("Kraft-Session heute absolviert?", value=False)

st.sidebar.markdown("**Wähle die absolvierten Übungen aus:**")
u_hip = st.sidebar.checkbox("Hip Extension")
u_bauch = st.sidebar.checkbox("Bauch / Core")
u_lat = st.sidebar.checkbox("Latzug")
u_brust = st.sidebar.checkbox("Brustdrücken")
u_ruder = st.sidebar.checkbox("Ruderzug")
u_knie = st.sidebar.checkbox("Kniebeuge")
u_curl = st.sidebar.checkbox("Arm Curls")
u_ext = st.sidebar.checkbox("Arm Extensions")
u_wallsit = st.sidebar.checkbox("Wall Sit (Blutdruck & Oberschenkel)")

kraft_notiz = st.sidebar.text_input("Gewichte / Sätze Notiz (z.B. 3x10 @ 60kg)")

if kraft_gemacht and st.sidebar.button("Kraft-Einheit speichern"):
    ausgewaehlte_uebungen = []
    if u_hip: ausgewaehlte_uebungen.append("Hip Ext")
    if u_bauch: ausgewaehlte_uebungen.append("Bauch")
    if u_lat: ausgewaehlte_uebungen.append("Latzug")
    if u_brust: ausgewaehlte_uebungen.append("Brustdrücken")
    if u_ruder: ausgewaehlte_uebungen.append("Ruderzug")
    if u_knie: ausgewaehlte_uebungen.append("Kniebeuge")
    if u_curl: ausgewaehlte_uebungen.append("Arm Curls")
    if u_ext: ausgewaehlte_uebungen.append("Arm Extensions")
    if u_wallsit: ausgewaehlte_uebungen.append("Wall Sit")
    
    uebungen_str = ", ".join(ausgewaehlte_uebungen) if ausgewaehlte_uebungen else "Keine spezifischen Übungen"
    eintrag_text = f"{datetime.date.today()} | **Übungen:** {uebungen_str} — *Notiz:* {kraft_notiz if kraft_notiz else 'Keine Notiz'}"
    st.session_state.kraft_historie.append(eintrag_text)
    st.sidebar.success("Kraft-Session erfolgreich gespeichert!")

# --- Berechnungs- & Sicherheits-Logik ---
is_lang = "Lange Ausfahrt" in trainings_fokus
is_schwellen = "Doppelter Schwellentag" in trainings_fokus or "Normales Training" in trainings_fokus

if is_lang or is_schwellen:
    nuechtern_warnung = "⚠️ **Blutdruck- & Leistungs-Sicherheit:** Da du Ramipril und Amlodipin nimmst und heute eine harte/lange Einheit fährst, **nicht streng nüchtern trainieren!** Nutze Intra-Workout-Carbs (Maltodextrin/Isostar ab Minute 30), um Kreislaufabsackungen zu verhindern."
    carbs_pro_stunde = 75 if is_lang else 50
else:
    nuechtern_warnung = "✅ **Fasten-Fenster aktiv:** Perfekt für das Vormittags-Training im nüchternen Zustand (Essen ab 14:00 Uhr). Das entspannte Zone-2-Rollen harmoniert super mit deinen Blutdruckwerten."
    carbs_pro_stunde = 0

gesamt_carbs = int(carbs_pro_stunde * ausfahrt_stunden)

if coros_hrv == "Niedrig / Müde" or schlaf_stunden < 6.5:
    empfehlung_titel = "⚠️ Zone-2 Erholungseinheit (Coros-Biometrie meldet Erschöpfung)"
    ausgabe_struktur = "60 Minuten lockeres Rollen in Zone 2. Schone das Nervensystem."
    aktives_rezept = st.session_state.rezept_datenbank["regeneration"][0]
elif is_lang:
    empfehlung_titel = "🌴 Mallorca 312 Langdistanz-Einheit (Unter der Woche)"
    ausgabe_struktur = f"Strikte Zone 2 über {ausfahrt_stunden} Stunden. Konsequente Nahrungsaufnahme ab Minute 30!"
    aktives_rezept = st.session_state.rezept_datenbank["lang_ausfahrt_verpflegung"][0]
elif is_schwellen and "Doppelter Schwellentag" in trainings_fokus:
    empfehlung_titel = "🔥 Norwegischer Doppel-Schwellentag (2 Einheiten)"
    ausgabe_struktur = "Einheit 1 (Vormittag): 4x8 Min @ 90% FTP | Einheit 2 (Nachmittag): 3x6 Min @ 90% FTP."
    aktives_rezept = st.session_state.rezept_datenbank["schwellen_intervalle"][0]
else:
    empfehlung_titel = "🎯 Der norwegische Klassiker: 4 x 8 Minuten"
    ausgabe_struktur = "10 Min Warm-up | 4x (8 Min @ 90% FTP / 2 Min @ 55% FTP) | 10 Min Cool-down"
    aktives_rezept = st.session_state.rezept_datenbank["schwellen_intervalle"][0]

# --- Haupt-Dashboard ---
st.header("📋 Tagesempfehlung & Sicherheits-Check")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Gewicht", f"{gewicht} kg")
col2.metric("Coros HRV", coros_hrv.split()[0])
col3.metric("Carbs / Stunde", f"{carbs_pro_stunde} g/h")
col4.metric("Kraft-Log", f"{len(st.session_state.kraft_historie)} Einheiten")

st.markdown(f"### **{empfehlung_titel}**")
st.info(f"🎯 **Struktur-Vorgabe:** {ausgabe_struktur}")
st.warning(nuechtern_warnung)

# Tabs für Verlauf
tab1, tab2, tab3 = st.tabs(["📉 Gewichtsverlauf", "💪 Kraft-Historie", "📋 Dein Kraft-Plan"])
with tab1:
    if not st.session_state.gewicht_historie.empty:
        st.line_chart(st.session_state.gewicht_historie.set_index("Datum"))
        st.dataframe(st.session_state.gewicht_historie)
    else:
        st.write("Noch kein Gewicht gespeichert. Nutze den Button in der Sidebar.")

with tab2:
    if st.session_state.kraft_historie:
        for eintrag in st.session_state.kraft_historie:
            st.markdown(f"- {eintrag}")
    else:
        st.write("Noch keine Kraft-Einheiten dokumentiert.")

with tab3:
    st.markdown("### 🏋️ Dein persönliches Rad-Kraftprogramm")
    st.markdown("""
    * **Beine & Posterior Chain:** Kniebeuge, Hip Extension
    * **Isometrisch (Blutdruck & Oberschenkel):** Wall Sit
    * **Oberkörper Zug & Rumpf:** Ruderzug, Latzug, Bauch
    * **Oberkörper Druck & Arme:** Brustdrücken, Arm Curls, Arm Extensions
    """)

# Rezept & Thermomix-Guide
st.markdown("---")
st.subheader("🌱 Thermomix-Verpflegungs-Guide & Einkaufsliste")
st.markdown(f"**Empfohlenes Rezept:** {aktives_rezept['titel']}")
st.markdown(f"_Typ: {aktives_rezept['typ']} | {aktives_rezept['beschreibung']}_")

spalte_links, spalte_rechts = st.columns(2)
with spalte_links:
    st.markdown("🛒 **Einkaufsliste:**")
    for zutat in aktives_rezept['zutaten']:
        st.checkbox(zutat, key=f"z_{zutat}")
with spalte_rechts:
    st.markdown("🟢 **Thermomix-Schritte:**")
    for schritt in aktives_rezept['tm_schritte']:
        st.write(f"- {schritt}")