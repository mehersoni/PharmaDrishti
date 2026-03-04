# Technical Design Document: PharmaDrishti

## Document Information

**Product Name**: PharmaDrishti  
**Version**: 1.0  
**Date**: February 2026  
**Status**: Approved for Implementation  
**Owner**: Engineering Team  

---

## 1. System Overview

### 1.1 Purpose

This document describes the technical architecture, design decisions, and implementation approach for PharmaDrishti—an AI-powered market simulation platform for pharmaceutical product launches.

### 1.2 Scope

This design covers:
- System architecture and component design
- Data models and database schema
- Machine learning pipeline
- API specifications
- User interface design
- Security and compliance measures
- Deployment architecture

### 1.3 Design Principles

1. **Simplicity**: Favor simple, maintainable solutions over complex architectures
2. **Performance**: Predictions must complete within 3 seconds
3. **Scalability**: Design for 1,000+ personas and 100+ concurrent users
4. **Reliability**: 99.5% uptime with graceful error handling
5. **Explainability**: All AI predictions must be interpretable

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                            │
│  Web Browser (Chrome, Firefox, Safari)                      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                         │
│  Streamlit Web Application                                   │
│  - Dashboard UI                                              │
│  - Input Forms                                               │
│  - Visualization Components                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Persona    │  │  Prediction  │  │  Insights    │     │
│  │   Manager    │  │   Engine     │  │  Generator   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Persona    │  │  ML Models   │  │  Scenarios   │     │
│  │   Database   │  │  (XGBoost)   │  │  Storage     │     │
│  │   (JSON)     │  │   (PKL)      │  │  (SQLite)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Component Description

#### 2.2.1 Presentation Layer
- **Technology**: Streamlit 1.28+
- **Responsibility**: User interface, input validation, visualization
- **Key Features**: Real-time updates, interactive charts, responsive design

#### 2.2.2 Application Layer
- **Technology**: Python 3.8+, Pandas, NumPy
- **Responsibility**: Business logic, data processing, orchestration
- **Components**:
  - **Persona Manager**: Load, validate, filter personas
  - **Prediction Engine**: Calculate adoption probabilities
  - **Insights Generator**: Generate recommendations and explanations

#### 2.2.3 Data Layer
- **Persona Database**: JSON files for persona data
- **ML Models**: Serialized XGBoost models (Joblib)
- **Scenarios Storage**: SQLite for user scenarios and history

---

## 3. Data Models

### 3.1 Persona Data Model

```python
@dataclass
class Persona:
    """Represents a synthetic Indian healthcare consumer"""
    
    # Identifiers
    persona_id: str
    name: str
    
    # Demographics
    age: int  # 18-60
    gender: str  # Male, Female
    city_tier: str  # Tier 1, Tier 2, Tier 3
    city: str
    state: str
    occupation: str
    
    # Financial
    annual_income_inr: float
    income_level: str  # Low, Lower-Middle, Middle, Upper-Middle, High
    monthly_healthcare_spend_inr: float
    
    # Insurance
    insurance_status: str  # Uninsured, Government Scheme, Employer-Provided, etc.
    insurance_sum_assured_inr: float
    
    # Clinical
    chronic_diseases: str  # Comma-separated list
    no_of_chronic_conditions: int
    last_doctor_visit_months_ago: int
    
    # Behavioral
    price_sensitivity_score: float  # 0-1
    preferred_healthcare_provider: str
    digital_health_adoption: str  # None, Low, Medium, High
```

**Storage**: JSON file (`data/personas.json`)  
**Size**: ~100 KB for 100 personas  
**Access Pattern**: Load once at startup, cache in memory

### 3.2 Medicine Profile Data Model

```python
@dataclass
class MedicineProfile:
    """Represents a pharmaceutical product configuration"""
    
    medicine_id: str
    target_disease: str  # Type 2 Diabetes, Hypertension, etc.
    price_inr: float  # 50-5000
    brand_strength: float  # 0-1 (0=Generic, 1=Premium Brand)
    side_effect_risk: float  # 0-1 (0=Very Safe, 1=High Risk)
    availability_score: float  # 0-1 (0=Limited, 1=Widely Available)
    insurance_compatibility: float  # 0-1 (0=Not Covered, 1=Fully Covered)
    
    # Metadata
    created_at: datetime
    created_by: str
```

**Storage**: In-memory (user input), optionally saved to SQLite  
**Validation**: All scores must be 0-1, price must be positive

### 3.3 Prediction Result Data Model

