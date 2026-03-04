# PharmaDrishti Dashboard - Visual Guide

## Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  💊 PharmaDrishti: AI-Powered Pharma Launch Simulator               │
│  Predict medicine adoption in India's diverse market using AI       │
├──────────────────┬──────────────────────────────────────────────────┤
│                  │                                                   │
│  SIDEBAR         │  MAIN CONTENT AREA                                │
│  (Left Panel)    │  (Right Panel - Results)                          │
│                  │                                                   │
│  🔧 Medicine     │  ✅ Analysis Complete!                            │
│  Configuration   │                                                   │
│                  │  ┌─────────┬─────────┬─────────┐                 │
│  Target Disease  │  │Overall  │Market   │Revenue  │                 │
│  [Dropdown]▼     │  │Score    │Penetr.  │Estimate │                 │
│  Type 2 Diabetes │  │  68%    │ 68/100  │₹34.2L   │                 │
│                  │  └─────────┴─────────┴─────────┘                 │
│  Price (INR)     │                                                   │
│  [500]           │  📊 Suitability Score                             │
│                  │  ┌─────────────────────────────┐                 │
│  Launch Locality │  │     [GAUGE CHART]           │                 │
│  [Dropdown]▼     │  │        68%                  │                 │
│  Maharashtra     │  │   ╱────────────╲            │                 │
│                  │  │  ╱              ╲           │                 │
│  Brand Strength  │  │ │    ●          │           │                 │
│  ▬▬▬▬▬▬▬○▬▬▬     │  │  ╲              ╱           │                 │
│  0.7             │  │   ╲────────────╱            │                 │
│                  │  └─────────────────────────────┘                 │
│  Side Effect     │                                                   │
│  Risk            │  🔍 Why This Score? - Component Breakdown         │
│  ▬▬▬○▬▬▬▬▬▬▬     │  ┌──────────────┬──────────────────────┐        │
│  0.3             │  │Component     │Adoption by City Tier │        │
│                  │  │Scores        │                      │        │
│  Availability    │  │              │  ┌─┐                │        │
│  ▬▬▬▬▬▬▬▬○▬▬     │  │Disease Match │  │█│ Tier 1: 75%    │        │
│  0.8             │  │▓▓▓▓▓▓▓▓ 0.85 │  │█│                │        │
│                  │  │              │  ├─┤                │        │
│  Insurance       │  │Affordability │  │█│ Tier 2: 65%    │        │
│  Compatibility   │  │▓▓▓▓▓ 0.52    │  │▓│                │        │
│  ▬▬▬▬▬▬▬▬▬○▬     │  │              │  ├─┤                │        │
│  0.9             │  │Availability  │  │▓│ Tier 3: 45%    │        │
│                  │  │▓▓▓▓▓▓ 0.68   │  │░│                │        │
│  ⚙️ AI Config    │  │              │  └─┘                │        │
│  [Expand]        │  │Brand Align   │                      │        │
│                  │  │▓▓▓▓▓▓▓ 0.71  │                      │        │
│  🚀 Analyze      │  │              │                      │        │
│  Market          │  │Risk Tolerance│                      │        │
│  Suitability     │  │▓▓▓▓▓▓▓▓ 0.79 │                      │        │
│  [BUTTON]        │  └──────────────┴──────────────────────┘        │
│                  │                                                   │
│                  │  ⚠️ Key Issues Identified                         │
│                  │  🔴 Price Too High: Medicine is unaffordable     │
│                  │     for many personas                             │
│                  │  🟡 Brand Mismatch: Brand positioning doesn't    │
│                  │     match target audience                         │
│                  │                                                   │
│                  │  💡 AI-Powered Recommendations                    │
│                  │  ┌─────────────────────────────────────┐         │
│                  │  │ 1. Why is the score 68%?            │         │
│                  │  │    • Strong disease match (0.85)    │         │
│                  │  │    • Moderate affordability (0.52)  │         │
│                  │  │    • Good availability (0.68)       │         │
│                  │  │                                     │         │
│                  │  │ 2. Main barriers to adoption:       │         │
│                  │  │    • Price exceeds 5% of monthly    │         │
│                  │  │      income for 45% of personas     │         │
│                  │  │    • Limited penetration in Tier 3  │         │
│                  │  │                                     │         │
│                  │  │ 3. Recommendations:                 │         │
│                  │  │    • Reduce price to ₹350 for      │         │
│                  │  │      +15% adoption                  │         │
│                  │  │    • Focus on Tier 1 cities first  │         │
│                  │  │      (75% adoption)                 │         │
│                  │  │    • Partner with insurance for    │         │
│                  │  │      +12% adoption                  │         │
│                  │  └─────────────────────────────────────┘         │
│                  │                                                   │
│                  │  📈 Market Comparison                             │
│                  │  ℹ️ Found 23 similar medicines in market         │
│                  │  Average market price: ₹425.50                   │
│                  │  [View similar medicines ▼]                      │
│                  │                                                   │
│                  │  📋 View Detailed Results [Expand ▼]             │
│                  │                                                   │
│                  │  📥 Download Results (CSV) [BUTTON]              │
│                  │                                                   │
└──────────────────┴──────────────────────────────────────────────────┘
```

---

## Step-by-Step Walkthrough

### Step 1: Configure Your Medicine

**Location**: Left sidebar

**What to do**:
1. Select target disease from dropdown
2. Enter price in INR (₹50-₹5000)
3. Choose launch locality (state or Pan-India)
4. Adjust sliders for:
   - Brand strength (0 = generic, 1 = premium)
   - Side effect risk (0 = safe, 1 = risky)
   - Availability (0 = limited, 1 = widespread)
   - Insurance compatibility (0 = not covered, 1 = fully covered)

**Example Configuration**:
```
Disease: Type 2 Diabetes
Price: ₹500
Locality: Maharashtra
Brand Strength: 0.7 (established brand)
Side Effect Risk: 0.3 (relatively safe)
Availability: 0.8 (widely available)
Insurance: 0.9 (mostly covered)
```

---

### Step 2: Optional - Configure AI

**Location**: Sidebar, under "⚙️ AI Configuration" (expandable)

**What to do**:
1. Click to expand AI Configuration section
2. Enter your Gemini API key (if not in secrets.toml)
3. Or skip if you already configured it

**Why**:
- Enables AI-powered explanations and recommendations
- Free API key from Google AI Studio
- Optional but highly recommended

---

### Step 3: Analyze Market Suitability

**Location**: Sidebar, bottom

**What to do**:
1. Click the "🚀 Analyze Market Suitability" button
2. Wait 2-3 seconds for analysis

**What happens**:
- Loads 100 diverse Indian healthcare personas
- Calculates suitability score for each persona
- Aggregates results by segment
- Generates AI insights (if configured)
- Downloads market data (first time only)

---

### Step 4: Review Overall Metrics

**Location**: Top of main content area

**What you see**:
```
┌─────────────────┬─────────────────┬─────────────────┐
│ Overall         │ Market          │ Revenue         │
│ Suitability     │ Penetration     │ Estimate        │
│ Score           │                 │                 │
│                 │                 │                 │
│    68%          │   68/100        │   ₹34.2L        │
│ +18% vs baseline│   68%           │ from sample     │
└─────────────────┴─────────────────┴─────────────────┘
```

**What it means**:
- **Overall Score**: Average adoption probability (68% = good)
- **Market Penetration**: How many personas likely to adopt (68 out of 100)
- **Revenue Estimate**: Potential revenue from sample (multiply by market size)

---

### Step 5: Understand the Score (Gauge Chart)

**Location**: Below metrics

**What you see**:
```
        Market Suitability (%)
              68%
         ╱────────────╲
        ╱              ╲
       │       ●        │
        ╲              ╱
         ╲────────────╱
    
    Red (0-40%)  Yellow (40-70%)  Green (70-100%)
