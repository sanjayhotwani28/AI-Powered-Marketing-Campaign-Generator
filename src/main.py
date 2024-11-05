import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import random
import sys
import os
import traceback
from typing import Dict, Any, Optional

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import custom components
from ui.components import (
    initialize_page,
    display_customer_profile,
    display_campaign_content,
    display_performance_metrics,
    display_campaign_preview,
    create_download_button
)

# Import utilities
from utils.api_utils import initialize_anthropic, test_api_connection, make_api_call
from utils.cache_utils import async_cache_data

# Import data and models
from data.synthetic_data import generate_synthetic_data, init_session_state
from models.campaign_generator import generate_campaign, estimate_campaign_performance
from models.customer_insights import create_customer_insights

# Import configuration
from config.settings import load_config, DATA_SETTINGS, CAMPAIGN_TYPES

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

# Import other utilities
from utils.api_utils import initialize_anthropic, test_api_connection, make_api_call
from data.synthetic_data import generate_synthetic_data, init_session_state
from models.campaign_generator import generate_campaign, estimate_campaign_performance
from models.customer_insights import create_customer_insights
from config.settings import load_config, DATA_SETTINGS
from config.brand_guidelines import BRAND_GUIDELINES
# Add this import at the top
from utils.cache_utils import async_cache_data


# Cache data generation
@async_cache_data(ttl=3600)
def get_cached_data(num_records: int) -> Optional[pd.DataFrame]:
    return generate_synthetic_data(num_records)