```python
@dataclass
class PredictionResult:
    """Represents adoption prediction for a persona-medicine pair"""
    
    persona_id: str
    medicine_id: str
    adoption_probability: float  # 0-1
    
    # Component scores
    disease_match_score: float
    affordability_score: float
    availability_score: float
    brand_alignment_score: float
    risk_tolerance_score: float
    
    # Metadata
    predicted_at: datetime
    model_version: str
```

**Storage**: In-memory during session, exported to CSV on demand

### 3.4 Scenario Data Model

```python
@dataclass
class Scenario:
    """Represents a saved medicine configuration with results"""
    
    scenario_id: str
    scenario_name: str
    medicine_profile: MedicineProfile
    
    # Aggregated results
    overall_adoption_rate: float
    revenue_estimate: float
    best_segment: str
    
    # Metadata
    created_at: datetime
    user_id: str
```

**Storage**: SQLite database (`data/scenarios.db`)  
**Schema**:
```sql
CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    medicine_profile JSON NOT NULL,
    overall_adoption_rate REAL,
    revenue_estimate REAL,
    best_segment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT
);
```

---

## 4. Machine Learning Pipeline

### 4.1 Training Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Persona   │────▶│  Interaction │────▶│   Feature   │
│    Data     │     │  Generation  │     │ Engineering │
└─────────────┘     └──────────────┘     └─────────────┘
                                                 │
                                                 ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Trained   │◀────│    Model     │◀────│  Training   │
│    Model    │     │  Evaluation  │     │    Data     │
└─────────────┘     └──────────────┘     └─────────────┘
```

#### 4.1.1 Interaction Generation

For each persona-medicine pair, calculate suitability score:

```python
def calculate_suitability_score(persona: Persona, medicine: MedicineProfile) -> float:
    """
    Calculate suitability score using weighted formula
    
    Returns: float between 0 and 1
    """
    
    # 1. Disease Match (35% weight)
    disease_match = 1.0 if medicine.target_disease in persona.chronic_diseases else 0.0
    
    # 2. Affordability (25% weight)
    monthly_income = persona.annual_income_inr / 12
    affordability = max(0, 1.0 - (medicine.price_inr / monthly_income))
    affordability = min(1.0, affordability)  # Cap at 1.0
    
    # 3. Availability (15% weight)
    tier_accessibility = {
        'Tier 1': 0.9,
        'Tier 2': 0.7,
        'Tier 3': 0.5
    }
    location_factor = tier_accessibility.get(persona.city_tier, 0.5)
    availability = medicine.availability_score * location_factor
    
    # 4. Brand Alignment (15% weight)
    # Higher brand strength appeals to less price-sensitive consumers
    brand_alignment = medicine.brand_strength * (1 - persona.price_sensitivity_score)
    
    # 5. Risk Tolerance (10% weight)
    # Price-sensitive consumers are more risk-averse
    risk_score = medicine.side_effect_risk * persona.price_sensitivity_score
    
    # Weighted sum
    weighted_sum = (
        0.35 * disease_match +
        0.25 * affordability +
        0.15 * availability +
        0.15 * brand_alignment +
        0.10 * (1 - risk_score)
    )
    
    # Sigmoid transformation to get probability
    probability = 1 / (1 + math.exp(-weighted_sum))
    
    return probability
```

#### 4.1.2 Feature Engineering

```python
def extract_features(persona: Persona, medicine: MedicineProfile) -> dict:
    """Extract ML features from persona and medicine"""
    
    features = {
        # Persona features
        'age': persona.age,
        'income': persona.annual_income_inr,
        'city_tier_encoded': encode_tier(persona.city_tier),  # 1, 2, 3
        'insurance_status_encoded': encode_insurance(persona.insurance_status),
        'chronic_condition_count': persona.no_of_chronic_conditions,
        'price_sensitivity': persona.price_sensitivity_score,
        'digital_adoption_encoded': encode_digital(persona.digital_health_adoption),
        
        # Medicine features
        'price': medicine.price_inr,
        'brand_strength': medicine.brand_strength,
        'side_effect_risk': medicine.side_effect_risk,
        'availability': medicine.availability_score,
        'insurance_compatibility': medicine.insurance_compatibility,
        'disease_encoded': encode_disease(medicine.target_disease),
        
        # Interaction features
        'disease_match': calculate_disease_match(persona, medicine),
        'affordability': calculate_affordability(persona, medicine),
        'availability_match': calculate_availability_match(persona, medicine),
        'brand_alignment': calculate_brand_alignment(persona, medicine),
        'risk_score': calculate_risk_score(persona, medicine)
    }
    
    return features
