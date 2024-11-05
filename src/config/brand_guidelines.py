"""
Brand guidelines configuration for CommBank
"""

BRAND_GUIDELINES = {
    'colors': {
        'primary': '#FDB813',      # CommBank Yellow
        'secondary': '#000000',    # Black
        'accent': '#BE9B59',       # Gold
        'text': '#1E1E1E',        # Dark text
        'background': '#FFFFFF'    # White
    },
    'segments': {
        'Premium': {
            'tone': 'Sophisticated, exclusive, and personalized',
            'style': 'Professional and premium',
            'visual': {
                'style': 'Minimalist and elegant',
                'imagery': 'Sophisticated, luxury-focused imagery',
                'colors': ['#FDB813', '#BE9B59', '#000000']
            },
            'messages': {
                'primary_tone': 'Exclusive and personalized',
                'cta_style': 'Sophisticated and direct'
            }
        },
        'Standard': {
            'tone': 'Professional, friendly, and informative',
            'style': 'Clear and professional',
            'visual': {
                'style': 'Clean and modern',
                'imagery': 'Professional, lifestyle imagery',
                'colors': ['#FDB813', '#000000', '#FFFFFF']
            },
            'messages': {
                'primary_tone': 'Professional and helpful',
                'cta_style': 'Clear and actionable'
            }
        },
        'Basic': {
            'tone': 'Clear, simple, and direct',
            'style': 'Straightforward and helpful',
            'visual': {
                'style': 'Simple and clean',
                'imagery': 'Clear, relatable imagery',
                'colors': ['#FDB813', '#000000', '#FFFFFF']
            },
            'messages': {
                'primary_tone': 'Simple and direct',
                'cta_style': 'Easy to understand'
            }
        }
    },
    'typography': {
        'primary_font': 'CommBank Sans, Arial, sans-serif',
        'secondary_font': 'CommBank Headline, Arial, sans-serif',
        'sizes': {
            'small': '0.875rem',
            'base': '1rem',
            'large': '1.25rem',
            'xlarge': '1.5rem'
        },
        'weights': {
            'regular': '400',
            'medium': '500',
            'bold': '700'
        }
    },
    'channels': {
        'digital': {
            'primary': ['CommBank App', 'NetBank'],
            'secondary': ['Email', 'SMS'],
            'style': 'Digital-first approach'
        },
        'physical': {
            'primary': ['Branch', 'Direct Mail'],
            'secondary': ['Phone', 'ATM'],
            'style': 'Personal touch approach'
        }
    },
    'legal': {
        'disclaimer': 'Terms and conditions apply. Consider the relevant Product Disclosure Statement available at commbank.com.au before making any decisions.',
        'copyright': '© Commonwealth Bank of Australia 2024 ABN 48 123 123 124 AFSL and Australian credit licence 234945',
        'regulatory': {
            'banking': 'Banking products and services by Commonwealth Bank of Australia.',
            'investment': 'Investment products are subject to investment risk.',
            'insurance': 'Insurance products are subject to eligibility criteria.'
        }
    }
}

def get_segment_guidelines(segment: str) -> dict:
    """Get guidelines for a specific customer segment"""
    return BRAND_GUIDELINES['segments'].get(segment, BRAND_GUIDELINES['segments']['Standard'])

def get_visual_style(segment: str) -> dict:
    """Get visual style guidelines for a specific segment"""
    return BRAND_GUIDELINES['segments'][segment]['visual']

def get_tone_guidelines(segment: str) -> str:
    """Get tone guidelines for a specific segment"""
    return BRAND_GUIDELINES['segments'][segment]['tone']

def get_message_style(segment: str) -> dict:
    """Get message style guidelines for a specific segment"""
    return BRAND_GUIDELINES['segments'][segment]['messages']

def get_channel_recommendations(engagement_level: str) -> list:
    """Get channel recommendations based on engagement level"""
    if engagement_level == 'High':
        return BRAND_GUIDELINES['channels']['digital']['primary']
    elif engagement_level == 'Low':
        return BRAND_GUIDELINES['channels']['physical']['primary']
    else:
        return (BRAND_GUIDELINES['channels']['digital']['primary'] +
                BRAND_GUIDELINES['channels']['physical']['secondary'])

def get_brand_colors(segment: str) -> list:
    """Get brand colors for a specific segment"""
    return BRAND_GUIDELINES['segments'][segment]['visual']['colors']

def get_legal_disclaimer(product_type: str = 'banking') -> str:
    """Get legal disclaimer based on product type"""
    return (f"{BRAND_GUIDELINES['legal']['regulatory'][product_type]} "
            f"{BRAND_GUIDELINES['legal']['disclaimer']}")