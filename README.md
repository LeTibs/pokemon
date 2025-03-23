# 📊 Dashboard Interactif Pokémon - Streamlit App

### 🔗 [Accéder à l'application →](https://pokemon-9urra72uhad4hk4scjltw4.streamlit.app)

---

## 🎯 Objectif du projet

Ce projet a été réalisé dans le cadre de la constitution d’un portfolio personnel, en vue d’intégrer un **Master SID (Science des Données / Informatique Décisionnelle)**.  
L’objectif était de concevoir un **dashboard interactif** autour d’un univers familier (Pokémon), afin de mettre en œuvre :

- 🧼 Du **web scraping** (récupération des données depuis Poképédia)
- 📊 De la **visualisation de données** (avec `Plotly`, `Matplotlib`, `Seaborn`)
- 🧩 Une interface claire et interactive avec **Streamlit**
- 💡 Une structuration modulaire du code (séparation des fonctions dans `poke_utils.py`)

---

## 📦 Données

- Les données ont été **scrapées directement sur Poképédia**, couvrant l’ensemble des générations.
- Chaque Pokémon possède :
  - Nom, types, génération
  - Statistiques complètes (PV, Attaque, Défense, etc.)
  - Somme totale des stats
  - Image associée (hébergée sur GitHub)

---

## 🧭 Fonctionnalités du dashboard

| Fonction | Description |
|---------|-------------|
| 🧬 **Radar Chart** | Compare les statistiques de deux Pokémon sélectionnés |
| 📊 **Histogramme des types** | Visualise la répartition des types (primaires et secondaires) dans un graphe interactif |
| 🥇 **Classement par puissance** | Classe les Pokémon selon leur "Somme Stats", avec filtres possibles |
| 📈 **Évolution temporelle** | Montre l’évolution de la puissance moyenne par type à travers les générations |
| 🌱 **Treemap dynamique** | Vue hiérarchique des Pokémon par génération → type → nom, avec couleur par type |

---

## 📸 Aperçu

![aperçu de l'application](https://github.com/LeTibs/pokemon/raw/main/Assets/Capture_dashboard.png)

---

## 🛠️ Technologies utilisées

- **Python**
- **Streamlit** (frontend)
- **BeautifulSoup / requests** (scraping)
- **Pandas / NumPy** (traitement des données)
- **Plotly & Matplotlib** (visualisation)
- **GitHub + Streamlit Cloud** (déploiement)

---

## 🚀 Lancer l'application en local

```bash
git clone https://github.com/LeTibs/pokemon.git
cd pokemon
pip install -r requirements.txt
streamlit run app.py
# pokemon