```

#### 4.1.3 Model Training

```python
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def train_model(interactions_df: pd.DataFrame) -> XGBRegressor:
    """Train XGBoost model on interaction data"""
    
    # Prepare features and target
    X = interactions_df.drop(['persona_id', 'medicine_id', 'suitability_score'], axis=1)
    y = interactions_df['suitability_score']
    
    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Configure model
    model = XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        objective='reg:squarederror'
    )
    
    # Train
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        early_stopping_rounds=10,
        verbose=False
    )
    
    # Evaluate
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Performance:")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  R² Score: {r2:.4f}")
    
    return model
```

**Model Hyperparameters**:
- `n_estimators`: 100 (number of trees)
- `max_depth`: 6 (tree depth, prevents overfitting)
- `learning_rate`: 0.1 (step size)
- `subsample`: 0.8 (row sampling)
- `colsample_bytree`: 0.8 (column sampling)

**Expected Performance**:
- R² Score: > 0.85
- RMSE: < 0.15
- Training Time: < 5 minutes on standard laptop

### 4.2 Prediction Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Medicine   │────▶│   Feature    │────▶│   Model     │
│   Input     │     │  Extraction  │     │ Prediction  │
└─────────────┘     └──────────────┘     └─────────────┘
       │                                         │
       │                                         ▼
       │                                  ┌─────────────┐
       │                                  │   Results   │
       │                                  │ Aggregation │
       │                                  └─────────────┘
       │                                         │
       ▼                                         ▼
┌─────────────┐                          ┌─────────────┐
│   Persona   │                          │  Dashboard  │
│    Data     │                          │   Display   │
└─────────────┘                          └─────────────┘
```

```python
def predict_adoption(
    medicine: MedicineProfile,
    personas: List[Persona],
    model: XGBRegressor
) -> List[PredictionResult]:
    """Predict adoption for all personas"""
    
    results = []
    
    for persona in personas:
        # Extract features
        features = extract_features(persona, medicine)
        X = pd.DataFrame([features])
        
        # Predict
        adoption_prob = model.predict(X)[0]
        adoption_prob = max(0.0, min(1.0, adoption_prob))  # Clip to [0, 1]
        
        # Create result
        result = PredictionResult(
            persona_id=persona.persona_id,
            medicine_id=medicine.medicine_id,
            adoption_probability=adoption_prob,
            disease_match_score=features['disease_match'],
            affordability_score=features['affordability'],
            availability_score=features['availability_match'],
            brand_alignment_score=features['brand_alignment'],
            risk_tolerance_score=features['risk_score'],
            predicted_at=datetime.now(),
            model_version="1.0"
        )
        
        results.append(result)
    
    return results
```

### 4.3 SHAP Explainability

```python
import shap

def explain_predictions(
    model: XGBRegressor,
    X: pd.DataFrame
) -> dict:
    """Generate SHAP explanations for predictions"""
    
    # Create explainer
    explainer = shap.TreeExplainer(model)
    
    # Calculate SHAP values
    shap_values = explainer.shap_values(X)
    
    # Get feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': abs(shap_values).mean(axis=0)
    }).sort_values('importance', ascending=False)
    
    return {
        'shap_values': shap_values,
        'feature_importance': feature_importance,
        'base_value': explainer.expected_value
    }
```

---

## 5. API Specifications

### 5.1 Internal APIs

#### 5.1.1 Persona Manager API

```python
class PersonaManager:
    """Manages persona data loading and filtering"""
    
    def load_personas(self, filepath: str) -> List[Persona]:
        """Load personas from JSON file"""
        pass
    
    def filter_personas(
        self,
        personas: List[Persona],
        filters: dict
    ) -> List[Persona]:
        """Filter personas by attributes"""
        pass
    
    def get_persona_statistics(
        self,
        personas: List[Persona]
    ) -> dict:
        """Get demographic distribution statistics"""
        pass
```

#### 5.1.2 Prediction Engine API

```python
class PredictionEngine:
    """Handles adoption predictions"""
    
    def __init__(self, model_path: str):
        """Initialize with trained model"""
        self.model = joblib.load(model_path)
    
    def predict(
        self,
        medicine: MedicineProfile,
        personas: List[Persona]
    ) -> List[PredictionResult]:
        """Predict adoption for all personas"""
        pass
    
    def aggregate_results(
        self,
        results: List[PredictionResult]
    ) -> dict:
        """Aggregate predictions by segment"""
        pass
```

