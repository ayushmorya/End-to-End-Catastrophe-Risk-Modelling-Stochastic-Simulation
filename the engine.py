import pandas as pd
import numpy as np

# Load EDM parquet Output
edm = pd.read_parquet("edm path here")


# this is the stochastic hurricane event
catalog_data = {
    'event_id': [1,2,3,4,5,6,7,8,9,10],
    'description': [
        'Minor Storm', 'Moderate Storm', 'Severe Storm',
        'Cyclonic Event', 'Extreme Cyclone',
        'Rare Hurricane', 'Very Rare Hurricane',
        'Cat 4 Event', 'Cat 5 Event', 'Mega Cat Event'
    ],
    'annual_rate': [0.1, 0.05, 0.04, 0.02, 0.01,
                    0.005, 0.004, 0.002, 0.001, 0.0005]
}

catalog_df = pd.DataFrame(catalog_data)

# hazard tootprint simulation function
def simulate_hazard_footprint(locations, events):
    """
    This function answers:
    “If storm happens… how strong is the wind at each building?”
    """
    
    footprints = []

    for _, evt in events.iterrows(): #checking storms one by one
        event_id = evt['event_id']
        base_intensity = 50 + (1 / evt['annual_rate']) * 0.5
        
        n_locs = len(locations)
        
        #creating random wind speed here
        intensities = np.random.normal(
            loc=base_intensity,
            scale=15,
            size=n_locs
            #this creates wind speed for each building
        )
        
        intensities = np.clip(intensities, 0, 250) #wind cant be negative and more than 250 mph
        
        temp_df = pd.DataFrame({
            'event_id': event_id,
            'location_id': locations['location_id'],
            'hazard_intensity': intensities
        })
        
        footprints.append(temp_df)

    return pd.concat(footprints, ignore_index=True)


hazard_df = simulate_hazard_footprint(edm, catalog_df)

print(hazard_df.head())


#----------------------------------------------------------
# Module 2: The Vulnerability Engine (Damage Functions)
def get_vulnerability_mdr(row):
    """
    Calculates Mean Damage Ratio (MDR) based on Construction and Hazard Intensity.
    Includes Secondary Modifier logic for Year Built.
    """
    const_code = row['const_code']
    intensity = row['hazard_intensity'] # in Mph
    year_built = row['year_built']
    
    mdr = 0.0
    
    if const_code == 1: # Wood is weak
        if intensity > 60: #damage starts after 60mph
            mdr = min(1.0, (intensity - 60) / 100) # Reaches 100% at 160mph
    elif const_code == 6: # RCC is strong
        if intensity > 90: #damage starts after 90mph
            mdr = min(0.8, (intensity - 90) / 150) # Max 80% damage at 240mph
    else: # Masonry/Steel (Intermediate)
        if intensity > 75:
            mdr = min(0.9, (intensity - 75) / 120)
            
    # assume modern codes (post-2000) reduce damage by 20% because post 2000 building are way more stronger
    if year_built > 2000:
        mdr = mdr * 0.80 #20% less damage
        
    return mdr

# merge hazard with exposure to get attributes
full_exposure_view = pd.merge(hazard_df, edm, on='location_id')

# calculate MDR
full_exposure_view['mdr'] = full_exposure_view.apply(get_vulnerability_mdr, axis=1)



# Module 3: the financial engine (Loss Calculation)
def calculate_financial_loss(row):
    tiv = row['tiv']
    mdr = row['mdr']
    deductible_pct = row['deductible'] 
    limit = row['limit']
    coinsurance = row['coinsurance']
    
    #1. Ground Up Loss
    gu_loss = tiv * mdr
    
    #2. Apply Deductible
    # Deductible is % of TIV
    deductible_amount = tiv * deductible_pct
    loss_net_deductible = max(0, gu_loss - deductible_amount)
    
    # 3. limit
    # Insurance will not pay more than the policy limit
    loss_net_limit = min(loss_net_deductible, limit)
    
    # 4. Apply Coinsurance
    # Insurer pays 'coinsurance' share (usually 1.0 or 100%)
    gross_loss = loss_net_limit * coinsurance
    
    return pd.Series([gu_loss, gross_loss],index=['gu_loss', 'gross_loss'])

