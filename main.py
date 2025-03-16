import requests
from bs4 import BeautifulSoup

# URL de la page Poképédia
url = "https://www.pokepedia.fr/Liste_des_Pokémon_de_la_première_génération"

# Récupérer le contenu HTML de la page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Trouver le tableau contenant la liste des Pokémon
table = soup.find("table", class_="tableaustandard")

# Vérifier que le tableau est trouvé
if table:
    # Trouver toutes les lignes du tableau
    rows = table.find_all("tr")[1:]  # On saute la première ligne qui contient les en-têtes

    pokemon_names = []
    
    pokemon_types = []

    for row in rows:
        # Trouver toutes les cellules <td> dans la ligne
        cells = row.find_all("td")

        if cells:
            # Le nom du Pokémon est dans la deuxième colonne (index 2)
            name_tag = cells[2].find("a")  # Prendre le <a> qui contient le nom du Pokémon
            if name_tag:
                pokemon_names.append(name_tag.text)
            
            types_tag = cells[7].find_all("span")

            types = []
            for type_tag in types_tag:
               
               a_tag

            pokemon_types.append(types)




    #Afficher les noms des Pokémon
    for name in pokemon_names:
        print(name)

    for types in pokemon_types:
        print(types)

else:
    print("Tableau non trouvé. La structure de la page a peut-être changé.")

