"""
Application settings and configuration
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application Settings
APP_SETTINGS = {
    'page_title': 'CommBank Marketing Campaign Generator',
    'page_icon': '🏦',
    'layout': 'wide'
}

# Data Generation Settings
DATA_SETTINGS = {
    'min_records': 10,
    'max_records': 1000,
    'default_records': 100
}

# API Settings
API_SETTINGS = {
    'model': 'claude-2',
    'max_tokens': 1500,
    'temperature': 0.7
}

# Cache Settings
CACHE_SETTINGS = {
    'ttl': 3600,  # 1 hour
    'max_entries': 1000
}

# Campaign Types
CAMPAIGN_TYPES = {
    'product_launch': {
        'tone': 'Exciting and innovative',
        'focus': 'Features and benefits',
        'required_elements': ['Product features', 'Launch offers', 'How to get started']
    },
    'cross_sell': {
        'tone': 'Helpful and informative',
        'focus': 'Added value and convenience',
        'required_elements': ['Current product tie-in', 'Benefits of addition', 'Special offer']
    },
    'retention': {
        'tone': 'Appreciative and valuable',
        'focus': 'Relationship and loyalty',
        'required_elements': ['Relationship recap', 'Exclusive benefits', 'Thank you message']
    },
    'educational': {
        'tone': 'Informative and helpful',
        'focus': 'Knowledge and empowerment',
        'required_elements': ['Key insights', 'Practical tips', 'Next steps']
    }
}


def load_config() -> Dict[str, Any]:
    """Load application configuration"""
    config = {
        'api_key': os.getenv('ANTHROPIC_API_KEY'),
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'debug': os.getenv('DEBUG', 'false').lower() == 'true',
        'app_settings': APP_SETTINGS,
        'data_settings': DATA_SETTINGS,
        'api_settings': API_SETTINGS,
        'cache_settings': CACHE_SETTINGS,
        'campaign_types': CAMPAIGN_TYPES
    }

    # Validate required settings
    if not config['api_key']:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    return config