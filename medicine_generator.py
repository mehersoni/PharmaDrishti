"""
Medicine Generator Module

Generates synthetic medicine profiles for PharmaDrishti simulation.
"""

import numpy as np
import pandas as pd

# List of target diseases
DISEASES = [
    'Type 2 Diabetes',
    'Hypertension',
    'Asthma',
    'Arthritis',
    'Heart Disease',
    'Thyroid Disorder',
    'Chronic Kidney Disease',
    'Obesity',
    'Anemia',
    'COPD'
]


def generate_medicines(n=5000):
    """
    Generate synthetic medicine profiles with realistic distributions.
    
    Parameters:
    -----------
    n : int, default=5000
        Number of medicine profiles to generate (increased for 500k interactions)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing medicine profiles with columns:
        - medicine_id: Unique identifier (e.g., MED_00001)
        - target_disease: Disease the medicine treats
        - batch_price_inr: Batch price in Indian Rupees (₹5000-₹500000, log-normal distribution)
        - side_effect_risk: Side effect risk score (0-1, beta distribution skewed to low risk)
        - manufacturing_score: Manufacturing capability score (0-1)
        - insurance_compatibility: Insurance compatibility score (0-1)
    
    Example:
    --------
    >>> medicines = generate_medicines(5000)
    >>> print(f"Generated {len(medicines)} medicines")
    >>> print(medicines.head())
    """
    np.random.seed(42)  # For reproducibility
    
    medicines = []
    
    for i in range(n):
        medicine = {
            'medicine_id': f'MED_{i+1:05d}',
            'target_disease': np.random.choice(DISEASES),
            'batch_price_inr': np.clip(np.random.lognormal(mean=10, sigma=1.5), 5000, 500000),
            'side_effect_risk': np.random.beta(a=2, b=5),  # Skewed to low risk
            'manufacturing_score': np.random.uniform(0, 1),
            'insurance_compatibility': np.random.uniform(0, 1)
        }
        medicines.append(medicine)
    
    return pd.DataFrame(medicines)
