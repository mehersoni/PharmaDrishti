"""
PharmaDrishti - Model Training Script

This script trains the XGBoost model for adoption prediction.
It loads personas, generates medicines, creates interaction dataset,
trains the model, and saves it for use in the dashboard.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
import time
from pathlib import Path

# Import local modules
from data_loader import load_personas
from medicine_generator import generate_medicines
from suitability_calculator import create_interaction_dataset


def main():
    """Train the adoption prediction model"""
    print("=" * 60)
    print("PharmaDrishti - Model Training Pipeline")
    print("=" * 60)
    
    start_time = time.time()
    
    # Step 1: Load personas
    print("\n[1/7] Loading personas...")
    personas = load_personas()
    if personas.empty:
        print("❌ Error: Failed to load personas")
        return
    print(f"✓ Loaded {len(personas)} personas")
    
    # Step 2: Generate medicines
    print("\n[2/7] Generating medicines...")
    medicines = generate_medicines(n=5000)
    print(f"✓ Generated {len(medicines)} medicine profiles")
    
    # Step 3: Create interaction dataset
    print("\n[3/7] Creating interaction dataset...")
    print("   This may take a few minutes for 500k interactions...")
    interactions = create_interaction_dataset(personas, medicines)
    print(f"✓ Created {len(interactions)} interaction pairs")
    print(f"   Expected: {len(personas)} × {len(medicines)} = {len(personas) * len(medicines)}")
    
    # Step 4: Prepare features and target
    print("\n[4/7] Preparing features and target...")
    
    # Drop identifier columns and target variable
    feature_cols = [col for col in interactions.columns 
                   if col not in ['persona_id', 'medicine_id', 'suitability_score']]
    
    X = interactions[feature_cols]
    y = interactions['suitability_score']
    
    print(f"✓ Features: {X.shape[1]} columns")
    print(f"   Feature names: {list(X.columns)}")
    print(f"✓ Target: {y.shape[0]} samples")
    print(f"   Target range: [{y.min():.3f}, {y.max():.3f}]")
    print(f"   Target mean: {y.mean():.3f}")
    
    # Step 5: Train-test split
    print("\n[5/7] Splitting data (80-20 train-test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"✓ Training set: {len(X_train)} samples")
    print(f"✓ Test set: {len(X_test)} samples")
    
    # Step 6: Train XGBoost model
    print("\n[6/7] Training XGBoost model...")
    print("   Hyperparameters:")
    print("   - n_estimators: 200 (increased for larger dataset)")
    print("   - max_depth: 8 (increased for more complex patterns)")
    print("   - learning_rate: 0.05")
    print("   - subsample: 0.8")
    print("   - colsample_bytree: 0.8")
    print("   - random_state: 42")
    
    model = XGBRegressor(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        objective='reg:squarederror',
        verbosity=0,  # Suppress XGBoost warnings
        n_jobs=-1  # Use all CPU cores
    )
    
    model.fit(X_train, y_train)
    print("✓ Model training complete")
    
    # Evaluate model
    print("\n   Evaluating model performance...")
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_rmse = np.sqrt(test_mse)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    
    print(f"\n   Training Performance:")
    print(f"   - R² Score: {train_r2:.4f}")
    
    print(f"\n   Test Performance:")
    print(f"   - R² Score: {test_r2:.4f}")
    print(f"   - RMSE: {test_rmse:.4f}")
    print(f"   - MAE: {test_mae:.4f}")
    
    # Check success criteria
    if test_r2 >= 0.80:
        print(f"\n   ✓ SUCCESS: R² score {test_r2:.4f} meets requirement (> 0.80)")
    else:
        print(f"\n   ⚠ WARNING: R² score {test_r2:.4f} below requirement (> 0.80)")
    
    # Step 7: Save model and encoders
    print("\n[7/7] Saving model and encoders...")
    
    # Create models directory if it doesn't exist
    models_dir = Path('models')
    models_dir.mkdir(exist_ok=True)
    
    # Save model
    model_path = models_dir / 'adoption_model.pkl'
    joblib.dump(model, model_path)
    print(f"✓ Model saved to: {model_path}")
    
    # Save feature names for later use
    feature_names_path = models_dir / 'feature_names.pkl'
    joblib.dump(list(X.columns), feature_names_path)
    print(f"✓ Feature names saved to: {feature_names_path}")
    
    # Calculate and display training time
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"Total time: {minutes}m {seconds}s")
    
    # Check time requirement
    if elapsed_time < 600:  # 10 minutes = 600 seconds (adjusted for larger dataset)
        print(f"✓ SUCCESS: Training completed in < 10 minutes")
    else:
        print(f"⚠ WARNING: Training took longer than 10 minutes")
    
    print("\nModel artifacts saved in models/ folder:")
    print(f"  - {model_path}")
    print(f"  - {feature_names_path}")
    print("\nYou can now use this model in the dashboard!")
    print("=" * 60)


if __name__ == "__main__":
    main()