```

**What it means**:
- **Red zone**: Low adoption, high risk
- **Yellow zone**: Moderate adoption, needs optimization
- **Green zone**: High adoption, strong market fit
- **Needle position**: Your current score (68% = upper yellow)

---

### Step 6: Analyze Components

**Location**: Component Breakdown section

**Left Chart - Component Scores**:
```
Disease Match     ▓▓▓▓▓▓▓▓▓ 0.85
Affordability     ▓▓▓▓▓ 0.52
Availability      ▓▓▓▓▓▓▓ 0.68
Brand Alignment   ▓▓▓▓▓▓▓ 0.71
Risk Tolerance    ▓▓▓▓▓▓▓▓ 0.79
```

**What it means**:
- **Disease Match (0.85)**: Strong - many personas need this medicine
- **Affordability (0.52)**: Moderate - price is a barrier for some
- **Availability (0.68)**: Good - decent distribution
- **Brand Alignment (0.71)**: Good - brand matches audience
- **Risk Tolerance (0.79)**: Strong - side effects acceptable

**Right Chart - Segment Analysis**:
```
Tier 1: ████████ 75%
Tier 2: ██████ 65%
Tier 3: ████ 45%
```

**What it means**:
- Best performance in Tier 1 cities (metros)
- Moderate in Tier 2 (mid-size cities)
- Weakest in Tier 3 (smaller towns)
- Suggests phased launch strategy

---

### Step 7: Identify Key Issues

**Location**: Key Issues section

**What you see**:
```
⚠️ Key Issues Identified

🔴 Price Too High: Medicine is unaffordable for many personas

🟡 Brand Mismatch: Brand positioning doesn't match target audience
```

**What it means**:
- **🔴 Critical**: Must address before launch
- **🟡 Warning**: Should optimize for better results
- Each issue points to specific problem area

---

### Step 8: Get AI Recommendations

**Location**: AI-Powered Recommendations section

**What you see**:
```
💡 AI-Powered Recommendations

1. Why is the suitability score at this level?
   • Strong disease match (0.85) drives adoption
   • Moderate affordability (0.52) limits Tier 2/3 penetration
   • Good availability (0.68) supports distribution

2. What are the main barriers to adoption?
   • Price point of ₹500 exceeds 5% of monthly income for 45% of personas
   • Limited brand recognition in Tier 3 cities
   • Competition from generic alternatives at ₹300-350

