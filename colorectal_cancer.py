import numpy as np


def CRC_family_history(row):
    CRC_family_history = 0
    family_history_prob = 0.034
    sample = np.random.uniform()
    if sample < family_history_prob:
        CRC_family_history = 1

    return CRC_family_history


def Relative_risk_Zhao_RM(row, x_RM):
    row['Red meat intake'] = x_RM * row['Red meat intake']

    if row['Red meat intake'] > 0:
        gradient_red_meat = np.random.normal(0.0016, 0.0005)
        RR_red_meat = max(row['Red meat intake'] * gradient_red_meat + 1, 1)
    else:
        RR_red_meat = 1

    return RR_red_meat


def Relative_risk_Zhao_CM(row, x_PM):
    row['Processed meat intake'] = x_PM * row['Processed meat intake']

    if row['Processed meat intake'] > 0:
        gradient_processed_meat = np.random.normal(0.0044, 0.002)
        RR_processed_meat = max(row['Processed meat intake'] * gradient_processed_meat + 1, 1)
    else:
        RR_processed_meat = 1

    return RR_processed_meat


def CRC_risk(row, with_diabetes):

    age = row['Age']
    sex = row['Sex']
    ethnicity = row['Ethnicity']
    pack_years = row['Smoking pack years']
    alcohol_drinks = row['Daily Drinks']
    BMI = row['BMI']
    years_education = row['Years of Education']
    previously_taken_aspirin = row['Taking Aspirin']
    taking_aspirin = row['Taking Aspirin']
    CRC_family_history = row['CRC family history']
    taking_multivitamins = row['Taking Multivitamins']
    hours_moderate_PA = row['Hours moderate physical activity']
    taking_estrogen = row['Taking Estrogen']
    previously_taken_estrogen = row['Taking Estrogen']

    if with_diabetes:
        diabetes = 1
    else:
        diabetes = row['Diabetes']

    if sex == 1:

        intercept = -6.6419738
        risk_age = 0.091669179 * age - 3.7411814e-05 * max(age - 47, 0) ** 3 + 7.794128e-05 * max(age - 60,
                                                                                                  0) ** 3 - 4.0529466e-05 * max(
            age - 72, 0) ** 3

        if ethnicity == 1 or ethnicity == 2:
            risk_ethnicity = -0.13659953
        elif ethnicity == 3:
            risk_ethnicity = -0.16728044
        elif ethnicity == 6:
            risk_ethnicity = 0.25353936
        else:
            risk_ethnicity = 0

        risk_pack_years = 0.00022581331 * pack_years + 1.1341047e-05 * max(pack_years, 0) ** 3 - 1.3522018e-05 * max(
            pack_years - 6.375, 0) ** 3 + 2.1809706e-06 * max(pack_years - 39.525, 0) ** 3

        risk_alcohol = 0.28379769 * alcohol_drinks - 0.21424251 * max(alcohol_drinks, 0) ** 3 + 0.22570057 * max(
            alcohol_drinks - 0.14457189, 0) ** 3 - 0.011458065 * max(alcohol_drinks - 2.8477722, 0) ** 3

        risk_BMI = 0.018020786 * BMI + 9.4715899e-05 * max(BMI - 22.047175, 0) ** 3 - 0.00015791645 * max(
            BMI - 25.941735, 0) ** 3 + 6.3200548e-05 * max(BMI - 31.778341, 0) ** 3

        risk_years_education = 0.072052428 * years_education - 0.00060634342 * max(years_education - 7,
                                                                                   0) ** 3 + 0.0016674444 * max(
            years_education - 14, 0) ** 3 - 0.001061101 * max(years_education - 18, 0) ** 3

        risk_aspirin = -0.032284161 * previously_taken_aspirin - 0.20960315 * taking_aspirin

        risk_family_history = 0.24250922 * CRC_family_history

        risk_multivitamins = -0.19175375 * taking_multivitamins

        # risk_Total_meat = 0.073141733   *  TotalMeat - 0.0043503766  * max(TotalMeat - 0.59081962, 0)**3 + 0.0065250851  * max(TotalMeat - 2.0822052, 0)**3 - 0.0021747085  * max(TotalMeat - 5.0656345, 0)**3

        if diabetes:
            risk_diabetes = 0.11020556
        else:
            risk_diabetes = 0

        risk_physical_activity = -0.090669913 * hours_moderate_PA + 0.0093816671 * max(hours_moderate_PA - 0.10714286,
                                                                                       0) ** 3 - 0.011850527 * max(
            hours_moderate_PA - 0.82142857, 0) ** 3 + 0.0024688598 * max(hours_moderate_PA - 3.5357143, 0) ** 3

        Sum = intercept + risk_age + risk_ethnicity + risk_pack_years + risk_alcohol + risk_BMI + risk_years_education + risk_aspirin + risk_family_history + risk_multivitamins + risk_diabetes + risk_physical_activity
        P = 1 - 0.9846654 ** np.exp(Sum)


    elif sex == 2:

        intercept = -5.9026635
        risk_age = 0.090012542 * age - 4.4217156e-05 * max(age - 47, 0) ** 3 + 9.2119076e-05 * max(age - 60,0) ** 3 - 4.7901919e-05 * max(age - 72, 0) ** 3

        if ethnicity == 1 or ethnicity == 2:
            risk_ethnicity = -0.39669678
        elif ethnicity == 3:
            risk_ethnicity = -0.34056094
        elif ethnicity == 6:
            risk_ethnicity = 0.014010715
        else:
            risk_ethnicity = 0

        risk_pack_years = 0.062703176 * pack_years - 0.002446026 * max(pack_years, 0) ** 3 + 0.003038396 * max(
            pack_years - 1.25, 0) ** 3 - 0.00059134632 * max(pack_years - 6.375, 0) ** 3 - 1.023614e-06 * max(
            pack_years - 27.5125, 0) ** 3
        risk_alcohol = -0.08856241 * alcohol_drinks + 0.62375456 * max(alcohol_drinks, 0) ** 3 - 0.7191129 * max(
            alcohol_drinks - 0.10740682, 0) ** 3 + 0.095358349 * max(alcohol_drinks - 0.8099724, 0) ** 3
        risk_BMI = 0.0075233925 * BMI + 6.7918662e-05 * max(BMI - 20.371336, 0) ** 3 - 0.00011039091 * max(
            BMI - 25.508027, 0) ** 3 + 4.2472244e-05 * max(BMI - 33.722266, 0) ** 3

        risk_years_education = 0.07443905 * years_education - 0.00062546554 * max(years_education - 7,
                                                                                  0) ** 3 + 0.0017200302 * max(
            years_education - 14, 0) ** 3 - 0.0010945647 * max(years_education - 18, 0) ** 3
        risk_estrogen = -0.24500762 * taking_estrogen - 0.044320489 * previously_taken_estrogen

        risk_pain_med = -0.046383323 * previously_taken_aspirin - 0.236997 * taking_aspirin
        risk_family_history = 0.31589053 * CRC_family_history
        risk_multivitamins = - 0.1665365 * taking_multivitamins

        if diabetes:
            risk_diabetes = 0.23328937
        else:
            risk_diabetes = 0

        Sum = intercept + risk_age + risk_ethnicity + risk_pack_years + risk_alcohol + risk_BMI + risk_years_education + risk_pain_med + risk_family_history + risk_multivitamins + risk_diabetes
        P = 1 - 0.9901043 ** np.exp(Sum)

    CRC_rate = -np.log(1 - P) / 10
    CRC_risk = 1 - np.exp(-CRC_rate)

    RR_red_meat = row['RM_HR_CRC']
    RR_processed_meat = row['PM_HR_CRC']

    CRC_risk = CRC_risk * RR_processed_meat * RR_red_meat

    if sex == 1:
        if age < 50:
            CRC_risk = CRC_risk / 1.56
        elif age < 65:
            CRC_risk = CRC_risk / 1.5
        elif age < 80:
            CRC_risk = CRC_risk / 1.79
        else:
            CRC_risk = CRC_risk / 1.27
    else:
        if age < 50:
            CRC_risk = CRC_risk / 1.67
        elif age < 65:
            CRC_risk = CRC_risk / 1.78
        elif age < 80:
            CRC_risk = CRC_risk / 1.92
        else:
            CRC_risk = CRC_risk / 0.93


    # ## calibration assuming no contribution from unprocessed red meat
    # if sex == 1:
    #     if age < 50:
    #         CRC_risk = CRC_risk / 1.43
    #     elif age < 65:
    #         CRC_risk = CRC_risk / 1.36
    #     elif age < 80:
    #         CRC_risk = CRC_risk / 1.67
    #     else:
    #         CRC_risk = CRC_risk / 1.2
    # else:
    #     if age < 50:
    #         CRC_risk = CRC_risk / 1.6
    #     elif age < 65:
    #         CRC_risk = CRC_risk / 1.7
    #     elif age < 80:
    #         CRC_risk = CRC_risk / 1.85
    #     else:
    #         CRC_risk = CRC_risk / 0.88

    return CRC_risk