@async_cache_data(ttl=3600)
def get_cached_insights(customer_data_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    customer_data = pd.Series(customer_data_dict)
    return create_customer_insights(customer_data)


def initialize_app() -> Optional[Dict[str, Any]]:
    """Initialize the Streamlit application"""
    try:
        initialize_page()
        config = load_config()
        init_session_state()
        return config
    except Exception as e:
        st.error(f"Error initializing application: {str(e)}")
        return None


def show_debug_info():
    """Display debug information with unique key"""
    with st.sidebar.expander("Debug Information", expanded=False):
        st.json({
            'timestamp': datetime.now().isoformat(),
            'streamlit_version': st.__version__,
            'api_initialized': st.session_state.get('api_tested', False),
            'data_loaded': st.session_state.get('customer_data') is not None
        })


def handle_data_generation(num_records: int):
    """Handle synthetic data generation"""
    with st.spinner("Generating synthetic data..."):
        data = get_cached_data(num_records)
        if data is not None:
            st.session_state.customer_data = data
            st.success("✅ Data generated successfully!")
            return True
        else:
            st.error("Failed to generate data. Please try again.")
            return False


def apply_filters(data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """Apply filters to the dataset"""
    filtered_data = data.copy()

    if filters['segments']:
        filtered_data = filtered_data[filtered_data['customer_segment'].isin(filters['segments'])]
    if filters['engagement']:
        filtered_data = filtered_data[filtered_data['digital_engagement'].isin(filters['engagement'])]

    filtered_data = filtered_data[
        (filtered_data['age'] >= filters['age_range'][0]) &
        (filtered_data['age'] <= filters['age_range'][1])
        ]

    return filtered_data.reset_index(drop=True)


def main():
    """Main application function"""
    try:
        # Initialize application
        config = initialize_app()
        if not config:
            st.stop()

        # Sidebar configuration
        st.sidebar.title("Campaign Configuration")

        # Debug mode with unique key
        if st.sidebar.checkbox("Debug Mode", key="debug_mode_checkbox"):
            show_debug_info()

        # Data generation
        if 'customer_data' not in st.session_state or st.session_state.customer_data is None:
            num_records = st.sidebar.number_input(
                "Number of synthetic records",
                min_value=DATA_SETTINGS['min_records'],
                max_value=DATA_SETTINGS['max_records'],
                value=DATA_SETTINGS['default_records'],
                key="num_records_input"
            )

            if st.sidebar.button("Generate Data", key="generate_data_button"):
                if not handle_data_generation(num_records):
                    st.stop()

        # Process data if available
        if hasattr(st.session_state, 'customer_data') and st.session_state.customer_data is not None:
            # Data filtering
            st.subheader("Filter Customers")

            col1, col2, col3 = st.columns(3)

            with col1:
                segment_filter = st.multiselect(
                    "Customer Segment",
                    options=st.session_state.customer_data['customer_segment'].unique(),
                    default=[],
                    key="segment_filter"
                )

            with col2:
                engagement_filter = st.multiselect(
                    "Digital Engagement",
                    options=st.session_state.customer_data['digital_engagement'].unique(),
                    default=[],
                    key="engagement_filter"
                )

            with col3:
                min_age = int(st.session_state.customer_data['age'].min())
                max_age = int(st.session_state.customer_data['age'].max())
                age_range = st.slider(
                    "Age Range",
                    min_value=min_age,
                    max_value=max_age,
                    value=(min_age, max_age),
                    key="age_range_slider"
                )

            # Apply filters
            filters = {
                'segments': segment_filter,
                'engagement': engagement_filter,
                'age_range': age_range
            }
            filtered_data = apply_filters(st.session_state.customer_data, filters)

            if filtered_data.empty:
                st.warning("No customers match the selected filters. Please adjust your criteria.")
                st.stop()

            # Display filtered data
            with st.expander("View Customer Data", expanded=False):
                st.dataframe(filtered_data)

            # Customer selection
            st.subheader("Select Customer")

            customer_options = [
                f"Customer {idx + 1} - {row['customer_segment']} Segment - "
                f"{row['age']} years - {row['occupation']} - "
                f"${row['income']:,.0f}/year"
                for idx, row in filtered_data.iterrows()
            ]

            if customer_options:
                selected_index = st.selectbox(
                    "Select a customer to generate campaign",
                    range(len(customer_options)),
                    format_func=lambda x: customer_options[x],
                    key="customer_selector"
                )

                customer_data = filtered_data.iloc[selected_index]

                if st.button("Generate Campaign", key="generate_campaign_button"):
                    try:
                        with st.spinner("Generating campaign..."):
                            # Generate insights
                            insights = get_cached_insights(customer_data.to_dict())

                            if insights:
                                # Display customer profile
                                display_customer_profile(customer_data, insights)

                                # Generate campaign
                                campaign_content = generate_campaign(customer_data.to_dict())

                                if campaign_content:
                                    # Display campaign content
                                    display_campaign_content(campaign_content, customer_data)
                                    display_campaign_preview(campaign_content, customer_data)

                                    # Calculate and display metrics
                                    metrics = estimate_campaign_performance(
                                        campaign_content,
                                        customer_data.to_dict()
                                    )
                                    display_performance_metrics(metrics)

                                    # Create download button
                                    campaign_data = {
                                        'campaign_content': campaign_content,
                                        'customer_profile': customer_data.to_dict(),
                                        'insights': insights,
                                        'performance_metrics': metrics,
                                        'generated_at': datetime.now().isoformat()
                                    }
                                    create_download_button(
                                        campaign_data,
                                        f"commbank_campaign_customer_{selected_index}.json"
                                    )
                                else:
                                    st.error("Failed to generate campaign content.")
                            else:
                                st.error("Failed to generate customer insights.")

                    except Exception as e:
                        st.error(f"Error generating campaign: {str(e)}")
                        if st.sidebar.checkbox("Show Error Details", key="show_campaign_error"):
                            st.code(traceback.format_exc())
            else:
                st.warning("No customers available for selection. Please adjust the filters.")
        else:
            st.info("Please generate customer data using the sidebar controls.")

    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        if st.sidebar.checkbox("Show Error Details", key="show_main_error"):
            st.code(traceback.format_exc())


if __name__ == "__main__":
    main()