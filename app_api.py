import flask
from flask import request, jsonify
from flask_cors import CORS # <-- NOVA LLIBRERIA NECESSÀRIA
# Ja no cal importar res més.

# --- 1. Configuració de l'API ---
app = flask.Flask(__name__)
CORS(app) # <-- AQUESTA LÍNIA SOLUCIONA EL BLOQUEIG DE WEBNODE!

# --- 2. Dades Fictícies (Simulació de Recomanació) ---
RECOMANACIONS_FICTICIES = [
    {"id": "Risoterapia_Grup"},
    {"id": "Sessio_Individual"},
    {"id": "Xerrada_Gesti"},
    {"id": "Taller_Equips"}
]

# --- 3. La Ruta de Recomanació (Endpoint) ---
@app.route('/api/recomana', methods=['GET'])
def recomana():
    producte_actual_id = request.args.get('producte') 

    if not producte_actual_id:
        return jsonify({"error": "Producte no especificat"}), 400

    try:
        # 3.2. Retorna les recomanacions Fictícies
        return jsonify({"recomanacions": RECOMANACIONS_FICTICIES})

    except Exception as e:
        return jsonify({"error": "Error intern de l'API fictícia: " + str(e)}), 500

# Executar l'API per a proves locals
if __name__ == '__main__':
    app.run(debug=True)