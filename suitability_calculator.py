"""
Suitability Calculator Module

Calculates adoption probability for persona-medicine pairs using a weighted formula.
This is the core logic for generating training data for the ML model.
"""

import math
import pandas as pd
import numpy as np


def calculate_suitability(persona, medicine, market_data=None):
    """
    Calculate adoption probability for a persona-medicine pair.
    
    Uses a weighted formula considering:
    - Disease match (30%): Binary match between medicine disease and persona conditions
    - Affordability (25%): Price relative to persona income
    - Market pricing (20%): Price competitiveness vs market alternatives
    - Availability (15%): Medicine availability × persona location accessibility
    - Risk tolerance (10%): Side effect risk × persona risk aversion
    
    Parameters:
    -----------
    persona : dict or pd.Series
        Persona data containing:
        - chronic_diseases: str (comma-separated or "None")
        - annual_income_inr: float
        - city_tier: str ("Tier 1", "Tier 2", "Tier 3")
        - price_sensitivity_score: float (0-1)
    
    medicine : dict or pd.Series
        Medicine profile containing:
        - target_disease: str
        - batch_price_inr: float
        - manufacturing_score: float (0-1)
        - side_effect_risk: float (0-1)
    
    market_data : pd.DataFrame, optional
        Market pricing data for competitive analysis
    
    Returns:
    --------
    float
        Adoption probability between 0 and 1
    """
    # 1. Disease Match (30% weight) - Reduced from 35%
    persona_diseases = str(persona.get('chronic_diseases', '')).lower()
    target_disease = str(medicine.get('target_disease', '')).lower()
    
    disease_match = 1.0 if target_disease in persona_diseases else 0.0
    
    # 2. Affordability (25% weight)
    monthly_income = persona.get('annual_income_inr', 0) / 12
    batch_price = medicine.get('batch_price_inr', 0)
    
    if monthly_income > 0:
        affordability = max(0.0, 1.0 - (batch_price / (monthly_income * 100)))
        affordability = min(1.0, affordability)
    else:
        affordability = 0.0
    
    # 3. Market Pricing Competitiveness (20% weight) - NEW
    market_pricing_score = 0.5  # Default neutral score
    
    if market_data is not None and not market_data.empty:
        try:
            # Find similar medicines in market
            disease_keywords = target_disease.split()
            similar_medicines = market_data[
                market_data['medicine_name'].str.contains('|'.join(disease_keywords), case=False, na=False)
            ]
            
            if len(similar_medicines) > 0:
                market_prices = similar_medicines['price_numeric'].dropna()
                if len(market_prices) > 0:
                    avg_market_price = market_prices.mean()
                    
                    # Calculate competitiveness score
                    if avg_market_price > 0:
                        price_ratio = batch_price / avg_market_price
                        
                        # Score based on price position:
                        # - Much cheaper (< 0.7): 1.0 (very competitive)
                        # - Competitive (0.7-1.3): 0.8-0.6 (good)
                        # - Expensive (1.3-2.0): 0.6-0.2 (poor)
                        # - Very expensive (> 2.0): 0.1 (very poor)
                        
                        if price_ratio < 0.7:
                            market_pricing_score = 1.0
                        elif price_ratio < 1.3:
                            # Linear interpolation between 1.0 and 0.6
                            market_pricing_score = 1.0 - (price_ratio - 0.7) * (0.4 / 0.6)
                        elif price_ratio < 2.0:
                            # Linear interpolation between 0.6 and 0.2
                            market_pricing_score = 0.6 - (price_ratio - 1.3) * (0.4 / 0.7)
                        else:
                            market_pricing_score = 0.1
        except Exception:
            # If market analysis fails, use neutral score
            market_pricing_score = 0.5
    
    # 4. Manufacturing (15% weight)
    tier_accessibility = {
        'Tier 1': 0.9,
        'Tier 2': 0.7,
        'Tier 3': 0.5
    }
    city_tier = persona.get('city_tier', 'Tier 3')
    location_factor = tier_accessibility.get(city_tier, 0.5)
    manufacturing = medicine.get('manufacturing_score', 0.5) * location_factor
    
    # 5. Risk Tolerance (10% weight) - Reduced from 25%
    side_effect_risk = medicine.get('side_effect_risk', 0.5)
    price_sensitivity = persona.get('price_sensitivity_score', 0.5)
    risk_score = side_effect_risk * price_sensitivity
    
    # Calculate weighted sum with new market pricing component
    weighted_sum = (
        0.30 * disease_match +
        0.25 * affordability +
        0.20 * market_pricing_score +
        0.15 * manufacturing +
        0.10 * (1 - risk_score)
    )
    
    # Apply sigmoid transformation to get probability (0-1)
    scaled_sum = (weighted_sum - 0.5) * 12
    probability = 1 / (1 + math.exp(-scaled_sum))
    
    return probability



