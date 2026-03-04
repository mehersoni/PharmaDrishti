import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_personas
from suitability_calculator import calculate_suitability
import google.generativeai as genai

st.set_page_config(page_title="PharmaDrishti", page_icon="💊", layout="wide")

# Custom CSS for white background and styling
st.markdown("""
<style>
    /* Main app background - Pure White */
    .stApp {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    /* Sidebar styling - Dark background with white text */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #ffffff !important;
    }

    /* Selectbox in sidebar - white text on dark bg */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #334155 !important;
    }

    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] input {
        color: #ffffff !important;
    }

    /* Number input in sidebar */
    section[data-testid="stSidebar"] .stNumberInput input,
    section[data-testid="stSidebar"] .stTextInput input {
        background-color: #334155 !important;
        border: 1px solid #475569 !important;
        color: #ffffff !important;
    }

    /* Slider labels and value text in sidebar */
    section[data-testid="stSidebar"] .stSlider p,
    section[data-testid="stSidebar"] .stSlider span,
    section[data-testid="stSidebar"] .stSlider div {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] {
        color: #ffffff !important;
    }

    /* Slider current value tooltip/display */
    section[data-testid="stSidebar"] [data-testid="stSlider"] output,
    section[data-testid="stSidebar"] [data-testid="stSlider"] p,
    section[data-testid="stSidebar"] .stSlider > div > div > div > div {
        color: #ffffff !important;
    }

    /* Expander in sidebar */
    section[data-testid="stSidebar"] .stExpander,
    section[data-testid="stSidebar"] .stExpander summary,
    section[data-testid="stSidebar"] .stExpander summary p,
    section[data-testid="stSidebar"] .stExpander summary span,
    section[data-testid="stSidebar"] details summary {
        color: #ffffff !important;
        background-color: #334155 !important;
    }

    section[data-testid="stSidebar"] details {
        background-color: #334155 !important;
        border: 1px solid #475569 !important;
        border-radius: 6px;
    }

    /* ── DROPDOWN FIX ── */
    /* Background of the floating popup */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] > div > div {
        background-color: #1e293b !important;
    }

    /* Force WHITE text on every element inside the popup */
    div[data-baseweb="popover"] * {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }

    /* Individual option rows */
    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="popover"] li,
    ul[role="listbox"] li,
    ul[role="listbox"] [role="option"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }

    /* Hover state */
    div[data-baseweb="popover"] [role="option"]:hover,
    div[data-baseweb="popover"] li:hover,
    ul[role="listbox"] [role="option"]:hover,
    ul[role="listbox"] li:hover {
        background-color: #334155 !important;
        color: #ffffff !important;
    }

    /* Selected / active option */
    div[data-baseweb="popover"] [aria-selected="true"],
    ul[role="listbox"] [aria-selected="true"] {
        background-color: #475569 !important;
        color: #ffffff !important;
    }
    /* ── END DROPDOWN FIX ── */

    /* Main content area - White */
    .main .block-container {
        background-color: #ffffff !important;
        padding-top: 2rem;
        max-width: 1200px;
        color: #1a1a1a !important;
    }
    
    /* Metric containers - Dark text on white */
    [data-testid="stMetricValue"] {
        color: #1f77b4 !important;
        font-weight: 700;
        font-size: 26px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #1a1a1a !important;
        font-weight: 500;
    }
    
    /* Headers - Dark text on white */
    h1, h2, h3 {
        color: #1a1a1a !important;
        font-weight: 700;
    }

    /* Body text - Dark on white */
    body, p, span, div, .stMarkdown {
        color: #1a1a1a !important;
    }
    
    /* Cards and containers - White with border */
    .stAlert {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px;
    }
    
    .stExpander {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px;
    }
    
    /* Buttons - Blue theme */
    .stButton>button {
        background-color: #1f77b4 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 2.5rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #1557a0 !important;
        box-shadow: 0 4px 8px rgba(31, 119, 180, 0.3);
        transform: translateY(-2px);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: #ffffff !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8f9fa !important;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #555555 !important;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1f77b4 !important;
        font-weight: 600;
    }
    
    /* Slider styling */
    .stSlider>div>div>div>div {
        background-color: #1f77b4 !important;
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess {
        background-color: #d4edda !important;
        border: 1px solid #c3e6cb !important;
        color: #155724 !important;
    }
    
    .stInfo {
        background-color: #d1ecf1 !important;
        border: 1px solid #bee5eb !important;
        color: #0c5460 !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        border: 1px solid #ffeaa7 !important;
        color: #856404 !important;
    }
    
    /* Plotly charts - white background */
    .js-plotly-plot {
        background-color: #ffffff !important;
    }
    
    /* Remove default Streamlit branding colors */
    .css-1d391kg, .css-1v0mbdj {
        background-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini API (you'll need to set your API key)
@st.cache_resource
def init_gemini():
    """Initialize Gemini API with API key from environment or user input"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        api_key = st.secrets.get('GEMINI_API_KEY', None)
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.0-flash')
    return None

# Load personas data
@st.cache_data
def load_data():
    """Load persona data"""
    personas = load_personas('data/indian_healthcare_personas.json')
    return personas

# Load market data from NPPAIPDMS dataset
@st.cache_data
def load_market_data():
    """Load market data from NPPAIPDMS dataset"""
    try:
        # Try to load from parent data directory first
        market_path = Path(__file__).parent.parent / 'data' / 'nppaipdms.csv'
        if not market_path.exists():
            # Try current directory
            market_path = Path('data/nppaipdms.csv')
        
        if market_path.exists():
            df = pd.read_csv(market_path)
            # Clean column names
            df.columns = ['id', 'year', 'medicine_name', 'formulation', 'notification', 'price']
            
            # Extract numeric price from price column (e.g., "₹ 0.28(1 Tablet)" -> 0.28)
            df['price_numeric'] = df['price'].str.extract(r'₹\s*([\d.]+)')[0].astype(float)
            
            return df
        else:
            st.warning("Market data file not found. Comparative analysis will be limited.")
            return None
    except Exception as e:
        st.warning(f"Could not load market data: {e}")
        return None

def calculate_detailed_scores(persona, medicine_config, market_data=None):
    """Calculate detailed component scores for explanation with market pricing"""
    
    # 1. Disease Match (30% weight)
    persona_diseases = str(persona.get('chronic_diseases', '')).lower()
    target_disease = str(medicine_config.get('target_disease', '')).lower()
    disease_match = 1.0 if target_disease in persona_diseases else 0.0
    
    # 2. Affordability (25% weight)
    monthly_income = persona.get('annual_income_inr', 0) / 12
    batch_price = medicine_config.get('batch_price_inr', 0)
    
    if monthly_income > 0:
        affordability = max(0.0, 1.0 - (batch_price / (monthly_income * 100)))
        affordability = min(1.0, affordability)
    else:
        affordability = 0.0
    
    # 3. Market Pricing Competitiveness (20% weight)
    market_pricing_score = 0.5  # Default neutral
    
    if market_data is not None and not market_data.empty:
        try:
            disease_keywords = target_disease.split()
            similar_medicines = market_data[
                market_data['medicine_name'].str.contains('|'.join(disease_keywords), case=False, na=False)
            ]
            
            if len(similar_medicines) > 0:
                market_prices = similar_medicines['price_numeric'].dropna()
                if len(market_prices) > 0:
                    avg_market_price = market_prices.mean()
                    
                    if avg_market_price > 0:
                        price_ratio = batch_price / avg_market_price
                        
                        if price_ratio < 0.7:
                            market_pricing_score = 1.0
                        elif price_ratio < 1.3:
                            market_pricing_score = 1.0 - (price_ratio - 0.7) * (0.4 / 0.6)
                        elif price_ratio < 2.0:
                            market_pricing_score = 0.6 - (price_ratio - 1.3) * (0.4 / 0.7)
                        else:
                            market_pricing_score = 0.1
        except Exception:
            market_pricing_score = 0.5
    
    # 4. Manufacturing (15% weight)
    tier_accessibility = {'Tier 1': 0.9, 'Tier 2': 0.7, 'Tier 3': 0.5}
    city_tier = persona.get('city_tier', 'Tier 3')
    location_factor = tier_accessibility.get(city_tier, 0.5)
    manufacturing = medicine_config.get('manufacturing_score', 0.5) * location_factor
    
    # 5. Risk Tolerance (10% weight)
    side_effect_risk = medicine_config.get('side_effect_risk', 0.5)
    price_sensitivity = persona.get('price_sensitivity_score', 0.5)
    risk_score = side_effect_risk * price_sensitivity
    
    return {
        'disease_match': disease_match,
        'affordability': affordability,
        'market_pricing': market_pricing_score,
        'manufacturing': manufacturing,
        'risk_score': risk_score
    }

def generate_ai_insights(medicine_config, overall_score, segment_scores, component_scores, model):
    """Generate AI-powered insights using Gemini"""
    if model is None:
        return "AI insights unavailable. Please configure GEMINI_API_KEY."
    
    prompt = f"""
    As a pharmaceutical market analyst, analyze this medicine launch scenario:
    
    Medicine Details:
    - Target Disease: {medicine_config['target_disease']}
    - Batch Price: ₹{medicine_config['batch_price_inr']:,}
    - Side Effect Risk: {medicine_config['side_effect_risk']:.2f}
    - Manufacturing Score: {medicine_config['manufacturing_score']:.2f}
    - Launch Locality: {medicine_config.get('launch_state', 'Pan-India')}
    
    Market Analysis Results:
    - Overall Suitability Score: {overall_score:.1%}
    - Best Performing Segment: {segment_scores['best_segment']} ({segment_scores['best_score']:.1%})
    - Worst Performing Segment: {segment_scores['worst_segment']} ({segment_scores['worst_score']:.1%})
    
    Component Scores (Average):
    - Disease Match: {component_scores['disease_match']:.2f}
    - Affordability: {component_scores['affordability']:.2f}
    - Manufacturing: {component_scores['manufacturing']:.2f}
    - Risk Score: {component_scores['risk_score']:.2f}
    
    Provide:
    1. Why is the suitability score at this level? (2-3 key reasons)
    2. What are the main barriers to adoption? (2-3 specific issues)
    3. Actionable recommendations to improve market launch (3-4 specific suggestions with expected impact)
    
    Be specific, data-driven, and actionable. Format with clear sections.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating AI insights: {e}"

def compare_with_market(medicine_config, market_df):
    """Compare medicine with market data and provide detailed analysis"""
    if market_df is None:
        return None
    
    try:
        target = medicine_config['target_disease'].lower()
        batch_price = medicine_config['batch_price_inr']
        
        # Search for similar medicines by disease/ingredient keywords
        disease_keywords = {
            'Type 2 Diabetes': ['insulin', 'metformin', 'glipizide', 'diabetes'],
            'Hypertension': ['amlodipine', 'losartan', 'atenolol', 'blood pressure'],
            'Asthma': ['salbutamol', 'budesonide', 'formoterol', 'inhaler'],
            'Arthritis': ['diclofenac', 'ibuprofen', 'naproxen', 'arthritis'],
            'Heart Disease': ['aspirin', 'atorvastatin', 'clopidogrel', 'cardiac'],
            'Thyroid Disorder': ['levothyroxine', 'thyroid'],
            'Chronic Kidney Disease': ['erythropoietin', 'kidney', 'renal'],
            'Obesity': ['orlistat', 'weight'],
            'Anemia': ['iron', 'ferrous', 'folic acid', 'anemia'],
            'COPD': ['tiotropium', 'copd', 'bronchodilator']
        }
        
        keywords = disease_keywords.get(medicine_config['target_disease'], [target])
        
        # Filter similar medicines
        similar_medicines = market_df[
            market_df['medicine_name'].str.lower().str.contains('|'.join(keywords), na=False, regex=True)
        ]
        
        if len(similar_medicines) > 0:
            avg_price = similar_medicines['price_numeric'].mean()
            min_price = similar_medicines['price_numeric'].min()
            max_price = similar_medicines['price_numeric'].max()
            
            # Price comparison
            price_position = "competitive"
            if batch_price < avg_price * 0.8:
                price_position = "below market average"
            elif batch_price > avg_price * 1.2:
                price_position = "above market average"
            
            return {
                'count': len(similar_medicines),
                'avg_price': avg_price,
                'min_price': min_price,
                'max_price': max_price,
                'price_position': price_position,
                'sample': similar_medicines.head(10),
                'years': similar_medicines['year'].unique().tolist()
            }
        else:
            return {
                'count': 0,
                'message': f"No similar medicines found for {medicine_config['target_disease']} in market database"
            }
    except Exception as e:
        st.warning(f"Market comparison error: {e}")
        return None

# Main App
# Display logo and title
logo_path = Path(__file__).parent / 'pharma.png'
if logo_path.exists():
    # Center the logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(str(logo_path), width="stretch")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### AI-Powered Pharmaceutical Market Intelligence Platform")
    st.markdown("Predict medicine adoption in India's diverse market using AI-powered insights")
else:
    st.title("💊 PharmaDrishti: AI-Powered Pharma Launch Simulator")
    st.markdown("Predict medicine adoption in India's diverse market using AI-powered insights")

# Sidebar - Medicine Configuration
st.sidebar.header("🔧 Medicine Configuration")

# Disease selection
disease = st.sidebar.selectbox(
    "Target Disease",
    ['Type 2 Diabetes', 'Hypertension', 'Asthma', 'Arthritis', 
     'Heart Disease', 'Thyroid Disorder', 'Chronic Kidney Disease', 
     'Obesity', 'Anemia', 'COPD'],
    help="Select the primary disease this medicine treats"
)

# Price input
batch_price = st.sidebar.number_input(
    "Batch Price (INR)",
    min_value=5000,
    max_value=500000,
    value=50000,
    step=5000,
    help="Medicine batch price in Indian Rupees"
)

units_per_batch = st.sidebar.number_input(
    "Units per Batch",
    min_value=100,
    value=1000,
    step=100
)

unit_price = batch_price / units_per_batch

# Launch locality
launch_state = st.sidebar.selectbox(
    "Launch Locality",
    ['Pan-India', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 
     'Gujarat', 'West Bengal', 'Uttar Pradesh', 'Rajasthan', 'Punjab'],
    help="Target state/region for launch"
)

# Side effect risk
side_effect_risk = st.sidebar.slider(
    "Side Effect Risk",
    0.0, 1.0, 0.3,
    help="0 = Very safe, 1 = High risk of side effects"
)

# Manufacturing score
manufacturing_score = st.sidebar.slider(
    "Manufacturing Score",
    0.0, 1.0, 0.8,
    help="0 = Limited manufacturing capability, 1 = High manufacturing capability"
)

# Insurance compatibility
insurance_compat = st.sidebar.slider(
    "Insurance Compatibility under Schemes",
    0.0, 1.0, 0.9,
    help="0 = Not covered by any scheme, 1 = Fully covered by insurance schemes"
)

# Gemini API Key input (if not in environment)
with st.sidebar.expander("⚙️ AI Configuration"):
    gemini_key = st.text_input(
        "Gemini API Key (optional)",
        type="password",
        help="Enter your Google Gemini API key for AI-powered insights"
    )
    if gemini_key:
        os.environ['GEMINI_API_KEY'] = gemini_key

# Predict button
predict_button = st.sidebar.button("🚀 Analyze Market Suitability", type="primary")

# Main content area
if predict_button:
    with st.spinner("🔍 Analyzing market suitability..."):
        # Load data
        personas = load_data()
        market_data = load_market_data()
        gemini_model = init_gemini()
        
        if personas.empty:
            st.error("❌ Could not load persona data. Please check data/indian_healthcare_personas.json")
        else:
            # Create medicine configuration
            medicine_config = {
                'target_disease': disease,
                'batch_price_inr': batch_price,
                'side_effect_risk': side_effect_risk,
                'manufacturing_score': manufacturing_score,
                'insurance_compatibility': insurance_compat,
                'launch_state': launch_state
            }
            
            # Calculate suitability for all personas
            results = []
            component_scores_list = []
            
            for idx, persona in personas.iterrows():
                score = calculate_suitability(persona, medicine_config, market_data)
                detailed = calculate_detailed_scores(persona, medicine_config, market_data)
                
                results.append({
                    'persona': persona['name'],
                    'age': persona['age'],
                    'income': persona['annual_income_inr'],
                    'city_tier': persona['city_tier'],
                    'state': persona.get('state', 'Unknown'),
                    'suitability_score': score,
                    **detailed
                })
                component_scores_list.append(detailed)
            
            results_df = pd.DataFrame(results)
            
            # Filter by launch state if not Pan-India
            if launch_state != 'Pan-India':
                filtered_results = results_df[results_df['state'] == launch_state]
                if len(filtered_results) > 0:
                    results_df = filtered_results
                else:
                    st.warning(f"⚠️ No personas found for {launch_state}. Showing Pan-India results.")
            
            # Calculate overall metrics
            overall_score = results_df['suitability_score'].mean()
            
            # Segment analysis
            tier_scores = results_df.groupby('city_tier')['suitability_score'].mean()
            best_tier = tier_scores.idxmax()
            worst_tier = tier_scores.idxmin()
            
            segment_scores = {
                'best_segment': best_tier,
                'best_score': tier_scores[best_tier],
                'worst_segment': worst_tier,
                'worst_score': tier_scores[worst_tier]
            }
            
            # Average component scores
            avg_components = {
                'disease_match': results_df['disease_match'].mean(),
                'affordability': results_df['affordability'].mean(),
                'market_pricing': results_df['market_pricing'].mean(),
                'manufacturing': results_df['manufacturing'].mean(),
                'risk_score': results_df['risk_score'].mean()
            }
            
            # Display results
            st.success("✅ Analysis Complete!")
            
            # Overall Score
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Overall Suitability Score",
                    f"{overall_score:.1%}",
                    delta=f"{overall_score - 0.5:.1%} vs baseline"
                )
            
            with col2:
                market_penetration = (results_df['suitability_score'] > 0.5).sum()
                st.metric(
                    "Market Penetration",
                    f"{market_penetration}/{len(results_df)}",
                    f"{market_penetration/len(results_df):.1%}"
                )
            
            with col3:
                estimated_population = 10000  # scalable assumption
                expected_adoption = results_df['suitability_score'].mean()
                revenue_estimate = expected_adoption * estimated_population * unit_price
                st.metric(
                  "Projected Revenue Potential",
                  f"₹{revenue_estimate/10000000:.2f} Cr",
                  "Modeled Projection"
                )
            
            # Gauge Chart
            st.subheader("📊 Suitability Score")
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=overall_score * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Market Suitability (%)"},
                delta={'reference': 50, 'increasing': {'color': "green"}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightcoral"},
                        {'range': [40, 70], 'color': "lightyellow"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='#111111', size=14),
                title_font=dict(color='#111111', size=18),
                xaxis=dict(title_font=dict(color='#111111'), tickfont=dict(color='#111111')),
                yaxis=dict(title_font=dict(color='#111111'), tickfont=dict(color='#111111'))
            )
            st.plotly_chart(fig_gauge, width='stretch')
            
            # Component Analysis
            st.subheader("🔍 Why This Score? - Component Breakdown")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Component scores bar chart
                components_df = pd.DataFrame({
                    'Component': ['Disease Match', 'Affordability', 'Market Pricing', 'Manufacturing', 'Risk Tolerance'],
                    'Score': [
                        avg_components['disease_match'],
                        avg_components['affordability'],
                        avg_components['market_pricing'],
                        avg_components['manufacturing'],
                        1 - avg_components['risk_score']
                    ],
                    'Weight': [0.30, 0.25, 0.20, 0.15, 0.10]
                })
                
                fig_components = px.bar(
                    components_df,
                    x='Score',
                    y='Component',
                    orientation='h',
                    title='Component Scores (0-1 scale)',
                    color='Score',
                    color_continuous_scale='Viridis',
                    text='Score'
                )
                fig_components.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                fig_components.update_layout(
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    font=dict(color='#111111', size=13),
                    title_font=dict(color='#111111', size=15),
                    xaxis=dict(
                        title_font=dict(color='#111111'),
                        tickfont=dict(color='#111111'),
                        gridcolor='#e0e0e0'
                    ),
                    yaxis=dict(
                        title_font=dict(color='#111111'),
                        tickfont=dict(color='#111111')
                    ),
                    coloraxis_colorbar=dict(
                        tickfont=dict(color='#111111'),
                        title_font=dict(color='#111111')
                    )
                )
                st.plotly_chart(fig_components, width='stretch')
            
            with col2:
                # Segment comparison
                fig_tier = px.bar(
                    x=tier_scores.index,
                    y=tier_scores.values * 100,
                    labels={'x': 'City Tier', 'y': 'Suitability Score (%)'},
                    title='Suitability by City Tier',
                    color=tier_scores.values,
                    color_continuous_scale='Blues'
                )
                fig_tier.update_layout(
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    font=dict(color='#111111', size=13),
                    title_font=dict(color='#111111', size=15),
                    xaxis=dict(
                        title_font=dict(color='#111111'),
                        tickfont=dict(color='#111111')
                    ),
                    yaxis=dict(
                        title_font=dict(color='#111111'),
                        tickfont=dict(color='#111111'),
                        gridcolor='#e0e0e0'
                    ),
                    coloraxis_colorbar=dict(
                        tickfont=dict(color='#111111'),
                        title_font=dict(color='#111111')
                    )
                )
                st.plotly_chart(fig_tier, width='stretch')
            
            # Key Issues
            st.subheader("⚠️ Key Issues Identified")
            issues = []
            
            if avg_components['disease_match'] < 0.3:
                issues.append("🔴 **Low Disease Match**: Few personas have the target disease")
            if avg_components['affordability'] < 0.5:
                issues.append("🔴 **Batch Price Too High**: Medicine batch is unaffordable for many personas")
            if avg_components['market_pricing'] < 0.4:
                issues.append("🔴 **Poor Market Positioning**: Price significantly higher than market alternatives")
            elif avg_components['market_pricing'] < 0.6:
                issues.append("🟡 **Above Market Average**: Price higher than typical market rates")
            if avg_components['manufacturing'] < 0.5:
                issues.append("🔴 **Limited Manufacturing**: Manufacturing capability challenges in target regions")
            if avg_components['risk_score'] > 0.5:
                issues.append("🟡 **High Risk Perception**: Side effects concern price-sensitive consumers")
            
            if issues:
                for issue in issues:
                    st.markdown(issue)
            else:
                st.success("✅ No major issues identified!")
            
            # AI-Powered Recommendations
            st.subheader("💡 AI-Powered Recommendations")
            
            with st.spinner("🤖 Generating AI insights..."):
                ai_insights = generate_ai_insights(
                    medicine_config,
                    overall_score,
                    segment_scores,
                    avg_components,
                    gemini_model
                )
                st.markdown(ai_insights)
            
            # Market Comparison
            st.subheader("📈 Market Comparison Analysis")
            
            if market_data is not None:
                market_comp = compare_with_market(medicine_config, market_data)
                if market_comp and market_comp.get('count', 0) > 0:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Similar Medicines", market_comp['count'])
                    with col2:
                        st.metric("Avg Market Price", f"₹{market_comp['avg_price']:.2f}")
                    with col3:
                        st.metric("Price Range", f"₹{market_comp['min_price']:.2f} - ₹{market_comp['max_price']:.2f}")
                    with col4:
                        st.metric("Your Position", market_comp['price_position'].title())
                    
                    st.info(f"📊 Found {market_comp['count']} similar medicines in NPPAIPDMS database from years: {', '.join(map(str, market_comp['years']))}")
                    
                    # Price comparison chart
                    fig_price_comp = go.Figure()
                    fig_price_comp.add_trace(go.Bar(
                        x=['Market Min', 'Market Avg', 'Your Price', 'Market Max'],
                        y=[market_comp['min_price'], market_comp['avg_price'], batch_price, market_comp['max_price']],
                        marker_color=['lightblue', 'blue', 'orange', 'lightblue'],
                        text=[f"₹{market_comp['min_price']:.2f}", f"₹{market_comp['avg_price']:.2f}", 
                              f"₹{batch_price:.2f}", f"₹{market_comp['max_price']:.2f}"],
                        textposition='outside'
                    ))
                    fig_price_comp.update_layout(
                        title='Price Comparison with Market',
                        title_font=dict(color='#111111', size=15),
                        yaxis_title='Price (INR)',
                        showlegend=False,
                        paper_bgcolor='white',
                        plot_bgcolor='white',
                        font=dict(color='#111111', size=13),
                        xaxis=dict(
                            title_font=dict(color='#111111'),
                            tickfont=dict(color='#111111')
                        ),
                        yaxis=dict(
                            title_font=dict(color='#111111'),
                            tickfont=dict(color='#111111'),
                            gridcolor='#e0e0e0'
                        )
                    )
                    st.plotly_chart(fig_price_comp, use_container_width=True)
                    
                    with st.expander("📋 View Similar Medicines in Market"):
                        st.dataframe(
                            market_comp['sample'][['year', 'medicine_name', 'formulation', 'price', 'price_numeric']],
                            use_container_width=True
                        )
                elif market_comp:
                    st.info(market_comp.get('message', 'No similar medicines found in market database'))
            else:
                st.warning("⚠️ Market data not available. Please ensure nppaipdms.csv is in the data/ folder.")
            
            # Detailed Results Table
            with st.expander("📋 View Detailed Results"):
                st.dataframe(
                    results_df.sort_values('suitability_score', ascending=False),
                    use_container_width=True
                )
            
            # Download Results
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results (CSV)",
                data=csv,
                file_name=f"pharmadrishti_analysis_{disease.replace(' ', '_')}.csv",
                mime="text/csv"
            )

else:
    # Welcome screen
    st.info("👈 Configure your medicine details in the sidebar and click 'Analyze Market Suitability' to begin")
    
    st.markdown("""
    ### How It Works
    
    1. **Configure Medicine**: Enter your medicine details including disease, price, and launch locality
    2. **AI Analysis**: Our AI analyzes suitability across 100+ diverse Indian healthcare personas
    3. **Get Insights**: Receive detailed explanations of why the score is what it is
    4. **Actionable Recommendations**: Get specific suggestions to improve market launch success
    
    ### Features
    
    - 🎯 **Suitability Scoring**: Comprehensive analysis across multiple factors
    - 🤖 **AI-Powered Insights**: Gemini AI explains results and provides recommendations
    - 📊 **Market Comparison**: Compare with real market data from Kaggle
    - 🗺️ **Locality Analysis**: Target specific states or go Pan-India
    - 💰 **Revenue Estimation**: Predict potential revenue from launch
    """)