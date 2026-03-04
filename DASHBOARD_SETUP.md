# PharmaDrishti Dashboard Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd pharmadrishti
pip install -r requirements.txt
```

### 2. Configure Gemini API (Optional but Recommended)

To enable AI-powered insights, you need a Google Gemini API key:

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

Or set as environment variable:
```bash
export GEMINI_API_KEY="your-actual-api-key-here"
```

Or enter it directly in the dashboard sidebar under "AI Configuration"

### 3. Run the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Features

### 1. Medicine Configuration
- **Target Disease**: Select from 10 common diseases
- **Price**: Set medicine price (₹50-₹5000)
- **Launch Locality**: Choose specific state or Pan-India
- **Brand Strength**: Generic (0) to Premium (1)
- **Side Effect Risk**: Safe (0) to High Risk (1)
- **Availability**: Limited (0) to Widely Available (1)
- **Insurance Compatibility**: Not Covered (0) to Fully Covered (1)

### 2. Suitability Analysis
The dashboard calculates suitability scores based on:
- **Disease Match (35%)**: Does the medicine treat persona's condition?
- **Affordability (25%)**: Can the persona afford it?
- **Availability (15%)**: Is it accessible in their location?
- **Brand Alignment (15%)**: Does brand match persona preferences?
- **Risk Tolerance (10%)**: Are side effects acceptable?

### 3. AI-Powered Insights (Requires Gemini API)
- Explains why the suitability score is at its current level
- Identifies main barriers to adoption
- Provides actionable recommendations to improve launch

### 4. Market Comparison (Automatic)
- Downloads and compares with real Indian medicine market data from Kaggle
- Shows similar medicines and average market prices
- Helps benchmark your pricing strategy

### 5. Visualizations
- **Gauge Chart**: Overall suitability score
- **Component Breakdown**: See which factors drive the score
- **Segment Analysis**: Compare performance across city tiers
- **Detailed Results Table**: Persona-level breakdown

### 6. Export Results
- Download complete analysis as CSV
- Share with stakeholders

## Usage Example

1. **Configure Medicine**:
   - Disease: Type 2 Diabetes
   - Price: ₹500
   - Launch: Maharashtra
   - Brand Strength: 0.7
   - Side Effect Risk: 0.3
   - Availability: 0.8
   - Insurance: 0.9

2. **Click "Analyze Market Suitability"**

3. **Review Results**:
   - Overall score: 68%
   - Best segment: Tier 1 cities (75%)
   - Key issue: Price too high for Tier 3

4. **Get AI Recommendations**:
   - Reduce price by 15% to increase adoption
   - Focus initial launch on Tier 1 cities
   - Partner with insurance providers

5. **Download Results** for presentation

## Troubleshooting

### "Could not load persona data"
- Ensure `data/indian_healthcare_personas.json` exists
- Check file path is correct

### "AI insights unavailable"
- Add Gemini API key to `.streamlit/secrets.toml`
- Or enter in sidebar under "AI Configuration"

### "Could not load market data"
- Requires internet connection for Kaggle download
- First run may take longer to download dataset
- Data is cached for subsequent runs

### Dashboard won't start
- Check all dependencies installed: `pip install -r requirements.txt`
- Verify Python version >= 3.8
- Try: `streamlit run dashboard.py --server.port 8502` (different port)

## Advanced Configuration

### Custom Persona Data
Replace `data/indian_healthcare_personas.json` with your own persona dataset. Required fields:
- name, age, annual_income_inr, city_tier, state
- chronic_diseases, price_sensitivity_score
- no_of_chronic_conditions, monthly_healthcare_spend_inr

### Adjust Scoring Weights
Edit `suitability_calculator.py` to modify component weights:
```python
weighted_sum = (
    0.35 * disease_match +      # Adjust these weights
    0.25 * affordability +
    0.15 * availability +
    0.15 * brand_alignment +
    0.10 * (1 - risk_score)
)
```

## API Keys & Security

- Never commit API keys to version control
- Use `.streamlit/secrets.toml` (already in .gitignore)
- Or use environment variables
- For production, use secure secret management

## Support

For issues or questions:
1. Check this guide
2. Review error messages in dashboard
3. Check Streamlit logs in terminal
4. Verify all dependencies installed

## Next Steps

- Add more diseases to the dropdown
- Integrate with your CRM/database
- Add user authentication for multi-user access
- Deploy to Streamlit Cloud for team access
