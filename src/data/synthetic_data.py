import pandas as pd
import numpy as np
from faker import Faker
import random
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import streamlit as st
from config.settings import DATA_SETTINGS

# Initialize Faker
fake = Faker()


class CustomerDataGenerator:
    def __init__(self):
        """Initialize data generation parameters"""
        self.interests = [
            'Travel', 'Investment', 'Shopping', 'Technology', 'Education',
            'Real Estate', 'Luxury', 'Family', 'Retirement', 'Small Business',
            'International Banking', 'Cryptocurrency', 'Sustainable Banking',
            'Health & Insurance', 'Arts & Culture'
        ]

        self.channels = [
            'Email', 'SMS', 'Mobile App', 'Web', 'Social Media',
            'Push Notification', 'Branch Visit', 'Phone Banking'
        ]

        self.life_stages = [
            'Student', 'Young Professional', 'Family Builder',
            'Mid-Career', 'Pre-retirement', 'Retired'
        ]

        self.occupations = [
            'Software Engineer', 'Doctor', 'Teacher', 'Business Owner',
            'Sales Manager', 'Financial Analyst', 'Marketing Manager',
            'Lawyer', 'Architect', 'Consultant', 'Engineer', 'Professor',
            'Small Business Owner', 'Executive', 'Freelancer'
        ]

        self.products = [
            'Savings Account', 'Checking Account', 'Credit Card',
            'Investment Account', 'Mortgage', 'Personal Loan',
            'Insurance', 'Business Account'
        ]

    def _generate_income(self, age: int, occupation: str) -> float:
        """Generate realistic income based on age and occupation"""
        base_income = random.uniform(30000, 80000)

        # Age multiplier
        age_multiplier = 1.0
        if age < 25:
            age_multiplier = 0.7
        elif age < 35:
            age_multiplier = 1.0
        elif age < 45:
            age_multiplier = 1.3
        elif age < 55:
            age_multiplier = 1.5
        else:
            age_multiplier = 1.4

        # Occupation multiplier
        occupation_multipliers = {
            'Software Engineer': 1.4,
            'Doctor': 1.8,
            'Business Owner': 1.6,
            'Financial Analyst': 1.3,
            'Lawyer': 1.7,
            'Executive': 2.0,
            'Professor': 1.3,
            'Teacher': 0.9,
            'Freelancer': 0.8
        }

        occupation_multiplier = occupation_multipliers.get(occupation, 1.0)

        return round(base_income * age_multiplier * occupation_multiplier, -3)

    def _determine_life_stage(self, age: int) -> str:
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

    def _determine_segment(self, income: float,
                           product_holdings: int,
                           relationship_tenure: int) -> str:
        """Determine customer segment based on various factors"""
        points = 0

        # Income points
        if income > 150000:
            points += 3
        elif income > 80000:
            points += 2
        elif income > 50000:
            points += 1

        # Product holdings points
        points += min(product_holdings, 4)

        # Tenure points
        points += min(relationship_tenure // 2, 3)

        # Determine segment
        if points >= 7:
            return 'Premium'
        elif points >= 4:
            return 'Standard'
        else:
            return 'Basic'

    def _generate_transaction_patterns(self) -> Dict[str, float]:
        """Generate realistic transaction patterns"""
        return {
            'transaction_frequency': random.randint(5, 30),
            'average_transaction': round(random.uniform(50, 5000), 2),
            'online_transactions_ratio': random.uniform(0.3, 0.9),
            'international_transactions_ratio': random.uniform(0, 0.3)
        }

    def _generate_product_holdings(self, age: int, income: float) -> List[str]:
        """Generate realistic product holdings based on customer profile"""
        base_products = ['Savings Account', 'Checking Account']
        additional_products = []

        # Credit Card
        if income > 30000:
            base_products.append('Credit Card')

        # Investment Account
        if income > 80000 or age > 35:
            additional_products.append('Investment Account')

        # Mortgage
        if age > 30 and income > 60000:
            additional_products.append('Mortgage')

        # Insurance
        if age > 25:
            additional_products.append('Insurance')

        # Business Account
        if random.random() < 0.2:
            additional_products.append('Business Account')

        # Randomly select additional products
        num_additional = random.randint(0, len(additional_products))
        selected_products = base_products + random.sample(additional_products, num_additional)

        return selected_products

    def generate_customer(self) -> Dict[str, Any]:
        """Generate a single customer record"""
        age = random.randint(18, 75)
        occupation = random.choice(self.occupations)
        income = self._generate_income(age, occupation)
        relationship_tenure = min(random.randint(0, 20), age - 18)
        product_holdings = self._generate_product_holdings(age, income)

        transaction_patterns = self._generate_transaction_patterns()
        digital_engagement = 'High' if transaction_patterns['online_transactions_ratio'] > 0.7 else \
            'Medium' if transaction_patterns['online_transactions_ratio'] > 0.4 else 'Low'

        customer = {
            'customer_id': fake.uuid4(),
            'age': age,
            'gender': random.choice(['M', 'F']),
            'location': fake.city(),
            'income': income,
            'occupation': occupation,
            'life_stage': self._determine_life_stage(age),
            'customer_segment': self._determine_segment(income, len(product_holdings), relationship_tenure),
            'relationship_tenure': relationship_tenure,
            'product_holdings': product_holdings,
            'num_products': len(product_holdings),
            'primary_interests': random.sample(self.interests, k=random.randint(2, 5)),
            'preferred_channels': random.sample(self.channels, k=random.randint(2, 4)),
            'digital_engagement': digital_engagement,
            'transaction_frequency': transaction_patterns['transaction_frequency'],
            'average_transaction': transaction_patterns['average_transaction'],
            'online_transaction_ratio': transaction_patterns['online_transactions_ratio'],
            'international_transaction_ratio': transaction_patterns['international_transactions_ratio'],
            'credit_score': random.randint(300, 850),
            'last_interaction': (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
            'satisfaction_score': random.randint(1, 100)
        }

        return customer

    def generate_dataset(self, num_records: int) -> pd.DataFrame:
        """Generate a dataset with specified number of records"""
        customers = [self.generate_customer() for _ in range(num_records)]
        return pd.DataFrame(customers)


def init_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.customer_data = None
        st.session_state.api_tested = False


def generate_synthetic_data(num_records: int = 100) -> Optional[pd.DataFrame]:
    """
    Generate synthetic customer data

    Args:
        num_records (int): Number of records to generate

    Returns:
        Optional[pd.DataFrame]: Generated customer data or None if generation fails
    """
    try:
        if num_records < DATA_SETTINGS['min_records'] or num_records > DATA_SETTINGS['max_records']:
            st.error(f"Number of records must be between {DATA_SETTINGS['min_records']} "
                     f"and {DATA_SETTINGS['max_records']}")
            return None

        generator = CustomerDataGenerator()
        data = generator.generate_dataset(num_records)

        # Add some random correlations and patterns
        data['engagement_score'] = (data['transaction_frequency'] * 0.3 +
                                    data['num_products'] * 0.3 +
                                    data['satisfaction_score'] * 0.4)

        data['churn_risk'] = 100 - data['engagement_score']

        return data

    except Exception as e:
        st.error(f"Error generating synthetic data: {str(e)}")
        return None