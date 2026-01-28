"""CSS styles for Jow Gourmet app."""


def get_custom_css():
    """Return the complete responsive CSS for the application."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Base styles with responsive units */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #FFF9F0;
        font-size: clamp(14px, 1vw + 0.5rem, 16px);
    }

    .main {
        background: linear-gradient(135deg, #FFF9F0 0%, #FFF2E0 100%);
        padding: clamp(0.5rem, 2vw, 2rem);
    }

    .hero-container {
        padding: clamp(1rem, 3vw, 2rem) clamp(0.5rem, 2vw, 1rem);
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        border-radius: clamp(12px, 2vw, 20px);
        color: white;
        text-align: center;
        margin-bottom: clamp(1rem, 3vw, 2rem);
        box-shadow: 0 10px 30px rgba(255, 75, 43, 0.3);
    }
    
    .hero-container h1 {
        font-size: clamp(1.5rem, 4vw, 2.5rem) !important;
        margin: 0 !important;
    }
    
    .hero-container p {
        font-size: clamp(0.9rem, 2vw, 1.1rem) !important;
        margin: 0 !important;
    }

    
    /* Recipe Card Wrapper - The main card shell */
    .recipe-card-wrapper {
        background: white;
        border-radius: clamp(16px, 2.5vw, 20px);
        padding: clamp(0.5rem, 1vw, 1rem);
        margin-bottom: clamp(1.5rem, 3vw, 2rem);
        margin-top: clamp(3rem, 6vw, 4rem);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: visible;
    }
    
    .recipe-card-wrapper:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    
    /* Elevated Recipe Card section */
    .recipe-card-elevated {
        padding: 0;
        padding-top: clamp(80px, 15vw, 120px);
        border: none;
        background: transparent;
    }
    
    /* Image Container - circular image that overflows */
    .card-image-container {
        position: absolute;
        top: clamp(-60px, -12vw, -80px);
        left: 50%;
        transform: translateX(-50%);
        width: clamp(140px, 28vw, 180px);
        height: clamp(140px, 28vw, 180px);
        border-radius: 50%;
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        background: white;
        z-index: 10;
        border: 4px solid white;
    }
    
    /* Card Image */
    .card-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
        display: block;
        transition: transform 0.3s ease;
    }
    
    .recipe-card-elevated:hover .card-image {
        transform: scale(1.1);
    }
    
    /* Card Content */
    .card-content-elevated {
        padding: clamp(1rem, 2.5vw, 1.5rem);
        padding-top: clamp(0.5rem, 1vw, 0.8rem);
        text-align: center;
    }
    
    /* Card Badges Container */
    .card-badges {
        display: flex;
        flex-wrap: wrap;
        gap: clamp(6px, 1.2vw, 8px);
        margin-bottom: clamp(10px, 2vw, 14px);
        justify-content: center;
    }
    
    /* Old recipe card styles (kept for backwards compatibility) */
    .recipe-card {
        background: white;
        border-radius: clamp(10px, 2vw, 15px);
        height: 100%;
        padding: 0;
        margin-bottom: clamp(15px, 3vw, 20px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #FFE0C0;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }

    .recipe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(255, 75, 43, 0.15);
    }

    .card-content {
        padding: clamp(0.8rem, 2vw, 1.2rem);
        flex: 1;
    }

    .card-title {
        color: #2C2C2C;
        font-size: clamp(1.1rem, 2.5vw, 1.4rem);
        font-weight: 600;
        margin-bottom: clamp(0.8rem, 1.5vw, 1rem);
        line-height: 1.3;
        text-align: center;
    }

    .card-badge {
        display: inline-block;
        background: #F5F5F5;
        color: #555;
        padding: clamp(4px, 0.8vw, 6px) clamp(10px, 2vw, 14px);
        border-radius: clamp(12px, 2vw, 16px);
        font-size: clamp(0.75rem, 1.5vw, 0.85rem);
        font-weight: 500;
        margin-right: 0;
        margin-bottom: 0;
        white-space: nowrap;
    }
    
    .ing-list {
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
        color: #666;
        padding-left: clamp(20px, 3vw, 25px);
        margin-top: clamp(10px, 2vw, 12px);
        max-height: clamp(140px, 22vw, 180px);
        overflow-y: auto;
        border-top: 1px solid #F0F0F0;
        padding-top: clamp(8px, 1.5vw, 10px);
        line-height: 1.6;
        text-align: left;
    }
    
    .ing-list li {
        margin-bottom: 0.3rem;
    }
    
    /* Favorites specific styles */
    .favorite-card {
        position: relative;
    }
    
    .favorite-date {
        font-size: clamp(0.75rem, 1.3vw, 0.85rem);
        color: #999;
        margin-bottom: clamp(0.6rem, 1.2vw, 0.8rem);
        text-align: center;
        font-style: italic;
    }
    
    /* Grid layout with responsive padding */
    [data-testid="column"] {
        padding: 0 clamp(0.25rem, 1vw, 0.5rem);
    }

    /* Standardize buttons in card footer */
    .recipe-card-wrapper .stButton button, 
    .recipe-card-wrapper a[data-testid="stBaseLinkButton"] {
        border-radius: 12px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem !important;
        height: 42px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
        border: 1px solid #EEE !important;
        box-shadow: none !important;
    }

    .recipe-card-wrapper .stButton button:hover,
    .recipe-card-wrapper a[data-testid="stBaseLinkButton"]:hover {
        background-color: #F8F8F8 !important;
        border-color: #DDD !important;
        transform: translateY(-1px);
    }

    /* Red heart hover specific */
    .recipe-card-wrapper div[data-testid="column"]:last-child .stButton button:hover {
        color: #FF6B6B !important;
        background-color: #FFF5F5 !important;
        border-color: #FFDADA !important;
    }
    
    /* Responsive images in cards */
    .recipe-card img {
        width: 100%;
        height: auto;
        min-height: clamp(150px, 25vw, 250px);
        max-height: clamp(200px, 30vw, 300px);
        object-fit: cover;
    }
    
    /* Media Queries for specific breakpoints */
    
    /* Mobile phones (portrait) */
    @media (max-width: 600px) {
        .recipe-card {
            flex-direction: column !important;
        }
        
        .recipe-card img {
            width: 100% !important;
            min-height: 180px;
            max-height: 220px;
        }
        
        .card-content {
            width: 100% !important;
        }
        
        .hero-container {
            padding: 1rem 0.5rem;
        }
        
        .card-badge {
            font-size: 0.7rem;
            padding: 2px 6px;
        }
    }
    
    /* Tablets (portrait) */
    @media (min-width: 601px) and (max-width: 900px) {
        .recipe-card img {
            width: 45% !important;
            min-height: 200px;
        }
        
        .card-title {
            font-size: 1.1rem;
        }
    }
    
    /* Desktop and larger */
    @media (min-width: 901px) {
        .recipe-card img {
            width: 50% !important;
        }
    }
    
    /* Very large screens */
    @media (min-width: 1400px) {
        .main {
            max-width: 1400px;
            margin: 0 auto;
        }
    }
    </style>
    """
