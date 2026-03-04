# PharmaDrishti - Metrics and Formulas Documentation

## Date: March 1, 2026

---

## 📊 Core Suitability Score Formula

### Overall Suitability Score

The suitability score predicts the adoption probability for a medicine across the Indian healthcare market.

**Formula:**
```
Weighted_Sum = (0.30 × Disease_Match) + 
               (0.25 × Affordability) + 
               (0.20 × Market_Pricing) + 
               (0.15 × Manufacturing) + 
               (0.10 × Risk_Tolerance)

Suitability_Score = 1 / (1 + e^(-scaled_sum))

where: scaled_sum = (Weighted_Sum - 0.5) × 12
```

**Component Weights:**
- Disease Match: 30%
- Affordability: 25%
- Market Pricing: 20%
- Manufacturing: 15%
- Risk Tolerance: 10%

---

## 🔍 Component Formulas

### 1. Disease Match Score (30% weight)

**Purpose:** Determines if the medicine treats the persona's condition

**Formula:**
```
Disease_Match = 1.0  if target_disease in persona_diseases
              = 0.0  otherwise
```

**Example:**
```
Persona has: "Type 2 Diabetes, Hypertension"
Medicine treats: "Type 2 Diabetes"
Disease_Match = 1.0 (Perfect match)
```

**Range:** 0.0 to 1.0 (Binary)

---

### 2. Affordability Score (25% weight)

**Purpose:** Measures if the persona can afford the medicine batch

**Formula:**
```
Monthly_Income = Annual_Income / 12

Affordability = max(0.0, 1.0 - (Batch_Price / (Monthly_Income × 100)))
Affordability = min(1.0, Affordability)
```

**Example:**
```
Annual Income: ₹600,000
Monthly Income: ₹50,000
Batch Price: ₹30,000

Affordability = 1.0 - (30,000 / (50,000 × 100))
              = 1.0 - (30,000 / 5,000,000)
              = 1.0 - 0.006
              = 0.994 (Highly affordable)
```

**Range:** 0.0 (unaffordable) to 1.0 (very affordable)

**Interpretation:**
- 0.8 - 1.0: Highly affordable
- 0.5 - 0.8: Moderately affordable
- 0.0 - 0.5: Expensive/Unaffordable

---

### 3. Market Pricing Score (20% weight) - NEW

**Purpose:** Evaluates price competitiveness vs market alternatives

**Formula:**
```
Step 1: Find similar medicines in NPPAIPDMS dataset
        Similar_Medicines = medicines where disease keywords match

Step 2: Calculate average market price
        Avg_Market_Price = mean(Similar_Medicines.prices)

Step 3: Calculate price ratio
        Price_Ratio = Your_Batch_Price / Avg_Market_Price

Step 4: Determine competitiveness score
        if Price_Ratio < 0.7:
            Market_Pricing_Score = 1.0
        elif 0.7 ≤ Price_Ratio < 1.3:
            Market_Pricing_Score = 1.0 - (Price_Ratio - 0.7) × (0.4 / 0.6)
        elif 1.3 ≤ Price_Ratio < 2.0:
            Market_Pricing_Score = 0.6 - (Price_Ratio - 1.3) × (0.4 / 0.7)
        else:  # Price_Ratio ≥ 2.0
            Market_Pricing_Score = 0.1
```

**Example:**
```
Your Price: ₹50,000
Market Average: ₹45,000
Price_Ratio = 50,000 / 45,000 = 1.11

Since 0.7 ≤ 1.11 < 1.3:
Market_Pricing_Score = 1.0 - (1.11 - 0.7) × (0.4 / 0.6)
                     = 1.0 - (0.41 × 0.667)
                     = 1.0 - 0.273
                     = 0.727 (Competitive)
```

**Range:** 0.1 (very expensive) to 1.0 (very competitive)

**Interpretation:**
- 0.8 - 1.0: Much cheaper than market (excellent positioning)
- 0.6 - 0.8: Competitive pricing (good positioning)
- 0.2 - 0.6: Above market average (poor positioning)
- 0.0 - 0.2: Significantly overpriced (very poor positioning)

---

### 4. Manufacturing Score (15% weight)

**Purpose:** Assesses manufacturing capability and location accessibility

**Formula:**
```
Tier_Accessibility = {
    'Tier 1': 0.9,
    'Tier 2': 0.7,
    'Tier 3': 0.5
}

Location_Factor = Tier_Accessibility[Persona_City_Tier]

Manufacturing_Score = Medicine_Manufacturing_Score × Location_Factor
```

**Example:**
```
Medicine Manufacturing Score: 0.8
Persona City Tier: Tier 2
Location_Factor: 0.7

Manufacturing_Score = 0.8 × 0.7 = 0.56
```

**Range:** 0.0 to 1.0

**Interpretation:**
- 0.7 - 1.0: Excellent manufacturing access
- 0.5 - 0.7: Good manufacturing access
- 0.3 - 0.5: Limited manufacturing access
- 0.0 - 0.3: Poor manufacturing access

