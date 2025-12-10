import flask
from flask import request, jsonify
from flask_cors import CORS

# --- 1. Configuració de l'API ---
app = flask.Flask(__name__)
CORS(app) 

# --- 2. Dades de Personalització Final (SOLUCIÓ AL PROBLEMA 2) ---
RECOMANACIONS_PERSONALITZADES = {
    # CLAU: SLUG del producte que es mira
    # VALOR: Llista de 4 SLUGS que es recomanen
    "excellent-encyclopedia": ["litre-of-longevity", "nas-de-pallasso-classic", "fancy-folder", "targetes-de-reptes-divertits"],
    "litre-of-longevity": ["excellent-encyclopedia", "nas-de-pallasso-classic", "bottle-of-bliss", "spacious-sachet"],
    "nas-de-pallasso-classic": ["excellent-encyclopedia", "litre-of-longevity", "beneficial-book", "mitjons-divertits-amb-emoticones-de-riure"],
    "pilota-antiestres-en-forma-de-cor": ["pilota-antiestres-de-colors", "coixi-relaxant-amb-frases-positives", "llibreta-amb-frases-motivadores", "trencaclosques-humoristic-amb-caricatures"],
    "cartes-de-bromes-innocents": ["targetes-de-reptes-divertits", "daus-de-bromes-rapides", "joc-de-tauler-el-riure-contagios", "samarreta-amb-dibuix-humoristic"],
    "targetes-de-reptes-divertits": ["cartes-de-bromes-innocents", "kit-de-jocs-rapids-per-a-festes", "joc-de-mimica-fes-riure-sense-parlar", "samarreta-el-riure-es-el-meu-superpoder"],
    "joc-de-tauler-el-riure-contagios": ["joc-de-taula-endevina-l-acudit", "joc-de-cartes-d-acudits", "trencaclosques-humoristic-amb-caricatures", "col-leccio-d-acudits-dolents-pack"],
    "joc-de-taula-endevina-l-acudit": ["joc-de-tauler-el-riure-contagios", "joc-de-cartes-d-acudits", "daus-de-bromes-rapides", "cartes-de-bromes-innocents"],
    "joc-de-cartes-d-acudits": ["joc-de-tauler-el-riure-contagios", "joc-de-taula-endevina-l-acudit", "imant-de-nevera-amb-acudits", "col-leccio-d-acudits-dolents-pack"],
    "imant-de-nevera-amb-acudits": ["joc-de-cartes-d-acudits", "llibreta-amb-frases-motivadores", "tassa-amb-acudit-breu", "boligraf-amb-acudit-incorporat"],
    "mitjons-divertits-amb-emoticones-de-riure": ["samarreta-amb-dibuix-humoristic", "samarreta-el-riure-es-el-meu-superpoder", "bossa-de-roba-emporta-m-de-rialles", "coixi-petit-amb-cara-riallera"],
    "llibreta-amb-frases-motivadores": ["tassa-amb-missatge-positiu-avui-sera-un-gran-dia", "boligraf-amb-acudit-incorporat", "imant-de-nevera-amb-acudits", "coixi-relaxant-amb-frases-positives"],
    "boligraf-amb-acudit-incorporat": ["llibreta-amb-frases-motivadores", "imant-de-nevera-amb-acudits", "tassa-amb-acudit-breu", "clauer-amb-mini-cares-somrients"],
    "bossa-de-roba-emporta-m-de-rialles": ["samarreta-amb-dibuix-humoristic", "samarreta-el-riure-es-el-meu-superpoder", "mitjons-divertits-amb-emoticones-de-riure", "ampolla-reutilitzable-amb-frases-divertides"],
    "clauer-amb-mini-cares-somrients": ["boligraf-amb-acudit-incorporat", "coixi-petit-amb-cara-riallera", "llibreta-amb-frases-motivadores", "pilota-antiestres-en-forma-de-cor"],
    "coixi-petit-amb-cara-riallera": ["clauer-amb-mini-cares-somrients", "coixi-relaxant-amb-frases-positives", "pack-sorpresa-somriu-avui", "mitjons-divertits-amb-emoticones-de-riure"],
    "bottle-of-bliss": ["litre-of-longevity", "excellent-encyclopedia", "fancy-folder", "spacious-sachet"],
    "beneficial-book": ["excellent-encyclopedia", "litre-of-longevity", "spacious-sachet", "pack-of-popcorn"],
    "pilota-antiestres-de-colors": ["pilota-antiestres-en-forma-de-cor", "coixi-relaxant-amb-frases-positives", "pack-sorpresa-relax-expres", "pack-sorpresa-somriu-avui"],
    "coixi-relaxant-amb-frases-positives": ["pilota-antiestres-en-forma-de-cor", "pilota-antiestres-de-colors", "pack-sorpresa-relax-expres", "llibreta-amb-frases-motivadores"],
    "pack-sorpresa-relax-expres": ["coixi-relaxant-amb-frases-positives", "pack-sorpresa-somriu-avui", "pack-sorpresa-risoterapia-total", "pilota-antiestres-de-colors"],
    "pack-sorpresa-somriu-avui": ["pack-sorpresa-relax-expres", "pack-sorpresa-risoterapia-total", "tassa-amb-missatge-positiu-avui-sera-un-gran-dia", "clauer-amb-mini-cares-somrients"],
    "pack-sorpresa-risoterapia-total": ["pack-sorpresa-somriu-avui", "pack-sorpresa-relax-expres", "tassa-amb-missatge-positiu-avui-sera-un-gran-dia", "ampolla-reutilitzable-amb-frases-divertides"],
    "tassa-amb-missatge-positiu-avui-sera-un-gran-dia": ["tassa-amb-acudit-breu", "llibreta-amb-frases-motivadores", "ampolla-reutilitzable-amb-frases-divertides", "pack-sorpresa-somriu-avui"],
    "tassa-amb-acudit-breu": ["tassa-amb-missatge-positiu-avui-sera-un-gran-dia", "boligraf-amb-acudit-incorporat", "imant-de-nevera-amb-acudits", "ampolla-reutilitzable-amb-frases-divertides"],
    "ampolla-reutilitzable-amb-frases-divertides": ["tassa-amb-missatge-positiu-avui-sera-un-gran-dia", "tassa-amb-acudit-breu", "bossa-de-roba-emporta-m-de-rialles", "pack-d-adhesius-divertits"],
    "samarreta-amb-dibuix-humoristic": ["samarreta-el-riure-es-el-meu-superpoder", "mitjons-divertits-amb-emoticones-de-riure", "bossa-de-roba-emporta-m-de-rialles", "pack-d-adhesius-divertits"],
    "spacious-sachet": ["excellent-encyclopedia", "litre-of-longevity", "pack-of-popcorn", "fancy-folder"],
    "pack-of-popcorn": ["spacious-sachet", "beneficial-book", "bottle-of-bliss", "fancy-folder"],
    "fancy-folder": ["bottle-of-bliss", "spacious-sachet", "excellent-encyclopedia", "pack-of-popcorn"],
    "kit-de-jocs-rapids-per-a-festes": ["daus-de-bromes-rapides", "cartes-de-bromes-innocents", "joc-de-tauler-el-riure-contagios", "globus-amb-frases-divertides-pack-de-10"],
    "pack-d-adhesius-divertits": ["llibreta-amb-frases-motivadores", "ampolla-reutilitzable-amb-frases-divertides", "samarreta-amb-dibuix-humoristic", "diadema-amb-antenes-flexibles"],
    "diadema-amb-antenes-flexibles": ["pack-d-adhesius-divertits", "globus-amb-frases-divertides-pack-de-10", "spacious-sachet", "pack-of-popcorn"],
    "samarreta-el-riure-es-el-meu-superpoder": ["samarreta-amb-dibuix-humoristic", "mitjons-divertits-amb-emoticones-de-riure", "bossa-de-roba-emporta-m-de-rialles", "ampolla-reutilitzable-amb-frases-divertides"],
    "globus-amb-frases-divertides-pack-de-10": ["diadema-amb-antenes-flexibles", "kit-de-jocs-rapids-per-a-festes", "pack-d-adhesius-divertits", "trencaclosques-humoristic-amb-caricatures"],
    "daus-de-bromes-rapides": ["cartes-de-bromes-innocents", "targetes-de-reptes-divertits", "kit-de-jocs-rapids-per-a-festes", "joc-de-tauler-el-riure-contagios"],
    "trencaclosques-humoristic-amb-caricatures": ["joc-de-tauler-el-riure-contagios", "joc-de-mimica-fes-riure-sense-parlar", "globus-amb-frases-divertides-pack-de-10", "pack-d-adhesius-divertits"],
    "joc-de-mimica-fes-riure-sense-parlar": ["targetes-de-reptes-divertits", "trencaclosques-humoristic-amb-caricatures", "kit-de-jocs-rapids-per-a-festes", "daus-de-bromes-rapides"],
    "col-leccio-d-acudits-dolents-pack": ["joc-de-cartes-d-acudits", "joc-de-tauler-el-riure-contagios", "imant-de-nevera-amb-acudits", "llibreta-amb-frases-motivadores"],
    
    # PRODUCTES NO LLISTATS AQUÍ O EN CAS D'ERROR, MOSTRA UN DEFAULT SEGUR
    "default-producte": ["excellent-encyclopedia", "llibreta-amb-frases-motivadores", "samarreta-amb-dibuix-humoristic", "pilota-antiestres-de-colors"]
}