def create_interaction_dataset(personas_df, medicines_df):
    """
    Create interaction dataset with all persona-medicine pairs.
    
    For each persona-medicine combination:
    - Calculate suitability score using calculate_suitability()
    - Extract features for ML training
    - Store in interaction record
    
    Parameters:
    -----------
    personas_df : pd.DataFrame
        DataFrame containing persona data with columns:
        - name, age, annual_income_inr, city_tier, price_sensitivity_score,
          chronic_diseases, no_of_chronic_conditions, etc.
    
    medicines_df : pd.DataFrame
        DataFrame containing medicine profiles with columns:
        - medicine_id, target_disease, batch_price_inr,
          side_effect_risk, manufacturing_score, insurance_compatibility
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with all interaction pairs containing:
        - persona_id: Persona identifier
        - medicine_id: Medicine identifier
        - suitability_score: Calculated adoption probability (0-1)
        - Feature columns for ML training (age, income, city_tier, price, etc.)
    
    Example:
    --------
    >>> personas = load_personas()
    >>> medicines = generate_medicines(5000)
    >>> interactions = create_interaction_dataset(personas, medicines)
    >>> print(f"Generated {len(interactions)} interaction pairs")
    >>> print(f"Expected: {len(personas)} × {len(medicines)} = {len(personas) * len(medicines)}")
    """
    interactions = []
    
    # Encoding mappings for categorical features
    tier_encoding = {'Tier 1': 1, 'Tier 2': 2, 'Tier 3': 3}
    
    # Create all persona-medicine pairs
    for persona_idx, persona in personas_df.iterrows():
        for medicine_idx, medicine in medicines_df.iterrows():
            # Calculate suitability score
            suitability = calculate_suitability(persona, medicine)
            
            # Calculate disease match (binary feature)
            persona_diseases = str(persona.get('chronic_diseases', '')).lower()
            target_disease = str(medicine.get('target_disease', '')).lower()
            disease_match = 1.0 if target_disease in persona_diseases else 0.0
            
            # Calculate affordability score
            monthly_income = persona.get('annual_income_inr', 0) / 12
            batch_price = medicine.get('batch_price_inr', 0)
            if monthly_income > 0:
                affordability = max(0.0, 1.0 - (batch_price / (monthly_income * 100)))
                affordability = min(1.0, affordability)
            else:
                affordability = 0.0
            
            # Calculate manufacturing match
            tier_accessibility = {'Tier 1': 0.9, 'Tier 2': 0.7, 'Tier 3': 0.5}
            city_tier = persona.get('city_tier', 'Tier 3')
            location_factor = tier_accessibility.get(city_tier, 0.5)
            manufacturing_match = medicine.get('manufacturing_score', 0.5) * location_factor
            
            # Calculate risk score
            risk_score = medicine.get('side_effect_risk', 0.5) * persona.get('price_sensitivity_score', 0.5)
            
            # Create interaction record with features
            # Use index-based ID to ensure uniqueness (names can be duplicated)
            persona_id = f"{persona.get('name', '')}_{persona_idx}"
            
            interaction = {
                # Identifiers
                'persona_id': persona_id,
                'medicine_id': medicine.get('medicine_id', ''),
                
                # Target variable
                'suitability_score': suitability,
                
                # Persona features
                'age': persona.get('age', 0),
                'income': persona.get('annual_income_inr', 0),
                'city_tier_encoded': tier_encoding.get(persona.get('city_tier', 'Tier 3'), 3),
                'chronic_condition_count': persona.get('no_of_chronic_conditions', 0),
                'price_sensitivity': persona.get('price_sensitivity_score', 0.5),
                'monthly_healthcare_spend': persona.get('monthly_healthcare_spend_inr', 0),
                
                # Medicine features
                'price': medicine.get('batch_price_inr', 0),
                'side_effect_risk': medicine.get('side_effect_risk', 0.5),
                'manufacturing': medicine.get('manufacturing_score', 0.5),
                'insurance_compatibility': medicine.get('insurance_compatibility', 0.5),
                
                # Interaction features (calculated scores)
                'disease_match': disease_match,
                'affordability': affordability,
                'manufacturing_match': manufacturing_match,
                'risk_score': risk_score
            }
            
            interactions.append(interaction)
    
    return pd.DataFrame(interactions)
