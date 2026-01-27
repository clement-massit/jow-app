import streamlit as st
from jow_api import Jow
import pandas as pd
import traceback

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Jow Gourmet - Recettes qui donnent faim",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- APPETIZING CSS ---
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #FFF9F0; /* Cream / Warm background */
    }

    .main {
        background: linear-gradient(135deg, #FFF9F0 0%, #FFF2E0 100%);
    }

    /* Hero Section */
    .hero-container {
        padding: 3rem 1rem;
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(255, 75, 43, 0.3);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #FFE0B2;
    }

    /* Card Styling */
    .recipe-card {
        background: white;
        border-radius: 15px;
        padding: 0;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #FFE0C0;
        overflow: hidden;
    }

    .recipe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(255, 75, 43, 0.15);
    }

    .card-content {
        padding: 1.5rem;
    }

    .card-title {
        color: #E65100;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }

    .card-badge {
        display: inline-block;
        background: #FFF3E0;
        color: #E65100;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(255, 75, 43, 0.4);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: white !important;
        border-radius: 10px !important;
        border: 1px solid #F3F4F6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://jow.fr/favicon.ico", width=50)
    st.markdown("### 🛠️ Configuration")
    query = st.text_input("Qu'est-ce qu'on mange ?", placeholder="ex: poulet coco, pâtes carbo...", value="")
    st.button("Rechercher")
    limit = st.slider("Nombre de festins", 1, 20, 6)
    st.divider()
    debug = st.checkbox("🔍 Mode expert (debug)", value=False)
    
    st.markdown("---")
    st.markdown("💡 *Astuce: Utilisez des ingrédients précis pour de meilleurs résultats.*")

# --- MAIN CONTENT ---
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Jow Gourmet 🍕</div>
        <div class="hero-subtitle">Trouvez l'inspiration pour votre prochain repas délicieux</div>
    </div>
""", unsafe_allow_html=True)

if not query:
    st.info("👋 Bonjour ! Tapez quelque chose dans la barre latérale pour commencer l'aventure culinaire.")
    # Show some appetizing categories or images here optionally
    col1, col2, col3 = st.columns(3)
    with col1: st.button("🔥 Populaires", width="stretch")
    with col2: st.button("🥦 Végétarien", width="stretch")
    with col3: st.button("⏱️ Express", width="stretch")

else:
    with st.spinner(f"👩‍🍳 Préparation de la liste pour '{query}'..."):
        try:
            recipes = Jow.search(query, limit=limit)
            
            if not recipes:
                st.warning("🧐 On n'a pas trouvé ça dans le grimoire Jow. Réessayez avec un autre mot !")
            else:
                st.markdown(f"### 🌟 {len(recipes)} idées pour vous régaler")
                
                # Display in a grid of 2-3 columns
                cols = st.columns(2)
                for idx, recipe in enumerate(recipes):
                    col = cols[idx % 2]
                    
                    with col:
                        name = getattr(recipe, 'name', 'Recette sans nom')
                        prepa = getattr(recipe, 'preparationTime', 0)
                        cuisson = getattr(recipe, 'cookingTime', 0)
                        covers = getattr(recipe, 'coversCount', '?')
                        url = getattr(recipe, 'url', '#')
                        img = getattr(recipe, 'imageUrl', None)
                        description = getattr(recipe, 'description', '')
                        ingredients = 
                        
                        # Card HTML
                        st.markdown(f"""
                            <div class="recipe-card">
                                {'<img src="' + img + '" style="width:50%; height:100%; object-fit:cover;">' if img else ''}
                                <div class="card-content">
                                    <div class="card-title">{name}</div>
                                    <div class="card-badge">⏱️ {prepa + cuisson} min</div>
                                    <div class="card-badge">👥 {covers} pers.</div>
                                    <div class="card-badge">🍳 {cuisson} min cuisson</div>
                                </div>



                              

                                
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📖 Voir les détails & ingrédients"):
                            c1, c2 = st.columns([1.5, 1])
                            with c1:
                                title = getattr(recipe, 'name', 'Recette sans nom')
                                st.markdown(f"### {title}")
                                desc = getattr(recipe, 'description', '')
                                if desc:
                                    st.markdown(f"**Description**")
                                    st.write(desc)
                                
                                st.markdown("#### 🛒 Ingrédients")
                                ingredients = getattr(recipe, 'ingredients', [])
                                if ingredients:
                                    for ing in ingredients:
                                        ing_name = getattr(ing, 'name', 'Inconnu')
                                        qty = getattr(ing, 'quantity', '')
                                        unit = getattr(ing, 'unit', '')
                                        st.markdown(f"- **{ing_name}** : {qty} {unit}")
                                else:
                                    st.info("Ingrédients non disponibles")
                                    
                            with c2:
                                if img:
                                    st.image(img, width="stretch")
                                st.link_button("🚀 Voir la recette sur Jow.fr", url, width="stretch")
            
                    

        except Exception as e:
            st.error("🤯 Oups ! La cuisine a pris feu...")
            st.info(f"**Erreur** : {str(e)[:150]}...")
            if debug:
                st.code(traceback.format_exc())

# --- FOOTER ---
st.divider()
st.markdown(
    "<div style='text-align: center; color: #888;'>Fait avec ❤️ pour les gourmands</div>", 
    unsafe_allow_html=True
)
