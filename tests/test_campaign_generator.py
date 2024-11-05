import pytest
from models.campaign_generator import CampaignGenerator, generate_campaign
from datetime import datetime


@pytest.fixture
def sample_persona():
    return {
        'demographic': {
            'age': 35,
            'gender': 'F',
            'location': 'New York',
            'income': 85000,
            'occupation': 'Software Engineer',
            'life_stage': 'Young Professional'
        },
        'behavioral': {
            'transaction_frequency': 15,
            'average_transaction': 1200,
            'digital_engagement': 'High',
            'customer_segment': 'Premium',
            'product_holdings': 3,
            'relationship_tenure': 5
        },
        'psychographic': {
            'interests': ['Technology', 'Investment', 'Travel'],
            'preferred_channels': ['Mobile App', 'Email']
        }
    }


def test_campaign_generator_initialization(sample_persona):
    generator = CampaignGenerator(sample_persona)
    assert generator.persona == sample_persona
    assert hasattr(generator, 'model_settings')
    assert hasattr(generator, 'brand_guidelines')


def test_prompt_creation(sample_persona):
    generator = CampaignGenerator(sample_persona)
    prompt = generator._create_prompt()

    # Check if prompt contains all necessary elements
    assert 'Demographics' in prompt
    assert 'Behavioral Data' in prompt
    assert 'Psychographic Data' in prompt
    assert 'Brand Guidelines' in prompt
    assert 'Requirements' in prompt


def test_campaign_content_validation(sample_persona):
    generator = CampaignGenerator(sample_persona)

    # Test valid content
    valid_content = {
        'primary_message': 'Valid primary message',
        'secondary_message': 'Valid secondary message',
        'visual_elements': {
            'color_scheme': 'Blue and white',
            'imagery': 'Modern tech imagery',
            'layout': 'Clean and minimal',
            'visual_hierarchy': 'Logo > Message > CTA'
        },
        'channel_strategy': {
            'primary_channels': ['Mobile App', 'Email'],
            'secondary_channels': ['Web', 'SMS'],
            'channel_specific_adaptations': {
                'Mobile App': 'Push notification format',
                'Email': 'HTML email format'
            }
        },
        'personalization_elements': {
            'key_variables': ['name', 'product_holdings'],
            'dynamic_content': ['personalized_offer', 'usage_stats'],
            'personalization_rules': 'Based on segment and engagement'
        },
        'tone_guidelines': {
            'voice': 'Professional and sophisticated',
            'style': 'Modern and tech-savvy',
            'language_level': 'Professional'
        }
    }

    assert generator._validate_campaign_content(valid_content) is True

    # Test invalid content
    invalid_content = {
        'primary_message': 'Missing required fields'
    }

    assert generator._validate_campaign_content(invalid_content) is False


def test_response_parsing(sample_persona):
    generator = CampaignGenerator(sample_persona)

    # Test valid JSON response
    valid_response = '{"primary_message": "Test message"}'
    parsed_content = generator._parse_response(valid_response)
    assert parsed_content is not None
    assert parsed_content['primary_message'] == 'Test message'