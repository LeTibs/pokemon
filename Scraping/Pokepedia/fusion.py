import pandas as pd

pokemon_all_gen = pd.read_csv("Data/pokemon_gen1.csv")
for i in range(2,10):
    df =pd.read_csv(f"Data/pokemon_gen{i}.csv")
    pokemon_all_gen= pd.concat([pokemon_all_gen, df], ignore_index=True)

print(pokemon_all_gen.info())

pokemon_all_gen.to_csv("pokemon_all_gen.csv", encoding="utf-8")