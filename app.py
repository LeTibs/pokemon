import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import os

# Charger les données
file_path = "Data/pokemon_all_gen.csv"
df = pd.read_csv(file_path)

# Nettoyage du type
df['Type'] = df['Type'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df['Primary Type'] = df['Type'].apply(lambda x: x[0] if isinstance(x, list) else x)

# ---- En-tête ----
left_co, cent_co,last_co = st.columns(3)
with cent_co:
        st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://github.com/LeTibs/pokemon/blob/main/Data/Images/logo-Pokemon.jpg" width="250">
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

# ---- Scatter Plot ----
st.subheader("Répartition des Pokémon par Type et Puissance")
fig1 = px.scatter(filtered_df, x='Noms', y='Somme Stats', color='Primary Type', size='Somme Stats', title="Puissance des Pokémon")
st.plotly_chart(fig1)

# ---- Tableau des Pokémon ----
st.subheader("Classement des Pokémon par puissance")
st.dataframe(filtered_df[['Noms', 'Primary Type', 'Somme Stats', 'Génération']].sort_values(by='Somme Stats', ascending=False))

# ---- Histogramme des Types ----
st.subheader("Distribution des Types de Pokémon")
type_counts = df['Primary Type'].value_counts()
fig2, ax = plt.subplots()
type_counts.plot(kind='bar', ax=ax, color='skyblue')
st.pyplot(fig2)

# ---- Comparaison de Pokémon ----

image_folder = "Data/Images"
image_extensions = [".png", ".jpg", ".jpeg", ".webp"]

def get_pokemon_image_path(pokemon_name):
    """Retourne le chemin de l'image du Pokémon si elle existe, sinon None."""
    for ext in image_extensions:
        path = os.path.join(image_folder, f"{pokemon_name}{ext}")  # Conserve la majuscule
        if os.path.exists(path):
            return path
    return None

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
def get_pokemon_stats(name):
    return df[df['Noms'] == name][['PV', 'Attaque', 'Attaque Spéciale', 'Défense', 'Défense Spéciale', 'Vitesse']].values.flatten()

stats1 = get_pokemon_stats(poke1)
stats2 = get_pokemon_stats(poke2)

# ---- Création du Radar Chart ----
labels = ['PV', 'Attaque', 'Attaque Spéciale', 'Défense', 'Défense Spéciale', 'Vitesse']
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
stats1 = np.concatenate((stats1, [stats1[0]]))
stats2 = np.concatenate((stats2, [stats2[0]]))
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

ax.fill(angles, stats1, alpha=0.3, label=poke1)
ax.fill(angles, stats2, alpha=0.3, label=poke2)
ax.plot(angles, stats1, linewidth=2)
ax.plot(angles, stats2, linewidth=2)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

# Déplacer la légende en haut du radar
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False, columnspacing =2)

# ---- Affichage du Radar Chart dans la colonne du milieu ----
with col2:
    st.pyplot(fig)

# ---- Treemap ----
st.subheader("Treemap des Pokémon")
# 📸 Ajouter une colonne "Image" avec les chemins réels des images
df["Image"] = df["Noms"].apply(lambda x: get_pokemon_image_path(x))

# 🏆 Création du Treemap avec les images en `customdata`
fig4 = px.treemap(
    df, 
    path=['Génération', 'Primary Type', 'Noms'], 
    values='Somme Stats', 
    title="Répartition des Pokémon par Génération et Type",
    custom_data=['Image']  # Associe l’image à chaque Pokémon
)

# 🎨 Affichage des images au survol (si elles existent)
fig4.update_traces(
    hovertemplate="<b>%{label}</b><br><img src='%{customdata[0]}' width='50'>" 
)

# 📊 Affichage du graphique
st.plotly_chart(fig4)
