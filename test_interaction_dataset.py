"""
Unit tests for create_interaction_dataset function.
Tests the generation of persona-medicine interaction pairs with features.
"""

import pytest
import pandas as pd
import numpy as np
from suitability_calculator import create_interaction_dataset
from data_loader import load_personas
from medicine_generator import generate_medicines


class TestCreateInteractionDataset:
    """Test suite for create_interaction_dataset function"""
    
    def test_interaction_count(self):
        """Test that correct number of interactions are generated"""
        # Create small test datasets
        personas = load_personas()
        medicines = generate_medicines(n=50)
        
        interactions = create_interaction_dataset(personas, medicines)
        
        expected_count = len(personas) * len(medicines)
        assert len(interactions) == expected_count, \
            f"Expected {expected_count} interactions, got {len(interactions)}"
    
    def test_required_columns(self):
        """Test that all required columns are present"""
        personas = load_personas()
        medicines = generate_medicines(n=10)
        
        interactions = create_interaction_dataset(personas, medicines)
        
        required_columns = [
            'persona_id', 'medicine_id', 'suitability_score',
            'age', 'income', 'city_tier_encoded', 'chronic_condition_count',
            'price_sensitivity', 'monthly_healthcare_spend',
            'price', 'brand_strength', 'side_effect_risk',
            'availability', 'insurance_compatibility',
            'disease_match', 'affordability', 'availability_match',
            'brand_alignment', 'risk_score'
        ]
        
        for col in required_columns:
            assert col in interactions.columns, f"Missing column: {col}"
    
    def test_suitability_score_range(self):
        """Test that suitability scores are between 0 and 1"""
        personas = load_personas()
        medicines = generate_medicines(n=10)
        
        interactions = create_interaction_dataset(personas, medicines)
        
        assert interactions['suitability_score'].min() >= 0.0
        assert interactions['suitability_score'].max() <= 1.0
    
    def test_city_tier_encoding(self):
        """Test that city tiers are properly encoded"""
        personas = load_personas()
        medicines = generate_medicines(n=10)
        
        interactions = create_interaction_dataset(personas, medicines)
        
        # City tier should be encoded as 1, 2, or 3
        unique_tiers = interactions['city_tier_encoded'].unique()
        assert all(tier in [1, 2, 3] for tier in unique_tiers)
    
    def test_disease_match_binary(self):
        """Test that disease match is binary (0 or 1)"""
        personas = load_personas()
        medicines = generate_medicines(n=10)
        
        interactions = create_interaction_dataset(personas, medicines)
        
        unique_values = interactions['disease_match'].unique()
        assert all(val in [0.0, 1.0] for val in unique_values)
    
    def test_affordability_range(self):
        """Test that affordability scores are between 0 and 1"""
        personas = load_personas()
        medicines = generate_medicines(n=10)
        
        interactions = create_interaction_dataset(personas, medicines)
        
        assert interactions['affordability'].min() >= 0.0
        assert interactions['affordability'].max() <= 1.0
    
    def test_no_missing_values(self):
        """Test that there are no missing values in critical columns"""
        personas = load_personas()
        medicines = generate_medicines(n=10)
        
        interactions = create_interaction_dataset(personas, medicines)
        
        critical_columns = [
            'persona_id', 'medicine_id', 'suitability_score',
            'age', 'income', 'price'
        ]
        
        for col in critical_columns:
            assert interactions[col].isnull().sum() == 0, \
                f"Column {col} has missing values"
    
    def test_feature_types(self):
        """Test that features have correct data types"""
        personas = load_personas()
        medicines = generate_medicines(n=10)
        
        interactions = create_interaction_dataset(personas, medicines)
        
        # Numeric features
        numeric_features = [
            'age', 'income', 'price', 'suitability_score',
            'affordability', 'brand_strength'
        ]
        
        for col in numeric_features:
            assert pd.api.types.is_numeric_dtype(interactions[col]), \
                f"Column {col} should be numeric"
    
    def test_interaction_uniqueness(self):
        """Test that each persona-medicine pair appears exactly once"""
        personas = load_personas()
        medicines = generate_medicines(n=10)
        
        interactions = create_interaction_dataset(personas, medicines)
        
        # Check for duplicate persona-medicine pairs
        duplicates = interactions.duplicated(subset=['persona_id', 'medicine_id']).sum()
        assert duplicates == 0, f"Found {duplicates} duplicate persona-medicine pairs"
    
    def test_small_dataset(self):
        """Test with minimal dataset (2 personas, 3 medicines)"""
        # Create minimal test data
        personas = pd.DataFrame([
            {
                'name': 'Persona1',
                'age': 30,
                'annual_income_inr': 600000,
                'city_tier': 'Tier 1',
                'price_sensitivity_score': 0.3,
                'chronic_diseases': 'Type 2 Diabetes',
                'no_of_chronic_conditions': 1,
                'monthly_healthcare_spend_inr': 2000
            },
            {
                'name': 'Persona2',
                'age': 45,
                'annual_income_inr': 300000,
                'city_tier': 'Tier 2',
                'price_sensitivity_score': 0.7,
                'chronic_diseases': 'Hypertension',
                'no_of_chronic_conditions': 1,
                'monthly_healthcare_spend_inr': 1500
            }
        ])
        
        medicines = pd.DataFrame([
            {
                'medicine_id': 'MED_001',
                'target_disease': 'Type 2 Diabetes',
                'price_inr': 500,
                'brand_strength': 0.7,
                'side_effect_risk': 0.2,
                'availability_score': 0.8,
                'insurance_compatibility': 0.9
            },
            {
                'medicine_id': 'MED_002',
                'target_disease': 'Hypertension',
                'price_inr': 300,
                'brand_strength': 0.5,
                'side_effect_risk': 0.1,
                'availability_score': 0.9,
                'insurance_compatibility': 0.8
            },
            {
                'medicine_id': 'MED_003',
                'target_disease': 'Asthma',
                'price_inr': 1000,
                'brand_strength': 0.8,
                'side_effect_risk': 0.3,
                'availability_score': 0.7,
                'insurance_compatibility': 0.6
            }
        ])
        
        interactions = create_interaction_dataset(personas, medicines)
        
        # Should have 2 × 3 = 6 interactions
        assert len(interactions) == 6
        
        # Check that all combinations exist
        persona_ids = set(interactions['persona_id'])
        medicine_ids = set(interactions['medicine_id'])
        
        # Persona IDs now include index: Persona1_0, Persona2_1
        assert persona_ids == {'Persona1_0', 'Persona2_1'}
        assert medicine_ids == {'MED_001', 'MED_002', 'MED_003'}
    
    def test_success_criteria_5000_pairs(self):
        """Test success criteria: Can generate 5,000 interaction pairs (100 personas × 50 medicines)"""
        personas = load_personas()
        medicines = generate_medicines(n=50)
        
        interactions = create_interaction_dataset(personas, medicines)
        
        # Success criteria: 5,000 interaction pairs
        assert len(interactions) == 5000, \
            f"Expected 5,000 interaction pairs, got {len(interactions)}"
        
        # Verify all required features are present
        assert 'suitability_score' in interactions.columns
        assert 'age' in interactions.columns
        assert 'income' in interactions.columns
        assert 'price' in interactions.columns
        assert 'brand_strength' in interactions.columns
        
        print(f"✓ Successfully generated {len(interactions)} interaction pairs")
        print(f"✓ Personas: {len(personas)}, Medicines: {len(medicines)}")
        print(f"✓ Features: {len(interactions.columns)} columns")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
