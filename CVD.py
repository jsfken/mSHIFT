import numpy as np



def Hazard_ratio_RM_CVD(row, x_RM):
    row['Red meat intake'] = x_RM * row['Red meat intake']

    serving_size = (row[
                        'Red meat intake'] * 0.035274) / 4  ## convert from grams to oz then normalise by the serving size in Zhong 2019

    if serving_size == 0:
        Hazard_ratio = 1
    elif serving_size < 0.1:
        Hazard_ratio = np.random.normal(1.0176, 0.006)
    elif serving_size < 0.2:
        Hazard_ratio = np.random.normal(1.0347, 0.015)
    elif serving_size < 0.3:
        Hazard_ratio = np.random.normal(1.0512, 0.022)
    elif serving_size < 0.4:
        Hazard_ratio = np.random.normal(1.0672, 0.025)
    elif serving_size < 0.5:
        Hazard_ratio = np.random.normal(1.0825, 0.035)
    elif serving_size < 0.6:
        Hazard_ratio = np.random.normal(1.0972, 0.035)
    elif serving_size < 0.7:
        Hazard_ratio = np.random.normal(1.1112, 0.045)
    elif serving_size < 0.8:
        Hazard_ratio = np.random.normal(1.1246, 0.045)
    elif serving_size < 0.9:
        Hazard_ratio = np.random.normal(1.1371, 0.05)
    elif serving_size < 1.0:
        Hazard_ratio = np.random.normal(1.1489, 0.05)
    elif serving_size < 1.1:
        Hazard_ratio = np.random.normal(1.1599, 0.05)
    elif serving_size < 1.2:
        Hazard_ratio = np.random.normal(1.1701, 0.06)
    elif serving_size < 1.3:
        Hazard_ratio = np.random.normal(1.1794, 0.065)
    elif serving_size < 1.4:
        Hazard_ratio = np.random.normal(1.1879, 0.075)
    elif serving_size < 1.5:
        Hazard_ratio = np.random.normal(1.1955, 0.075)
    elif serving_size < 1.6:
        Hazard_ratio = np.random.normal(1.2022, 0.075)
    elif serving_size < 1.7:
        Hazard_ratio = np.random.normal(1.208, 0.075)
    elif serving_size < 1.8:
        Hazard_ratio = np.random.normal(1.2128, 0.085)
    elif serving_size < 1.9:
        Hazard_ratio = np.random.normal(1.2167, 0.085)
    elif serving_size < 2.0:
        Hazard_ratio = np.random.normal(1.2196, 0.085)
    else:
        Hazard_ratio = np.random.normal(1.2216, 0.1)

    return Hazard_ratio


def Hazard_ratio_CM_CVD(row, x_PM):

    row['Processed meat intake'] = x_PM * row['Processed meat intake']

    serving_size = row['Processed meat intake'] / 30  # One serving size defined in Zhong et al. as 2 slices of bacon ~30g

    #
    if serving_size == 0:
        Hazard_ratio = 1
    elif serving_size < 0.1:
        Hazard_ratio = np.random.normal(1.0267, 0.005)
    elif serving_size < 0.2:
        Hazard_ratio = np.random.normal(1.052, 0.015)
    elif serving_size < 0.3:
        Hazard_ratio = np.random.normal(1.0759, 0.02)
    elif serving_size < 0.4:
        Hazard_ratio = np.random.normal(1.0981, 0.025)
    elif serving_size < 0.5:
        Hazard_ratio = np.random.normal(1.1186, 0.035)
    elif serving_size < 0.6:
        Hazard_ratio = np.random.normal(1.1372, 0.035)
    elif serving_size < 0.7:
        Hazard_ratio = np.random.normal(1.1539, 0.04)
    elif serving_size < 0.8:
        Hazard_ratio = np.random.normal(1.1685, 0.045)
    elif serving_size < 0.9:
        Hazard_ratio = np.random.normal(1.181, 0.045)
    elif serving_size < 1.0:
        Hazard_ratio = np.random.normal(1.1912, 0.05)
    elif serving_size < 1.1:
        Hazard_ratio = np.random.normal(1.1992, 0.05)
    elif serving_size < 1.2:
        Hazard_ratio = np.random.normal(1.2049, 0.05)
    elif serving_size < 1.3:
        Hazard_ratio = np.random.normal(1.2082, 0.055)
    elif serving_size < 1.4:
        Hazard_ratio = np.random.normal(1.2092, 0.055)
    elif serving_size < 1.5:
        Hazard_ratio = np.random.normal(1.2077, 0.055)
    elif serving_size < 1.6:
        Hazard_ratio = np.random.normal(1.2039, 0.056)
    elif serving_size < 1.7:
        Hazard_ratio = np.random.normal(1.1978, 0.056)
    elif serving_size < 1.8:
        Hazard_ratio = np.random.normal(1.1893, 0.06)
    elif serving_size < 1.9:
        Hazard_ratio = np.random.normal(1.1786, 0.07)
    elif serving_size < 2.0:
        Hazard_ratio = np.random.normal(1.1657, 0.075)
    else:
        Hazard_ratio = np.random.normal(1.1507, 0.075)

    #Hazard_ratio = max(np.random.normal(loc=0.0052, scale=0.0009) * row['Processed meat intake'] + 1, 1)

    return Hazard_ratio

