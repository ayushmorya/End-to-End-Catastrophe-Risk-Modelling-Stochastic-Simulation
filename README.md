# End-to-End-Catastrophe-Risk-Modelling-Live-Simulation
This project demonstrates how insurers estimate financial losses from natural disasters such as hurricanes and cyclones using stochastic modelling techniques.


📌 Project Objective

Insurance companies face one critical question:

“If a major disaster occurs tomorrow, how much financial loss will we suffer?”

Traditional historical data cannot predict future catastrophic losses accurately.

This project solves that problem by:

Simulating thousands of possible future disaster scenarios

Estimating physical damage to insured assets

Converting damage into financial loss

Calculating portfolio risk metrics such as:

Average Annual Loss (AAL)

Exceedance Probability (EP) Curve

Probable Maximum Loss (PML)

🧠 Catastrophe Modelling Workflow

This project follows the industry-standard Four-Box CAT Model Architecture:

1️⃣ Exposure Module

Identifies insured assets such as:

Building Location

Construction Type

Year Built

Total Insured Value (TIV)

Policy Terms (Deductible, Limit, Coinsurance)

2️⃣ Hazard Module

Simulates stochastic hurricane events and generates:

Wind speed intensity for each building

Spatial variability using probability distributions

3️⃣ Vulnerability Module

Calculates physical damage using:

Mean Damage Ratio (MDR)

Which represents:

0 → No Damage
1 → Total Destruction

Damage depends on:

Construction Type

Hazard Intensity

Year Built (modern building code credit)

4️⃣ Financial Module

Converts damage into monetary loss using insurance policy terms:

Ground Up Loss (GU)

Deductible Application

Policy Limit

Coinsurance

Final insurer payout is calculated as:

Gross Loss
📊 Risk Metrics Generated
🔹 Average Annual Loss (AAL)

Expected average loss per year from all simulated disasters.

🔹 Exceedance Probability (EP) Curve

Shows probability that loss will exceed a given threshold.

Example:

There is a 1% probability (1-in-100 year event) that losses will exceed $850M.

🔹 Probable Maximum Loss (PML)

Worst-case financial loss at selected return periods such as:

10-Year PML

50-Year PML

100-Year PML

500-Year PML

⚙️ Technologies Used

Python

NumPy

Pandas

PySpark (ETL)

AWS Glue (Exposure Data Engineering)

🚀 How to Run the Project
Step 1: Install Dependencies
pip install pandas numpy
Step 2: Run Modelling Engine
python modelling_engine.py
📁 Project Structure
Catastrophe-Risk-Model
│
├── edm_local_copy.parquet
├── modelling_engine.py
└── README.md
🧑‍💼 Resume Description

Built an end-to-end stochastic catastrophe risk model replicating Moody’s RMS workflow using Python and AWS Glue to estimate portfolio-level financial losses under simulated disaster scenarios.

📈 Future Enhancements

Multi-Peril Modelling

Reinsurance Layer Analysis

Cat Bond Simulation

Climate Scenario Modelling

📜 License

This project is for educational and portfolio purposes.
