import os # <-- NECESSARI per al canvi de ruta
from flask import request, jsonify
import flask # Cal importar Flask
import pickle
import pandas as pd
from implicit.utils import check_blas_config 

check_blas_config() 

# --- 1. Configuració de l'API ---
app = flask.Flask(__name__)

# --- 2. Carregar el Cervell de la IA (model.pkl) ---

# Aquesta línia utilitza 'os' per construir una ruta ABSOLUTA
# i força el servidor a buscar el fitxer dins del mateix directori de l'script.
pkl_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'algoritme_ia_final.pkl')

try:
    with open(pkl_file_path, 'rb') as file: # <-- S'utilitza la nova variable de ruta
        data_to_save = pickle.load(file)
        model = data_to_save['model']
        item_reverse_map = data_to_save['item_reverse_map']
        item_map = data_to_save['item_map']
        
        print("Model d'IA carregat amb èxit.")
except Exception as e:
    # Aquest 'print' ens dirà als logs de Render si l'error persisteix
    print(f"Error carregant el model: {e}") 
    model = None 


# --- 3. La Ruta de Recomanació (Endpoint) ---
@app.route('/api/recomana', methods=['GET'])
def recomana():
    # 3.1. Rebre la petició
    producte_actual_id = request.args.get('producte') 

    if not model or not producte_actual_id:
        # Aquest error es dispara si el model no es carrega (Error 400)
        return jsonify({"error": "Dades o model no disponibles"}), 400

    try:
        # 3.2. Cerca de Recomanacions
        producte_codi = item_reverse_map.get(producte_actual_id)
        
        if producte_codi is None:
            return jsonify({"error": "Producte desconegut a l'entrenament"}), 404

        # La funció CLAU: el model calcula els 5 ítems més similars
        ids, scores = model.similar_items(producte_codi, N=6) 
        
        # 3.3. Preparació de la Resposta
        resultats_finals = []
        for codi in ids[1:]: 
            item_real = item_map.get(codi)
            
            # EL FILTRE CLAU: Només inclou la recomanació si l'ID es troba al nostre mapa (no és null)
            if item_real is not None:
                resultats_finals.append({"id": item_real})

        # 3.4. Retornar el resultat a Webnode en format JSON
        return jsonify({"recomanacions": resultats_finals})

    except Exception as e:
        return jsonify({"error": "Error intern de l'algorisme: " + str(e)}), 500

# Executar l'API per a proves locals
if __name__ == '__main__':
    app.run(debug=True)