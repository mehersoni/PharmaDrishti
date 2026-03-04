# Product Requirements Document: PharmaDrishti

## Document Information

**Product Name**: PharmaDrishti  
**Version**: 1.0  
**Date**: February 2026  
**Status**: Approved for Development  
**Owner**: Product Management Team  

---

## 1. Product Overview

### 1.1 Vision Statement

PharmaDrishti will become the leading AI-powered market intelligence platform for pharmaceutical product launches in India, enabling companies to make data-driven decisions that reduce launch failures by 50% while cutting research costs by 90%.

### 1.2 Product Description

PharmaDrishti is a SaaS platform that uses synthetic persona modeling and machine learning to predict pharmaceutical product adoption across India's diverse healthcare market. The platform enables pharmaceutical companies to test unlimited product scenarios, optimize pricing strategies, and identify target segments before physical market entry.

### 1.3 Target Users

**Primary Users**:
- Product Managers at pharmaceutical companies
- Marketing Directors planning product launches
- Business Analysts conducting market research
- Strategic Planning teams

**Secondary Users**:
- Healthcare consultants
- Market research agencies
- Pharmaceutical investors conducting due diligence

### 1.4 Success Metrics

- **User Adoption**: 20 pharmaceutical companies within 12 months
- **Usage**: Average 15 simulations per customer per month
- **Accuracy**: 85%+ prediction accuracy validated against real launches
- **Customer Satisfaction**: NPS score > 50
- **Business Impact**: Customers report 30%+ reduction in launch failures

---

## 2. Functional Requirements

### 2.1 Persona Management System

**Requirement ID**: FR-001  
**Priority**: P0 (Critical)  
**User Story**: As a product manager, I need access to diverse Indian healthcare personas so that I can test how different demographic segments will respond to my product.

**Acceptance Criteria**:
1. System shall provide access to minimum 100 pre-loaded synthetic personas
2. Each persona shall include:
   - Demographics: age, gender, location (city tier, state)
   - Financial: annual income, income level, insurance status
   - Clinical: chronic diseases, number of conditions, healthcare spend
   - Behavioral: price sensitivity, digital adoption, provider preference
3. Personas shall represent diversity across:
   - City tiers: Tier 1 (metros), Tier 2 (mid-cities), Tier 3 (towns)
   - Income levels: Low (<₹2L), Lower-Middle (₹2-5L), Middle (₹5-10L), Upper-Middle (₹10-25L), High (>₹25L)
   - Age groups: 18-30, 31-45, 46-60 years
   - Health conditions: Minimum 10 disease categories
4. System shall display persona distribution statistics (demographics breakdown)
5. System shall allow filtering personas by attributes

**Dependencies**: None  
**Risks**: Persona realism may be questioned—mitigation through validation against NFHS-5 data

---

### 2.2 Medicine Profile Configuration

**Requirement ID**: FR-002  
**Priority**: P0 (Critical)  
**User Story**: As a product manager, I need to input my medicine's attributes so that the system can predict its market adoption.

**Acceptance Criteria**:
1. System shall provide input interface for medicine attributes:
   - Target disease (dropdown with 10+ options)
   - Price in INR (numeric input, range ₹50-₹5000)
   - Brand strength (slider 0-1, labeled "Generic" to "Premium Brand")
   - Side effect risk (slider 0-1, labeled "Very Safe" to "High Risk")
   - Availability score (slider 0-1, labeled "Limited" to "Widely Available")
   - Insurance compatibility (slider 0-1, labeled "Not Covered" to "Fully Covered")
2. System shall validate inputs:
   - Price must be positive number
   - All scores must be between 0 and 1
   - Target disease must be selected
3. System shall provide tooltips explaining each attribute
4. System shall allow saving medicine profiles for later use
5. System shall support quick reset to default values

**Dependencies**: FR-001 (Persona Management)  
**Risks**: Users may not understand attribute meanings—mitigation through clear labels and help text

---

### 2.3 Adoption Prediction Engine

**Requirement ID**: FR-003  
**Priority**: P0 (Critical)  
**User Story**: As a product manager, I need instant adoption predictions so that I can quickly evaluate product viability.

