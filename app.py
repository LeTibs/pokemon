import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

# Charger les données
file_path = "Data/pokemon_all_gen.csv"
df = pd.read_csv(file_path)

# Nettoyage du type
df['Type'] = df['Type'].apply(lambda x: eval(x) if isinstance(x, str) else x)
df['Primary Type'] = df['Type'].apply(lambda x: x[0] if isinstance(x, list) else x)

# ---- En-tête ----
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("Data/Images/logo-Pokemon.jpg", width=200)

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
fig1 = px.scatter(filtered_df, x='Names', y='Somme Stats', color='Primary Type', size='Somme Stats', title="Puissance des Pokémon")
st.plotly_chart(fig1)

# ---- Tableau des Pokémon ----
st.subheader("Classement des Pokémon par puissance")
st.dataframe(filtered_df[['Names', 'Primary Type', 'Somme Stats', 'Génération']].sort_values(by='Somme Stats', ascending=False))

# ---- Histogramme des Types ----
st.subheader("Distribution des Types de Pokémon")
type_counts = df['Primary Type'].value_counts()
fig2, ax = plt.subplots()
type_counts.plot(kind='bar', ax=ax, color='skyblue')
st.pyplot(fig2)

# ---- Comparaison de Pokémon ----

# ---- Sélection des Pokémon ----
st.subheader("Comparer deux Pokémon")

col1, col2 = st.columns(2)
with col1:
    poke1 = st.selectbox("Choisir le premier Pokémon", df['Names'], index=0)
with col2:
    poke2 = st.selectbox("Choisir le deuxième Pokémon", df['Names'], index=1)

# ---- Fonction pour récupérer les statistiques ----
def get_pokemon_stats(name):
    stats = df[df['Names'] == name][['PV', 'Attaque', 'Attaque Spéciale', 'Défense', 'Défense Spéciale', 'Vitesse']].values.flatten()
    return stats

# Récupérer les stats des Pokémon sélectionnés
stats1 = get_pokemon_stats(poke1)
stats2 = get_pokemon_stats(poke2)

# ---- Création du Radar Chart ----
labels = ['PV', 'Attaque', 'Attaque Spéciale', 'Défense', 'Défense Spéciale', 'Vitesse']
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
stats1 = np.concatenate((stats1, [stats1[0]]))  # Boucler pour fermer le polygone
stats2 = np.concatenate((stats2, [stats2[0]]))
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

ax.fill(angles, stats1, color="blue", alpha=0.3, label=poke1)
ax.fill(angles, stats2, color="red", alpha=0.3, label=poke2)
ax.plot(angles, stats1, color="blue", linewidth=2)
ax.plot(angles, stats2, color="red", linewidth=2)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))

# Afficher le graphique dans Streamlit
st.pyplot(fig)
# ---- Treemap ----
st.subheader("Treemap des Pokémon")
fig4 = px.treemap(df, path=['Génération', 'Primary Type', 'Names'], values='Somme Stats', title="Répartition des Pokémon par Génération et Type")
st.plotly_chart(fig4)