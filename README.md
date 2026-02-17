📌 End-to-End Catastrophe Risk Modelling Platform
Project Overview

This project is an enterprise-grade replication of the Moody’s RMS Catastrophe Risk Modeling Workflow, built using open-source technologies to simulate real-world insurance risk analytics pipelines.

Catastrophe (CAT) modeling is widely used by:

Insurance Companies

Reinsurance Firms

Risk Engineering Teams

Capital Market Investors (ILS / CAT Bonds)

to estimate financial losses caused by natural disasters like:

🌪 Hurricanes
🌍 Earthquakes
🌊 Floods
🔥 Wildfires

This project demonstrates the complete Exposure → Hazard → Vulnerability → Financial Loss modeling pipeline using:

AWS Glue (PySpark ETL)

Amazon S3 Data Lake

Python Stochastic Simulation Engine

Portfolio Loss Modeling

AAL & EP Curve Calculation

Catastrophe Bond Risk Transfer Simulation

The objective is to convert messy raw exposure datasets into meaningful insurance risk metrics such as:

✔ Average Annual Loss (AAL)
✔ Occurrence Exceedance Probability (OEP)
✔ Probable Maximum Loss (PML)
✔ Catastrophe Bond Expected Loss (EL)

Industry Framework Used – The Four Box Model

This platform replicates the industry-standard CAT modeling architecture 

Catastrophe Modeling Project Wo…

:

Module	Description	Output
Hazard	Simulates physical disaster intensity	Wind Speed / Ground Motion
Exposure	Assets exposed to catastrophe risk	EDM Schema
Vulnerability	Damage estimation from hazard	Mean Damage Ratio (MDR)
Financial	Policy loss calculation	GU Loss / Gross Loss
☁️ System Architecture
Raw Exposure Data (CSV)
        ↓
Amazon S3 (Data Lake)
        ↓
AWS Glue ETL (PySpark)
        ↓
Exposure Data Module (EDM)
        ↓
Local Modeling Engine (Python)
        ↓
Hazard Simulation
        ↓
Damage Estimation
        ↓
Policy Financial Modeling
        ↓
Event Loss Table (ELT)
        ↓
Portfolio Risk Metrics
(AAL, EP Curve, PML)
        ↓
CAT Bond Simulation

🏗 Data Engineering Layer (AWS)
🔹 S3 Lakehouse Architecture
Layer	Description
Bronze	Raw Exposure Data
Silver	Cleaned Data
Gold	EDM Standardized Data
🔹 Raw Inputs

location_raw.csv

policy_raw.csv

🔹 ETL using AWS Glue + PySpark

Performed:

Schema Casting

Data Quality Validation

Geolocation Checks

TIV Cleansing

Construction Code Mapping

Occupancy Code Mapping

Financial Policy Join

Mapped to RMS-standardized:

Construction Codes

Occupancy Codes

Policy Deductibles

Policy Limits

Final EDM stored in:

s3://cat-mod-resume-project/curated/edm/


in Parquet Format for optimized analytics performance.

⚙️ Modeling Engine (Python)
📍 Module 1 – Hazard Engine

Generates Stochastic Event Set (SES)

Simulates Hurricane Events

Uses probabilistic event frequency

Wind intensity simulated using:

Gamma / Normal Distribution


Produces:

Hazard Intensity per Location

📍 Module 2 – Vulnerability Engine

Converts Hazard Intensity → Physical Damage

Damage Metric:

Mean Damage Ratio (MDR)


Based on:

Construction Type

Occupancy

Hazard Intensity

Year Built (Secondary Modifier)

Post-2000 Buildings:

✔ Receive Vulnerability Credit
✔ Reduced Structural Damage

📍 Module 3 – Financial Engine

Loss Waterfall Applied:

1️⃣ Ground Up Loss (GU)

GU Loss = TIV × MDR


2️⃣ Deductible Applied

3️⃣ Policy Limit Applied

4️⃣ Coinsurance Applied

Final Output:

Gross Loss (GR)


Stored as:

Event Loss Table (ELT)

📊 Portfolio Risk Metrics
🔹 Average Annual Loss (AAL)

Expected yearly portfolio loss:

AAL = Σ(Event Loss × Annual Rate)

🔹 EP Curve (Occurrence Exceedance Probability)

Shows probability that loss exceeds threshold L:

Used for:

✔ Capital Planning
✔ Reinsurance Purchase
✔ Risk Appetite Decisions

Example Interpretation:

There is a 1% probability that the annual portfolio loss will exceed the 100-Year PML.

💰 Advanced Risk Transfer – CAT Bond Simulation

Modeled:

Indemnity Trigger CAT Bond

Parameter	Value
Attachment	$100M
Exhaustion	$200M
Principal	$100M

Calculated:

✔ Bond Payout
✔ Expected Loss (EL)

Used for:

ILS Pricing

Risk Spread Calculation

Capital Market Risk Transfer

🧪 Business Simulation – Portfolio Roll-Up

Simulated Renewal Season Scenario:

New Account Added:

ACC_FL_CONDO (Miami Portfolio)


Impact:

Metric	Before	After
100-Year PML	$85M	$92M
Marginal Impact	+$7M	

Business Insight:

➡ Highly correlated peak catastrophe risk
➡ Requires capital adjustment
➡ May need facultative reinsurance

🛠 Tech Stack

AWS S3

AWS Glue

PySpark

Python

Pandas

NumPy

SciPy

Matplotlib

VS Code

📈 Resume Highlights

Architected AWS Lakehouse for Insurance Risk Modeling

Built EDM using Glue + PySpark

Implemented Hazard–Vulnerability–Financial CAT Model

Calculated AAL & EP Curve for Portfolio Risk

Simulated CAT Bond Expected Loss

Performed Marginal Impact Analysis for Underwriting

📚 References

Moody’s RMS Workflow & CAT Modeling Framework
