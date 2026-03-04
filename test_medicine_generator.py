"""
Unit tests for medicine_generator module
"""

import pytest
import pandas as pd
import numpy as np
from medicine_generator import generate_medicines, DISEASES


def test_generate_medicines_default():
    """Test generating default 50 medicines"""
    medicines = generate_medicines()
    
    assert len(medicines) == 50
    assert isinstance(medicines, pd.DataFrame)


def test_generate_medicines_custom_count():
    """Test generating custom number of medicines"""
    medicines = generate_medicines(n=100)
    
    assert len(medicines) == 100


def test_medicine_columns():
    """Test that all required columns are present"""
    medicines = generate_medicines(n=10)
    
    required_columns = [
        'medicine_id',
        'target_disease',
        'price_inr',
        'brand_strength',
        'side_effect_risk',
        'availability_score',
        'insurance_compatibility'
    ]
    
    for col in required_columns:
        assert col in medicines.columns, f"Missing column: {col}"


def test_medicine_id_format():
    """Test medicine ID format (MED_001, MED_002, etc.)"""
    medicines = generate_medicines(n=5)
    
    assert medicines.iloc[0]['medicine_id'] == 'MED_001'
    assert medicines.iloc[4]['medicine_id'] == 'MED_005'


def test_target_disease_valid():
    """Test that target diseases are from the valid list"""
    medicines = generate_medicines(n=50)
    
    for disease in medicines['target_disease']:
        assert disease in DISEASES


def test_price_range():
    """Test that prices are within ₹50-₹5000 range"""
    medicines = generate_medicines(n=50)
    
    assert medicines['price_inr'].min() >= 50
    assert medicines['price_inr'].max() <= 5000


def test_score_ranges():
    """Test that all scores are between 0 and 1"""
    medicines = generate_medicines(n=50)
    
    score_columns = [
        'brand_strength',
        'side_effect_risk',
        'availability_score',
        'insurance_compatibility'
    ]
    
    for col in score_columns:
        assert medicines[col].min() >= 0, f"{col} has values below 0"
        assert medicines[col].max() <= 1, f"{col} has values above 1"


def test_side_effect_risk_distribution():
    """Test that side effect risk is skewed to low risk (beta distribution)"""
    medicines = generate_medicines(n=100)
    
    # With beta(2, 5), mean should be around 0.286
    # Most values should be below 0.5
    low_risk_count = (medicines['side_effect_risk'] < 0.5).sum()
    
    assert low_risk_count > 60, "Side effect risk should be skewed to low risk"


def test_price_log_normal_distribution():
    """Test that prices follow log-normal distribution"""
    medicines = generate_medicines(n=100)
    
    # Log-normal distribution should have more lower prices than higher prices
    median_price = medicines['price_inr'].median()
    mean_price = medicines['price_inr'].mean()
    
    # Mean should be higher than median for log-normal distribution
    assert mean_price > median_price


def test_reproducibility():
    """Test that generation is reproducible with same seed"""
    medicines1 = generate_medicines(n=10)
    medicines2 = generate_medicines(n=10)
    
    # Should be identical due to seed
    pd.testing.assert_frame_equal(medicines1, medicines2)


def test_no_missing_values():
    """Test that there are no missing values"""
    medicines = generate_medicines(n=50)
    
    assert medicines.isnull().sum().sum() == 0


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
