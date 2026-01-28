"""Jow Gourmet - Main Streamlit Application."""
import streamlit as st
import traceback

# Import custom modules
from database import init_db, get_all_favorites, clear_all_favorites
from api_client import search_with_offset
from recipe_adapter import adapt_for_nb_people
from styles import get_custom_css
from ui_components import render_hero, render_recipe_card, render_pagination, render_favorite_item

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Jow Gourmet - Recettes qui donnent faim",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# --- CONSTANTS ---
RECIPES_PER_PAGE = 4

# --- SESSION STATE INITIALIZATION ---
if 'current_recipes' not in st.session_state:
    st.session_state.current_recipes = []
if 'all_fetched_recipes' not in st.session_state:
    st.session_state.all_fetched_recipes = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'last_query' not in st.session_state:
    st.session_state.last_query = ""
if 'last_nb_personnes' not in st.session_state:
    st.session_state.last_nb_personnes = 4
if 'last_limit' not in st.session_state:
    st.session_state.last_limit = 5

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://jow.fr/favicon.ico", width=40)
    st.title("Jow Gourmet")
    
    # Navigation tabs
    menu = st.segmented_control(
        "Navigation",
        ["🔍 Recherche", "💖 Mes Favoris"],
        default="🔍 Recherche",
        label_visibility="collapsed"
    )
    st.divider()
    
    if menu == "🔍 Recherche":
        st.markdown("### 🛠️ Filtres")
        query = st.text_input("Ingrédient ou plat", placeholder="ex: lasagnes, saumon...", key="search_query")
        limit = 20
        nb_personnes = st.slider("Nombre de personnes", 1, 10, 4)
        search_clicked = st.button("Lancer la recherche", type="primary", width='stretch')
    else:
        st.markdown("### ⚙️ Options")
        if st.button("🗑️ Vider tout", type="secondary", width='stretch'):
            clear_all_favorites()
            st.toast("Favoris vidés !")
            st.rerun()

# --- MAIN PAGE ---
if menu == "🔍 Recherche":
    render_hero()

    if 'search_query' in st.session_state and st.session_state.search_query:
        # Reset if new search query, different number of people, or different limit
        if (st.session_state.last_query != st.session_state.search_query or 
            st.session_state.last_nb_personnes != nb_personnes or
            st.session_state.last_limit != limit):
            st.session_state.all_fetched_recipes = []
            st.session_state.current_page = 0
            st.session_state.last_query = st.session_state.search_query
            st.session_state.last_nb_personnes = nb_personnes
            st.session_state.last_limit = limit
        
        # Fetch all recipes if not already fetched
        if len(st.session_state.all_fetched_recipes) == 0:
            with st.spinner("👩‍🍳 Recherche en cours..."):
                try:
                    # Fetch all recipes based on limit
                    recipes = search_with_offset(st.session_state.search_query, limit=limit, offset=0)
                    recipes = [adapt_for_nb_people(r, nb_personnes) for r in recipes]
                    st.session_state.all_fetched_recipes = recipes
                except Exception as e:
                    st.error(f"Erreur API: {e}")
                    if st.checkbox("Debug Mode"):
                        st.code(traceback.format_exc())
        
        # Calculate pagination
        total_recipes = len(st.session_state.all_fetched_recipes)
        total_pages = (total_recipes + RECIPES_PER_PAGE - 1) // RECIPES_PER_PAGE  # Ceiling division
        
        # Get current page recipes
        start_idx = st.session_state.current_page * RECIPES_PER_PAGE
        end_idx = min(start_idx + RECIPES_PER_PAGE, total_recipes)
        current_page_recipes = st.session_state.all_fetched_recipes[start_idx:end_idx]
        
        # Display current page of recipes
        if current_page_recipes:
            st.success(f"Affichage de {len(current_page_recipes)} recettes (Page {st.session_state.current_page + 1}/{total_pages}) - Total: {total_recipes} recettes")
            
            # Responsive Grid
            cols = st.columns(2)
            for idx, recipe in enumerate(current_page_recipes):
                with cols[idx % 2]:
                    render_recipe_card(recipe, idx)
            
            # Pagination controls
            action = render_pagination(st.session_state.current_page, total_pages)
            if action == 'prev':
                st.session_state.current_page -= 1
                st.rerun()
            elif action == 'next':
                st.session_state.current_page += 1
                st.rerun()
        else:
            if total_recipes == 0:
                st.warning("Aucune recette trouvée.")
    else:
        st.info("👋 Entrez un mot-clé dans la barre latérale pour commencer !")

else:  # FAVORITES VIEW
    # Custom header for favorites
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #2C2C2C; font-size: clamp(1.8rem, 4vw, 2.5rem); margin-bottom: 0.5rem;">
                💖 Mes Recettes Favorites
            </h1>
            <p style="color: #999; font-size: clamp(0.9rem, 2vw, 1.1rem);">
                Votre collection personnelle de délices culinaires
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    favs = get_all_favorites()
    
    if favs.empty:
        st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🍽️</div>
                <h3 style="color: #666;">Aucun favori pour le moment</h3>
                <p style="color: #999;">Explorez des recettes et ajoutez vos préférées ici !</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Display count
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <span style="background: #F5F5F5; padding: 0.5rem 1.5rem; border-radius: 20px; color: #666; font-weight: 500;">
                    {len(favs)} recette{'s' if len(favs) > 1 else ''} sauvegardée{'s' if len(favs) > 1 else ''}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        # Show favorites in grid
        cols = st.columns(2)
        for idx, (_, row) in enumerate(favs.iterrows()):
            with cols[idx % 2]:
                if render_favorite_item(row):
                    st.rerun()

# --- FOOTER ---
st.markdown("<br><div style='text-align: center; color: #888;'>Fait avec ❤️ pour les gourmands</div>", unsafe_allow_html=True)
