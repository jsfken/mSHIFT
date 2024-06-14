import numpy as np




mortality_table = { 1: {18 :0.000811 , 19: 0.000945,
                        20: 0.001082, 21: 0.001214, 22: 0.001327, 23: 0.001413, 24: 0.001476, 25: 0.001531, 26: 0.001584, 27: 0.001633, 28: 0.001681 , 29: 0.001739,
                        30: 0.001779, 31: 0.001829, 32: 0.001888, 33: 0.001957, 34: 0.002032, 35: 0.002119, 36: 0.002209, 37: 0.002286, 38: 0.002346, 39: 0.002401,
                        40: 0.002468, 41: 0.002565, 42: 0.002700, 43: 0.002876, 44: 0.003084, 45: 0.003318, 46: 0.003572, 47: 0.003850, 48: 0.004161, 49: 0.004515,
                        50: 0.004895, 51: 0.005362, 52: 0.005835, 53: 0.006438, 54: 0.007098, 55: 0.007765, 56: 0.008432, 57: 0.009126, 58: 0.009870, 59: 0.010670,
                        60: 0.011534, 61: 0.012431, 62: 0.013332, 63: 0.014219, 64: 0.015117, 65: 0.016078, 66: 0.017216, 67: 0.018401, 68: 0.019666, 69: 0.021099,
                        70: 0.022544, 71: 0.024099, 72: 0.026447, 73: 0.028617, 74: 0.031390, 75: 0.034322 , 76: 0.037970, 77: 0.041944, 78: 0.045881, 79: 0.050573,
                        80: 0.055675, 81: 0.061704, 82: 0.068389, 83: 0.075732, 84: 0.085241, 85: 0.094489, 86: 0.104787, 87: 0.117465, 88: 0.131319, 89: 0.146372,
                        90: 0.162625, 91: 0.180060, 92: 0.198626, 93: 0.218248, 94: 0.238820, 95: 0.260206, 96: 0.282243, 97: 0.304747, 98: 0.327517, 99: 0.350342
                        },
                    2: {18: 0.000329, 19: 0.000365,
                        20: 0.000402, 21: 0.000441, 22: 0.000481, 23: 0.000521, 24: 0.000560, 25: 0.000598, 26: 0.000635, 27: 0.000675, 28: 0.000718 , 29: 0.000765,
                        30: 0.000818, 31: 0.000872, 32: 0.000928, 33: 0.000983, 34: 0.001037, 35: 0.001097, 36: 0.001160, 37: 0.001274, 38: 0.001274, 39: 0.001330,
                        40: 0.001396, 41: 0.001480, 42: 0.001584, 43: 0.001709, 44: 0.001849, 45: 0.002002, 46: 0.002167, 47: 0.002348, 48: 0.002551, 49: 0.002781,
                        50: 0.003028, 51: 0.003299, 52: 0.003615, 53: 0.003974, 54: 0.004357, 55: 0.004746, 56: 0.005135, 57: 0.005530, 58: 0.005940, 59: 0.006376,
                        60: 0.006849, 61: 0.007354, 62: 0.007879, 63: 0.008425, 64: 0.009008, 65: 0.009638, 66: 0.010386, 67: 0.011235, 68: 0.012237, 69: 0.013393,
                        70: 0.014731, 71: 0.016080, 72: 0.017952, 73: 0.019637, 74: 0.021744, 75: 0.023929, 76: 0.026629, 77: 0.029547, 78: 0.032857, 79: 0.036519,
                        80: 0.040589, 81: 0.045639, 82: 0.051261, 83: 0.057423, 84: 0.065035, 85: 0.072862, 86: 0.080121, 87: 0.090650, 88: 0.102322, 89: 0.115196,
                        90: 0.129319, 91: 0.144719, 92: 0.161402, 93: 0.179347, 94: 0.198504, 95: 0.218788, 96: 0.240082, 97: 0.262235, 98: 0.285066, 99: 0.308369
                        }
                    }



