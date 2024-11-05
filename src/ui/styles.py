"""
Streamlit UI styles based on CommBank's brand guidelines
"""

from config.brand_guidelines import BRAND_GUIDELINES

# Define fallback sizes for typography
TYPOGRAPHY_SIZES = {
    'small': '0.875rem',  # 14px
    'base': '1rem',       # 16px
    'large': '1.25rem',   # 20px
    'title': '2rem'       # 32px
}

# Define fallback weights for typography
TYPOGRAPHY_WEIGHTS = {
    'regular': '400',
    'medium': '500',
    'bold': '700'
}

# Define fallback colors
COLORS = {
    'primary': '#FDB813',      # CommBank Yellow
    'secondary': '#000000',    # Black
    'accent': '#BE9B59',       # Gold
    'text': '#1E1E1E',        # Dark text
    'background': '#FFFFFF',   # White
    'support': {
        'success': '#287D3C',  # Green
        'warning': '#FF9900',  # Orange
        'error': '#DA1710',    # Red
        'info': '#2C88FF'      # Blue
    }
}

# Use brand guidelines colors if available, otherwise use fallbacks
THEME_COLORS = {
    'primary': BRAND_GUIDELINES.get('colors', {}).get('primary', COLORS['primary']),
    'secondary': BRAND_GUIDELINES.get('colors', {}).get('secondary', COLORS['secondary']),
    'text': BRAND_GUIDELINES.get('colors', {}).get('text', COLORS['text']),
    'background': BRAND_GUIDELINES.get('colors', {}).get('background', COLORS['background']),
    'success': COLORS['support']['success'],
    'warning': COLORS['support']['warning'],
    'error': COLORS['support']['error'],
    'info': COLORS['support']['info']
}

# Main CSS styling for the application
CUSTOM_CSS = f"""
<style>
    /* Main Container Styles */
    .main {{
        background-color: {THEME_COLORS['background']};
        color: {THEME_COLORS['text']};
        font-family: {BRAND_GUIDELINES['typography']['primary_font']};
    }}
    
    /* Header Styles */
    .stApp header {{
        background-color: {THEME_COLORS['primary']};
    }}
    
    /* Title and Headers */
    h1, h2, h3 {{
        font-family: {BRAND_GUIDELINES['typography']['secondary_font']};
        color: {THEME_COLORS['secondary']};
    }}
    
    h1 {{
        font-size: {TYPOGRAPHY_SIZES['title']};
        font-weight: {TYPOGRAPHY_WEIGHTS['bold']};
    }}
    
    h2 {{
        font-size: {TYPOGRAPHY_SIZES['large']};
        font-weight: {TYPOGRAPHY_WEIGHTS['bold']};
    }}
    
    h3 {{
        font-size: {TYPOGRAPHY_SIZES['base']};
        font-weight: {TYPOGRAPHY_WEIGHTS['medium']};
    }}
    
    /* Button Styles */
    .stButton button {{
        background-color: {THEME_COLORS['primary']};
        color: {THEME_COLORS['text']};
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: {TYPOGRAPHY_WEIGHTS['medium']};
        border: none;
        transition: transform 0.2s;
    }}
    
    .stButton button:hover {{
        background-color: {THEME_COLORS['secondary']};
        transform: translateY(-2px);
    }}
    
    /* Metric Cards */
    .metric-card {{
        background-color: {THEME_COLORS['background']};
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    /* Success Message */
    .success-message {{
        background-color: {THEME_COLORS['success']};
        color: {THEME_COLORS['background']};
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }}
    
    /* Warning Message */
    .warning-message {{
        background-color: {THEME_COLORS['warning']};
        color: {THEME_COLORS['background']};
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }}
    
    /* Error Message */
    .error-message {{
        background-color: {THEME_COLORS['error']};
        color: {THEME_COLORS['background']};
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }}
    
    /* Info Message */
    .info-message {{
        background-color: {THEME_COLORS['info']};
        color: {THEME_COLORS['background']};
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }}
    
    /* Sidebar Styles */
    .css-1d392kg {{  /* Sidebar */
        background-color: {THEME_COLORS['background']};
    }}
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {THEME_COLORS['background']};
        border-radius: 4px 4px 0 0;
        color: {THEME_COLORS['secondary']};
        padding: 0.5rem 1rem;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {THEME_COLORS['primary']};
        color: {THEME_COLORS['background']};
    }}
    
    /* DataFrames and Tables */
    .dataframe {{
        font-size: {TYPOGRAPHY_SIZES['small']};
    }}
    
    .dataframe th {{
        background-color: {THEME_COLORS['background']};
        font-weight: {TYPOGRAPHY_WEIGHTS['medium']};
        padding: 0.5rem;
    }}
    
    /* Custom Classes */
    .premium-card {{
        background: linear-gradient(135deg, {THEME_COLORS['primary']}, {THEME_COLORS['secondary']});
        padding: 1.5rem;
        border-radius: 8px;
        color: {THEME_COLORS['background']};
    }}
    
    .stat-card {{
        background-color: {THEME_COLORS['background']};
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }}
    
    .insight-card {{
        border-left: 4px solid {THEME_COLORS['primary']};
        padding: 1rem;
        margin: 1rem 0;
        background-color: {THEME_COLORS['background']};
    }}
    
    /* Disclaimer Text */
    .disclaimer-text {{
        font-size: {TYPOGRAPHY_SIZES['small']};
        color: {THEME_COLORS['secondary']};
        margin-top: 1rem;
        padding: 0.5rem;
        border-top: 1px solid {THEME_COLORS['secondary']};
    }}
    
    /* Loading Animation */
    .stProgress .st-bo {{
        background-color: {THEME_COLORS['primary']};
    }}
    
    /* Download Button */
    .download-button {{
        background-color: {THEME_COLORS['success']};
        color: {THEME_COLORS['background']};
        padding: 0.75rem 1.5rem;
        border-radius: 4px;
        text-decoration: none;
        display: inline-block;
        margin: 1rem 0;
        font-weight: {TYPOGRAPHY_WEIGHTS['medium']};
    }}
    
    .download-button:hover {{
        background-color: {THEME_COLORS['success']};
        opacity: 0.9;
    }}
</style>
"""

