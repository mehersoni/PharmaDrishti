"""
Verification script for suitability_calculator.
Tests the function with realistic scenarios and displays results.
"""

from suitability_calculator import calculate_suitability
import pandas as pd
from data_loader import load_personas
from medicine_generator import generate_medicines


def verify_suitability_calculator():
    """Verify suitability calculator with real data"""
    
    print("=" * 70)
    print("Suitability Calculator Verification")
    print("=" * 70)
    
    # Load real personas
    personas_df = load_personas('data/indian_healthcare_personas.json')
    if personas_df.empty:
        print("Error: Could not load personas")
        return
    
    # Generate medicines
    medicines_df = generate_medicines(10)
    
    print(f"\nLoaded {len(personas_df)} personas and {len(medicines_df)} medicines")
    
    # Test with a few persona-medicine pairs
    print("\n" + "=" * 70)
    print("Sample Suitability Calculations")
    print("=" * 70)
    
    # Test 1: Perfect match
    persona1 = personas_df.iloc[1].to_dict()  # Priya Nair with Hypertension
    medicine1 = {
        'target_disease': 'Hypertension',
        'price_inr': 300,
        'availability_score': 0.8,
        'brand_strength': 0.6,
        'side_effect_risk': 0.2
    }
    
    prob1 = calculate_suitability(persona1, medicine1)
    print(f"\nTest 1: Good Match")
    print(f"  Persona: {persona1['name']}, {persona1['chronic_diseases']}")
    print(f"  Medicine: {medicine1['target_disease']}, ₹{medicine1['price_inr']}")
    print(f"  Suitability: {prob1:.3f}")
    
    # Test 2: No disease match
    medicine2 = {
        'target_disease': 'Type 2 Diabetes',
        'price_inr': 300,
        'availability_score': 0.8,
        'brand_strength': 0.6,
        'side_effect_risk': 0.2
    }
    
    prob2 = calculate_suitability(persona1, medicine2)
    print(f"\nTest 2: No Disease Match")
    print(f"  Persona: {persona1['name']}, {persona1['chronic_diseases']}")
    print(f"  Medicine: {medicine2['target_disease']}, ₹{medicine2['price_inr']}")
    print(f"  Suitability: {prob2:.3f}")
    
    # Test 3: Expensive medicine
    medicine3 = {
        'target_disease': 'Hypertension',
        'price_inr': 3000,
        'availability_score': 0.8,
        'brand_strength': 0.9,
        'side_effect_risk': 0.1
    }
    
    prob3 = calculate_suitability(persona1, medicine3)
    print(f"\nTest 3: Expensive Medicine")
    print(f"  Persona: {persona1['name']}, Income: ₹{persona1['annual_income_inr']}/year")
    print(f"  Medicine: {medicine3['target_disease']}, ₹{medicine3['price_inr']}")
    print(f"  Suitability: {prob3:.3f}")
    
    # Calculate suitability for all persona-medicine pairs
    print("\n" + "=" * 70)
    print("Distribution Analysis")
    print("=" * 70)
    
    results = []
    for _, persona in personas_df.head(20).iterrows():
        for _, medicine in medicines_df.iterrows():
            prob = calculate_suitability(persona.to_dict(), medicine.to_dict())
            results.append({
                'persona_id': persona['name'],
                'medicine_id': medicine['medicine_id'],
                'disease_match': medicine['target_disease'] in str(persona['chronic_diseases']),
                'probability': prob
            })
    
    results_df = pd.DataFrame(results)
    
    print(f"\nTotal calculations: {len(results_df)}")
    print(f"\nProbability Statistics:")
    print(f"  Mean: {results_df['probability'].mean():.3f}")
    print(f"  Median: {results_df['probability'].median():.3f}")
    print(f"  Min: {results_df['probability'].min():.3f}")
    print(f"  Max: {results_df['probability'].max():.3f}")
    print(f"  Std Dev: {results_df['probability'].std():.3f}")
    
    print(f"\nWith Disease Match:")
    matched = results_df[results_df['disease_match'] == True]
    if len(matched) > 0:
        print(f"  Count: {len(matched)}")
        print(f"  Mean Probability: {matched['probability'].mean():.3f}")
    else:
        print("  No matches found")
    
    print(f"\nWithout Disease Match:")
    unmatched = results_df[results_df['disease_match'] == False]
    print(f"  Count: {len(unmatched)}")
    print(f"  Mean Probability: {unmatched['probability'].mean():.3f}")
    
    print("\n" + "=" * 70)
    print("✓ Verification Complete")
    print("=" * 70)


if __name__ == '__main__':
    verify_suitability_calculator()
