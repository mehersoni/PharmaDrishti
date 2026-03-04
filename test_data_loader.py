"""
Test script for data_loader module.
Tests the load_personas() function and displays basic statistics.
"""

import sys
from pathlib import Path

# Add parent directory to path to import data_loader
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import load_personas


def test_load_personas():
    """Test loading personas and display statistics."""
    
    print("=" * 60)
    print("Testing PharmaDrishti Data Loader")
    print("=" * 60)
    print()
    
    # Load personas
    print("Loading personas from data/indian_healthcare_personas.json...")
    df = load_personas()
    
    # Verify data loaded
    if df.empty:
        print("❌ FAILED: No data loaded!")
        return False
    
    print(f"✓ Successfully loaded {len(df)} personas")
    print()
    
    # Display first few rows
    print("-" * 60)
    print("First 5 personas:")
    print("-" * 60)
    print(df.head().to_string())
    print()
    
    # Display basic statistics
    print("-" * 60)
    print("Basic Statistics:")
    print("-" * 60)
    
    # Count by city tier
    print("\n1. Distribution by City Tier:")
    tier_counts = df['city_tier'].value_counts().sort_index()
    for tier, count in tier_counts.items():
        print(f"   {tier}: {count} personas ({count/len(df)*100:.1f}%)")
    
    # Count by income level
    print("\n2. Distribution by Income Level:")
    income_counts = df['income_level'].value_counts()
    for level, count in income_counts.items():
        print(f"   {level}: {count} personas ({count/len(df)*100:.1f}%)")
    
    # Age statistics
    print("\n3. Age Statistics:")
    print(f"   Min age: {df['age'].min()} years")
    print(f"   Max age: {df['age'].max()} years")
    print(f"   Average age: {df['age'].mean():.1f} years")
    
    # Income statistics
    print("\n4. Income Statistics:")
    print(f"   Min income: ₹{df['annual_income_inr'].min():,.0f}")
    print(f"   Max income: ₹{df['annual_income_inr'].max():,.0f}")
    print(f"   Average income: ₹{df['annual_income_inr'].mean():,.0f}")
    
    # Gender distribution
    print("\n5. Gender Distribution:")
    gender_counts = df['gender'].value_counts()
    for gender, count in gender_counts.items():
        print(f"   {gender}: {count} personas ({count/len(df)*100:.1f}%)")
    
    # Insurance status
    print("\n6. Insurance Status:")
    insurance_counts = df['insurance_status'].value_counts()
    for status, count in insurance_counts.items():
        print(f"   {status}: {count} personas ({count/len(df)*100:.1f}%)")
    
    print()
    print("=" * 60)
    print("✓ SUCCESS: All tests passed!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = test_load_personas()
    sys.exit(0 if success else 1)