#### 5.1.3 Insights Generator API

```python
class InsightsGenerator:
    """Generates business recommendations"""
    
    def generate_recommendations(
        self,
        results: List[PredictionResult],
        medicine: MedicineProfile
    ) -> List[str]:
        """Generate actionable recommendations"""
        pass
    
    def identify_best_segment(
        self,
        results: List[PredictionResult]
    ) -> str:
        """Identify highest-adoption segment"""
        pass
    
    def calculate_revenue_estimate(
        self,
        results: List[PredictionResult],
        price: float,
        market_size_multiplier: int = 1000
    ) -> float:
        """Estimate revenue based on adoption"""
        pass
```

---

## 6. User Interface Design

### 6.1 Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│  💊 PharmaDrishti                              [User] [Help] │
├──────────────┬──────────────────────────────────────────────┤
│              │                                               │
│  SIDEBAR     │  MAIN CONTENT AREA                            │
│              │                                               │
│  Medicine    │  ┌─────────────────────────────────────────┐ │
│  Config      │  │  Overall Adoption Rate                  │ │
│              │  │  [========68%========]                  │ │
│  Disease: ▼  │  │                                         │ │
│  Diabetes    │  └─────────────────────────────────────────┘ │
│              │                                               │
│  Price:      │  ┌──────────────┐  ┌──────────────────────┐ │
│  ₹500        │  │ Adoption by  │  │ Adoption by Income   │ │
│              │  │ City Tier    │  │ Level                │ │
│  Brand: ▬▬▬  │  │ [Bar Chart]  │  │ [Bar Chart]          │ │
│              │  └──────────────┘  └──────────────────────┘ │
│  Risk: ▬▬    │                                               │
│              │  💡 Recommendations                           │
│  [Predict]   │  • Target Tier 1 cities (75% adoption)       │
│              │  • Consider ₹400-600 price range             │
│  [Save]      │  • Strong affordability factor               │
│              │                                               │
│  Scenarios   │  📥 [Download CSV] [Download PDF]            │
│  • Scenario1 │                                               │
│  • Scenario2 │                                               │
└──────────────┴──────────────────────────────────────────────┘
```

### 6.2 Color Scheme

- **Primary**: #1f77b4 (Blue) - Trust, healthcare
- **Success**: #2ca02c (Green) - High adoption (>70%)
- **Warning**: #ff7f0e (Orange) - Medium adoption (40-70%)
- **Danger**: #d62728 (Red) - Low adoption (<40%)
- **Background**: #ffffff (White)
- **Text**: #333333 (Dark Gray)

### 6.3 Key Visualizations

#### 6.3.1 Gauge Chart (Overall Adoption)
```python
import plotly.graph_objects as go

fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=68,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Adoption Rate"},
    delta={'reference': 50},
    gauge={
        'axis': {'range': [None, 100]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 40], 'color': "lightgray"},
            {'range': [40, 70], 'color': "gray"},
            {'range': [70, 100], 'color': "lightgreen"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 50
        }
    }
))
```

#### 6.3.2 Bar Chart (Segment Comparison)
```python
import plotly.express as px

fig = px.bar(
    x=['Tier 1', 'Tier 2', 'Tier 3'],
    y=[75, 65, 52],
    labels={'x': 'City Tier', 'y': 'Adoption Rate (%)'},
    title='Adoption by City Tier',
    color=[75, 65, 52],
    color_continuous_scale='Blues'
)
```

---

## 7. Security & Compliance

### 7.1 Data Security

**Encryption**:
- HTTPS for all communications (TLS 1.3)
- Data at rest encrypted using AES-256
- API keys stored in environment variables (not in code)

**Access Control**:
- Role-based access control (RBAC)
- Session management with secure cookies
- Password hashing using bcrypt

**Audit Logging**:
- Log all user actions (login, predictions, exports)
- Store logs for 90 days
- Regular security audits

### 7.2 DPDP Act Compliance

- 100% synthetic data (no real patient information)
- Clear privacy policy and terms of service
- User consent for data collection
- Right to data deletion
- Data minimization (collect only necessary data)

### 7.3 Model Security

- Model versioning and rollback capability
- Input validation to prevent adversarial attacks
- Rate limiting to prevent abuse
- Model performance monitoring

---

## 8. Deployment Architecture

### 8.1 Infrastructure

```
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud                               │
│                                                              │
│  ┌────────────────┐         ┌────────────────┐             │
│  │   CloudFront   │────────▶│   S3 Bucket    │             │
│  │   (CDN)        │         │   (Static)     │             │
│  └────────────────┘         └────────────────┘             │
│          │                                                   │
│          ▼                                                   │
│  ┌────────────────┐         ┌────────────────┐             │
│  │   EC2 Instance │────────▶│   RDS (SQLite) │             │
│  │   (Streamlit)  │         │   (Scenarios)  │             │
│  └────────────────┘         └────────────────┘             │
│          │                                                   │
│          ▼                                                   │
│  ┌────────────────┐                                         │
│  │   S3 Bucket    │                                         │
│  │   (Models)     │                                         │
│  └────────────────┘                                         │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Deployment Process