# Component-specific styles
METRIC_CARD_STYLE = f"""
<div class="metric-card">
    <h4 style="color: {THEME_COLORS['secondary']};">{{title}}</h4>
    <p style="font-size: {TYPOGRAPHY_SIZES['large']}; 
              color: {THEME_COLORS['primary']};
              font-weight: {TYPOGRAPHY_WEIGHTS['bold']};">
        {{value}}
    </p>
    <p style="font-size: {TYPOGRAPHY_SIZES['small']}; 
              color: {THEME_COLORS['secondary']};">
        {{subtitle}}
    </p>
</div>
"""

PREMIUM_CARD_STYLE = f"""
<div class="premium-card">
    <h3 style="color: {THEME_COLORS['background']}; 
               font-weight: {TYPOGRAPHY_WEIGHTS['bold']};">{{title}}</h3>
    <p style="color: {THEME_COLORS['background']};">{{content}}</p>
</div>
"""

INSIGHT_CARD_STYLE = f"""
<div class="insight-card">
    <h4 style="color: {THEME_COLORS['secondary']};
               font-weight: {TYPOGRAPHY_WEIGHTS['bold']};">{{title}}</h4>
    <p style="color: {THEME_COLORS['secondary']};">{{content}}</p>
    <p style="color: {THEME_COLORS['secondary']}; 
              font-size: {TYPOGRAPHY_SIZES['small']};">
        {{subtitle}}
    </p>
</div>
"""

def get_segment_style(segment: str) -> dict:
    """Get segment-specific styling"""
    styles = {
        'Premium': {
            'background': f"linear-gradient(135deg, {THEME_COLORS['primary']}, "
                         f"{THEME_COLORS['secondary']})",
            'text_color': THEME_COLORS['background'],
            'font_family': BRAND_GUIDELINES['typography']['secondary_font'],
            'padding': '1.5rem',
            'border_radius': '8px'
        },
        'Standard': {
            'background': THEME_COLORS['background'],
            'text_color': THEME_COLORS['secondary'],
            'font_family': BRAND_GUIDELINES['typography']['primary_font'],
            'padding': '1rem',
            'border_radius': '4px'
        },
        'Basic': {
            'background': THEME_COLORS['background'],
            'text_color': THEME_COLORS['secondary'],
            'font_family': BRAND_GUIDELINES['typography']['primary_font'],
            'padding': '1rem',
            'border_radius': '4px'
        }
    }
    return styles.get(segment, styles['Standard'])

def get_disclaimer_html(product_type: str = None) -> str:
    """Get formatted disclaimer HTML"""
    disclaimer = BRAND_GUIDELINES['compliance']['regulatory_text'].get(
        product_type,
        BRAND_GUIDELINES['compliance']['required_disclaimers'][0]
    )
    return f"""
    <div class="disclaimer-text">
        {disclaimer}
    </div>
    """