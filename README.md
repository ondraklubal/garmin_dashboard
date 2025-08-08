--- CZ ---
# 📊 Garmin Dashboard

Tato aplikace slouží k vizualizaci sportovních aktivit stažených z Garmin Connect. Umožňuje sledovat vývoj výkonů v čase, procházet podrobné statistiky jednotlivých sportů a zobrazovat mapy tras.

## 🧩 Funkce

- Přihlášení do Garmin Connect API
- Načtení posledních 1000 aktivit
- Filtrace dle sportu a časového období
- Výpočet celkových statistik (vzdálenost, čas, kalorie)
- Vizualizace kilometrů po týdnech
- Zobrazení tabulky aktivit s tempem, délkou, tepem atd.
- Mapa trasy vybrané aktivity
- Automatické rozpoznání typu sportu do kategorií (běh, kolo, plavání atd.)

## 🏃‍♂️ Podporované sporty

Aplikace seskupuje aktivity do následujících skupin:

- Běh (včetně běžeckého pásu, trailového běhu)
- Cyklistika (silniční, gravel, indoor)
- Plavání (bazén, otevřená voda)
- Turistika a chůze
- Silový trénink
- Ostatní


## 🛠️ Spuštění lokálně


git clone https://github.com/your-username/garmin-dashboard.git
cd garmin-dashboard

nainstalujte závislosti:
pip install -r requirements.txt

do kódu si přidejte (nikdy nesdílejte veřejně):
mail=vas-email@example.com
pwd=vaseGarminHeslo

spusťte lokálně přes terminál:
streamlit run app.py


# 📊 Garmin Dashboard

This Streamlit application visualizes your Garmin Connect sports activities. It helps you monitor your performance over time, view detailed stats by sport type, and display route maps for individual activities.

---

## 🧩 Features

- Secure login to Garmin Connect API
- Load up to 1000 past activities
- Filter by activity type and date range
- Summary metrics: distance, duration, calories
- Weekly activity trend chart
- Table view with pace, duration, HR, and calories
- Interactive map with route preview
- Smart grouping of activities (e.g. indoor cycling, gravel cycling → Cycling)

---

## 🏃‍♂️ Supported Sport Groups

Activities are grouped into these sport categories:

- **Running** – road, treadmill, trail
- **Cycling** – road, gravel, indoor
- **Swimming** – pool, open water
- **Hiking/Walking**
- **Strength Training**
- **Other** – anything not covered above

---

## 🛠️ Setup & Run Locally


```bash
git clone https://github.com/your-username/garmin-dashboard.git
cd garmin-dashboard

install dependencies:
pip install -r requirements.txt

add to your code (never share publicly):
mail=your-email@example.com
pwd=yourGarminPassword

run locally via bash:
streamlit run app.py

