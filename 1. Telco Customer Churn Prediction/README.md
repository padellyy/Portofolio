# Telco Customer Churn Prediction

## Project Overview
This project focuses on analyzing and predicting customer churn for a telecommunications company. By identifying key factors that drive churn and comparing the performance of predictive models, specifically Logistic Regression, Random Forest, and XGBoost, the company can accurately identify high-risk customers. Furthermore, this project incorporates Business Intelligence (BI) analysis integrated with an interactive Power BI dashboard to deliver actionable insights and support targeted retention strategies.

## Machine Learning/Predictive Model
### Data Insegtion
The dataset was obtained from Kaggle: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn). 

To ensure consistent, column names were standardized as follows:
* `customerID` ➔ `CustomerID`
* `gender` ➔ `Gender`
* `tenure` ➔ `Tenure`
### Exploratory Data Analysis
**Dataset Overview:** The initial dataset consists of 7,043 rows and 21 columns, with `Churn` as the binary target variable (`Yes`/`No`).

**Data Type Handling:** The `TotalCharges` column was incorrectly detected as an object data type due to blank string spaces and required conversion to numerical format.

**Feature Distributions & Outliers:** 
`Tenure` exhibits a relatively stable distribution across customer groups.
 `MonthlyCharges` shows a right-skewed distribution.
 Box plot analysis confirmed no significant outliers, so no outlier treatment was required.

**Categorical Consistency:** Several categorical features contained inconsistent value representations (such as binary inputs formatted as both `Yes`/`No` and `1`/`0`) as well as redundant categories (e.g., `No` vs. `No internet service`). These were identified for standardization during preprocessing.

**Class Imbalance:** The target variable `Churn` exhibits a notable class imbalance, where the `No` class represents approximately 73% of observations. This imbalance will be handled during the modeling phase.
### Data Preprocessing
**Missing Values & Duplicate Handling:** No explicit missing values were initially detected in the raw dataset. Duplicate records were checked while excluding `CustomerID`, leading to the identification and removal of 22 duplicate rows.

**Type Conversion & Cleaning:** `TotalCharges` was converted to a numeric data type. Using `errors='coerce'`, 10 records containing whitespace-only strings (e.g., `"   "`) were converted to `NaN` and subsequently removed. `CustomerID` was dropped from the dataset as it serves as a unique identifier with no predictive value.

**Categorical Standardization & Encoding:** Binary feature values were standardized into boolean (`True`/`False`) values across categories sharing identical meanings. Due to the relatively large number of categorical features, Ordinal Encoding was applied to maintain model simplicity and avoid generating a high-dimensional sparse dataset.

### Modelling & Evaluation
**Model Selection & Top Results:** The non-oversampled XGBoost model emerged as the top performer, delivering a peak accuracy of 80.46% alongside a macro F1-score of 73.13%. Overall, XGBoost trained on the original sampling distribution was chosen as the optimal configuration based on these evaluation metrics.

**Model Comparison & Insights:** XGBoost excelled primarily due to its sequential gradient boosting framework, which iteratively corrects prior tree errors to capture complex, non-linear feature interactions. In contrast, Logistic Regression achieved slightly lower performance because its linear assumptions struggle with intricate churn patterns. Random Forest delivered competitive results but fell just short, as its parallel tree construction is less effective at refining hard-to-predict edge cases compared to XGBoost.

**Class Imbalance & Sampling Effects:** Securing the highest macro F1-score confirms that the winning model maintains balanced predictions across both churners and non-churners despite the underlying class imbalance. Interestingly, applying SMOTE-Tomek did not improve overall performance, indicating that altering the training distribution provided no additional predictive value when evaluated on the original test set.

**Key Feature Drivers:** Feature importance analysis via Logistic Regression identified `Contract` as the primary driver of churn risk. Customers on month-to-month plans face low switching friction and churn far more frequently, whereas long-term contracts naturally reflect higher subscriber commitment.

## BI Dashboard
![Dashboard Power BI](https://lh3.googleusercontent.com/d/1VAZDWHp_pi8FE6bQIoiFjxCRfEe_pkU8)

The Business Intelligence (BI) dashboard was created to provide interactive visualizations that enable stakeholders to easily monitor overall business health, track customer retention patterns, and formulate data-driven retention strategies.

Key Performance Indicators (KPIs) highlighted in the dashboard:

**Average Customer Lifetime:** This metric measures the average tenure of subscribers in months to evaluate customer longevity and loyalty before drop-off. The results show that retained customers stay significantly longer at 37.57 months compared to churned customers at 17.98 months, concluding that the early tenure phase is the most critical period for retention efforts.

**MRR: Retained vs Lost:** This indicator tracks the distribution of Monthly Recurring Revenue between active and churned accounts to quantify the direct financial impact of customer churn. The data reveals an 8M or 30.77% revenue loss out of a 25M total MRR, concluding that churn severely impacts the top-line growth of the company.

**Churn Distribution by Household Composition:** This chart segments customer retention and churn across different family status combinations to identify vulnerable demographic groups that are highly prone to leaving. The analysis shows that Single No Dependents represents the highest churn volume with 1,123 lost users, concluding that single customers without dependents are the highest risk segment.

**Long-Term Contract Share:** This metric monitors the proportion of the user base signed to multi-year plans to measure the overall level of extended customer commitment. The current share stands at 0.45 or 45%, concluding that more than half of the customers are on short-term arrangements and remain highly susceptible to quick churn.

**VIP Customer Retention Rate:** This KPI measures the percentage of high-value customers that the company successfully retains to ensure that critical revenue generating accounts remain active. The rate is currently at 0.64 or 64%, concluding that 36% of these valuable accounts are still being lost and require immediate strategic intervention.

**Churned Customers by Payment Type:** This visualization categorizes lost accounts based on their chosen payment method to detect whether specific billing processes cause friction or increase churn risk. Electronic check is identified as the primary churn driver with 2,365 lost customers, concluding there are potential issues with payment reliability or manual billing friction that need resolution.

**Early Flight Risk:** This trend line tracks monthly customer drop-offs during their first year of service to pinpoint the exact timeframe where onboarding fails and customers leave. The graph demonstrates a sharp decline peaking in Month 1 with 380 drop-offs before stabilizing after Month 6, concluding that retention strategies must be heavily focused on the first 90 days.
