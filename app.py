import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
from PIL import Image
from io import BytesIO
from sklearn.cluster import KMeans
from utils import get_dominant_color, get_pokemon_image_path, get_pokemon_stats, load_pokemon_data, type_colors

# Charger les données
df = load_pokemon_data()

# Nettoyage du type
df['Type'] = df['Type'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df['Primary Type'] = df['Type'].apply(lambda x: x[0] if isinstance(x, list) else x)

# ---- En-tête ----
left_co, cent_co,last_co = st.columns(3)
with cent_co:
        st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/LeTibs/pokemon/main/Data/Images/logo-Pokemon.jpg
" width="250">
    </div>
    """,
    unsafe_allow_html=True
        )
# ---- En-tête et Cartes de Statistiques ----
st.markdown(
    """
    <style>
    .stat-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        font-size: 18px;
        font-weight: bold;
        margin: 10px;
    }
    .stat-number {
        font-size: 24px;
        color: #007BFF;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div>Total Pokémon</div>
        <div class="stat-number">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div>Moyenne Statistique</div>
        <div class="stat-number">{round(df['Moyenne Statistique'].mean(), 2)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div>Top Génération</div>
        <div class="stat-number">{df['Génération'].mode()[0]}</div>
    </div>
    """, unsafe_allow_html=True)


# ---- Filtres ----
st.sidebar.header("Filtres")
gen_filter = st.sidebar.slider("Sélectionner une génération", int(df['Génération'].min()), int(df['Génération'].max()), (1, 9))
type_filter = st.sidebar.multiselect("Sélectionner un type", df['Primary Type'].unique(), default=df['Primary Type'].unique())

# Filtrage des données
filtered_df = df[(df['Génération'].between(*gen_filter)) & (df['Primary Type'].isin(type_filter))]
st.markdown("<br><br>", unsafe_allow_html=True)  # Ajoute un espace vertical


# ---- Graphique d'évolution des stats des types par génération ----
st.subheader("Évolution des Stats Totales des Pokémon par Type et Génération")

# 📌 Transformer la colonne Type (qui contient ['Plante', 'Vol']) en lignes séparées
df_exploded = df.explode("Type")

# 📊 Regrouper les stats totales par Génération et Type
stats_by_type_gen = df_exploded.groupby(["Génération", "Type"])["Somme Stats"].sum().reset_index()

# 🎨 Création du graphique avec une ligne par type
fig3 = px.line(stats_by_type_gen, 
               x="Génération", 
               y="Somme Stats", 
               color="Type",  
               markers=True,
               color_discrete_map=type_colors)  # Personnalisation des couleurs

# ✅ Affichage dans Streamlit
st.plotly_chart(fig3)

# ---- Tableau des Pokémon ----
st.subheader("Classement des Pokémon par puissance")
st.dataframe(filtered_df[['Noms', 'Primary Type', 'Somme Stats', 'Génération']].sort_values(by='Somme Stats', ascending=False), height=250)

st.markdown("<br><br>", unsafe_allow_html=True)  # Ajoute un espace vertical

# ---- Histogramme des Types ----
st.subheader("Distribution des Types de Pokémon")

# 📌 Ajouter un slider pour choisir la plage de générations
min_gen, max_gen = int(df["Génération"].min()), int(df["Génération"].max())
selected_range = st.slider("Sélectionner une génération", min_gen, max_gen, (min_gen, max_gen), key="gen_slider")


# 📌 Filtrer le dataframe en fonction des générations sélectionnées
filtered_df = df[(df["Génération"] >= selected_range[0]) & (df["Génération"] <= selected_range[1])]

# 📌 Transformer la colonne Type (qui contient ['Plante', 'Vol']) en lignes séparées
all_types = filtered_df["Type"].explode()

# 📊 Compter les occurrences de chaque type
type_counts = all_types.value_counts().reset_index(name="Nombre de Pokémon")
type_counts.columns = ["Type", "Nombre de Pokémon"]  # Renomme les colonnes pour éviter l'erreur

# 🎨 Création du graphique interactif avec infobulles
fig2 = px.bar(type_counts, 
              x="Type", 
              y="Nombre de Pokémon", 
              text="Nombre de Pokémon",  # Afficher le nombre sur les barres
              color="Type",
              color_discrete_map=type_colors # Ajoute des couleurs par type
)
              

# ✅ Affichage dans Streamlit
st.plotly_chart(fig2)

st.markdown("<br><br>", unsafe_allow_html=True)  # Ajoute un espace vertical
st.subheader("Comparaison radar chart")



# ---- Comparaison de Pokémon ----
# ---- Création des Colonnes ----
col1, col2, col3 = st.columns([1, 2, 1])  # La colonne centrale est plus large

# ---- Sélection des Pokémon ----
with col1:
    poke1 = st.selectbox("Choisir le premier Pokémon", df['Noms'], index=0)
    poke1_image = get_pokemon_image_path(poke1)
    if poke1_image:
        st.image(poke1_image, caption=poke1, use_container_width=True)
    else:
        st.warning(f"Image introuvable pour {poke1}")

with col3:
    poke2 = st.selectbox("Choisir le second Pokémon", df['Noms'], index=1)
    poke2_image = get_pokemon_image_path(poke2)
    if poke2_image:
        st.image(poke2_image, caption=poke2, use_container_width=True)
    else:
        st.warning(f"Image introuvable pour {poke2}")

# ---- Récupération des statistiques ----

stats1 = get_pokemon_stats(poke1, df)
stats2 = get_pokemon_stats(poke2, df)

# ---- Création du Radar Chart ----
labels = ['PV', 'Attaque', 'Attaque Spéciale', 'Défense', 'Défense Spéciale', 'Vitesse']
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
stats1 = np.concatenate((stats1, [stats1[0]]))
stats2 = np.concatenate((stats2, [stats2[0]]))
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

color1 = get_dominant_color(poke1, k=4, threshold=50)
color2 = get_dominant_color(poke2, k=4, threshold=50)


ax.fill(angles, stats1, color= color1, alpha=0.3, label=poke1)
ax.fill(angles, stats2, color= color2, alpha=0.3, label=poke2)
ax.plot(angles, stats1, color= color1, linewidth=2)
ax.plot(angles, stats2, color= color2, linewidth=2)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

# Déplacer la légende en haut du radar
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False, columnspacing =2)

# ---- Affichage du Radar Chart dans la colonne du milieu ----
with col2:
    st.pyplot(fig)




# ---- Treemap ----
# 📸 Ajouter une colonne "Image" avec les chemins réels des images
# 🔸 1. Créer les colonnes "Nombre de Types" et "Stats Normalisées"
df["Nombre de Types"] = df["Type"].apply(len)
df["Stats Normalisées"] = df["Somme Stats"] / df["Nombre de Types"]

# 🔸 3. Exploser les types (après toutes les colonnes calculées)
df_exploded = df.explode("Type")

# 🔸 4. Créer le label HTML (image + stats)
# 🔹 1️⃣ Créer un label HTML avec les stats formatées
df_exploded["Label Stats"] = df_exploded.apply(lambda row: 
    f"<b>{row['Noms']}</b><br>"  # Nom du Pokémon en gras
    f"❤️ PV: {row['PV']} | ⚔️ Attaque: {row['Attaque']}<br>"  # PV et Attaque
    f"🛡️ Défense: {row['Défense']} | 🌀 Att Spé: {row['Attaque Spéciale']}<br>"  # Défense et Attaque Spéciale
    f"🛡️ Déf Spé: {row['Défense Spéciale']} | ⚡ Vit: {row['Vitesse']}", 
    axis=1
)

# 🔹 2️⃣ Créer le Treemap avec les stats affichées
fig_treemap = px.treemap(
    df_exploded, 
    path=['Génération', 'Type', 'Label Stats'],  # Utiliser le label avec stats
    values="Stats Normalisées",
    color="Type",
    color_discrete_map=type_colors
)

# 🔹 3️⃣ S'assurer que le texte des cases affiche bien les stats
fig_treemap.update_traces(textinfo="label")

# 🔹 4️⃣ Afficher le Treemap dans Streamlit
st.plotly_chart(fig_treemap)





