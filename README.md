# IBM HR Analytics: Workforce Retention & Compensation Equity Audit

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

---

## Executive Summary

This repository presents an enterprise-grade statistical audit and predictive modeling project based on the **IBM HR Analytics Employee Attrition & Performance** dataset (1,470 records, 35 features). 

The goal of this analysis is to address elevated voluntary employee turnover (**16.1%**) relative to industry benchmarks (**10–12%**). Replacing talent creates severe financial overhead—costing an estimated $1.5\times$ to $2.0\times$ an employee's annual salary in hiring, onboarding, and lost productivity. 

Using a two-track analytical framework, this project audits compensation parity across several features and constructs a predictive flight-risk engine to enable proactive HR intervention.

---

## Stakeholder Mandates

| Stakeholder | Role | Business Goal | Primary Analytical Deliverable |
| :--- | :--- | :--- | :--- |
| **CFO** | Chief Financial Officer | Audit compensation parity to ensure fair pay based on role/experience and identify salary anomalies. | **Multiple Linear Regression & ANCOVA Equity Model** (`notebooks/01_compensation_audit.ipynb`) |
| **CHRO** | Chief Human Resources Officer | Identify core drivers of voluntary turnover and build an early-warning flight risk classifier. | **Binomial Logistic Regression Flight Risk Engine** (`notebooks/02_attrition_analysis.ipynb`) |
| **VP of People Ops** | Vice President of People Operations | Monitor compensation metrics and turnover risk across departments in an interactive interface. | **Interactive Tableau Executive Dashboard** (`dashboard/atlas_executive_dashboard.twbx`) |

---

## Project Structure

```text
ibm-hr-analytics-turnover-compensation/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                  <-- IBM HR raw dataset snapshot
│   ├── processed/            <-- Cleaned, transformed feature-engineered data
├── notebooks/
│   ├── 00_data_profiling.ipynb   <-- Data cleaning
│   ├── 01_compensation_audit.ipynb   <-- Track 1: Linear Regression