3. Actionable recommendations to improve market launch:
   • Reduce price to ₹350 (expected +15% adoption, especially in Tier 2/3)
   • Focus initial launch on Tier 1 cities (75% adoption vs 45% in Tier 3)
   • Partner with Ayushman Bharat for insurance coverage (+12% adoption)
   • Consider tiered pricing: ₹500 (Tier 1), ₹400 (Tier 2), ₹350 (Tier 3)
```

**What it means**:
- AI analyzes your results in context
- Explains WHY the score is what it is
- Identifies SPECIFIC barriers
- Provides ACTIONABLE recommendations with expected impact

---

### Step 9: Compare with Market

**Location**: Market Comparison section

**What you see**:
```
📈 Market Comparison

ℹ️ Found 23 similar medicines in market database
Average market price: ₹425.50

[View similar medicines ▼]
  Medicine A - ₹380 - Generic
  Medicine B - ₹450 - Branded
  Medicine C - ₹520 - Premium
  ...
```

**What it means**:
- Your price (₹500) is above market average (₹425)
- Explains why affordability score is moderate
- Helps benchmark pricing strategy
- Shows competitive landscape

---

### Step 10: Export Results

**Location**: Bottom of page

**What to do**:
1. Click "📥 Download Results (CSV)" button
2. Save file to your computer

**What you get**:
- CSV file with all persona-level results
- Includes: name, age, income, city tier, state, suitability score, component scores
- Filename: `pharmadrishti_analysis_Type_2_Diabetes.csv`

**Use for**:
- Sharing with stakeholders
- Further analysis in Excel/Python
- Documentation and compliance
- Historical tracking

---

## Common Workflows

### Workflow 1: Price Optimization

**Goal**: Find optimal price point

**Steps**:
1. Configure medicine with initial price (e.g., ₹500)
2. Analyze and note overall score (e.g., 68%)
3. Reduce price to ₹400
4. Analyze again and note score (e.g., 75%)
5. Reduce to ₹300
6. Analyze and note score (e.g., 82%)
7. Compare revenue estimates
8. Choose price with best revenue (adoption × price)

**Result**: Data-driven pricing decision

---

### Workflow 2: Market Segmentation

**Goal**: Identify best target segments

**Steps**:
1. Configure medicine
2. Analyze with "Pan-India" locality
3. Review segment analysis (Tier 1, 2, 3)
4. Note best-performing segment (e.g., Tier 1: 75%)
5. Re-analyze with specific state (e.g., Maharashtra)
6. Compare results
7. Plan phased launch strategy

**Result**: Targeted launch plan

---

### Workflow 3: Product Positioning

**Goal**: Decide generic vs branded

**Steps**:
1. Configure as generic (brand strength: 0.2, price: ₹300)
2. Analyze and note results
3. Configure as branded (brand strength: 0.8, price: ₹800)
4. Analyze and note results
5. Compare adoption rates and revenue
6. Review AI recommendations
7. Decide positioning strategy

**Result**: Optimal brand positioning

---

## Tips for Success

### 1. Start Realistic
- Use actual medicine prices from research
- Set brand strength based on company position
- Be honest about side effect risks

### 2. Test Multiple Scenarios
- Try 3-5 different price points
- Compare generic vs branded
- Test different localities

### 3. Focus on Insights
- Don't just look at overall score
- Identify weakest component
- Prioritize AI recommendations

### 4. Use Market Data
- Compare your price with market average
- Understand competitive landscape
- Identify pricing opportunities

### 5. Export and Share
- Download results for presentations
- Share with product, marketing, finance teams
- Use data to build business cases

---

## Troubleshooting

### Issue: Low Overall Score (<40%)

**Check**:
1. Component breakdown - which is lowest?
2. Key issues section - what's flagged?
3. AI recommendations - what to fix?

**Common Causes**:
- Price too high (reduce by 20-30%)
- Low disease prevalence (wrong target disease)
- Poor availability (improve distribution)

---

### Issue: AI Insights Not Showing

**Check**:
1. Gemini API key configured?
2. Internet connection working?
3. Error message in dashboard?

**Fix**:
1. Add API key to `.streamlit/secrets.toml`
2. Or enter in sidebar under "AI Configuration"
3. Verify key is active at Google AI Studio

---

### Issue: Market Comparison Not Working

**Check**:
1. Internet connection for Kaggle download
2. First run takes longer (downloading dataset)
3. Subsequent runs use cached data

**Fix**:
- Wait for initial download to complete
- Check internet connection
- Restart dashboard if stuck

---

## Next Steps

After mastering the dashboard:

1. **Test Real Products**: Use actual medicine data
2. **Share with Team**: Export results and present
3. **Iterate**: Refine based on insights
4. **Deploy**: Consider cloud deployment for team access
5. **Integrate**: Connect with your CRM/database
6. **Expand**: Add more diseases, personas, features

---

**Ready to start? Run the dashboard and explore!**

```bash
cd pharmadrishti
streamlit run dashboard.py
```

🚀 **PharmaDrishti** - Your AI-powered pharmaceutical market intelligence platform.