# Execute Financial Module
financial_results = full_exposure_view.apply(calculate_financial_loss, axis=1)

# Bind results back to the main dataframe
full_results = pd.concat([full_exposure_view, financial_results], axis=1)


#Probabilistic Metrics: AAL and EP Curves
#Average Annual Loss (AAL)

#1. Aggregate Loss by Event
# We sum up the losses for all locations for each unique Event ID
portfolio_elt = full_results.groupby('event_id').agg({
    'gross_loss': 'sum',
    'gu_loss': 'sum'
}).reset_index()

#2. Merge Annual Rates from Catalog
portfolio_elt = pd.merge(portfolio_elt, catalog_df[['event_id', 'annual_rate', 'description']], on='event_id')

#3. Calculate AAL Contribution per Event
portfolio_elt['aal_contribution'] = portfolio_elt['gross_loss'] * portfolio_elt['annual_rate']

#4. Calculate Portfolio AAL
portfolio_aal = portfolio_elt['aal_contribution'].sum()
print(f"Portfolio Gross AAL: ${portfolio_aal:,.2f}")


# 4.2 Exceedance Probability (EP) Curve
# OEP (Occurrence Exceedance Probability): Probability of at least one event exceeding loss $x$.
# AEP (Aggregate Exceedance Probability): Probability of the sum of losses in a year exceeding loss $x$.
# For this project, we implement the OEP calculation.

# Sort by Loss (Largest First)
ep_curve_df = portfolio_elt.sort_values(by='gross_loss', ascending=False).copy()

# Calculate Cumulative Rate (Frequency of losses >= x)
ep_curve_df['cumulative_rate'] = ep_curve_df['annual_rate'].cumsum()

# Calculate Return Period (RP = 1 / Probability)
ep_curve_df['return_period'] = 1 / ep_curve_df['cumulative_rate']

# Display the EP Table
print(ep_curve_df[['description', 'gross_loss', 'return_period']])

#----------------------------------------------------------
# 5. Advanced Risk Transfer: Catastrophe Bonds
# Python Simulation of Bond Performance
# We apply this logic to our stochastic portfolio_elt to calculate the Expected Loss (EL) of the bond. The EL is the critical metric investors use to price the bond (i.e., determine the coupon/spread).   
# def calculate_cat_bond_payout(row):
#     loss = row['gross_loss']
#     attachment = 100_000_000
#     exhaustion = 200_000_000
#     principal = 100_000_000
    
#     if loss < attachment:
#         return 0
#     elif loss >= exhaustion:
#         return principal
#     else:
#         return loss - attachment

# # Calculate Payout for each stochastic event
# portfolio_elt['bond_payout'] = portfolio_elt.apply(calculate_cat_bond_payout, axis=1)

# # Calculate Bond Expected Loss (EL)
# # EL = Sum(Payout * Rate) / Principal
# bond_expected_payout = (portfolio_elt['bond_payout'] * portfolio_elt['annual_rate']).sum()
# bond_el_percent = bond_expected_payout / 100000000

# print(f"Cat Bond Expected Loss (EL): {bond_el_percent:.2%}")



# ==============================
# EXPORT FILES FOR POWER BI

# portfolio_elt.to_csv(
#     r"C:\Users\ayush\OneDrive\Desktop\part 2\portfolio_elt.csv",
#     index=False
# )

# full_results.to_csv(
#     r"C:\Users\ayush\OneDrive\Desktop\part 2\location_event_losses.csv",
#     index=False
# )

# ep_curve_df.to_csv(
#     r"C:\Users\ayush\OneDrive\Desktop\part 2\ep_curve.csv",
#     index=False
# )

# print("Files Exported Successfully for Power BI Dashboard")