# TAULA DE NOMS REALS (SOLUCIÓ AL PROBLEMA 3a)
SLUG_A_NOM_REAL = {
    "excellent-encyclopedia": "Ulleres amb nas de pallaso", "litre-of-longevity": "Nas de pallaso amb llum LED",
    "nas-de-pallasso-classic": "Nas de pallaso clàssic", "pilota-antiestres-en-forma-de-cor": "Pilota antiestrès en forma de cor",
    "cartes-de-bromes-innocents": "Cartas de \"bromes inocentes\"", "targetes-de-reptes-divertits": "Targetes de reptes divertits",
    "joc-de-tauler-el-riure-contagios": "Joc de tauler “El riure contagiós", "joc-de-taula-endevina-l-acudit": "Joc de taula \"Endevina l'acudit\"",
    "joc-de-cartes-d-acudits": "Joc de cartes d’acudits", "imant-de-nevera-amb-acudits": "Imant de nevera con acudits",
    "mitjons-divertits-amb-emoticones-de-riure": "Mitjons divertits amb emoticones de riure", "llibreta-amb-frases-motivadores": "Llibreta amb frases motivadores",
    "boligraf-amb-acudit-incorporat": "Bolígraf amb acudit incorporat", "bossa-de-roba-emporta-m-de-rialles": "Bossa de roba \"Emporta'm de rialles\"",
    "clauer-amb-mini-cares-somrients": "Clauer amb mini cares somrients", "coixi-petit-amb-cara-riallera": "Coixí petit con cara riallera",
    "bottle-of-bliss": "Corbata amb llums LED", "beneficial-book": "Ulleres gegants de colors",
    "pilota-antiestres-de-colors": "Pilota antiestrès de colores", "coixi-relaxant-amb-frases-positives": "Coixí relaxant amb frases positives",
    "pack-sorpresa-relax-expres": "Pack sorpresa “Relax Exprés”", "pack-sorpresa-somriu-avui": "Pack sorpresa \"Somriu Avui\"",
    "pack-sorpresa-risoterapia-total": "Pack sorpresa \"Risoteràpia Total\"", "tassa-amb-missatge-positiu-avui-sera-un-gran-dia": "Tassa amb missatge positiu",
    "tassa-amb-acudit-breu": "Tassa amb acudit breu", "ampolla-reutilitzable-amb-frases-divertides": "Ampolla reutilitzable amb frases divertides",
    "samarreta-amb-dibuix-humoristic": "Samarreta amb dibuix humorístic", "spacious-sachet": "Barret de pallasso multicolor",
    "pack-of-popcorn": "Perruca de colores", "fancy-folder": "Pajarita gegant",
    "kit-de-jocs-rapids-per-a-festes": "Kit de jocs ràpids per a festes", "pack-d-adhesius-divertits": "Pack d'adhesius divertits",
    "diadema-amb-antenes-flexibles": "Diadema amb antenes flexibles", "samarreta-el-riure-es-el-meu-superpoder": "Samarreta \"El riure és el meu superpoder\"",
    "globus-amb-frases-divertides-pack-de-10": "Globus amb frases divertides (pack de 10)", "daus-de-bromes-rapides": "Daus de bromes ràpides",
    "trencaclosques-humoristic-amb-caricatures": "Trencaclosques humorístic", "joc-de-mimica-fes-riure-sense-parlar": "Joc de mímica",
    "col-leccio-d-acudits-dolents-pack": "Col·lecció d’acudits dolents"
}

# --- 3. La Ruta de Recomanació (Endpoint) ---
@app.route('/api/recomana', methods=['GET'])
def recomana():
    producte_slug = request.args.get('producte') 
    
    # 3.1. Busquem les recomanacions personalitzades
    # Si no troba l'SLUG, retorna el default.
    recomanacions_slugs = RECOMANACIONS_PERSONALITZADES.get(producte_slug, RECOMANACIONS_PERSONALITZADES["default-producte"])

    try:
        # 3.2. Afegim el NOM REAL a la resposta per al JavaScript
        recomanacions_finals = []
        for slug in recomanacions_slugs:
            nom_real = SLUG_A_NOM_REAL.get(slug, slug) # Si no troba el nom real, usa l'slug
            recomanacions_finals.append({"id": slug, "nom": nom_real}) 

        return jsonify({"recomanacions": recomanacions_finals})

    except Exception as e:
        return jsonify({"error": "Error intern de l'API (Simulació Personalitzada): " + str(e)}), 500


# Executar l'API (això Render ho ignora)
if __name__ == '__main__':
    app.run(debug=True)