**Acceptance Criteria**:
1. System shall predict adoption probability for each persona based on medicine attributes
2. Prediction algorithm shall consider:
   - Disease match (35% weight): Binary match between medicine disease and persona conditions
   - Affordability (25% weight): Price relative to persona income
   - Availability (15% weight): Medicine availability × persona location accessibility
   - Brand alignment (15% weight): Brand strength × persona brand preference
   - Risk tolerance (10% weight): Side effect risk × persona risk aversion
3. System shall complete predictions for 100 personas within 3 seconds
4. System shall display:
   - Overall adoption rate (percentage)
   - Adoption by city tier (Tier 1, 2, 3)
   - Adoption by income level (Low, Lower-Middle, Middle, Upper-Middle, High)
   - Adoption by age group (18-30, 31-45, 46-60)
5. System shall show confidence intervals for predictions
6. System shall handle edge cases (e.g., zero income, missing data) gracefully

**Dependencies**: FR-001, FR-002  
**Risks**: Prediction accuracy may vary—mitigation through continuous model retraining

---

### 2.4 Interactive Dashboard

**Requirement ID**: FR-004  
**Priority**: P0 (Critical)  
**User Story**: As a marketing director, I need visual insights so that I can quickly understand market opportunities and present to stakeholders.

**Acceptance Criteria**:
1. System shall provide web-based dashboard accessible via browser
2. Dashboard shall display:
   - Gauge chart showing overall adoption rate (0-100%)
   - Bar chart comparing adoption across city tiers
   - Bar chart comparing adoption across income levels
   - Pie chart showing segment distribution
   - Data table with persona-level predictions
3. Charts shall be interactive (hover for details, click to filter)
4. Dashboard shall update in real-time when medicine attributes change
5. Dashboard shall be responsive (works on desktop, tablet)
6. Dashboard shall load within 5 seconds
7. System shall provide export options (CSV, PNG, PDF)

**Dependencies**: FR-003  
**Risks**: Performance issues with large datasets—mitigation through data pagination and caching

---

### 2.5 Scenario Comparison

**Requirement ID**: FR-005  
**Priority**: P1 (High)  
**User Story**: As a pricing strategist, I need to compare multiple pricing scenarios side-by-side so that I can identify the optimal price point.

**Acceptance Criteria**:
1. System shall allow users to save current medicine configuration as named scenario
2. System shall support minimum 5 saved scenarios simultaneously
3. System shall display comparison table showing:
   - Scenario name
   - Key attributes (price, brand strength, etc.)
   - Overall adoption rate
   - Revenue estimate
   - Best target segment
4. System shall highlight best-performing scenario (highest revenue or adoption)
5. System shall allow deleting saved scenarios
6. System shall allow exporting comparison table
7. Scenarios shall persist during user session

**Dependencies**: FR-002, FR-003  
**Risks**: User confusion with too many scenarios—mitigation through clear naming and limits

---

### 2.6 Explainable AI Insights

**Requirement ID**: FR-006  
**Priority**: P1 (High)  
**User Story**: As a business analyst, I need to understand why the AI predicts certain adoption rates so that I can trust the recommendations and explain them to stakeholders.

**Acceptance Criteria**:
1. System shall compute SHAP (SHapley Additive exPlanations) values for predictions
2. System shall display feature importance chart showing:
   - Top 5 factors influencing adoption
   - Positive vs negative impact
   - Magnitude of impact
3. System shall provide segment-specific explanations:
   - "Tier 1 adoption is high because affordability is strong"
   - "Tier 3 adoption is low due to availability constraints"
4. System shall show individual persona explanations on demand
5. Explanations shall use business-friendly language (not technical jargon)
6. System shall update explanations when medicine attributes change

**Dependencies**: FR-003  
**Risks**: SHAP computation may be slow—mitigation through pre-computation and caching

---

### 2.7 Business Recommendations

**Requirement ID**: FR-007  
**Priority**: P1 (High)  
**User Story**: As a product manager, I need actionable recommendations so that I can make informed launch decisions quickly.

**Acceptance Criteria**:
1. System shall generate automated recommendations based on predictions:
   - Optimal price range for maximum adoption or revenue
   - Best target segments (city tier, income level)
   - Market entry strategy (phased vs full launch)
   - Risk factors and mitigation strategies
