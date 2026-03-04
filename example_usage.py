"""
Example Usage of PharmaDrishti API

This script demonstrates how to use PharmaDrishti programmatically
without the dashboard interface.
"""

from data_loader import load_personas
from suitability_calculator import calculate_suitability
import pandas as pd

def main():
    print("=" * 60)
    print("PharmaDrishti - Example Usage")
    print("=" * 60)
    print()
    
    # Load personas
    print("Loading personas...")
    personas = load_personas('data/indian_healthcare_personas.json')
    print(f"✓ Loaded {len(personas)} personas")
    print()
    
    # Define medicine configuration
    medicine = {
        'target_disease': 'Type 2 Diabetes',
        'price_inr': 500,
        'brand_strength': 0.7,
        'side_effect_risk': 0.3,
        'availability_score': 0.8,
        'insurance_compatibility': 0.9
    }
    
    print("Medicine Configuration:")
    print(f"  Disease: {medicine['target_disease']}")
    print(f"  Price: ₹{medicine['price_inr']}")
    print(f"  Brand Strength: {medicine['brand_strength']}")
    print(f"  Side Effect Risk: {medicine['side_effect_risk']}")
    print(f"  Availability: {medicine['availability_score']}")
    print(f"  Insurance Compatibility: {medicine['insurance_compatibility']}")
    print()
    
    # Calculate suitability for all personas
    print("Calculating suitability scores...")
    results = []
    
    for idx, persona in personas.iterrows():
        score = calculate_suitability(persona, medicine)
        results.append({
            'name': persona['name'],
            'age': persona['age'],
            'income': persona['annual_income_inr'],
            'city_tier': persona['city_tier'],
            'suitability_score': score
        })
    
    results_df = pd.DataFrame(results)
    
    # Overall statistics
    overall_score = results_df['suitability_score'].mean()
    high_adoption = (results_df['suitability_score'] > 0.7).sum()
    medium_adoption = ((results_df['suitability_score'] >= 0.4) & 
                       (results_df['suitability_score'] <= 0.7)).sum()
    low_adoption = (results_df['suitability_score'] < 0.4).sum()
    
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print()
    print(f"Overall Suitability Score: {overall_score:.1%}")
    print()
    print("Adoption Distribution:")
    print(f"  High (>70%):   {high_adoption} personas ({high_adoption/len(results_df):.1%})")
    print(f"  Medium (40-70%): {medium_adoption} personas ({medium_adoption/len(results_df):.1%})")
    print(f"  Low (<40%):    {low_adoption} personas ({low_adoption/len(results_df):.1%})")
    print()
    
    # Segment analysis
    tier_scores = results_df.groupby('city_tier')['suitability_score'].mean()
    print("Suitability by City Tier:")
    for tier, score in tier_scores.items():
        print(f"  {tier}: {score:.1%}")
    print()
    
    # Top 5 personas
    print("Top 5 Most Suitable Personas:")
    top_5 = results_df.nlargest(5, 'suitability_score')
    for idx, row in top_5.iterrows():
        print(f"  {row['name']}: {row['suitability_score']:.1%} "
              f"(Age: {row['age']}, Income: ₹{row['income']:,.0f}, {row['city_tier']})")
    print()
    
    # Bottom 5 personas
    print("Bottom 5 Least Suitable Personas:")
    bottom_5 = results_df.nsmallest(5, 'suitability_score')
    for idx, row in bottom_5.iterrows():
        print(f"  {row['name']}: {row['suitability_score']:.1%} "
              f"(Age: {row['age']}, Income: ₹{row['income']:,.0f}, {row['city_tier']})")
    print()
    
    # Revenue estimation
    revenue_per_persona = results_df['suitability_score'] * medicine['price_inr']
    total_revenue = revenue_per_persona.sum()
    print(f"Estimated Revenue (from {len(personas)} personas): ₹{total_revenue:,.0f}")
    print(f"Average Revenue per Persona: ₹{total_revenue/len(personas):,.0f}")
    print()
    
    # Save results
    output_file = 'example_results.csv'
    results_df.to_csv(output_file, index=False)
    print(f"✓ Results saved to {output_file}")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