---

### 5. Risk Tolerance Score (10% weight)

**Purpose:** Evaluates side effect acceptability based on risk aversion

**Formula:**
```
Risk_Score = Side_Effect_Risk × Price_Sensitivity

Risk_Tolerance = 1 - Risk_Score
```

**Example:**
```
Side Effect Risk: 0.3 (low risk)
Price Sensitivity: 0.6 (moderately price-sensitive)

Risk_Score = 0.3 × 0.6 = 0.18
Risk_Tolerance = 1 - 0.18 = 0.82 (High tolerance)
```

**Range:** 0.0 (no tolerance) to 1.0 (high tolerance)

**Interpretation:**
- 0.7 - 1.0: High risk tolerance (side effects acceptable)
- 0.4 - 0.7: Moderate risk tolerance
- 0.0 - 0.4: Low risk tolerance (side effects concerning)

---

## 📈 Sigmoid Transformation

**Purpose:** Convert weighted sum to probability (0-1 range)

**Formula:**
```
Scaled_Sum = (Weighted_Sum - 0.5) × 12

Probability = 1 / (1 + e^(-Scaled_Sum))
```

**Why Sigmoid?**
- Maps any real number to (0, 1) range
- Creates smooth probability curve
- Centers around 0.5 for balanced predictions

**Example:**
```
Weighted_Sum = 0.75
Scaled_Sum = (0.75 - 0.5) × 12 = 3.0

Probability = 1 / (1 + e^(-3.0))
            = 1 / (1 + 0.0498)
            = 1 / 1.0498
            = 0.953 (95.3% adoption probability)
```

---

## 💰 Revenue Estimation

**Formula:**
```
Revenue_Per_Persona = Batch_Price × Suitability_Score

Total_Revenue = Σ(Revenue_Per_Persona) for all personas
```

**Example:**
```
Batch Price: ₹50,000
Persona 1 Suitability: 0.85
Persona 2 Suitability: 0.60
Persona 3 Suitability: 0.40

Revenue = (50,000 × 0.85) + (50,000 × 0.60) + (50,000 × 0.40)
        = 42,500 + 30,000 + 20,000
        = ₹92,500
```

---

## 🎯 Market Penetration

**Formula:**
```
Market_Penetration = Count(Personas with Suitability > 0.5) / Total_Personas × 100%
```

**Example:**
```
Total Personas: 100
Personas with Score > 0.5: 68

Market_Penetration = 68 / 100 × 100% = 68%
```

**Interpretation:**
- 70-100%: High penetration (strong market fit)
- 40-70%: Moderate penetration (needs optimization)
- 0-40%: Low penetration (major changes needed)

---

## 📊 Segment Analysis

### City Tier Segmentation

**Formula:**
```
Tier_Score = mean(Suitability_Scores for personas in tier)
```

**Example:**
```
Tier 1 Personas: [0.85, 0.90, 0.78, 0.82]
Tier 1 Score = (0.85 + 0.90 + 0.78 + 0.82) / 4 = 0.8375 (83.75%)

Tier 2 Personas: [0.65, 0.70, 0.60]
Tier 2 Score = (0.65 + 0.70 + 0.60) / 3 = 0.65 (65%)

Tier 3 Personas: [0.40, 0.35, 0.45]
Tier 3 Score = (0.40 + 0.35 + 0.45) / 3 = 0.40 (40%)
```

### Income Level Segmentation

**Categories:**
- High Income: > ₹1,000,000/year
- Middle Income: ₹300,000 - ₹1,000,000/year
- Low Income: < ₹300,000/year

**Formula:**
```
Income_Segment_Score = mean(Suitability_Scores for personas in income bracket)
```

---

## 🔢 Key Performance Indicators (KPIs)

### 1. Overall Suitability Score
```
Overall_Score = mean(All_Persona_Suitability_Scores)
```

### 2. Best Performing Segment
```
Best_Segment = argmax(Segment_Scores)
Best_Score = max(Segment_Scores)
```

### 3. Worst Performing Segment
```
Worst_Segment = argmin(Segment_Scores)
Worst_Score = min(Segment_Scores)
```

### 4. Component Averages
```
Avg_Disease_Match = mean(Disease_Match_Scores)
Avg_Affordability = mean(Affordability_Scores)
Avg_Market_Pricing = mean(Market_Pricing_Scores)
Avg_Manufacturing = mean(Manufacturing_Scores)
Avg_Risk_Tolerance = mean(Risk_Tolerance_Scores)
```

---

## 📉 Market Comparison Metrics

### Similar Medicines Count
```
Similar_Count = Count(Medicines where disease keywords match)
```

### Average Market Price
```
Avg_Market_Price = mean(Similar_Medicines.prices)
```

### Price Range
```
Min_Price = min(Similar_Medicines.prices)
Max_Price = max(Similar_Medicines.prices)
Price_Range = [Min_Price, Max_Price]
```

### Price Position
```
if Your_Price < Avg_Market_Price:
    Position = "Below Average"
elif Your_Price == Avg_Market_Price:
    Position = "At Average"
else:
    Position = "Above Average"
```