2. Recommendations shall be categorized:
   - High adoption (>70%): "Strong market fit, consider premium pricing"
   - Medium adoption (40-70%): "Optimize targeting, consider tiered pricing"
   - Low adoption (<40%): "High risk, consider product modifications"
3. System shall provide specific, quantified recommendations:
   - "Reduce price by 20% to increase adoption from 45% to 62%"
   - "Focus on Tier 2 cities for 15% higher adoption"
4. System shall highlight critical risks (e.g., "Price too high for target segment")
5. Recommendations shall be exportable for presentations

**Dependencies**: FR-003, FR-006  
**Risks**: Recommendations may not align with business constraints—mitigation through customizable rules

---

### 2.8 Revenue Estimation

**Requirement ID**: FR-008  
**Priority**: P2 (Medium)  
**User Story**: As a finance analyst, I need revenue projections so that I can evaluate product ROI.

**Acceptance Criteria**:
1. System shall calculate estimated revenue based on:
   - Adoption probability per persona
   - Medicine price
   - Assumed market size (personas represent population segments)
2. System shall display:
   - Total revenue estimate
   - Revenue by segment (city tier, income level)
   - Revenue per persona
3. System shall allow users to input:
   - Market size multiplier (e.g., each persona represents 10,000 people)
   - Expected purchase frequency (monthly, quarterly, annually)
4. System shall show revenue sensitivity to price changes
5. Revenue estimates shall include confidence intervals

**Dependencies**: FR-003  
**Risks**: Revenue estimates may be inaccurate without real market data—mitigation through clear disclaimers

---

### 2.9 Data Export & Reporting

**Requirement ID**: FR-009  
**Priority**: P2 (Medium)  
**User Story**: As a marketing director, I need to export results so that I can share insights with my team and executives.

**Acceptance Criteria**:
1. System shall support exporting:
   - Prediction results (CSV format)
   - Charts and visualizations (PNG, PDF formats)
   - Full report (PDF with all insights)
2. CSV export shall include:
   - Persona ID, demographics, adoption probability
   - All input medicine attributes
   - Timestamp of prediction
3. PDF report shall include:
   - Executive summary
   - Key metrics (adoption rate, revenue estimate)
   - Charts (adoption by segment)
   - Recommendations
   - Methodology explanation
4. System shall allow customizing report content (select sections to include)
5. Exports shall be generated within 10 seconds
6. System shall track export history

**Dependencies**: FR-003, FR-004, FR-007  
**Risks**: Large exports may be slow—mitigation through background processing

---

### 2.10 Model Training & Updates

**Requirement ID**: FR-010  
**Priority**: P2 (Medium)  
**User Story**: As a data scientist, I need to retrain the model with new data so that predictions remain accurate as market conditions change.

**Acceptance Criteria**:
1. System shall support uploading new persona data (JSON format)
2. System shall validate uploaded data for completeness and format
3. System shall trigger model retraining with new data
4. Retraining shall complete within 10 minutes
5. System shall compare new model performance with previous model
6. System shall only deploy new model if performance improves (R² score increase)
7. System shall maintain model version history with:
   - Version number
   - Training date
   - Performance metrics (R², RMSE, MAE)
   - Data size (number of personas, interactions)
8. System shall allow rolling back to previous model version
9. System shall log all retraining activities for audit

**Dependencies**: FR-001, FR-003  
**Risks**: Model retraining may degrade performance—mitigation through A/B testing and rollback capability

---

## 3. Non-Functional Requirements

### 3.1 Performance

**NFR-001**: System shall complete predictions for 100 personas within 3 seconds (95th percentile)  
**NFR-002**: Dashboard shall load within 5 seconds on standard broadband connection  
**NFR-003**: System shall support 50 concurrent users without performance degradation  
**NFR-004**: System shall maintain 99.5% uptime during business hours (9 AM - 6 PM IST)  

### 3.2 Scalability

**NFR-005**: System shall scale to support 1,000+ personas without architecture changes  
**NFR-006**: System shall handle 10,000+ predictions per day  
**NFR-007**: Database shall support 100,000+ saved scenarios  