# def Hazard_ratio_CM_CVD(row, x_PM):
# #
#     row['Processed meat intake'] = x_PM * row['Processed meat intake']
#
#
#
#     return Hazard_ratio




CVD_Framingham_coeff_2008_update = {
    1: {
        'Age': 3.06117,
        'TC': 1.12370,
        'HDL': -0.93263,
        'SBP_treated': 1.99881,
        'SBP_untreated': 1.93303,
        'Diabetes': 0.57367,
        'Smoker': 0.65451,
        'Baseline': 0.88936
    }
    ,
    2: {'Age': 2.32888,
        'TC': 1.20904,
        'HDL': -0.70833,
        'SBP_treated': 2.82263,
        'SBP_untreated': 2.76157,
        'Diabetes': 0.69154,
        'Smoker': 0.52873,
        'Baseline': 0.95012
        }
}


def updated_Framingham_CVD_risk(row, with_diabetes):

    age = row['Age']
    sex = row['Sex']
    tot_cholesterol = row['Total Cholesterol']
    HDL_cholesterol = row['HDL Cholesterol']
    taking_blood_pressure_medication = row['Taking BPM']
    systolic_blood_pressure = row['Systolic Blood Pressure']
    smoker = row['Current Smoker']

    if with_diabetes:
        diabetes = 1
    else:
        diabetes = row['Diabetes']

    CVD_dict = CVD_Framingham_coeff_2008_update[sex]

    S = 0
    S += np.log(age) * CVD_dict['Age']
    S += np.log(tot_cholesterol) * CVD_dict['TC']
    S += np.log(HDL_cholesterol) * CVD_dict['HDL']
    if taking_blood_pressure_medication == 1:
        S += np.log(systolic_blood_pressure) * CVD_dict['SBP_treated']
    else:
        S += np.log(systolic_blood_pressure) * CVD_dict['SBP_untreated']

    if diabetes:
        S += CVD_dict['Diabetes']

    if smoker == 1:
        S += CVD_dict['Smoker']

    CVD_risk_10yr = 0
    if sex == 2:
        CVD_risk_10yr = 1 - 0.95012 ** (np.exp(S - 26.1931))
    elif sex == 1:
        CVD_risk_10yr = 1 - 0.88936 ** (np.exp(S - 23.9802))

    CVD_rate = -np.log(1 - CVD_risk_10yr) / 10  ## Transform the 10 year risk from Yadlowsky to a one year risk
    CVD_risk = 1 - np.exp(-CVD_rate)

    HR_RM = row['RM_HR_CVD']
    HR_CM = row['PM_HR_CVD']
    CVD_risk = CVD_risk * HR_CM * HR_RM

    CVD_risk /= 1.2

    #CVD_risk /= 1.1

    #CVD_risk /= 1.15

    # assuming shi et al RR relation
    #CVD_risk /= 1.55

    #assuming 1 serving processed meat = 40g
    #CVD_risk /= 1.456



    return CVD_risk