1. **Build**: Package application with dependencies
2. **Test**: Run automated tests
3. **Deploy**: Push to EC2 instance
4. **Verify**: Health check and smoke tests
5. **Monitor**: CloudWatch metrics and logs

### 8.3 Monitoring & Alerting

**Metrics**:
- Response time (p50, p95, p99)
- Error rate
- Prediction accuracy
- User activity

**Alerts**:
- Response time > 5 seconds
- Error rate > 1%
- CPU usage > 80%
- Disk usage > 90%

---

## 9. Performance Optimization

### 9.1 Caching Strategy

```python
import streamlit as st

@st.cache_data
def load_personas():
    """Cache persona data (refreshes on file change)"""
    return pd.read_json('data/personas.json')

@st.cache_resource
def load_model():
    """Cache model (persists across sessions)"""
    return joblib.load('models/adoption_model.pkl')
```

### 9.2 Database Optimization

- Index on `scenario_id`, `user_id`, `created_at`
- Limit query results to 100 records
- Use connection pooling

### 9.3 Code Optimization

- Vectorize calculations using NumPy
- Batch predictions instead of loops
- Lazy load visualizations
- Compress exported files

---

## 10. Testing Strategy

### 10.1 Unit Tests

- Test individual functions (persona loading, feature extraction, etc.)
- Target: 80% code coverage
- Framework: pytest

### 10.2 Integration Tests

- Test end-to-end prediction pipeline
- Test dashboard interactions
- Test data export functionality

### 10.3 Performance Tests

- Load test with 100 concurrent users
- Stress test with 1,000 personas
- Measure prediction latency

### 10.4 User Acceptance Testing

- Pilot with 3-5 pharmaceutical companies
- Collect feedback on usability
- Validate prediction accuracy against real launches

---

## 11. Maintenance & Support

### 11.1 Model Retraining

- Retrain quarterly with new persona data
- A/B test new models before deployment
- Maintain model version history

### 11.2 Bug Fixes

- Critical bugs: Fix within 24 hours
- High priority: Fix within 1 week
- Medium/Low: Fix in next release

### 11.3 Feature Updates

- Monthly feature releases
- User feedback incorporated into roadmap
- Backward compatibility maintained

---

## 12. Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Model accuracy degrades | High | Medium | Regular retraining, A/B testing |
| Performance issues at scale | High | Low | Load testing, caching, optimization |
| Security breach | Critical | Low | Encryption, audits, monitoring |
| User adoption low | High | Medium | User research, training, support |
| Cloud costs exceed budget | Medium | Medium | Cost monitoring, optimization |

---

## 13. Appendix

### 13.1 Technology Stack Summary

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | Streamlit | 1.28+ |
| Backend | Python | 3.8+ |
| ML Framework | XGBoost | 1.7+ |
| Explainability | SHAP | 0.42+ |
| Data Processing | Pandas | 2.0+ |
| Visualization | Plotly | 5.14+ |
| Database | SQLite | 3.40+ |
| Cloud | AWS | - |

### 13.2 File Structure

```
pharmadrishti/
├── data/
│   ├── personas.json
│   └── scenarios.db
├── models/
│   ├── adoption_model.pkl
│   └── label_encoders.pkl
├── src/
│   ├── persona_manager.py
│   ├── prediction_engine.py
│   ├── insights_generator.py
│   └── utils.py
├── tests/
│   ├── test_persona_manager.py
│   ├── test_prediction_engine.py
│   └── test_integration.py
├── dashboard.py
├── train_model.py
├── requirements.txt
└── README.md
```

---

**PharmaDrishti Technical Design Document**  
© 2026 PharmaDrishti. Confidential and Proprietary.
