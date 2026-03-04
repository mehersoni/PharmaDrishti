# PharmaDrishti Dashboard - Quick Reference Card

## 🚀 Quick Start

```bash
cd pharmadrishti
pip install -r requirements.txt
streamlit run dashboard.py
```

Opens at: `http://localhost:8501`

---

## 📋 Input Fields

| Field | Range | Description |
|-------|-------|-------------|
| **Target Disease** | Dropdown | Disease medicine treats |
| **Price (INR)** | ₹50-₹5000 | Medicine price |
| **Launch Locality** | Dropdown | State or Pan-India |
| **Brand Strength** | 0.0-1.0 | Generic (0) to Premium (1) |
| **Side Effect Risk** | 0.0-1.0 | Safe (0) to Risky (1) |
| **Availability** | 0.0-1.0 | Limited (0) to Widespread (1) |
| **Insurance** | 0.0-1.0 | Not Covered (0) to Fully Covered (1) |

---

## 📊 Scoring Components

| Component | Weight | What It Measures |
|-----------|--------|------------------|
| **Disease Match** | 35% | Does persona need this medicine? |
| **Affordability** | 25% | Can persona afford it? |
| **Availability** | 15% | Can persona access it? |
| **Brand Alignment** | 15% | Does brand match preferences? |
| **Risk Tolerance** | 10% | Are side effects acceptable? |

---

## 🎯 Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| **70-100%** | High adoption, strong market fit | Launch with confidence |
| **40-70%** | Moderate adoption, needs optimization | Review AI recommendations |
| **0-40%** | Low adoption, high risk | Major changes needed |

---

## 🔍 Key Metrics

| Metric | What It Shows |
|--------|---------------|
| **Overall Suitability Score** | Average adoption probability |
| **Market Penetration** | # personas with >50% adoption |
| **Revenue Estimate** | Potential revenue from sample |
| **Best Segment** | Highest-performing city tier |

---

## 💡 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| **Low Score (<40%)** | Price too high | Reduce price by 20-30% |
| **Low Affordability** | Price vs income mismatch | Lower price or target higher income |
| **Low Availability** | Distribution challenges | Improve distribution or target Tier 1 |
| **Low Disease Match** | Wrong target disease | Change indication or target |
| **Low Brand Alignment** | Brand-audience mismatch | Adjust brand positioning |

---

## 🤖 AI Configuration

**Get API Key**: https://makersuite.google.com/app/apikey

**Option 1**: Add to `.streamlit/secrets.toml`
```toml
GEMINI_API_KEY = "your-key-here"
```

**Option 2**: Enter in dashboard sidebar under "⚙️ AI Configuration"

**Option 3**: Set environment variable
```bash
export GEMINI_API_KEY="your-key-here"
```

---

## 📈 Typical Workflows

### Price Optimization
1. Test at ₹500 → Note score
2. Test at ₹400 → Note score
3. Test at ₹300 → Note score
4. Compare revenue (adoption × price)
5. Choose optimal price

### Market Segmentation
1. Analyze Pan-India
2. Note best segment (Tier 1/2/3)
3. Analyze specific state
4. Plan phased launch

### Product Positioning
1. Test as generic (low brand, low price)
2. Test as branded (high brand, high price)
3. Compare adoption and revenue
4. Choose positioning

---

## 📥 Export Options

**CSV Export**: Complete results with all persona details

**Use For**:
- Stakeholder presentations
- Further analysis in Excel/Python
- Documentation and compliance
- Historical tracking

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Dashboard won't start | Check dependencies: `pip install -r requirements.txt` |
| AI insights missing | Configure Gemini API key |
| Market data not loading | Check internet connection, wait for download |
| Low scores | Review component breakdown, follow AI recommendations |
| Can't load personas | Verify `data/indian_healthcare_personas.json` exists |

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `DASHBOARD_SETUP.md` | Complete setup instructions |
| `FEATURES.md` | Detailed feature documentation |
| `DASHBOARD_GUIDE.md` | Visual walkthrough |
| `QUICK_REFERENCE.md` | This file - quick reference |
| `example_usage.py` | Python API example |

---

## 🎓 Best Practices

### ✅ Do
- Test multiple price points
- Review component breakdown
- Follow AI recommendations
- Export results for sharing
- Compare with market data

### ❌ Don't
- Rely on single scenario
- Ignore low component scores
- Skip AI configuration
- Forget to export results
- Ignore market comparison

---

## 📞 Quick Help

### Can't start dashboard?
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

### Need API key?
Visit: https://makersuite.google.com/app/apikey

### Want to see example?
```bash
python example_usage.py
```

### Need detailed help?
Read: `DASHBOARD_SETUP.md`

---

## 🎯 Success Checklist

Before presenting results:

- [ ] Tested 3+ price points
- [ ] Reviewed component breakdown
- [ ] Read AI recommendations
- [ ] Compared with market data
- [ ] Identified best segment
- [ ] Exported results as CSV
- [ ] Prepared action plan

---

## 💰 Value Proposition

| Traditional | PharmaDrishti | Improvement |
|-------------|---------------|-------------|
| 6-12 months | 2 seconds | **99% faster** |
| ₹50L-2Cr | ₹5L | **90-97% cheaper** |
| 2-3 scenarios | Unlimited | **∞ flexibility** |
| Urban-focused | Pan-India | **3x reach** |

---

## 🚀 Next Steps

1. **Install**: `pip install -r requirements.txt`
2. **Configure**: Get Gemini API key (optional)
3. **Run**: `streamlit run dashboard.py`
4. **Test**: Try different medicine configurations
5. **Export**: Download results
6. **Share**: Present to stakeholders
7. **Iterate**: Refine based on insights

---

**PharmaDrishti** - Instant, AI-powered pharmaceutical market intelligence

```bash
streamlit run dashboard.py
```

🎯 Transform your pharmaceutical market research today!