### 3.3 Security

**NFR-008**: System shall use HTTPS for all communications  
**NFR-009**: System shall implement role-based access control (admin, user, viewer)  
**NFR-010**: System shall encrypt sensitive data at rest  
**NFR-011**: System shall log all user actions for audit trail  
**NFR-012**: System shall comply with DPDP Act (Digital Personal Data Protection)  

### 3.4 Usability

**NFR-013**: System shall be usable by non-technical users without training  
**NFR-014**: System shall provide contextual help for all features  
**NFR-015**: System shall support English language (Hindi support in future)  
**NFR-016**: System shall be accessible (WCAG 2.1 Level AA compliance)  

### 3.5 Reliability

**NFR-017**: System shall handle errors gracefully without crashing  
**NFR-018**: System shall provide meaningful error messages to users  
**NFR-019**: System shall automatically retry failed predictions (max 3 attempts)  
**NFR-020**: System shall maintain data consistency across all operations  

### 3.6 Maintainability

**NFR-021**: Code shall follow PEP 8 style guidelines (Python)  
**NFR-022**: System shall have 80%+ unit test coverage  
**NFR-023**: System shall use version control (Git) for all code  
**NFR-024**: System shall have comprehensive API documentation  

---

## 4. Constraints & Assumptions

### 4.1 Constraints

1. **Budget**: Development budget limited to ₹50L for MVP
2. **Timeline**: MVP must be ready within 3 months
3. **Team**: Maximum 5 developers (2 backend, 2 frontend, 1 ML)
4. **Technology**: Must use Python for ML (existing team expertise)
5. **Deployment**: Cloud-based (AWS or Azure), no on-premise option initially

### 4.2 Assumptions

1. Users have basic understanding of pharmaceutical market research
2. Users have access to modern web browsers (Chrome, Firefox, Safari)
3. Users have stable internet connection (minimum 2 Mbps)
4. Synthetic personas are accepted as valid for simulation purposes
5. Initial 100 personas are sufficient for MVP validation

---

## 5. Dependencies

### 5.1 External Dependencies

1. **Data Sources**: NFHS-5, ICMR, NPPA data for persona validation
2. **Cloud Infrastructure**: AWS/Azure for hosting
3. **Third-party Libraries**: XGBoost, SHAP, Streamlit, Plotly
4. **Payment Gateway**: For subscription billing (Phase 2)

### 5.2 Internal Dependencies

1. **Legal Review**: Terms of service, privacy policy
2. **Compliance**: DPDP Act compliance certification
3. **Sales Team**: Customer onboarding process
4. **Support Team**: User documentation and training materials

---

## 6. Success Criteria

### 6.1 MVP Launch Criteria

- [ ] All P0 requirements implemented and tested
- [ ] System achieves 85%+ prediction accuracy on validation dataset
- [ ] Dashboard loads within 5 seconds
- [ ] Zero critical bugs in production
- [ ] User documentation complete
- [ ] 3 pilot customers onboarded successfully

### 6.2 Product-Market Fit Criteria

- [ ] 20+ paying customers within 6 months
- [ ] 70%+ customer retention rate
- [ ] NPS score > 50
- [ ] Customers report 30%+ reduction in research time
- [ ] Predictions validated against 10+ real product launches

---

## 7. Out of Scope (Future Phases)

The following features are explicitly out of scope for MVP:

- ❌ Mobile native apps (iOS, Android)
- ❌ Multi-language support (Hindi, regional languages)
- ❌ Real-time data integration from external APIs
- ❌ Competitor product comparison
- ❌ Historical trend analysis
- ❌ Integration with CRM systems (Salesforce, HubSpot)
- ❌ White-label solution for consulting firms
- ❌ Prescription data integration
- ❌ Doctor/pharmacy network analysis

---

## 8. Approval & Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | [Name] | _________ | ______ |
| Engineering Lead | [Name] | _________ | ______ |
| Design Lead | [Name] | _________ | ______ |
| Business Stakeholder | [Name] | _________ | ______ |

---

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Feb 2026 | Product Team | Initial PRD for MVP |

---

**PharmaDrishti Product Requirements Document**  
© 2026 PharmaDrishti. Confidential and Proprietary.
