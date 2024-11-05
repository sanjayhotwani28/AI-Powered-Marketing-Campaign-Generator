import streamlit as st
from typing import Dict, Any, Optional
import json
from datetime import datetime
import random
import pandas as pd
import numpy as np
import re
from utils.api_utils import make_api_call
from config.brand_guidelines import (
    BRAND_GUIDELINES,
    get_segment_guidelines,
    get_visual_style,
    get_tone_guidelines,
    get_message_style,
    get_channel_recommendations,
    get_brand_colors,
    get_legal_disclaimer
)


def format_persona(customer_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format customer data into a structured persona"""
    try:
        persona = {
            'demographic': {
                'age': int(customer_data['age']),
                'gender': str(customer_data['gender']),
                'location': str(customer_data['location']),
                'income': float(customer_data['income']),
                'occupation': str(customer_data['occupation']),
                'life_stage': get_life_stage(int(customer_data['age']))
            },
            'behavioral': {
                'transaction_frequency': int(customer_data['transaction_frequency']),
                'average_transaction': float(customer_data['average_transaction']),
                'digital_engagement': str(customer_data['digital_engagement']),
                'customer_segment': str(customer_data['customer_segment']),
                'product_holdings': len(customer_data['product_holdings']),
                'relationship_tenure': customer_data.get('relationship_tenure', 1)
            },
            'psychographic': {
                'interests': customer_data['primary_interests'],
                'preferred_channels': customer_data['preferred_channels']
            }
        }
        return persona
    except Exception as e:
        st.error(f"Error formatting persona: {str(e)}")
        st.error(f"Customer data: {customer_data}")
        return None


def get_life_stage(age: int) -> str:
    """Determine life stage based on age"""
    if age <= 22:
        return 'Student'
    elif age <= 30:
        return 'Young Professional'
    elif age <= 40:
        return 'Family Builder'
    elif age <= 50:
        return 'Mid-Career'
    elif age <= 65:
        return 'Pre-retirement'
    else:
        return 'Retired'


def generate_campaign_prompt(persona: Dict[str, Any]) -> str:
    """Generate prompt for campaign creation"""
    try:
        segment = persona['behavioral']['customer_segment']
        segment_guidelines = get_segment_guidelines(segment)
        visual_style = get_visual_style(segment)
        tone = get_tone_guidelines(segment)
        message_style = get_message_style(segment)
        colors = get_brand_colors(segment)
        channels = get_channel_recommendations(persona['behavioral']['digital_engagement'])
        legal = get_legal_disclaimer('banking')

        # Create the exact JSON structure we want
        example_json = {
            "primary_message": f"Discover banking solutions tailored to your {segment.lower()} needs",
            "secondary_message": "Visit your nearest CommBank branch or login to NetBank to learn more",
            "visual_elements": {
                "color_scheme": ", ".join(colors),
                "imagery": "Professional banking environment",
                "layout": "Clean, modern layout",
                "style": visual_style['style']
            },
            "channel_strategy": {
                "primary_channels": channels,
                "secondary_channels": persona['psychographic']['preferred_channels'],
                "channel_specific_adaptations": {
                    "CommBank App": "Mobile-optimized format",
                    "Email": "Responsive design layout"
                }
            },
            "personalization_elements": {
                "key_variables": ["products", "transactions", "preferences"],
                "dynamic_content": ["offers", "services", "features"],
                "personalization_rules": "Based on banking behavior and preferences"
            },
            "tone_guidelines": {
                "voice": tone,
                "style": segment_guidelines['style'],
                "language_level": "Professional and clear"
            },
            "legal_disclaimer": legal
        }

        # Convert example to string with proper formatting
        example_json_str = json.dumps(example_json, indent=2)

        return f"""REQUIRED: Generate a marketing campaign as a JSON object following this EXACT structure:

{example_json_str}

You are an expert marketing specialist. Create a personalized marketing campaign for a bank customer.
Create the content based on these banking details:
Segment: {segment}
Digital Usage: {persona['behavioral']['digital_engagement']}
Monthly Transactions: {persona['behavioral']['transaction_frequency']}
Average Transaction: ${persona['behavioral']['average_transaction']:,.2f}
Current Products: {persona['behavioral']['product_holdings']}
Banking History: {persona['behavioral']['relationship_tenure']} years
Preferred Channels: {', '.join(persona['psychographic']['preferred_channels'])}
Financial Interests: {', '.join(persona['psychographic']['interests'])}

Requirements:
1. Primary message should be max 150 words and focused on the customer's interests and life stage
2. Secondary message should be max 50 words and include a clear call to action
3. Visual elements should specify colors, imagery, and layout that appeal to this customer persona
4. Channel strategy should prioritize the customer's preferred channels
5. Include specific personalization elements based on the customer's data
6. Tone guidelines should match the bank's brand voice and the customer's segment

CRITICAL INSTRUCTIONS:
1. Return ONLY valid JSON - no other text
2. Follow the exact structure shown above
3. Use appropriate banking terminology
4. Keep messages professional and clear
5. Include all required fields
6. Maintain consistent formatting"""

    except Exception as e:
        st.error(f"Error generating prompt: {str(e)}")
        return None

def generate_campaign_prompt_1(persona: Dict[str, Any]) -> str:
    try:
        prompt = f"""You are an expert marketing specialist. Create a personalized marketing campaign for a bank customer.
        Format your response as a valid JSON object only, with no additional text, using this exact structure:
        {{
            "primary_message": "The main campaign message",
            "secondary_message": "The follow-up message",
            "visual_elements": "Visual design suggestions",
            "channel_strategy": "Channel recommendations",
            "personalization_elements": "Personalization details",
            "tone_guidelines": "Tone and style guidelines"
        }}

        Create the campaign based on this customer persona:

        Demographics:
        - Age: {persona['demographic']['age']}
        - Gender: {persona['demographic']['gender']}
        - Location: {persona['demographic']['location']}
        - Income: ${persona['demographic']['income']:,}
        - Occupation: {persona['demographic']['occupation']}
        - Life Stage: {persona['demographic']['life_stage']}

        Behavioral Data:
        - Transaction Frequency: {persona['behavioral']['transaction_frequency']} times per month
        - Average Transaction: ${persona['behavioral']['average_transaction']:,}
        - Digital Engagement: {persona['behavioral']['digital_engagement']}
        - Customer Segment: {persona['behavioral']['customer_segment']}
        - Product Holdings: {persona['behavioral']['product_holdings']}
        - Relationship Tenure: {persona['behavioral']['relationship_tenure']} years

        Psychographic Data:
        - Interests: {', '.join(persona['psychographic']['interests'])}
        - Preferred Channels: {', '.join(persona['psychographic']['preferred_channels'])}

        Requirements:
        1. Primary message should be max 150 words and focused on the customer's interests and life stage
        2. Secondary message should be max 50 words and include a clear call to action
        3. Visual elements should specify colors, imagery, and layout that appeal to this customer persona
        4. Channel strategy should prioritize the customer's preferred channels
        5. Include specific personalization elements based on the customer's data
        6. Tone guidelines should match the bank's brand voice and the customer's segment

        Remember to provide ONLY the JSON response with no additional text."""

        return prompt

    except Exception as e:
        st.error(f"Error generating prompt: {str(e)}")
        return None


def validate_campaign_content(content: Dict[str, Any]) -> bool:
    """Validate the generated campaign content"""
    required_keys = [
        'primary_message',
        'secondary_message',
        'visual_elements',
        'channel_strategy',
        'personalization_elements',
        'tone_guidelines'
    ]

    try:
        for key in required_keys:
            if key not in content:
                st.error(f"Missing required key: {key}")
                return False

        # Add legal disclaimer if not present
        if 'legal_disclaimer' not in content:
            content['legal_disclaimer'] = get_legal_disclaimer('banking')

        return True

    except Exception as e:
        st.error(f"Error validating campaign content: {str(e)}")
        return False


def extract_json_content(response_text: str) -> Optional[Dict[str, Any]]:
    """Extract and validate JSON content from API response"""
    try:
        # Clean the response text
        cleaned_text = response_text.strip()

        # Try direct JSON parsing first
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            pass

        # Find JSON content
        json_start = cleaned_text.find('{')
        json_end = cleaned_text.rfind('}') + 1

        if json_start >= 0 and json_end > json_start:
            json_content = cleaned_text[json_start:json_end]

            # Clean up common JSON issues
            json_content = json_content.replace('\n', ' ')
            json_content = json_content.replace('\\', '\\\\')
            json_content = re.sub(r'(?<!\\)"', '\\"', json_content)
            json_content = re.sub(r',\s*}', '}', json_content)
            json_content = re.sub(r',\s*]', ']', json_content)

            try:
                return json.loads(json_content)
            except json.JSONDecodeError as je:
                st.error(f"JSON Decode Error: {str(je)}")
                st.write("Cleaned JSON content:", json_content)
                return None

        st.error("No valid JSON structure found in response")
        st.write("Full response:", cleaned_text)
        return None

    except Exception as e:
        st.error(f"Error extracting JSON: {str(e)}")
        return None


# Update the generate_campaign function to use the new extraction
def generate_campaign(customer_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Generate personalized marketing campaign"""
    try:
        # Format customer data into persona
        persona = format_persona(customer_data)
        if not persona:
            return None

        # Generate prompt
        prompt = generate_campaign_prompt(persona)
        if not prompt:
            return None

        # Get campaign content from API
        response = make_api_call(prompt=prompt)

        if not response or 'completion' not in response:
            st.error("Failed to get API response")
            return None

        # Extract and validate JSON content
        try:
            content = response['completion'].strip()
            json_start = content.find('{')
            json_end = content.rfind('}') + 1

            if json_start == -1 or json_end <= json_start:
                st.error("No valid JSON found in response")
                return None

            json_content = content[json_start:json_end]
            campaign_content = json.loads(json_content)

            # Validate content
            if not validate_campaign_content(campaign_content):
                return None

            # Ensure all nested dictionaries are serializable
            def make_serializable(obj):
                if isinstance(obj, (pd.Series, pd.DataFrame)):
                    return obj.to_dict()
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {k: make_serializable(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [make_serializable(i) for i in obj]
                elif isinstance(obj, (int, float, str, bool, type(None))):
                    return obj
                else:
                    return str(obj)

            # Convert campaign content to serializable format
            campaign_content = make_serializable(campaign_content)

            # Add metadata
            campaign_content['metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'customer_segment': persona['behavioral']['customer_segment'],
                'brand_guidelines_version': '1.0',
                'campaign_type': 'personalized_banking'
            }

            return campaign_content

        except json.JSONDecodeError as e:
            st.error(f"Error parsing campaign content: {str(e)}")
            return None

    except Exception as e:
        st.error(f"Error generating campaign: {str(e)}")
        return None


def estimate_campaign_performance(campaign_content: Dict[str, Any],
                                  customer_data: Dict[str, Any]) -> Dict[str, Any]:
    """Estimate campaign performance metrics"""
    try:
        # Base metrics
        base_engagement = random.uniform(15, 35)
        base_optimization = random.uniform(75, 95)
        base_personalization = random.uniform(80, 98)
        base_alignment = random.uniform(85, 97)

        # Adjust based on customer segment
        segment_multiplier = {
            'Premium': 1.2,
            'Standard': 1.0,
            'Basic': 0.8
        }.get(str(customer_data.get('customer_segment')), 1.0)

        # Adjust based on digital engagement
        engagement_multiplier = {
            'High': 1.2,
            'Medium': 1.0,
            'Low': 0.8
        }.get(str(customer_data.get('digital_engagement')), 1.0)

        metrics = {
            'engagement_rate': base_engagement * segment_multiplier,
            'channel_optimization': base_optimization * engagement_multiplier,
            'personalization_score': base_personalization * segment_multiplier,
            'brand_alignment': base_alignment,
            'timestamp': datetime.now().isoformat()
        }

        return metrics

    except Exception as e:
        st.error(f"Error estimating performance: {str(e)}")
        return {
            'engagement_rate': 0.0,
            'channel_optimization': 0.0,
            'personalization_score': 0.0,
            'brand_alignment': 0.0,
            'timestamp': datetime.now().isoformat()
        }