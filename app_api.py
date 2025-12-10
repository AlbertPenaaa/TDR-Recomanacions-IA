import flask
from flask import request, jsonify
from flask_cors import CORS

# --- 1. Configuració de l'API ---
app = flask.Flask(__name__)
CORS(app) # Permet la connexió des de Webnode

# --- 2. Simuació de Grups (RECOMANACIONS PERSONALITZADES) ---
# Hem de definir quins productes reben quines recomanacions (Usant SLUGS reals)

RECOMANACIONS_PER_GRUP = {
    # GRUP 1: Productes d'Accessoris de Pallasso/Disfressa
    "PALLASSO": ["litre-of-longevity", "nas-de-pallasso-classic", "barret-de-pallasso-multicolor", "ulleres-gegants-de-colors"],
    # GRUP 2: Productes de Relaxació/Anti-Estrès
    "RELAX": ["coixi-relaxant-amb-frases-positives", "pack-sorpresa-relax-expres", "llibreta-amb-frases-motivadores", "pilota-antiestres-de-colors"],
    # GRUP 3: Productes de Jocs/Cartes
    "JOCS": ["targetes-de-reptes-divertits", "daus-de-bromes-rapides", "joc-de-tauler-el-riure-contagios", "kit-de-jocs-rapids-per-a-festes"],
    # GRUP 4: Productes de Roba/Accessoris Personalitzats
    "ROBA": ["samarreta-el-riure-es-el-meu-superpoder", "mitjons-divertits-amb-emoticones-de-riure", "bossa-de-roba-emporta-m-de-rialles", "tassa-amb-missatge-positiu-avui-sera-un-gran-dia"],
    # DEFAULT: Si un producte no està definit (Tasses, Clauers, etc.), surten aquests 4
    "DEFAULT": ["coixi-petit-amb-cara-riallera", "llibreta-amb-frases-motivadores", "tassa-amb-acudit-breu", "pack-sorpresa-somriu-avui"]
}

# MAPEIIG: A quin grup pertany cada SLUG (Això ens diu quines recomanacions ha de donar)
PRODUCTE_A_GRUP = {
    # PALLASSO
    "excellent-encyclopedia": "PALLASSO", "litre-of-longevity": "PALLASSO", "nas-de-pallasso-classic": "PALLASSO", 
    "bottle-of-bliss": "PALLASSO", "beneficial-book": "PALLASSO", "spacious-sachet": "PALLASSO", 
    "pack-of-popcorn": "PALLASSO", "fancy-folder": "PALLASSO",

    # RELAX
    "pilota-antiestres-en-forma-de-cor": "RELAX", "coixi-relaxant-amb-frases-positives": "RELAX", 
    "pack-sorpresa-relax-expres": "RELAX", "pilota-antiestres-de-colors": "RELAX",

    # JOCS
    "cartes-de-bromes-innocents": "JOCS", "joc-de-tauler-el-riure-contagios": "JOCS", "daus-de-bromes-rapides": "JOCS",
    "kit-de-jocs-rapids-per-a-festes": "JOCS", "targetes-de-reptes-divertits": "JOCS",
    "joc-de-taula-endevina-l-acudit": "JOCS", "joc-de-cartes-d-acudits": "JOCS", 
    "trencaclosques-humoristic-amb-caricatures": "JOCS", "joc-de-mimica-fes-riure-sense-parlar": "JOCS",
    "col-leccio-d-acudits-dolents-pack": "JOCS",

    # ROBA
    "samarreta-amb-dibuix-humoristic": "ROBA", "samarreta-el-riure-es-el-meu-superpoder": "ROBA", 
    "mitjons-divertits-amb-emoticones-de-riure": "ROBA", "bossa-de-roba-emporta-m-de-rialles": "ROBA",
    
    # PRODUCTES NO LLISTATS AQUÍ ANIRAN AL GRUP DEFAULT
}

# --- 3. La Ruta de Recomanació (Endpoint) ---
@app.route('/api/recomana', methods=['GET'])
def recomana():
    # 3.1. Obtenim l'SLUG del producte que ens arriba des de Webnode
    producte_slug = request.args.get('producte') 

    if not producte_slug:
        return jsonify({"error": "Producte no especificat"}), 400

    try:
        # 3.2. Busquem a quin grup pertany
        grup = PRODUCTE_A_GRUP.get(producte_slug, "DEFAULT")
        
        # 3.3. Obtenim les 4 IDs (SLUGS) de recomanació d'aquell grup
        recomanacions_slugs = RECOMANACIONS_PER_GRUP.get(grup)

        # 3.4. Preparem el format final per a Webnode
        recomanacions_finals = [{"id": slug} for slug in recomanacions_slugs]

        return jsonify({"recomanacions": recomanacions_finals})

    except Exception as e:
        return jsonify({"error": "Error intern de l'API (Simulació): " + str(e)}), 500