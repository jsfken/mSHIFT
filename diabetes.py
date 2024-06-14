import numpy as np


def Hazard_ratio_CM_Diabetes(row, x_PM):
    # np.random.seed(seed)

    row['Processed meat intake'] = x_PM * row['Processed meat intake']

    if row['Processed meat intake'] > 0:
        if row['Processed meat intake'] < 15:
            HR_best_fit = 0.02 * row['Processed meat intake'] + 1
        else:
            HR_best_fit = 0.0022 * row['Processed meat intake'] + 1.27

        if row['Processed meat intake'] < 15:
            #HR_2sigma = 0.0271 * row['Processed meat intake'] + 1  ## Estimated from the upper curve
            HR_2sigma = 0.03 * row['Processed meat intake'] + 1  ## Estimated from the upper curve
        else:
            HR_2sigma = 0.00366 * row['Processed meat intake'] + 1.28
            # HR_lower = 0.003*diet.red_meat + 0.88

        sigma = (HR_2sigma - HR_best_fit) / 2
        Hazard_ratio = max(np.random.normal(HR_best_fit, sigma), 1)
    else:
        Hazard_ratio = 1

    return Hazard_ratio


def Hazard_ratio_RM_Diabetes(row, x_RM):
    # np.random.seed(seed)
    row['Red meat intake'] = x_RM * row['Red meat intake']

    if row['Red meat intake'] > 0:
        if row['Red meat intake'] < 40:
            # HR_best_fit = 0.0035 * row['Red meat intake'] + 1
            # HR_2sigma = 0.0078 * row['Red meat intake'] + 1  ## Estimated from the upper curve

            HR_best_fit = 0.004 * row['Red meat intake'] + 1
            HR_2sigma = 0.0078 * row['Red meat intake'] + 1  ## Estimated from the upper curve
        else:
            # Old
            # HR_best_fit = 0.0065 * row['Red meat intake'] + 1.04
            # HR_2sigma = 0.0065 * row['Red meat intake'] + 1.22

            # Updated estimates
            HR_best_fit = 0.004 * row['Red meat intake'] + 1.0
            HR_2sigma = 0.004 * row['Red meat intake'] + 1.19


        sigma = (HR_2sigma - HR_best_fit) / 2
        Hazard_ratio = max(np.random.normal(HR_best_fit, sigma), 1)
    else:
        Hazard_ratio = 1

    return Hazard_ratio


Diabetes_dict = {

    'CARDIA': {

        'Age Group': 0.295,
        'Black': -0.055,
        'Male': -0.958,
        'BMI': 0.083,
        'Parental History': 0.507,
        'Smoker': -0.13,
        'High SBP': 1.347,
        'High Cholesterol': 0.431,
        'Time': 10,
        'Constant': -5.171

    },

    'CARDIA-10': {
        'Age Group': 0.217,
        'Black': 0.342,
        'Male': 0.322,
        'BMI': 0.134,
        'Parental History': 0.857,
        'Smoker': -0.013,
        'High SBP': 0.09,
        'High Cholesterol': 0.328,
        'Time': 10,
        'Constant': -7.516

    },

    'ARIC': {

        'Age Group': 0.076,
        'Black': 0.280,
        'Male': 0.454,
        'BMI': 0.130,
        'Parental History': 0.626,
        'Smoker': 0.305,
        'High SBP': 0.386,
        'High Cholesterol': 0.002,
        'Time': 9,
        'Constant': -6.662

    },
    'CHS': {

        'Age Group': -0.164,
        'Black': 0.235,
        'Male': 0.414,
        'BMI': 0.135,
        'Parental History': 0.281,  # What variable to use for parental history? Currently using 'family history'
        'Smoker': 0.181,
        'High SBP': 0.635,
        'High Cholesterol': -0.054,
        'Time': 7,
        'Constant': -7.405

    }
}


def Sigmoid(x):
    z = 1 / (1 + np.exp(-x))
    return z


def Diabetes_risk_Alva(row, Diabetes_dict):
    ## Age ranges don't precisely match up -- Double check

    if row['Age'] < 35:
        dict = Diabetes_dict['CARDIA']
    elif row['Age'] < 55:
        dict = Diabetes_dict['CARDIA-10']
    elif row['Age'] < 75:
        dict = Diabetes_dict['ARIC']
    else:
        dict = Diabetes_dict['CHS']

    S = 0

    S += dict['Age Group']

    if row['Ethnicity'] == 4:
        S += dict['Black']
    if row['Sex'] == 1:
        S += dict['Male']

    S += row['BMI'] * dict['BMI']
    S += row['Parental Diabetes History'] * dict['Parental History']
    S += row['Current Smoker'] * dict['Smoker']

    if row['Systolic Blood Pressure'] > 140:
        S += dict['High SBP']
    if row['Total Cholesterol'] > 240:
        S += dict['High Cholesterol']

    S += dict['Constant']

    P = Sigmoid(S)
    Diabetes_rate = -np.log(1 - P) / dict['Time']
    Diabetes_risk = 1 - np.exp(-Diabetes_rate)

    #
    HR_CM = row['PM_HR_Diabetes']
    HR_RM = row['RM_HR_Diabetes']

    Diabetes_risk = Diabetes_risk * HR_CM * HR_RM

    # calibration aster setting RR_red_meat=1
    # if row['Age'] < 45:
    #     Diabetes_risk = Diabetes_risk / 2.01
    # elif row['Age'] < 65:
    #     Diabetes_risk = Diabetes_risk / 1.4
    # else:
    #     Diabetes_risk = Diabetes_risk / 1.36


    if row['Age'] < 45:
        Diabetes_risk = Diabetes_risk / 2.37
    elif row['Age'] < 65:
        Diabetes_risk = Diabetes_risk / 1.73
    else:
        Diabetes_risk = Diabetes_risk / 1.62

    return Diabetes_risk
