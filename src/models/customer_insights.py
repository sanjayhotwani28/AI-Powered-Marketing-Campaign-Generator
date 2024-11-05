import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional
import random
from datetime import datetime, timedelta
# Add at the top of the file
from utils.cache_utils import async_cache_data

@async_cache_data(ttl=3600)
def create_transaction_pattern(customer_data: pd.Series) -> go.Figure:
    """Generate transaction pattern visualization"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Base transaction amount
    base_transaction = float(customer_data['average_transaction'])

    # Generate realistic transaction amounts with seasonality and trends
    transactions = []
    for i in range(12):
        # Add seasonality effect
        seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * i / 12)
        # Add random variation
        random_factor = np.random.normal(1, 0.1)
        amount = base_transaction * seasonal_factor * random_factor
        transactions.append(amount)

    # Create figure
    fig = go.Figure()

    # Add transaction line
    fig.add_trace(go.Scatter(
        x=months,
        y=transactions,
        mode='lines+markers',
        name='Transactions',
        line=dict(color='#FDB813', width=2),  # CommBank Yellow
        marker=dict(size=8)
    ))

    # Add average line
    fig.add_trace(go.Scatter(
        x=months,
        y=[base_transaction] * 12,
        mode='lines',
        name='Average',
        line=dict(color='#000000', width=2, dash='dash')  # Black
    ))

    # Update layout
    fig.update_layout(
        title='Monthly Transaction Pattern',
        xaxis_title='Month',
        yaxis_title='Transaction Amount ($)',
        showlegend=True,
        hovermode='x unified'
    )

    return fig

@async_cache_data(ttl=3600)
def create_product_usage(customer_data: pd.Series) -> go.Figure:
    """Generate product usage visualization"""
    # Get product holdings
    products = customer_data['product_holdings']

    # Generate usage scores based on customer segment and engagement
    base_score = {
        'Premium': 0.8,
        'Standard': 0.6,
        'Basic': 0.4
    }.get(customer_data['customer_segment'], 0.5)

    engagement_multiplier = {
        'High': 1.2,
        'Medium': 1.0,
        'Low': 0.8
    }.get(customer_data['digital_engagement'], 1.0)

    # Calculate usage scores
    usage_scores = {}
    for product in products:
        score = base_score * engagement_multiplier * random.uniform(0.8, 1.2)
        usage_scores[product] = min(score, 1.0)  # Cap at 1.0

    # Create figure
    fig = go.Figure()

    # Add bars
    fig.add_trace(go.Bar(
        x=list(usage_scores.keys()),
        y=list(usage_scores.values()),
        marker_color='#FDB813'  # CommBank Yellow
    ))

    # Update layout
    fig.update_layout(
        title='Product Usage Distribution',
        xaxis_title='Product',
        yaxis_title='Usage Score',
        showlegend=False,
        yaxis=dict(range=[0, 1])
    )

    return fig

@async_cache_data(ttl=3600)
def create_engagement_radar(customer_data: pd.Series) -> go.Figure:
    """Generate engagement radar chart"""
    # Calculate engagement metrics
    metrics = {
        'Transaction Activity': min(customer_data['transaction_frequency'] / 30, 1),
        'Digital Engagement': {'High': 0.9, 'Medium': 0.6, 'Low': 0.3}[customer_data['digital_engagement']],
        'Product Utilization': min(len(customer_data['product_holdings']) / 8, 1),
        'Relationship Tenure': min(customer_data.get('relationship_tenure', 1) / 20, 1),
        'Satisfaction': customer_data.get('satisfaction_score', 75) / 100
    }

    # Create radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=list(metrics.values()),
        theta=list(metrics.keys()),
        fill='toself',
        line_color='#FDB813'  # CommBank Yellow
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        title='Customer Engagement Profile'
    )

    return fig


def generate_recommendations(customer_data: pd.Series) -> list:
    """Generate personalized recommendations"""
    recommendations = []

    # Get current products and potential products
    current_products = set(customer_data['product_holdings'])
    potential_products = {
        'Savings Account', 'Checking Account', 'Credit Card',
        'Investment Account', 'Mortgage', 'Personal Loan',
        'Insurance', 'Business Account'
    }

    missing_products = potential_products - current_products

    # Product recommendations based on profile
    if 'Investment Account' in missing_products and customer_data['income'] > 80000:
        recommendations.append({
            'type': 'product',
            'title': 'Investment Account',
            'description': 'Based on your income level, you might benefit from our investment services.'
        })

    if 'Credit Card' in missing_products and customer_data.get('credit_score', 700) > 700:
        recommendations.append({
            'type': 'product',
            'title': 'Premium Credit Card',
            'description': 'Your excellent credit score qualifies you for our premium credit card.'
        })

    # Digital engagement recommendations
    if customer_data['digital_engagement'] == 'Low':
        recommendations.append({
            'type': 'service',
            'title': 'Digital Banking',
            'description': 'Discover the convenience of our CommBank app and NetBank services.'
        })

    # Transaction-based recommendations
    if customer_data.get('international_transaction_ratio', 0) > 0.2:
        recommendations.append({
            'type': 'service',
            'title': 'International Banking',
            'description': 'Our international banking services can help you save on overseas transactions.'
        })

    return recommendations


def calculate_metrics(customer_data: pd.Series) -> Dict[str, float]:
    """Calculate customer metrics"""
    # Calculate customer value
    monthly_value = float(customer_data['average_transaction']) * float(customer_data['transaction_frequency'])

    segment_multiplier = {
        'Premium': 1.5,
        'Standard': 1.0,
        'Basic': 0.8
    }.get(customer_data['customer_segment'], 1.0)

    engagement_multiplier = {
        'High': 1.2,
        'Medium': 1.0,
        'Low': 0.8
    }.get(customer_data['digital_engagement'], 1.0)

    customer_value = monthly_value * segment_multiplier * engagement_multiplier

    # Calculate churn risk
    churn_risk = 0
    if customer_data['transaction_frequency'] < 10:
        churn_risk += 30
    if customer_data['digital_engagement'] == 'Low':
        churn_risk += 30
    if len(customer_data['product_holdings']) < 2:
        churn_risk += 20

    # Calculate opportunity score
    opportunity_score = 0
    if customer_data['income'] > 100000:
        opportunity_score += 30
    opportunity_score += (8 - len(customer_data['product_holdings'])) * 5
    if customer_data['digital_engagement'] == 'High':
        opportunity_score += 20

    return {
        'customer_value': customer_value,
        'churn_risk': min(churn_risk, 100),
        'opportunity_score': min(opportunity_score, 100)
    }

@async_cache_data(ttl=3600)
def create_customer_insights(customer_data: pd.Series) -> Optional[Dict[str, Any]]:
    """
    Generate comprehensive customer insights

    Args:
        customer_data (pd.Series): Customer data series

    Returns:
        Optional[Dict[str, Any]]: Generated insights or None if generation fails
    """
    try:
        # Generate all visualizations
        transaction_pattern = create_transaction_pattern(customer_data)
        product_usage = create_product_usage(customer_data)
        engagement_radar = create_engagement_radar(customer_data)

        # Generate recommendations
        recommendations = generate_recommendations(customer_data)

        # Calculate metrics
        metrics = calculate_metrics(customer_data)

        # Compile all insights
        insights = {
            'visualizations': {
                'transaction_pattern': transaction_pattern,
                'product_usage': product_usage,
                'engagement_radar': engagement_radar
            },
            'recommendations': recommendations,
            'metrics': metrics,
            'summary': {
                'segment': customer_data['customer_segment'],
                'engagement_level': customer_data['digital_engagement'],
                'products_held': len(customer_data['product_holdings']),
                'generated_at': datetime.now().isoformat()
            }
        }

        return insights

    except Exception as e:
        st.error(f"Error generating customer insights: {str(e)}")
        return None