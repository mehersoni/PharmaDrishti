# PharmaDrishti - Technical Analysis Report

## Executive Summary

**Project**: PharmaDrishti - AI-Powered Pharmaceutical Market Intelligence Platform  
**Type**: Data Science & Machine Learning Web Application  
**Domain**: Healthcare Analytics & Pharmaceutical Market Research  
**Status**: Production-Ready  
**Date**: March 1, 2026

---

## 1. Project Overview

### 1.1 Purpose
PharmaDrishti is an intelligent market simulation platform that predicts pharmaceutical product adoption across India's diverse healthcare landscape using synthetic persona modeling and machine learning.

### 1.2 Core Value Proposition
- Reduces market research time from 6-12 months to 2-3 seconds
- Cuts research costs by 90-97% (from ₹50L-2Cr to ₹5L)
- Provides unlimited scenario testing vs traditional 2-3 scenarios
- Covers pan-India market vs urban-focused traditional research

---

## 2. Technical Architecture

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                      │
│              Streamlit Web Dashboard                     │
│         (Interactive UI with Real-time Updates)          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  APPLICATION LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Data       │  │  Suitability │  │  AI Insights │ │
│  │   Loader     │  │  Calculator  │  │  Generator   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Medicine    │  │   Market     │  │  Persona     │ │
│  │  Generator   │  │  Comparator  │  │  Manager     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                     DATA LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Personas   │  │  ML Models   │  │   Market     │ │
│  │   (JSON)     │  │  (XGBoost)   │  │   Data       │ │
│  │  100 records │  │   Trained    │  │  (NPPAIPDMS) │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | Streamlit | 1.28+ | Web UI framework |
| **Backend** | Python | 3.8+ | Core logic |
| **ML Framework** | XGBoost | 1.7+ | Gradient boosting |
| **Explainability** | SHAP | Latest | Feature importance |
| **AI Integration** | Google Gemini | Pro | NLP insights