# PharmaDrishti Dashboard - Complete Feature Guide

## Overview

The PharmaDrishti dashboard is an interactive web application that helps pharmaceutical companies analyze market suitability for new medicine launches. It combines AI-powered predictions with real market data to provide actionable insights.

---

## Core Features

### 1. Medicine Configuration Panel

Located in the sidebar, this is where you input your medicine details:

#### Input Fields:

**Target Disease** (Dropdown)
- Select from 10 common diseases in India
- Options: Type 2 Diabetes, Hypertension, Asthma, Arthritis, Heart Disease, Thyroid Disorder, Chronic Kidney Disease, Obesity, Anemia, COPD
- This determines which personas have a disease match

**Price (INR)** (Number Input)
- Range: ₹50 - ₹5,000
- Step: ₹50
- Directly impacts affordability scores
- Lower prices increase adoption in price-sensitive segments

**Launch Locality** (Dropdown)
- Options: Pan-India or specific states (Maharashtra, Karnataka, Tamil Nadu, etc.)
- Filters analysis to personas from selected region
- Use "Pan-India" for nationwide launch analysis

**Brand Strength** (Slider: 0.0 - 1.0)
- 0.0 = Generic/unbranded medicine
- 1.0 = Premium/established brand
- Higher values appeal to less price-sensitive consumers
- Affects brand alignment score

**Side Effect Risk** (Slider: 0.0 - 1.0)
- 0.0 = Very safe, minimal side effects
- 1.0 = High risk of side effects
- Price-sensitive consumers are more risk-averse
- Affects risk tolerance score

**Availability Score** (Slider: 0.0 - 1.0)
- 0.0 = Limited distribution, hard to find
- 1.0 = Widely available across pharmacies
- Multiplied by location accessibility factor
- Tier 1 cities have better access than Tier 3

**Insurance Compatibility** (Slider: 0.0 - 1.0)
- 0.0 = Not covered by any insurance
- 1.0 = Fully covered by major insurance schemes
- Increases adoption among insured personas

---

### 2. Suitability Scoring Engine

The core algorithm that calculates adoption probability for each persona.

#### Scoring Components (Weighted):

1. **Disease Match (35% weight)**
   - Binary: 1.0 if medicine treats persona's condition, 0.0 otherwise
   - Highest weight because need is fundamental
   - Example: Diabetes medicine scores 1.0 for diabetic personas

2. **Affordability (25% weight)**
   - Calculated as: 1.0 - (price / monthly_income)
   - Capped between 0.0 and 1.0
   - ₹500 medicine for ₹50,000/month income = 0.99 affordability
   - ₹500 medicine for ₹10,000/month income = 0.95 affordability

3. **Availability (15% weight)**
   - Medicine availability × location accessibility
   - Location factors: Tier 1 (0.9), Tier 2 (0.7), Tier 3 (0.5)
   - 0.8 availability in Tier 1 = 0.72 final score
   - 0.8 availability in Tier 3 = 0.40 final score

4. **Brand Alignment (15% weight)**
   - Brand strength × (1 - price sensitivity)
   - Premium brands appeal to affluent consumers
   - Generic brands appeal to price-sensitive consumers

5. **Risk Tolerance (10% weight)**
   - Side effect risk × price sensitivity
   - Price-sensitive consumers avoid risky medicines
   - Affluent consumers more tolerant of side effects

#### Final Score Calculation:

```
weighted_sum = (0.35 × disease_match + 
                0.25 × affordability + 
                0.15 × availability + 
                0.15 × brand_alignment + 
                0.10 × (1 - risk_score))

suitability_score = sigmoid(weighted_sum)
```

The sigmoid transformation ensures scores are between 0 and 1, representing adoption probability.

---

### 3. Results Dashboard

After clicking "Analyze Market Suitability", you get comprehensive results:

#### Key Metrics (Top Row):