def mortality_prob(row, mortality_table, with_diabetes, with_CVD):

    age =row['Age']
    sex =row['Sex']

    if age < 100:
        mortality_prob = mortality_table[sex][age]
    else:
        mortality_prob =0.99

    if with_CVD:
        RR_CVD = np.random.normal(2.0, 0.05)
        mortality_prob = mortality_prob *RR_CVD


    if with_diabetes:
        if age < 55:
            RR_Diabetes = np.random.normal(2.35, 0.085)
        elif age < 65:
            RR_Diabetes = np.random.normal(1.79, 0.03)
        elif age < 75:
            RR_Diabetes = np.random.normal(1.46, 0.015)
        else:
            RR_Diabetes = np.random.normal(1.19, 0.005)

        mortality_prob = mortality_prob *RR_Diabetes

    return mortality_prob

def CRC_mortality_prob(row):

    age =row['Age']
    sex =row['Sex']

    if sex == 1:
        if age < 50:
            mortality_probability = 0.0236
        elif age > 49 and age < 65:
            mortality_probability = 0.247
        elif age > 64 and age < 80:
            mortality_probability = 0.0226
        else:
            mortality_probability = 0.0796

    elif sex == 2:
        if age < 50:
            mortality_probability = 0.0426
        elif age > 49 and age < 65:
            mortality_probability = 0.0118
        elif age > 64 and age < 80:
            mortality_probability = 0.0347
        else:
            mortality_probability = 0.0308

    return mortality_probability


def expected_healthy_mortalities(row):
    expected_healthy_mortalities = 0

    if row['Diabetes'] == 1 or row['CVD'] == 1 or row['CRC'] == 1:
        pass
    else:
        expected_healthy_mortalities = row['healthy'] * row['Healthy mortality risk']

    return expected_healthy_mortalities


def expected_diabetes_mortalities(row):
    # Post-disease calculates additional mortalities among those that aquired the disease in that year
    ## Those that die that have diabetes, could have additional diseases ##

    exp_diabetes_mortalities = 0

    if row['CRC'] == 1 and row['Diabetes'] == 1:
        exp_diabetes_mortalities += row['Sample Weight'] * row['CRC mortality risk']
    elif row['CRC'] == 1 and row['Diabetes'] != 1:
        exp_diabetes_mortalities += row['New diabetes and CRC cases'] * row['CRC mortality risk']

    elif row['Diabetes'] == 1 and row['CVD'] != 1:
        # Just have diabetes
        SW_diabetes_only = row['Sample Weight'] - row['New CRC cases'] - row['New CVD cases'] + row[
            'New CVD and CRC cases']
        exp_diabetes_mortalities += SW_diabetes_only * row['diabetes mortality risk']
        # New CVD cases without CRC
        exp_diabetes_mortalities += (row['New CVD cases'] - row['New CVD and CRC cases']) * row[
            'diabetes and CVD mortality risk']
        # New CRC cases
        exp_diabetes_mortalities += row['New CRC cases'] * row['CRC mortality risk']

    elif row['CVD'] == 1 and row['Diabetes'] != 1:
        exp_diabetes_mortalities += (row['New diabetes cases'] - row['New diabetes and CRC cases']) * row[
            'diabetes and CVD mortality risk']
        exp_diabetes_mortalities += row['New diabetes and CRC cases'] * row['CRC mortality risk']

    elif row['Diabetes'] == 1 and row['CVD'] == 1:
        exp_diabetes_mortalities += (row['Sample Weight'] - row['New CRC cases']) * row[
            'diabetes and CVD mortality risk']
        exp_diabetes_mortalities += row['New CRC cases'] * row['CRC mortality risk']

    elif row['Diabetes'] != 1 and row['CVD'] != 1:

        SW_diabetes_only = row['New diabetes cases'] - row['New diabetes and CRC cases'] - row[
            'New diabetes and CVD cases'] + row['New diabetes and CVD and CRC cases']
        exp_diabetes_mortalities += SW_diabetes_only * row['diabetes mortality risk']
        exp_diabetes_mortalities += (row['New diabetes and CVD cases'] - row['New diabetes and CVD and CRC cases']) * row['diabetes and CVD mortality risk']
        exp_diabetes_mortalities += row['New diabetes and CRC cases'] * row['CRC mortality risk']

    return exp_diabetes_mortalities


