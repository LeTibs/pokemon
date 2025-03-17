import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("Data/pokemon_all_gen.csv")

df = load_data()

# 🎨 Interface Streamlit
st.title("🔍 Analyse des Pokémon : Scraping & Data Viz")
st.sidebar.header("Options de filtre")

# 📌 Extraire tous les types uniques
all_types = sorted(set(t for types in df["Type"] for t in types))  # Liste des types uniques

# 🎯 Sélection d'un type dans la barre latérale
selected_type = st.sidebar.selectbox("Choisir un type", all_types)

# 🎯 Filtrer les Pokémon qui contiennent ce type
filtered_df = df[df["Type"].apply(lambda x: selected_type in x)]

st.subheader(f"Liste des Pokémon de type {selected_type}")
st.dataframe(filtered_df)

# 📊 Visualisation de la répartition des statistiques des Pokémon
st.subheader("📊 Répartition des statistiques des Pokémon")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(filtered_df["Attaque"], bins=20, kde=True, ax=ax)
st.pyplot(fig)