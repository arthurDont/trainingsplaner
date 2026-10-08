import streamlit as st
import pandas as pd
import random

st.title("🚴‍♂️ Norwegischer Adaptiver Smart-Trainer-Planer")
st.write("Dein tagesaktueller Coach mit Coros-Biometrie, Waage, Thermomix & MyWhoosh-Planung!")

if "rezept_datenbank" not in st.session_state:
    st.session_state.rezept_datenbank = {
        "regeneration": [
            {
                "titel": "Norwegische Zone-2 Grundlagenfahrt",
                "typ": "Grundlagen / Aerobe Basis",
                "beschreibung": "Strikte Zone 2 (ca. 60-70% FTP). Perfekt für den Fettstoffwechsel.",
                "zutaten": ["100g Haferflocken", "350ml Sojamilch", "1 Banane", "1 EL Ahornsirup"],
                "tm_schritte": ["Porridge im Thermomix bei 90°C / Stufe 2.5 für 7 Minuten zubereiten."]
            }
        ],
        "schwellen_intervalle": [
            {
                "titel": "Der norwegische Klassiker: 4 x 8 Minuten",
                "typ": "Schwellen-Einheit (Vormittag)",
                "beschreibung": "4 Intervalle à 8 Minuten knapp unter der anaeroben Schwelle (~90% FTP) mit 2 Minuten Trabpause.",
                "zutaten": ["200g Vollkornpasta", "150g Rote Linsen", "400g Passierte Tomaten", "1 Zwiebel"],
                "tm_schritte": ["Zwiebel zerkleinern. Linsen und Tomaten zugeben, 20 Min / 100°C / Linkslauf garen."]
            }
        ],
        "doppel_schwellen_nachmittag": [
            {
                "titel": "Norwegische Nachmittagsschwelle: 3 x 6 Minuten",
                "typ": "Schwellen-Einheit 2 (Nachmittag)",
                "beschreibung": "Die zweite moderate Schwelleneinheit des Tages. Etwas kürzer, um den Reiz zu maximieren.",
                "zutaten": ["300g Süßkartoffel", "1 Dose Kichererbsen", "200ml Kokosmilch"],
                "tm_schritte": ["Süßkartoffel zerkleinern, Kokosmilch und Kichererbsen zugeben, 18 Min / 100°C kochen."]
            }
        ]
    }

st.sidebar.header("1. Biometrische Morgen-Daten")
ftp = st.sidebar.number_input("Deine aktuelle FTP (Watt)", value=225, step=5)
gewicht = st.sidebar.number_input("Aktuelles Gewicht heute (kg, Smart-Waage)", value=75.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.subheader("Coros Uhr (Biometrie & Schlaf)")
coros_hrv = st.sidebar.selectbox("Coros HRV-Status / Erholung", ["Gut / Im grünen Bereich", "Leicht erhöht / Stabil", "Niedrig / Müde"])
schlaf_stunden = st.sidebar.slider("Schlaf (Stunden)", 4.0, 10.0, 7.5, 0.5)
ist_doppel_tag = st.sidebar.checkbox("Doppelter Schwellentag (z.B. Freitag)?", value=False)
verfuegbare_zeit = st.sidebar.slider("Verfügbare Zeit heute (Minuten)", 30, 150, 75, 15)

carbs_empfehlung = int(gewicht * 1.2)

if coros_hrv == "Niedrig / Müde" or schlaf_stunden < 6.5:
    empfehlung_titel = "⚠️ Zone-2 Erholungseinheit (Coros-Biometrie meldet Erschöpfung)"
    ausgabe_struktur = "60 Minuten lockeres Rollen in Zone 2. Keine Intervalle."
    ernaehrung = f"Leichte Kost ({carbs_empfehlung}g Carbs als Ziel), Fokus auf Hydratation."
    aktives_rezept = st.session_state.rezept_datenbank["regeneration"][0]
elif ist_doppel_tag:
    empfehlung_titel = "🔥 Norwegischer Doppel-Schwellentag (2 Einheiten)"
    ausgabe_struktur = "Einheit 1 (Vormittag): 4x8 Min @ 90% FTP | Einheit 2 (Nachmittag): 3x6 Min @ 90% FTP."
    ernaehrung = f"Zwischen den Einheiten: Schnell verfügbare Kohlenhydrate zuführen! Tagesziel: ca. {carbs_empfehlung}g Carbs."
    aktives_rezept = st.session_state.rezept_datenbank["schwellen_intervalle"][0]
else:
    empfehlung_titel = "🎯 Der norwegische Klassiker: 4 x 8 Minuten"
    ausgabe_struktur = "10 Min Warm-up | 4x (8 Min @ 90% FTP / 2 Min @ 55% FTP) | 10 Min Cool-down"
    ernaehrung = f"Vollwertige Kohlenhydrate vor dem Training (~{carbs_empfehlung}g Kohlenhydrat-Fokus)."
    aktives_rezept = st.session_state.rezept_datenbank["schwellen_intervalle"][0]

st.header("📋 Tagesempfehlung nach norwegischer Methode")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Waage-Gewicht", f"{gewicht} kg")
col2.metric("Coros HRV", coros_hrv.split()[0])
col3.metric("Schlaf", f"{schlaf_stunden} Std")
col4.metric("Carb-Ziel", f"~{carbs_empfehlung} g")

st.markdown(f"### **{empfehlung_titel}**")
st.info(f"🎯 **Struktur-Vorgabe für MyWhoosh:** {ausgabe_struktur}")
st.success(f"💡 **Biometrischer Ernährungs-Tipp:** {ernaehrung}")

st.markdown("---")
st.subheader("🌱 Empfohlenes Recovery-Gericht & Thermomix-Guide")
st.markdown(f"**Gericht:** {aktives_rezept['titel']}")

spalte_links, spalte_rechts = st.columns(2)
with spalte_links:
    st.markdown("🛒 **Einkaufsliste:**")
    for zutat in aktives_rezept['zutaten']:
        st.checkbox(zutat, key=f"z_{zutat}")
with spalte_rechts:
    st.markdown("🟢 **Thermomix-Schritte:**")
    for schritt in aktives_rezept['tm_schritte']:
        st.write(f"- {schritt}")

if ist_doppel_tag and coros_hrv != "Niedrig / Müde":
    st.markdown("---")
    st.subheader("🌙 Nachi-Einheit: Gericht für nach der 2. Session")
    nachmittag_rezept = st.session_state.rezept_datenbank["doppel_schwellen_nachmittag"][0]
    st.markdown(f"**Gericht:** {nachmittag_rezept['titel']}")
    for schritt in nachmittag_rezept['tm_schritte']:
        st.write(f"- {schritt}")