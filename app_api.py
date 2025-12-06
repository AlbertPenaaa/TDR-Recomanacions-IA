import flask
from flask import request, jsonify
import pickle
import pandas as pd
from implicit.utils import check_blas_config # Per eliminar warnings

check_blas_config() 

# --- 1. Configuració de l'API ---
app = flask.Flask(__name__)

# --- 2. Carregar el Cervell de la IA (model.pkl) ---
try:
    with open('algoritme_ia_final.pkl', 'rb') as file:
        data_to_save = pickle.load(file)
        model = data_to_save['model']
        item_reverse_map = data_to_save['item_reverse_map']
        item_map = data_to_save['item_map']
        
        print("Model d'IA carregat amb èxit.")
except Exception as e:
    print(f"Error carregant el model: {e}")
    model = None 


# --- 3. La Ruta de Recomanació (Endpoint) ---
@app.route('/api/recomana', methods=['GET'])
def recomana():
    # 3.1. Rebre la petició
    producte_actual_id = request.args.get('producte') 

    if not model or not producte_actual_id:
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