**Overall Suitability Score**
- Average adoption probability across all personas
- Shown as percentage (0-100%)
- Delta shows difference from 50% baseline
- Color-coded: Green (>70%), Yellow (40-70%), Red (<40%)

**Market Penetration**
- Number of personas with >50% adoption probability
- Shown as fraction (e.g., 68/100) and percentage
- Indicates how many personas are likely to adopt

**Revenue Estimate**
- Sum of (adoption_probability × price) for all personas
- Shown in Lakhs (L) for readability
- Based on sample personas, multiply by market size for real estimate

#### Gauge Chart:

Visual representation of overall suitability:
- Red zone (0-40%): Low adoption, high risk
- Yellow zone (40-70%): Moderate adoption, needs optimization
- Green zone (70-100%): High adoption, strong market fit
- Needle shows current score
- Delta shows difference from 50% threshold

---

### 4. Component Breakdown Analysis

**Why This Score? - Component Breakdown**

Two visualizations side-by-side:

**Left: Component Scores Bar Chart**
- Shows average score for each of the 5 components
- Horizontal bars colored by score (red to green)
- Identifies which factors are strong/weak
- Example: High disease match but low affordability = price issue

**Right: Suitability by City Tier**
- Bar chart comparing Tier 1, Tier 2, Tier 3
- Shows which geographic segments are most suitable
- Helps target launch strategy
- Example: Tier 1 (75%), Tier 2 (65%), Tier 3 (45%)

---

### 5. Key Issues Identification

Automatic detection of problems:

**🔴 Critical Issues:**
- Low Disease Match (<0.3): Few personas need this medicine
- Price Too High (<0.5 affordability): Unaffordable for many
- Limited Availability (<0.5): Distribution challenges

**🟡 Warning Issues:**
- Brand Mismatch (<0.4): Brand doesn't match audience
- High Risk Perception (>0.5): Side effects concern consumers

Each issue includes:
- Severity indicator (🔴 critical, 🟡 warning)
- Clear description of the problem
- Implied action needed

---

### 6. AI-Powered Recommendations (Gemini Integration)

**Requires Gemini API Key** (optional but highly recommended)

The AI analyzes your results and provides:

**1. Why is the suitability score at this level?**
- 2-3 key reasons based on component scores
- Data-driven explanations
- Example: "Score is 68% primarily due to strong disease match (0.85) but moderate affordability (0.52) in Tier 2/3 cities"

**2. What are the main barriers to adoption?**
- 2-3 specific issues preventing higher adoption
- Prioritized by impact
- Example: "Price point of ₹500 exceeds 5% of monthly income for 45% of personas"

**3. Actionable recommendations to improve market launch**
- 3-4 specific suggestions with expected impact
- Prioritized by ROI
- Examples:
  - "Reduce price to ₹350 (expected +15% adoption)"
  - "Focus initial launch on Tier 1 cities (75% adoption vs 45% in Tier 3)"
  - "Partner with Ayushman Bharat for insurance coverage (+12% adoption)"

**How to Enable:**
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.streamlit/secrets.toml` or enter in sidebar
3. AI insights generate automatically with each analysis

---

### 7. Market Comparison (Kaggle Integration)

**Automatic - No Configuration Needed**

Compares your medicine with real market data:

**Data Source:**
- Kaggle dataset: "AZ Medicine Dataset of India"
- Contains real Indian medicine data
- Downloaded automatically on first run
- Cached for subsequent analyses

**Comparison Metrics:**
- Number of similar medicines found
- Average market price for similar medicines
- Sample of similar products (expandable table)

**Use Cases:**
- Benchmark your pricing
- Understand competitive landscape
- Validate assumptions about market

**Example Output:**
```
Found 23 similar medicines in market database
Average market price: ₹425.50