### Price Difference Percentage
```
Price_Difference = ((Your_Price - Avg_Market_Price) / Avg_Market_Price) × 100%
```

**Example:**
```
Your Price: ₹50,000
Market Average: ₹45,000

Price_Difference = ((50,000 - 45,000) / 45,000) × 100%
                 = (5,000 / 45,000) × 100%
                 = 11.11% above market average
```

---

## 🎨 Score Interpretation Guidelines

### Overall Suitability Score

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| 70-100% | High adoption, strong market fit | Launch with confidence |
| 40-70% | Moderate adoption, needs optimization | Review recommendations |
| 0-40% | Low adoption, high risk | Major changes needed |

### Component Score Thresholds

**Disease Match:**
- < 0.3: Low match (few personas have disease)
- ≥ 0.3: Adequate match

**Affordability:**
- < 0.5: Too expensive for target market
- ≥ 0.5: Affordable

**Market Pricing:**
- < 0.4: Significantly overpriced vs market
- 0.4-0.6: Above market average
- ≥ 0.6: Competitive pricing

**Manufacturing:**
- < 0.5: Limited manufacturing capability
- ≥ 0.5: Adequate manufacturing

**Risk Score:**
- > 0.5: High risk perception
- ≤ 0.5: Acceptable risk

---

## 🧮 Example: Complete Calculation

### Input Data:
```
Persona:
- Chronic Diseases: "Type 2 Diabetes"
- Annual Income: ₹600,000
- City Tier: Tier 1
- Price Sensitivity: 0.4

Medicine:
- Target Disease: "Type 2 Diabetes"
- Batch Price: ₹50,000
- Manufacturing Score: 0.8
- Side Effect Risk: 0.3

Market Data:
- Similar Medicines: 23 found
- Average Market Price: ₹45,000
```

### Step-by-Step Calculation:

**1. Disease Match:**
```
"Type 2 Diabetes" in "Type 2 Diabetes" = True
Disease_Match = 1.0
```

**2. Affordability:**
```
Monthly_Income = 600,000 / 12 = 50,000
Affordability = 1.0 - (50,000 / (50,000 × 100))
              = 1.0 - 0.01
              = 0.99
```

**3. Market Pricing:**
```
Price_Ratio = 50,000 / 45,000 = 1.11
Market_Pricing = 1.0 - (1.11 - 0.7) × (0.4 / 0.6)
               = 1.0 - 0.273
               = 0.727
```

**4. Manufacturing:**
```
Location_Factor = 0.9 (Tier 1)
Manufacturing = 0.8 × 0.9 = 0.72
```

**5. Risk Tolerance:**
```
Risk_Score = 0.3 × 0.4 = 0.12
Risk_Tolerance = 1 - 0.12 = 0.88
```

**6. Weighted Sum:**
```
Weighted_Sum = (0.30 × 1.0) + (0.25 × 0.99) + (0.20 × 0.727) + 
               (0.15 × 0.72) + (0.10 × 0.88)
             = 0.30 + 0.2475 + 0.1454 + 0.108 + 0.088
             = 0.8889
```

**7. Sigmoid Transformation:**
```
Scaled_Sum = (0.8889 - 0.5) × 12 = 4.667
Probability = 1 / (1 + e^(-4.667))
            = 1 / (1 + 0.0094)
            = 0.991 (99.1% adoption probability)
```

**Final Result:** 99.1% suitability score - Excellent market fit!

---

## 📚 Data Sources

### NPPAIPDMS Dataset
- **Records:** 953 medicines
- **Time Period:** 2013-2023
- **Columns:** id, year, medicine_name, formulation, notification, price
- **Source:** National Pharmaceutical Pricing Authority (NPPA)

### Persona Dataset
- **Count:** 100 synthetic personas
- **Attributes:** Demographics, income, location, health conditions, preferences
- **Coverage:** Represents India's diverse healthcare landscape

---

## 🔬 Model Validation

### Training Dataset
- **Size:** 500,000 interaction pairs
- **Personas:** 100
- **Medicines:** 5,000
- **Algorithm:** XGBoost Gradient Boosting

### Performance Metrics
- **R² Score:** > 0.80 (target)
- **RMSE:** Root Mean Squared Error
- **MAE:** Mean Absolute Error

---

## 📝 Summary

PharmaDrishti uses a sophisticated 5-component weighted scoring system that:

1. **Matches diseases** to ensure relevance
2. **Evaluates affordability** based on income
3. **Compares market pricing** for competitiveness
4. **Assesses manufacturing** capability and access
5. **Considers risk tolerance** for side effects

The system applies sigmoid transformation to convert scores into adoption probabilities, providing actionable insights for pharmaceutical market strategy.

**Key Innovation:** Integration of real market pricing data (NPPAIPDMS) to penalize overpricing and encourage competitive positioning.

---

**Last Updated:** March 1, 2026
**Version:** 2.0 (with Market Pricing Integration)
