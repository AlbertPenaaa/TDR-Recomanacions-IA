import pandas as pd
from scipy.sparse import coo_matrix
import implicit
import pickle

# --- 1. Preparació de les Dades ---
# 1.1. Carregar el fitxer CSV
# Hem afegit 'header=1' i 'usecols' per solucionar el problema de les columnes buides a l'inici del teu CSV.
df = pd.read_csv('dades_compra.csv', header=1, usecols=['user_id', 'item_id', 'valoracio'])

# 1.2. Mapejar IDs a valors numèrics (essencial per a l'algorisme)
df['user_id'] = df['user_id'].astype("category")
df['item_id'] = df['item_id'].astype("category")

# 1.3. Creació de la Matriu de Productes (Sparse Matrix)
sparse_item_user = coo_matrix((df['valoracio'].astype(float),
                                (df['item_id'].cat.codes,
                                 df['user_id'].cat.codes)))


# --- 2. Entrenament del Model ---
# 2.1. Definició de l'Algorisme: Alternating Least Squares (ALS)
model = implicit.als.AlternatingLeastSquares(factors=50, iterations=100)

# 2.2. Execució de l'Entrenament
print("Iniciant l'entrenament de l'algorisme ALS...") 
model.fit(sparse_item_user) 
print("Entrenament completat amb èxit.")


# --- 3. Guardar el Model (El Cervell) ---
data_to_save = {
    'model': model,
    'df': df,
    'item_reverse_map': dict(zip(df['item_id'], df['item_id'].cat.codes)),
    'item_map': dict(zip(df['item_id'].cat.codes, df['item_id']))
}

model_filename = 'algoritme_ia_final.pkl'
with open(model_filename, 'wb') as file:
    pickle.dump(data_to_save, file)

print(f"Model guardat amb èxit com a: {model_filename}")