def expected_CVD_mortalities(row):
    exp_mortalities = 0

    if row['CRC'] == 1 and row['CVD'] == 1:
        exp_mortalities += row['Sample Weight'] * row['CRC mortality risk']
    elif row['CRC'] == 1 and row['CVD'] != 1:
        exp_mortalities += row['New CVD and CRC cases'] * row['CRC mortality risk']

    elif row['CVD'] == 1 and row['Diabetes'] != 1:
        # Just have CVD
        SW_CVD_only = row['Sample Weight'] - row['New CRC cases'] - row['New diabetes cases'] + row[
            'New diabetes and CRC cases']
        exp_mortalities += SW_CVD_only * row['CVD mortality risk']
        # New diabetes cases without CRC
        exp_mortalities += (row['New diabetes cases'] - row['New diabetes and CRC cases']) * row[
            'diabetes and CVD mortality risk']
        # New CRC cases
        exp_mortalities += row['New CRC cases'] * row['CRC mortality risk']

    elif row['Diabetes'] == 1 and row['CVD'] != 1:
        # New CVD cases
        exp_mortalities += (row['New CVD cases'] - row['New CVD and CRC cases']) * row[
            'diabetes and CVD mortality risk']
        # New CRC cases
        exp_mortalities += row['New CVD and CRC cases'] * row['CRC mortality risk']


    elif row['Diabetes'] == 1 and row['CVD'] == 1:
        exp_mortalities += (row['Sample Weight'] - row['New CRC cases']) * row['diabetes and CVD mortality risk']
        exp_mortalities += row['New CRC cases'] * row['CRC mortality risk']

    elif row['Diabetes'] != 1 and row['CVD'] != 1 and row['CRC'] != 1:
        SW_CVD_only = row['New CVD cases'] - row['New CVD and CRC cases'] - row['New diabetes and CVD cases'] + row[
            'New diabetes and CVD and CRC cases']
        exp_mortalities += SW_CVD_only * row['CVD mortality risk']
        exp_mortalities += (row['New diabetes and CVD cases'] - row['New diabetes and CVD and CRC cases']) * row[
            'diabetes and CVD mortality risk']
        exp_mortalities += row['New CVD and CRC cases'] * row['CRC mortality risk']

    return exp_mortalities


def expected_CRC_mortalities(row):
    exp_mortalities = 0

    if row['CRC'] == 1:
        exp_mortalities += row['Sample Weight'] * row['CRC mortality risk']
    else:
        exp_mortalities += row['New CRC cases'] * row['CRC mortality risk']

    return exp_mortalities


def expected_diabetes_CVD_mortalities(row):
    exp_mortalities = 0

    if row['CRC'] == 1 and row['Diabetes'] == 1 and row['CVD'] == 1:
        exp_mortalities += row['Sample Weight'] * row['CRC mortality risk']
    elif row['CRC'] == 1:
        exp_mortalities += row['New diabetes and CVD cases'] * row['CRC mortality risk']
    elif row['Diabetes'] == 1 and row['CVD'] == 1:
        exp_mortalities += (row['Sample Weight'] - row['New CRC cases']) * row[
            'diabetes and CVD mortality risk']
        exp_mortalities += row['New CRC cases'] * row['CRC mortality risk']
    else:
        exp_mortalities += (row['New diabetes and CVD cases'] - row['New diabetes and CVD and CRC cases']) * row[
            'diabetes and CVD mortality risk']
        exp_mortalities += row['New diabetes and CVD and CRC cases'] * row['CRC mortality risk']

    return exp_mortalities


def expected_diabetes_CRC_mortalities(row):
    exp_mortalities = 0

    if row['CRC'] == 1 and row['Diabetes'] == 1:
        exp_mortalities += row['Sample Weight'] * row['CRC mortality risk']
    else:
        exp_mortalities += row['New diabetes and CRC cases'] * row['CRC mortality risk']

    return exp_mortalities


def expected_CVD_CRC_mortalities(row):
    exp_mortalities = 0

    if row['CRC'] == 1 and row['CVD'] == 1:
        exp_mortalities += row['Sample Weight'] * row['CRC mortality risk']
    else:
        exp_mortalities += row['New CVD and CRC cases'] * row['CRC mortality risk']

    return exp_mortalities


def expected_diabetes_CVD_CRC_mortalities(row):
    exp_mortalities = 0

    if row['Diabetes'] == 1 and row['CRC'] == 1 and row['CVD'] == 1:
        exp_mortalities += row['Sample Weight'] * row['CRC mortality risk']
    else:
        exp_mortalities += row['New diabetes and CVD and CRC cases'] * row['CRC mortality risk']

    return exp_mortalities