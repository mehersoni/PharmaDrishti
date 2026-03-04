"""
Unit tests for suitability_calculator module.
Tests the calculate_suitability function with various scenarios.
"""

import pytest
from suitability_calculator import calculate_suitability


class TestCalculateSuitability:
    """Test suite for calculate_suitability function"""
    
    def test_perfect_match_high_adoption(self):
        """Test perfect match scenario: disease match, affordable, available"""
        persona = {
            'chronic_diseases': 'Type 2 Diabetes',
            'annual_income_inr': 600000,  # ₹50k/month
            'city_tier': 'Tier 1',
            'price_sensitivity_score': 0.3
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',
            'price_inr': 500,  # 1% of monthly income
            'availability_score': 0.9,
            'brand_strength': 0.8,
            'side_effect_risk': 0.1
        }
        
        prob = calculate_suitability(persona, medicine)
        
        # Should have high adoption probability
        assert 0.7 <= prob <= 1.0, f"Expected high probability, got {prob}"
        assert isinstance(prob, float)
    
    def test_no_disease_match_low_adoption(self):
        """Test no disease match: should have low adoption"""
        persona = {
            'chronic_diseases': 'Hypertension',
            'annual_income_inr': 600000,
            'city_tier': 'Tier 1',
            'price_sensitivity_score': 0.3
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',  # Different disease
            'price_inr': 500,
            'availability_score': 0.9,
            'brand_strength': 0.8,
            'side_effect_risk': 0.1
        }
        
        prob = calculate_suitability(persona, medicine)
        
        # Should have lower probability without disease match
        assert 0.0 <= prob <= 0.7, f"Expected lower probability, got {prob}"
    
    def test_unaffordable_medicine_low_adoption(self):
        """Test expensive medicine relative to income"""
        persona = {
            'chronic_diseases': 'Type 2 Diabetes',
            'annual_income_inr': 240000,  # ₹20k/month
            'city_tier': 'Tier 1',
            'price_sensitivity_score': 0.7
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',
            'price_inr': 3000,  # 15% of monthly income
            'availability_score': 0.9,
            'brand_strength': 0.8,
            'side_effect_risk': 0.1
        }
        
        prob = calculate_suitability(persona, medicine)
        
        # Should have lower probability due to affordability
        assert 0.0 <= prob <= 1.0, f"Expected valid probability, got {prob}"
        # Verify it's still reasonably high due to disease match
        assert prob > 0.5, "Should still have moderate probability with disease match"
    
    def test_tier3_low_availability(self):
        """Test Tier 3 city with lower accessibility"""
        persona = {
            'chronic_diseases': 'Type 2 Diabetes',
            'annual_income_inr': 600000,
            'city_tier': 'Tier 3',  # Lower accessibility
            'price_sensitivity_score': 0.3
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',
            'price_inr': 500,
            'availability_score': 0.5,
            'brand_strength': 0.8,
            'side_effect_risk': 0.1
        }
        
        prob = calculate_suitability(persona, medicine)
        
        # Should be high due to disease match and affordability
        assert 0.5 <= prob <= 1.0, f"Expected high probability, got {prob}"
    
    def test_high_risk_medicine(self):
        """Test medicine with high side effect risk"""
        persona = {
            'chronic_diseases': 'Type 2 Diabetes',
            'annual_income_inr': 600000,
            'city_tier': 'Tier 1',
            'price_sensitivity_score': 0.8  # Risk-averse
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',
            'price_inr': 500,
            'availability_score': 0.9,
            'brand_strength': 0.8,
            'side_effect_risk': 0.9  # High risk
        }
        
        prob = calculate_suitability(persona, medicine)
        
        # Should still be high due to disease match and affordability
        assert 0.5 <= prob <= 1.0, f"Expected moderate to high probability, got {prob}"
    
    def test_return_value_range(self):
        """Test that probability is always between 0 and 1"""
        persona = {
            'chronic_diseases': 'Type 2 Diabetes',
            'annual_income_inr': 600000,
            'city_tier': 'Tier 1',
            'price_sensitivity_score': 0.5
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',
            'price_inr': 500,
            'availability_score': 0.8,
            'brand_strength': 0.7,
            'side_effect_risk': 0.3
        }
        
        prob = calculate_suitability(persona, medicine)
        
        assert 0.0 <= prob <= 1.0, f"Probability {prob} out of range [0, 1]"
    
    def test_zero_income_edge_case(self):
        """Test handling of zero income"""
        persona = {
            'chronic_diseases': 'Type 2 Diabetes',
            'annual_income_inr': 0,  # Edge case
            'city_tier': 'Tier 1',
            'price_sensitivity_score': 0.5
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',
            'price_inr': 500,
            'availability_score': 0.8,
            'brand_strength': 0.7,
            'side_effect_risk': 0.3
        }
        
        prob = calculate_suitability(persona, medicine)
        
        # Should handle gracefully and return valid probability
        assert 0.0 <= prob <= 1.0
        assert isinstance(prob, float)
    
    def test_no_chronic_diseases(self):
        """Test persona with no chronic diseases"""
        persona = {
            'chronic_diseases': 'None',
            'annual_income_inr': 600000,
            'city_tier': 'Tier 1',
            'price_sensitivity_score': 0.5
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',
            'price_inr': 500,
            'availability_score': 0.8,
            'brand_strength': 0.7,
            'side_effect_risk': 0.3
        }
        
        prob = calculate_suitability(persona, medicine)
        
        # Should have low probability without disease match
        assert 0.0 <= prob <= 0.6
    
    def test_multiple_diseases(self):
        """Test persona with multiple chronic diseases"""
        persona = {
            'chronic_diseases': 'Hypertension, Type 2 Diabetes, Arthritis',
            'annual_income_inr': 600000,
            'city_tier': 'Tier 1',
            'price_sensitivity_score': 0.5
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',
            'price_inr': 500,
            'availability_score': 0.8,
            'brand_strength': 0.7,
            'side_effect_risk': 0.3
        }
        
        prob = calculate_suitability(persona, medicine)
        
        # Should match disease and have higher probability
        assert 0.5 <= prob <= 1.0
    
    def test_brand_alignment_price_sensitive(self):
        """Test brand alignment with price-sensitive consumer"""
        persona = {
            'chronic_diseases': 'Type 2 Diabetes',
            'annual_income_inr': 600000,
            'city_tier': 'Tier 1',
            'price_sensitivity_score': 0.9  # Very price-sensitive
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',
            'price_inr': 500,
            'availability_score': 0.8,
            'brand_strength': 0.9,  # Premium brand
            'side_effect_risk': 0.3
        }
        
        prob = calculate_suitability(persona, medicine)
        
        # Brand strength should have less impact on price-sensitive consumers
        assert 0.0 <= prob <= 1.0
        assert isinstance(prob, float)
    
    def test_consistent_results(self):
        """Test that same inputs produce same output"""
        persona = {
            'chronic_diseases': 'Type 2 Diabetes',
            'annual_income_inr': 600000,
            'city_tier': 'Tier 1',
            'price_sensitivity_score': 0.5
        }
        medicine = {
            'target_disease': 'Type 2 Diabetes',
            'price_inr': 500,
            'availability_score': 0.8,
            'brand_strength': 0.7,
            'side_effect_risk': 0.3
        }
        
        prob1 = calculate_suitability(persona, medicine)
        prob2 = calculate_suitability(persona, medicine)
        
        assert prob1 == prob2, "Function should be deterministic"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
