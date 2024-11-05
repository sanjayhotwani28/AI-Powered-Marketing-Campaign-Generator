import streamlit as st
from typing import Dict, Any, Optional, List
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import numpy as np
import random
import json
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


def initialize_page():
    """Initialize Streamlit page with CommBank styling"""
    # Set page config
    st.set_page_config(
        page_title="CommBank Marketing Campaigns",
        page_icon="🏦",
        layout="wide"
    )

    # Apply custom styling
    st.markdown(
        """
        <style>
        .main {
            padding: 2rem;
        }
        .stButton button {
            background-color: #FDB813;
            color: black;
            font-weight: 500;
        }
        .stButton button:hover {
            background-color: #BE9B59;
            color: white;
        }
        .metric-card {
            background-color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #000000;
            font-family: 'CommBank Sans', Arial, sans-serif;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 1rem;
            font-weight: 500;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        .stTabs [data-baseweb="tab-border"] {
            background-color: #FDB813;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add header with logo
    st.markdown(
        f"""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: {BRAND_GUIDELINES['colors']['secondary']};">
                CommBank Marketing Campaign Generator
            </h1>
            <p style="color: {BRAND_GUIDELINES['colors']['text']}; font-size: 1.1rem;">
                Generate personalized marketing campaigns for banking customers
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add any session state initialization
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.customer_data = None
        st.session_state.campaign_history = []

def display_campaign_content(campaign_content: Dict[str, Any], customer_data: Dict[str, Any]):
    """Display campaign content with CommBank styling"""
    segment = customer_data['customer_segment']
    segment_guidelines = get_segment_guidelines(segment)

    st.subheader("Campaign Content")

    # Create tabs for different aspects of the campaign
    tabs = st.tabs(["Message", "Design", "Channels", "Legal"])

    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Primary Message")
            st.markdown(f">{campaign_content['primary_message']}")
        with col2:
            st.markdown("### Secondary Message")
            st.markdown(f">{campaign_content['secondary_message']}")

    with tabs[1]:
        st.markdown("### Visual Elements")
        st.json(campaign_content['visual_elements'])

        # Display color scheme
        colors = get_brand_colors(segment)
        st.markdown("### Color Scheme")
        cols = st.columns(len(colors))
        for col, color in zip(cols, colors):
            col.markdown(
                f"""
                <div style="background-color: {color}; 
                          height: 50px; 
                          border-radius: 4px;">
                </div>
                """,
                unsafe_allow_html=True
            )

    with tabs[2]:
        st.markdown("### Channel Strategy")
        st.json(campaign_content['channel_strategy'])

        # Display channel effectiveness
        if 'primary_channels' in campaign_content['channel_strategy']:
            channels = campaign_content['channel_strategy']['primary_channels']
            effectiveness = [random.uniform(0.7, 1.0) for _ in channels]

            df = pd.DataFrame({
                'Channel': channels,
                'Effectiveness': effectiveness
            })

            fig = px.bar(
                df,
                x='Channel',
                y='Effectiveness',
                title='Channel Effectiveness',
                color='Effectiveness',
                color_continuous_scale=['#FDB813', '#000000']
            )
            st.plotly_chart(fig)

    with tabs[3]:
        st.markdown("### Legal Information")
        st.markdown(f"*{get_legal_disclaimer('banking')}*")
        st.markdown(f"*{BRAND_GUIDELINES['legal']['copyright']}*")


def display_customer_profile(customer_data: Dict[str, Any], insights: Dict[str, Any]):
    """Display customer profile with CommBank styling"""
    segment = customer_data['customer_segment']
    segment_guidelines = get_segment_guidelines(segment)

    st.subheader("Customer Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Banking Profile")
        st.markdown(
            f"""
            - Segment: {segment}
            - Digital Engagement: {customer_data['digital_engagement']}
            - Relationship: {customer_data.get('relationship_tenure', 1)} years
            """
        )

    with col2:
        st.markdown("### Transaction Behavior")
        st.markdown(
            f"""
            - Monthly Transactions: {customer_data['transaction_frequency']}
            - Average Transaction: ${customer_data['average_transaction']:,.2f}
            - Products: {len(customer_data['product_holdings'])}
            """
        )

    with col3:
        st.markdown("### Preferences")
        st.markdown("**Preferred Channels:**")
        for channel in customer_data['preferred_channels']:
            st.markdown(f"- {channel}")

        st.markdown("**Interests:**")
        for interest in customer_data['primary_interests']:
            st.markdown(f"- {interest}")


def display_performance_metrics(metrics: Dict[str, float]):
    """Display performance metrics with CommBank styling"""
    st.subheader("Campaign Performance Metrics")

    cols = st.columns(4)

    with cols[0]:
        st.metric(
            "Engagement Score",
            f"{metrics['engagement_rate']:.1f}%",
            delta=f"{random.uniform(2, 8):.1f}%"
        )

    with cols[1]:
        st.metric(
            "Channel Optimization",
            f"{metrics['channel_optimization']:.1f}%",
            delta=f"{random.uniform(3, 10):.1f}%"
        )

    with cols[2]:
        st.metric(
            "Personalization Score",
            f"{metrics['personalization_score']:.1f}%",
            delta=f"{random.uniform(4, 12):.1f}%"
        )

    with cols[3]:
        st.metric(
            "Brand Alignment",
            f"{metrics['brand_alignment']:.1f}%",
            delta=f"{random.uniform(2, 6):.1f}%"
        )


def display_campaign_preview(campaign_content: Dict[str, Any], customer_data: Dict[str, Any]):
    """Display campaign preview in different formats"""
    st.subheader("Campaign Preview")

    preview_tabs = st.tabs(["Email", "Mobile App", "Web"])

    with preview_tabs[0]:
        st.markdown(
            f"""
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; 
                        border: 1px solid {BRAND_GUIDELINES['colors']['secondary']};
                        border-radius: 4px; background-color: white;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: {BRAND_GUIDELINES['colors']['primary']};">CommBank</h2>
                </div>
                <h3 style="color: {BRAND_GUIDELINES['colors']['secondary']};">
                    {campaign_content['primary_message']}
                </h3>
                <p style="color: {BRAND_GUIDELINES['colors']['text']}; margin: 20px 0;">
                    {campaign_content['secondary_message']}
                </p>
                <div style="text-align: center;">
                    <a href="#" style="background-color: {BRAND_GUIDELINES['colors']['primary']};
                                     color: black;
                                     padding: 10px 20px;
                                     text-decoration: none;
                                     border-radius: 4px;
                                     display: inline-block;">
                        Learn More
                    </a>
                </div>
                <div style="margin-top: 20px; font-size: 0.8rem; color: {BRAND_GUIDELINES['colors']['text']};">
                    {get_legal_disclaimer('banking')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with preview_tabs[1]:
        st.markdown(
            f"""
            <div style="max-width: 375px; margin: 0 auto; padding: 15px;
                        border: 1px solid {BRAND_GUIDELINES['colors']['secondary']};
                        border-radius: 8px; background-color: white;">
                <div style="background-color: {BRAND_GUIDELINES['colors']['primary']};
                           padding: 10px; border-radius: 4px; margin-bottom: 15px;">
                    <h4 style="color: black; margin: 0;">CommBank App</h4>
                </div>
                <h4 style="color: {BRAND_GUIDELINES['colors']['secondary']};">
                    {campaign_content['primary_message']}
                </h4>
                <p style="color: {BRAND_GUIDELINES['colors']['text']}; 
                          font-size: 0.9rem; margin: 10px 0;">
                    {campaign_content['secondary_message']}
                </p>
                <button style="background-color: {BRAND_GUIDELINES['colors']['primary']};
                             color: black;
                             border: none;
                             padding: 8px 16px;
                             border-radius: 4px;
                             width: 100%;
                             margin-top: 10px;">
                    Open App
                </button>
            </div>
            """,
            unsafe_allow_html=True
        )

    with preview_tabs[2]:
        st.markdown(
            f"""
            <div style="max-width: 800px; margin: 0 auto; padding: 30px;
                        border: 1px solid {BRAND_GUIDELINES['colors']['secondary']};
                        border-radius: 4px; background-color: white;">
                <nav style="margin-bottom: 20px; padding: 10px;
                           background-color: {BRAND_GUIDELINES['colors']['primary']};">
                    <h3 style="color: black; margin: 0;">CommBank</h3>
                </nav>
                <div style="display: flex; gap: 30px;">
                    <div style="flex: 2;">
                        <h2 style="color: {BRAND_GUIDELINES['colors']['secondary']};">
                            {campaign_content['primary_message']}
                        </h2>
                        <p style="color: {BRAND_GUIDELINES['colors']['text']}; 
                                  margin: 20px 0;">
                            {campaign_content['secondary_message']}
                        </p>
                        <div style="margin-top: 20px;">
                            <a href="#" style="background-color: {BRAND_GUIDELINES['colors']['primary']};
                                             color: black;
                                             padding: 12px 24px;
                                             text-decoration: none;
                                             border-radius: 4px;
                                             display: inline-block;">
                                Learn More
                            </a>
                        </div>
                    </div>
                    <div style="flex: 1;">
                        <div style="background-color: {BRAND_GUIDELINES['colors']['secondary']};
                                  height: 200px;
                                  border-radius: 4px;"></div>
                    </div>
                </div>
                <div style="margin-top: 30px; font-size: 0.8rem; 
                           color: {BRAND_GUIDELINES['colors']['text']};">
                    {get_legal_disclaimer('banking')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Display channel-specific details
    if 'channel_specific_adaptations' in campaign_content.get('channel_strategy', {}):
        st.markdown("### Channel Adaptations")
        adaptations = campaign_content['channel_strategy']['channel_specific_adaptations']
        for channel, details in adaptations.items():
            st.markdown(f"**{channel}:** {details}")


def create_download_button(data: Dict[str, Any], filename: str):
    """Create styled download button for campaign data"""
    try:
        # Create a serializable version of the data
        serializable_data = {
            'campaign_content': {
                'primary_message': data.get('campaign_content', {}).get('primary_message', ''),
                'secondary_message': data.get('campaign_content', {}).get('secondary_message', ''),
                'visual_elements': data.get('campaign_content', {}).get('visual_elements', {}),
                'channel_strategy': data.get('campaign_content', {}).get('channel_strategy', {}),
                'personalization_elements': data.get('campaign_content', {}).get('personalization_elements', {}),
                'tone_guidelines': data.get('campaign_content', {}).get('tone_guidelines', {}),
                'metadata': data.get('campaign_content', {}).get('metadata', {})
            },
            'customer_profile': {
                k: str(v) if isinstance(v, (pd.Series, pd.DataFrame, np.ndarray)) else v
                for k, v in data.get('customer_profile', {}).items()
            },
            'legal': {
                'disclaimer': get_legal_disclaimer('banking'),
                'copyright': BRAND_GUIDELINES['legal']['copyright'],
                'generated_at': datetime.now().isoformat()
            }
        }

        # Convert to JSON
        json_data = json.dumps(serializable_data, indent=2, default=str)

        st.download_button(
            label="Download Campaign Details",
            data=json_data,
            file_name=filename,
            mime="application/json"
        )
    except Exception as e:
        st.error(f"Error creating download button: {str(e)}")

# Export all functions
__all__ = [
    'initialize_page',
    'display_customer_profile',
    'display_campaign_content',
    'display_performance_metrics',
    'display_campaign_preview',
    'create_download_button'
]