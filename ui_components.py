"""Reusable UI components for Jow Gourmet app."""
import streamlit as st
from database import add_favorite


def render_hero():
    """Render the hero section."""
    st.markdown("""
        <div class="hero-container">
            <h1 style='margin:0;'>Jow Gourmet 🍕</h1>
            <p style='margin:0; opacity:0.9;'>Trouvez l'inspiration pour votre prochain festin</p>
        </div>
    """, unsafe_allow_html=True)


def render_recipe_card(recipe, idx):
    """
    Render a single recipe card with elevated image design.
    
    Args:
        recipe: JowResult object with adapted quantities
        idx (int): Index for unique button keys
    """
    # Get data
    name = getattr(recipe, 'name', 'Recette sans nom')
    prepa = getattr(recipe, 'preparationTime', 0)
    cuisson = getattr(recipe, 'cookingTime', 0)
    
    if prepa and cuisson:
        total = prepa + cuisson
    else:
        total = prepa
    
    img = getattr(recipe, 'imageUrl', '')
    ingredients = getattr(recipe, 'ingredients', [])

    
    # Render card with functional heart icon in a single shell
    st.markdown(f'<div class="recipe-card-wrapper">', unsafe_allow_html=True)
    
    # Card Header (Image, Title, Badges)
    st.markdown(f"""
                <div class="recipe-card-elevated">
                    <div class="card-image-container">
                        <img src="{img}" class="card-image" alt="{name}">
                    </div>
                    <div class="card-content-elevated">
                        <div class="card-title">{name}</div>
                        <div class="card-badges">
                            <div class="card-badge">⏱️ {total} min</div>
                            <div class="card-badge">🔥 {cuisson} min</div>
                            <div class="card-badge">👥 {getattr(recipe, 'adaptedFor', 2)} pers.</div>
                        </div>
                        <ul class="ing-list">
                            {"".join([f"<li>{i.name} : <b>{i.quantityAdapted} {i.unit}</b></li>" for i in ingredients])}
                        </ul>
                    </div>
                </div>
    """, unsafe_allow_html=True)
    
    # Buttons area
    c1, c2 = st.columns([0.6, 0.4])
    with c1:
        st.link_button("🚀 Voir la recette", getattr(recipe, 'url', '#'), use_container_width=True)
    with c2:
        if st.button("❤️", key=f"heart_{idx}", use_container_width=True):
            add_favorite(recipe, getattr(recipe, 'adaptedFor', 2), getattr(recipe, 'adaptationFactor', 1))
            st.toast(f"💖 {name} ajouté aux favoris !")
            
    st.markdown('</div><br>', unsafe_allow_html=True)


def render_pagination(current_page, total_pages):
    """
    Render pagination controls.
    
    Args:
        current_page (int): Current page number (0-indexed)
        total_pages (int): Total number of pages
        
    Returns:
        str: 'prev', 'next', or None based on button clicked
    """
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    action = None
    
    with col1:
        if current_page > 0:
            if st.button("⬅️ Page précédente", width='stretch'):
                action = 'prev'
    
    with col2:
        st.markdown(
            f"<div style='text-align: center; padding: 10px;'><b>Page {current_page + 1}/{total_pages}</b></div>",
            unsafe_allow_html=True
        )
    
    with col3:
        if current_page < total_pages - 1:
            if st.button("➡️ Page suivante", width='stretch'):
                action = 'next'
    
    return action


def render_favorite_item(row):
    """
    Render a single favorite item with modern card design.
    
    Args:
        row: Pandas row from favorites database
        
    Returns:
        bool: True if delete button was clicked
    """
    import json
    from database import remove_favorite
    
    delete_clicked = False
    
    # Get adapted quantities
    try:
        if row['ingredients'].startswith('['):
            ings = json.loads(row['ingredients'])
            ingredients_html = "".join([
                f"<li>{i['name']} : <b>{round(float(i['quantity']) * row['adaptationFactor'], 2)} {i['unit']}</b></li>" 
                for i in ings[:6]  # Limit to 6 ingredients for display
            ])
        else:
            ingredients_html = f"<li>{row['ingredients']}</li>"
    except:
        ingredients_html = f"<li>{row['ingredients']}</li>"
    
    # Calculate total time
    total_time = (row['prepa_time'] or 0) + (row['cooking_time'] or 0)
    
    # Render favorite card with same style as recipe cards
    st.markdown(f"""
        <div class="recipe-card-wrapper">
            <div class="recipe-card-elevated favorite-card">
                <div class="card-image-container">
                    <img src="{row['image_url']}" class="card-image" alt="{row['name']}">
                </div>
                <div class="card-content-elevated">
                    <div class="card-title">{row['name']}</div>
                    <div class="favorite-date">Ajouté le {row['created_at'][:10]}</div>
                    <div class="card-badges">
                        <div class="card-badge">⏱️ {total_time} min</div>
                        <div class="card-badge">🔥 {row['cooking_time'] or 0} min</div>
                        <div class="card-badge">👥 {row['adaptedFor']} pers.</div>
                    </div>
                    <ul class="ing-list">
                        {ingredients_html}
                    </ul>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Action Buttons
    c1, c2, _ = st.columns([0.5, 0.5, 0.8])
    with c1:
        if st.button("🗑️ Supprimer", key=f"del_{row['id']}", width='stretch', type="secondary"):
            remove_favorite(row['id'])
            delete_clicked = True
    with c2:
        st.link_button("🚀 Voir", row['url'], width='stretch')
    st.markdown("<br>", unsafe_allow_html=True)
    
    return delete_clicked
