import requests
import pandas as pd
import numpy as np
import cv2
import matplotlib.colors as mcolors
from PIL import Image
from io import BytesIO
from sklearn.cluster import KMeans



#############################################################################
csv_url = "https://raw.githubusercontent.com/LeTibs/pokemon/main/Data/pokemon_all_gen.csv"

def load_pokemon_data():
    """Charge le DataFrame des Pokémon depuis GitHub."""
    return pd.read_csv(csv_url)

##############################################################################
def get_pokemon_stats(name, df):
    return df[df['Noms'] == name][['PV', 'Attaque', 'Attaque Spéciale', 'Défense', 'Défense Spéciale', 'Vitesse']].values.flatten()

##############################################################################


def get_pokemon_image_path(pokemon_name):
    base_url = "https://raw.githubusercontent.com/LeTibs/pokemon/main/Data/Images/"
    return f"{base_url}{pokemon_name}.png"

##############################################################################
def get_dominant_color(pokemon_name, k=4, threshold=50):
    """Télécharge l'image et retourne la couleur dominante en HEX, en excluant les couleurs trop sombres."""
    try:
        # 📥 Télécharger l’image
        response = requests.get(get_pokemon_image_path(pokemon_name))
        if response.status_code != 200:
            return None  # Retourne None si l'image est inaccessible

        # 📸 Ouvrir l’image et la convertir en array NumPy
        img = Image.open(BytesIO(response.content))
        img = img.resize((50, 50))  # Réduction pour optimiser la performance
        img = np.array(img)

        # 🖼 Convertir en RGB (supprimer la transparence si nécessaire)
        if img.shape[-1] == 4:  # RGBA → RGB
            img = img[:, :, :3]

        # 🎨 Transformer en une liste de pixels
        img = img.reshape((-1, 3))

        # 🔍 Filtrer les couleurs très sombres (proches du noir)
        img = np.array([pixel for pixel in img if np.mean(pixel) > threshold])
        if len(img) == 0:
            return "#000000"  # Si toutes les couleurs sont sombres, retourner noir

        # 🎯 Appliquer K-Means Clustering
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(img)

        # 🎨 Sélectionner la couleur la plus fréquente parmi les clusters
        dominant_color = kmeans.cluster_centers_[np.argmax(np.bincount(kmeans.labels_))]

        # 🔵 Convertir en format HEX
        return "#{:02x}{:02x}{:02x}".format(int(dominant_color[0]), int(dominant_color[1]), int(dominant_color[2]))

    except Exception as e:
        print(f"Erreur lors de la récupération de la couleur : {e}")
        return None
    
 ###########################################################################
type_colors = {
    "Eau": "#3899F8",     
    "Feu": "#FF994D",      
    "Plante": "#57B956",   
    "Sol": "#AB7648",      
    "Roche": "#C5B678",    
    "Acier": "#5A8FA3",    
    "Glace": "#73D0C9",    
    "Électrik": "#FBD200", 
    "Dragon": "#006FC9",   
    "Spectre": "#52539C",  
    "Psy": "#FA7175",      
    "Normal": "#A0A29F",   
    "Combat": "#D33927",   
    "Poison": "#B567CE",   
    "Insecte": "#92BC2C", 
    "Vol": "#A0BBE6",      
    "Ténèbres": "#595761",
    "Fée": "#F4BDC9"      
}
