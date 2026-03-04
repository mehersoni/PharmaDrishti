"""
Verification script for create_interaction_dataset function.
Demonstrates the generation of persona-medicine interaction pairs with features.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from suitability_calculator import create_interaction_dataset
from data_loader import load_personas
from medicine_generator import generate_medicines


def verify_interaction_dataset():
    """Verify interaction dataset generation and display statistics."""
    
    print("=" * 70)
    print("PharmaDrishti: Interaction Dataset Generation Verification")
    print("=" * 70)
    print()
    
    # Load personas
    print("Step 1: Loading personas...")
    personas = load_personas()
    print(f"✓ Loaded {len(personas)} personas")
    print()
    
    # Generate medicines
    print("Step 2: Generating medicines...")
    medicines = generate_medicines(n=50)
    print(f"✓ Generated {len(medicines)} medicine profiles")
    print()
    
    # Create interaction dataset
    print("Step 3: Creating interaction dataset...")
    print(f"   Generating {len(personas)} × {len(medicines)} = {len(personas) * len(medicines)} interaction pairs...")
    interactions = create_interaction_dataset(personas, medicines)
    print(f"✓ Created {len(interactions)} interaction pairs")
    print()
    
    # Verify success criteria
    print("-" * 70)
    print("SUCCESS CRITERIA VERIFICATION")
    print("-" * 70)
    
    expected_count = 5000
    actual_count = len(interactions)
    
    if actual_count == expected_count:
        print(f"✓ SUCCESS: Generated {actual_count} interaction pairs (expected {expected_count})")
    else:
        print(f"✗ FAILED: Generated {actual_count} interaction pairs (expected {expected_count})")
        return False
    
    print()
    
    # Display dataset statistics
    print("-" * 70)
    print("DATASET STATISTICS")
    print("-" * 70)
    print()
    
    print("1. Dataset Shape:")
    print(f"   Rows: {len(interactions):,}")
    print(f"   Columns: {len(interactions.columns)}")
    print()
    
    print("2. Feature Columns:")
    feature_cols = [col for col in interactions.columns if col not in ['persona_id', 'medicine_id', 'suitability_score']]
    print(f"   Total features: {len(feature_cols)}")
    print(f"   Features: {', '.join(feature_cols[:10])}...")
    print()
    
    print("3. Suitability Score Distribution:")
    print(f"   Min: {interactions['suitability_score'].min():.4f}")
    print(f"   Max: {interactions['suitability_score'].max():.4f}")
    print(f"   Mean: {interactions['suitability_score'].mean():.4f}")
    print(f"   Median: {interactions['suitability_score'].median():.4f}")
    print()
    
    print("4. Disease Match Distribution:")
    disease_match_count = (interactions['disease_match'] == 1.0).sum()
    disease_match_pct = disease_match_count / len(interactions) * 100
    print(f"   Matches: {disease_match_count:,} ({disease_match_pct:.1f}%)")
    print(f"   No matches: {len(interactions) - disease_match_count:,} ({100 - disease_match_pct:.1f}%)")
    print()
    
    print("5. Affordability Distribution:")
    print(f"   Min: {interactions['affordability'].min():.4f}")
    print(f"   Max: {interactions['affordability'].max():.4f}")
    print(f"   Mean: {interactions['affordability'].mean():.4f}")
    print()
    
    print("6. City Tier Distribution:")
    tier_counts = interactions['city_tier_encoded'].value_counts().sort_index()
    for tier, count in tier_counts.items():
        tier_name = {1: 'Tier 1', 2: 'Tier 2', 3: 'Tier 3'}.get(tier, f'Tier {tier}')
        print(f"   {tier_name}: {count:,} interactions ({count/len(interactions)*100:.1f}%)")
    print()
    
    # Display sample interactions
    print("-" * 70)
    print("SAMPLE INTERACTIONS (First 5)")
    print("-" * 70)
    print()
    
    sample = interactions.head(5)
    for idx, row in sample.iterrows():
        print(f"Interaction {idx + 1}:")
        print(f"  Persona: {row['persona_id']}")
        print(f"  Medicine: {row['medicine_id']}")
        print(f"  Suitability Score: {row['suitability_score']:.4f}")
        print(f"  Disease Match: {'Yes' if row['disease_match'] == 1.0 else 'No'}")
        print(f"  Affordability: {row['affordability']:.4f}")
        print(f"  Age: {row['age']}, Income: ₹{row['income']:,.0f}, Price: ₹{row['price']:.0f}")
        print()
    
    # Display high suitability examples
    print("-" * 70)
    print("HIGH SUITABILITY EXAMPLES (Top 5)")
    print("-" * 70)
    print()
    
    top_5 = interactions.nlargest(5, 'suitability_score')
    for idx, (_, row) in enumerate(top_5.iterrows(), 1):
        print(f"{idx}. Suitability: {row['suitability_score']:.4f}")
        print(f"   Persona: {row['persona_id']}")
        print(f"   Medicine: {row['medicine_id']}")
        print(f"   Disease Match: {'Yes' if row['disease_match'] == 1.0 else 'No'}")
        print(f"   Affordability: {row['affordability']:.4f}")
        print()
    
    # Display low suitability examples
    print("-" * 70)
    print("LOW SUITABILITY EXAMPLES (Bottom 5)")
    print("-" * 70)
    print()
    
    bottom_5 = interactions.nsmallest(5, 'suitability_score')
    for idx, (_, row) in enumerate(bottom_5.iterrows(), 1):
        print(f"{idx}. Suitability: {row['suitability_score']:.4f}")
        print(f"   Persona: {row['persona_id']}")
        print(f"   Medicine: {row['medicine_id']}")
        print(f"   Disease Match: {'Yes' if row['disease_match'] == 1.0 else 'No'}")
        print(f"   Affordability: {row['affordability']:.4f}")
        print()
    
    # Verify data quality
    print("-" * 70)
    print("DATA QUALITY CHECKS")
    print("-" * 70)
    print()
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: No missing values
    total_checks += 1
    missing_count = interactions.isnull().sum().sum()
    if missing_count == 0:
        print("✓ No missing values")
        checks_passed += 1
    else:
        print(f"✗ Found {missing_count} missing values")
    
    # Check 2: Suitability scores in valid range
    total_checks += 1
    if (interactions['suitability_score'].min() >= 0.0 and 
        interactions['suitability_score'].max() <= 1.0):
        print("✓ Suitability scores in valid range [0, 1]")
        checks_passed += 1
    else:
        print("✗ Suitability scores out of range")
    
    # Check 3: Unique persona-medicine pairs
    total_checks += 1
    duplicates = interactions.duplicated(subset=['persona_id', 'medicine_id']).sum()
    if duplicates == 0:
        print("✓ All persona-medicine pairs are unique")
        checks_passed += 1
    else:
        print(f"✗ Found {duplicates} duplicate pairs")
    
    # Check 4: All features are numeric
    total_checks += 1
    numeric_cols = interactions.select_dtypes(include=['number']).columns
    if len(numeric_cols) >= len(feature_cols):
        print("✓ All features are numeric")
        checks_passed += 1
    else:
        print("✗ Some features are not numeric")
    
    print()
    print(f"Quality checks passed: {checks_passed}/{total_checks}")
    print()
    
    # Final summary
    print("=" * 70)
    if checks_passed == total_checks and actual_count == expected_count:
        print("✓ SUCCESS: All verifications passed!")
        print("✓ Ready for ML model training")
    else:
        print("✗ FAILED: Some verifications failed")
    print("=" * 70)
    
    return checks_passed == total_checks and actual_count == expected_count


if __name__ == "__main__":
    success = verify_interaction_dataset()
    sys.exit(0 if success else 1)
