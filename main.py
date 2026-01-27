import streamlit as st
from jow_api import Jow
import pandas as pd
import traceback
import sqlite3
import json

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Jow Gourmet - Recettes qui donnent faim",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATABASE LOGIC ---
DB_PATH = 'jow_favorites.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_resource
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            ingredients TEXT,
            url TEXT,
            image_url TEXT,
            prepa_time INTEGER,
            cooking_time INTEGER,
            covers INTEGER,
            adaptedFor INTEGER,
            adaptationFactor FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Add image_url column if it doesn't exist (migration for previous manual edits)
    try:
        c.execute('ALTER TABLE favorites ADD COLUMN image_url TEXT')
    except sqlite3.OperationalError: pass
    try:
        c.execute('ALTER TABLE favorites ADD COLUMN prepa_time INTEGER')
    except sqlite3.OperationalError: pass
    try:
        c.execute('ALTER TABLE favorites ADD COLUMN cooking_time INTEGER')
    except sqlite3.OperationalError: pass
    try:
        c.execute('ALTER TABLE favorites ADD COLUMN covers INTEGER')
    except sqlite3.OperationalError: pass
    
    conn.commit()
    conn.close()

init_db()

def add_favorite(recipe, adaptedFor, adaptationFactor):
    conn = get_db_connection()
    c = conn.cursor()
    # Serialize ingredients
    ings = []
    for ing in getattr(recipe, 'ingredients', []):
        ings.append({
            'name': getattr(ing, 'name', 'Inconnu'),
            'quantity': str(getattr(ing, 'quantity', '')),
            'unit': getattr(ing, 'unit', '')
        })
    
    c.execute(
        """INSERT INTO favorites 
           (name, description, ingredients, url, image_url, prepa_time, cooking_time, covers, adaptedFor, adaptationFactor) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            getattr(recipe, 'name', 'N/A'),
            getattr(recipe, 'description', ''),
            json.dumps(ings),
            getattr(recipe, 'url', ''),
            getattr(recipe, 'imageUrl', ''),
            getattr(recipe, 'preparationTime', 0),
            getattr(recipe, 'cookingTime', 0),
            getattr(recipe, 'coversCount', 0),
            adaptedFor,
            adaptationFactor
        )
    )
    conn.commit()
    conn.close()

def remove_favorite(fav_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM favorites WHERE id = ?", (fav_id,))
    conn.commit()
    conn.close()


def adapt_for_nb_people(recipe, nb_personnes=4):
    """Adapte une recette Jow pour exactement 4 personnes"""
    base_covers = getattr(recipe, 'coversCount', 2)
    if base_covers == nb_personnes:
        return recipe  # Déjà bon
    
    # Temps adapté
    extra_time_per_cover = getattr(recipe, 'preparationExtraTimePerCover', 0) if getattr(recipe, 'preparationExtraTimePerCover', 0) != None else 0
   
    recipe.preparationTimeAdapted = recipe.preparationTime + (extra_time_per_cover * (nb_personnes - base_covers))
    
    # Ingrédients x (4/base)
    factor = nb_personnes / base_covers
    for ing in getattr(recipe, 'ingredients', []):
        if ing.quantity:  # Évite les 0 ou None
            ing.quantityAdapted = ing.quantity * factor
            ing.quantityAdapted = round(ing.quantityAdapted, 1)
    
    recipe.adaptedFor = nb_personnes
    recipe.adaptationFactor = factor
    return recipe


# --- APPETIZING CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #FFF9F0;
    }

    .main {
        background: linear-gradient(135deg, #FFF9F0 0%, #FFF2E0 100%);
    }

    .hero-container {
        padding: 2rem 1rem;
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(255, 75, 43, 0.3);
    }

    .recipe-card {
        background: white;
        border-radius: 15px;
        height: 100%;
        padding: 0;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        border: 1px solid #FFE0C0;
        overflow: hidden;
    }

    .recipe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(255, 75, 43, 0.15);
    }

    .card-content {
        padding: 1.2rem;
    }

    .card-title {
        color: #E65100;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .card-badge {
        display: inline-block;
        background: #FFF3E0;
        color: #E65100;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    
    .ing-list {
        font-size: 0.85rem;
        color: #555;
        padding-left: 20px;
        margin-top: 10px;
        max-height: 150px;
        overflow-y: auto;
        border-top: 1px solid #FFF2E0;
        padding-top: 5px;
    }

    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Grid layout simulation */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAV ---
with st.sidebar:
    st.image("https://jow.fr/favicon.ico", width=40)
    st.title("Jow Gourmet")
    
    # Navigation tabs
    menu = st.segmented_control("Navigation", ["🔍 Recherche", "💖 Mes Favoris"], default="🔍 Recherche", label_visibility="collapsed")
    st.divider()
    if menu == "🔍 Recherche":
        st.markdown("### 🛠️ Filtres")
        query = st.text_input("Ingrédient ou plat", placeholder="ex: lasagnes, saumon...", key="search_query")
        limit = st.slider("Nombre de résultats", 1, 20, 6)
        nb_personnes = st.sidebar.slider("Nombre de personnes", 1, 6, 4)

        search_clicked = st.button("Lancer la recherche", type="primary", width='stretch')
    else:
        st.markdown("### ⚙️ Options")
        if st.button("️ Vider tout", type="secondary", width='stretch'):
            conn = get_db_connection()
            conn.execute("DELETE FROM favorites")
            conn.commit()
            conn.close()
            st.toast("Favoris vidés !")
            st.rerun()

# --- MAIN PAGE ---
if menu == "🔍 Recherche":
    st.markdown("""
        <div class="hero-container">
            <h1 style='margin:0;'>Jow Gourmet 🍕</h1>
            <p style='margin:0; opacity:0.9;'>Trouvez l'inspiration pour votre prochain festin</p>
        </div>
    """, unsafe_allow_html=True)

    if 'search_query' in st.session_state and st.session_state.search_query:
        with st.spinner("👩‍🍳 Recherche en cours..."):
            try:
                recipes = Jow.search(st.session_state.search_query, limit=limit)
                recipes = [adapt_for_nb_people(r, nb_personnes) for r in recipes]
                
                if not recipes:
                    st.warning("Aucune recette trouvée.")
                else:
                    st.success(f"Voici {len(recipes)} recettes pour vous !")
                    
                    # Responsive Grid
                    cols = st.columns(2)
                    for idx, recipe in enumerate(recipes):
                        with cols[idx % 2]:
                            # Get data
                            name = getattr(recipe, 'name', 'Recette sans nom')
                            prepa = getattr(recipe, 'preparationTime', 0)
                            cuisson = getattr(recipe, 'cookingTime', 0)
                            if prepa and cuisson:
                                total = prepa + cuisson
                            else:
                                total = prepa
                            covers = getattr(recipe, 'coversCount', '?')
                            img = getattr(recipe, 'imageUrl', '')
                            ingredients = getattr(recipe, 'ingredients', [])
                            quantity = getattr(recipe, 'quantityAdapted', '?')
                            unit = getattr(recipe, 'unit', '?')
                            
                            # Card UI
                            st.markdown(f"""
                                <div class="recipe-card" style="display: flex; align-items: stretch;">
                                    <img src="{img}" style="width: 50%; object-fit: cover;">
                                    <div class="card-content" style="flex: 1;">
                                        <div class="card-title">{name}</div>
                                        <div class="card-badge">⏱️ {total} min</div>
                                        <div class="card-badge">👥 {recipe.adaptedFor} pers. (Ratio: x{round(recipe.adaptationFactor, 1)})</div>
                                        <div class="card-badge">🔥 {cuisson} min</div>
                                        <ul class="ing-list">
                                            {"".join([f"<li>{i.name} : <b>{i.quantityAdapted} {i.unit}</b></li>" for i in ingredients])}
                                        </ul>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Action Buttons
                            c1, c2, _, _ = st.columns([1, 1, 2, 2])
                            with c1:
                                if st.button(f"⭐ Favoris", key=f"fav_{idx}", width='stretch'):
                                    add_favorite(recipe, recipe.adaptedFor, recipe.adaptationFactor)
                                    st.toast(f"💖 {name} ajouté !")
                            with c2:
                                st.link_button("🚀 Voir", getattr(recipe, 'url', '#'), width='stretch')
                            st.markdown("<br>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erreur API: {e}")
                if st.checkbox("Debug Mode"):
                    st.code(traceback.format_exc())
    else:
        st.info("👋 Entrez un mot-clé dans la barre latérale pour commencer !")

else:  # FAVORITES VIEW
    st.header("💖 Mes Recettes Favorites")
    
    conn = get_db_connection()
    favs = pd.read_sql_query("SELECT * FROM favorites ORDER BY created_at DESC", conn)
    conn.close()
    
    if favs.empty:
        st.info("Vous n'avez pas encore de favoris. Explorez des recettes !")
    else:
        # Show favorites in a similar grid or list
        for _, row in favs.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if row['image_url']:
                        st.image(row['image_url'], width='stretch')
                with col2:
                    st.subheader(row['name'])
                    st.caption(f"Ajouté le {row['created_at']}")
                    
                    c1, c2, c3 = st.columns([1, 1, 1])
                    with c1:
                        st.markdown(f"⏱️ **{row['prepa_time'] + row['cooking_time']} min**")
                    with c2:
                        st.markdown(f"👥 **{row['adaptedFor']} pers. (Ratio: x{round(row['adaptationFactor'], 1)})**")
                    with c3:
                        if st.button("🗑️ Supprimer", key=f"del_{row['id']}"):
                            remove_favorite(row['id'])
                            st.rerun()

                    try:
                        # Safely handle JSON or string
                        print(row)
                        if row['ingredients'].startswith('['):
                            ings = json.loads(row['ingredients'])
                            for i in ings:
                                st.write(f"- {i['name']} : {float(i['quantity']) * row['adaptationFactor']} {i['unit']}")
                        else:
                            st.write(row['ingredients'])
                    except:
                        st.write(row['ingredients'])
                    
                    st.link_button("🚀 Ouvrir sur Jow", row['url'], width='stretch')
                st.divider()

# --- FOOTER ---
st.markdown("<br><div style='text-align: center; color: #888;'>Fait avec ❤️ pour les gourmands</div>", unsafe_allow_html=True)