View similar medicines (expandable):
- Medicine A: ₹380
- Medicine B: ₹450
- Medicine C: ₹520
...
```

---

### 8. Detailed Results Table

**Expandable section: "View Detailed Results"**

Persona-level breakdown showing:
- Persona name
- Age, income, city tier, state
- Suitability score
- All 5 component scores

**Features:**
- Sortable by any column
- Searchable
- Scrollable for large datasets
- Helps identify specific persona segments

**Use Cases:**
- Deep-dive into specific personas
- Understand why certain segments score high/low
- Identify outliers
- Validate assumptions

---

### 9. Export Functionality

**Download Results (CSV)**

Exports complete analysis including:
- All persona details
- Suitability scores
- Component scores
- Timestamp

**File naming:** `pharmadrishti_analysis_{disease}.csv`

**Use Cases:**
- Share with stakeholders
- Further analysis in Excel/Python
- Documentation for compliance
- Historical tracking

---

## Advanced Features

### Session State Management

The dashboard maintains state across interactions:
- Scenario comparisons persist during session
- Previous analyses remain accessible
- No data loss when changing inputs

### Responsive Design

Works on:
- Desktop (optimal)
- Tablet (good)
- Mobile (basic support)

### Performance Optimization

- Persona data cached (loads once)
- Market data cached (downloads once)
- Gemini model cached (initializes once)
- Fast predictions (<2 seconds for 100 personas)

---

## Tips for Best Results

### 1. Start with Realistic Inputs
- Use actual medicine prices from your research
- Set brand strength based on your company's market position
- Be honest about side effect risks

### 2. Test Multiple Scenarios
- Try different price points (₹300, ₹500, ₹800)
- Compare generic vs branded positioning
- Test Pan-India vs state-specific launches

### 3. Focus on Actionable Insights
- Don't just look at overall score
- Identify which component is weakest
- Prioritize recommendations by expected impact

### 4. Use AI Insights
- Configure Gemini API for best experience
- AI provides context human analysis might miss
- Recommendations are data-driven and specific

### 5. Compare with Market Data
- Check if your price is competitive
- Understand market norms
- Identify pricing opportunities

### 6. Export and Share
- Download results for presentations
- Share with product, marketing, and finance teams
- Use data to build business cases

---

## Troubleshooting

### Low Suitability Scores (<40%)

**Possible Causes:**
1. Price too high for target market
2. Low disease prevalence in personas
3. Poor availability in target regions
4. Brand mismatch with audience

**Solutions:**
- Reduce price by 20-30%
- Target different disease/indication
- Improve distribution strategy
- Adjust brand positioning

### High Variance Across Segments

**Possible Causes:**
1. Price affects different income levels differently
2. Availability varies by city tier
3. Disease prevalence varies by region

**Solutions:**
- Consider tiered pricing strategy
- Phased launch (start with high-adoption segments)
- Region-specific marketing

### AI Insights Not Generating

**Possible Causes:**
1. Gemini API key not configured
2. API key invalid or expired
3. Network connectivity issues
4. API rate limits exceeded

**Solutions:**
- Check API key in `.streamlit/secrets.toml`
- Verify key is active at Google AI Studio
- Check internet connection
- Wait a few minutes and retry

---

## Next Steps

After analyzing your medicine:

1. **Review Results**: Understand overall suitability and key drivers
2. **Identify Issues**: Note critical barriers to adoption
3. **Implement Recommendations**: Prioritize AI suggestions by impact
4. **Test Scenarios**: Try different configurations to optimize
5. **Export Data**: Share with stakeholders for decision-making
6. **Iterate**: Refine medicine attributes based on insights
7. **Launch Strategy**: Use segment analysis to plan rollout

---

## Support

For questions or issues:
- Check [DASHBOARD_SETUP.md](DASHBOARD_SETUP.md) for setup help
- Review error messages in dashboard
- Check terminal logs for detailed errors
- Verify all dependencies installed

---

**PharmaDrishti** - Making pharmaceutical market research instant, affordable, and actionable.
