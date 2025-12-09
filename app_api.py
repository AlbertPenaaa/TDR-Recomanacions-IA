import flask
from flask import request, jsonify
# Ja no cal importar 'os', 'pickle', 'pandas', ni 'implicit'

# --- 1. Configuració de l'API ---
app = flask.Flask(__name__)

# --- 2. Dades Fictícies (Simulació de Recomanació) ---
# Aquesta llista simula les recomanacions que hauria de donar el teu model
RECOMANACIONS_FICTICIES = [
    {"id": "Risoterapia_Grup"},
    {"id": "Sessio_Individual"},
    {"id": "Xerrada_Gesti"},
    {"id": "Taller_Equips"}
]

# --- 3. La Ruta de Recomanació (Endpoint) ---
@app.route('/api/recomana', methods=['GET'])
def recomana():
    # 3.1. Rebre la petició (Només per complir el format)
    producte_actual_id = request.args.get('producte') 

    if not producte_actual_id:
        return jsonify({"error": "Producte no especificat"}), 400

    try:
        # 3.2. Retorna les recomanacions Fictícies
        # Sempre tornem el mateix, simulant que l'IA funciona
        return jsonify({"recomanacions": RECOMANACIONS_FICTICIES})

    except Exception as e:
        return jsonify({"error": "Error intern de l'API fictícia: " + str(e)}), 500

# Executar l'API per a proves locals
if __name__ == '__main__':
    app.run(debug=True)