import numpy as np
import pandas as pd
from diabetes import *
from colorectal_cancer import *
from CVD import *
from population import *
from incidence import expected_new_diabetes_cases, expected_new_CRC_cases, expected_new_CVD_cases


################# Diabetes #############################

def calibrate_diabetes_model(data, filter, num_runs, Diabetes_dict):
    df = data[filter].copy()
    diabetes_cases = []
    average_risks = []
    for seed in range(num_runs):
        np.random.seed(seed)
        df['PM_HR_Diabetes'] = df.apply(lambda row: Hazard_ratio_CM_Diabetes(row, x_PM=1), axis=1)
        df['RM_HR_Diabetes'] = df.apply(lambda row: Hazard_ratio_RM_Diabetes(row, x_RM=1), axis=1)
        df['Diabetes risk'] = df.apply(lambda row: Diabetes_risk_Alva(row, Diabetes_dict=Diabetes_dict), axis=1)
        df['New diabetes cases'] = df.apply(lambda row: expected_new_diabetes_cases(row), axis=1)

        avg_risk = (df['Diabetes risk']*df['Sample Weight']).sum()/df['Sample Weight'].sum()


        diabetes_cases.append(df['New diabetes cases'].sum())
        average_risks.append(avg_risk)

    print(f'average diabetes risk: {np.mean(average_risks)}')

    return diabetes_cases


def perform_diabetes_calibration(df, num_runs):
    #filter = (df['Age']<45)
    #filter = (df['Age']>44) & (df['Age']<65)
    #filter = (df['Age']>64)

    filter = (df['Sex'] == 2)
    cases = calibrate_diabetes_model(df, filter=filter, num_runs=num_runs, Diabetes_dict=Diabetes_dict)

    # plt.hist(cases, bins=100)
    # plt.show()
    print(np.mean(cases))
    print(np.std(cases))
    #
    # 1.71*np.mean(cases)/390000

    return

def calibrate_CVD_model(data, num_runs, seed):
    df =data.copy()
    CVD_cases = []
    #for seed in range(0, num_runs):
    np.random.seed(seed)

    df = run_sampling(df=df, x_PM=1, x_RM=1, seed=seed)
    print(df[['PM_HR_CVD', 'RM_HR_CVD']].head())
    df = calculate_risks(df=df, mortality_table=mortality_table, seed=seed)

    df['New CVD cases'] = df.apply(lambda row: expected_new_CVD_cases(row), axis=1)
    df = update_mortalities(df, year=1, pre_new_cases=False)
    CVD_mortalities = df['CVD mortalities year 1 post'].sum()

    print(df['New CVD cases'].sum() - df['CVD mortalities year 1 post'].sum())


    #df = apply_new_mortalities(df, year=1)
    #CVD_cases.append(df['New CVD cases'].sum())

    #print(np.mean(CVD_cases))
    #print(np.std(CVD_cases))

    return CVD_cases

def test_sim(data, years, seed, x_PM):
    df_sim = data.copy()
    df_sim = run_sampling(df_sim, x_PM=x_PM, x_RM=1, seed=seed)
    df_sim = calculate_risks(df_sim, mortality_table=mortality_table, seed=seed)






    for year in range(1, years + 1):
        print("\n")
        print(f"Year {year}")

        # print(f"Diabetes risk: {df_sim['Diabetes risk'].loc[93716.0]} ")
        print(f"CVD risk no diabetes: {df_sim['CVD risk no diabetes'].loc[93716.0]}")
        print(f"CVD risk with diabetes: {df_sim['CVD risk with diabetes'].loc[93716.0]}")
        # print(f"CRC risk: {df_sim['CRC risk no diabetes'].loc[93716.0]}")
        # print(f"Diabetes and CVD risk: {df_sim['Diabetes and CVD risk'].loc[93716.0]} ")
        # print(f"Diabetes and CRC risk: {df_sim['Diabetes and CRC risk'].loc[93716.0]} ")
        # print(f"CVD and CRC risk no diabetes: {df_sim['CVD and CRC risk no diabetes'].loc[93716.0]} ")
        # print(f"Diabetes and CVD and CRC risk: {df_sim['Diabetes and CVD and CRC risk'].loc[93716.0]} ")

        print(f"Mortality risk no disease: {df_sim['Healthy mortality risk'].loc[93716.0]} ")
        print(f"Diabetes mortality risk: {df_sim['diabetes mortality risk'].loc[93716.0]} ")
        print(f"CVD mortality risk: {df_sim['CVD mortality risk'].loc[93716.0]} ")
        print(f"diabetes and CVD mortality risk: {df_sim['diabetes and CVD mortality risk'].loc[93716.0]} ")
        print(f"CRC mortality risk: {df_sim['CRC mortality risk'].loc[93716.0]} ")


        df_sim = update_mortalities(df_sim, year=year, pre_new_cases=True)
        df_sim = update_cases(df_sim, year=year)
        df_sim = update_mortalities(df_sim, year=year, pre_new_cases=False)
        df_sim = apply_new_mortalities(df_sim, year=year)
        df_sim = update_df(df_sim)
        df_sim = calculate_risks(df_sim, mortality_table=mortality_table, seed=seed)

        print("\n")
        print(f"New diabetes cases: {df_sim[f'New diabetes cases year {year}'].loc[93716.0]}")
        print(f"New CVD cases: {df_sim[f'New CVD cases year {year}'].loc[93716.0]}")
        print(f"New CRC cases: {df_sim[f'New CRC cases year {year}'].loc[93716.0]}")
        print(f"New diabetes and CVD cases: {df_sim[f'New diabetes and CVD cases year {year}'].loc[93716.0]}")
        print(f"New diabetes and CRC cases: {df_sim[f'New diabetes and CRC cases year {year}'].loc[93716.0]}")
        print(f"New CVD and CRC cases: {df_sim[f'New CVD and CRC cases year {year}'].loc[93716.0]}")
        print(f"New diabetes and CVD and CRC cases: {df_sim[f'New diabetes and CVD and CRC cases year {year}'].loc[93716.0]}")

        print(f"Total mortalities: {df_sim[f'Total mortalities year {year} post'].loc[93716.0]} ")
        print(f"Mortalities no disease: {df_sim[f'Healthy mortalities year {year} post'].loc[93716.0]} ")
        print(f"Diabetes mortalities: {df_sim[f'diabetes mortalities year {year} post'].loc[93716.0]} ")
        print(f"CVD mortalities: {df_sim[f'CVD mortalities year {year} post'].loc[93716.0]} ")
        print(f"CRC mortalities: {df_sim[f'CRC mortalities year {year} post'].loc[93716.0]} ")
        print(f"diabetes and CVD mortalities: {df_sim[f'diabetes and CVD mortalities year {year} post'].loc[93716.0]} ")
        print(f"diabetes and CRC mortalities: {df_sim[f'diabetes and CRC mortalities year {year} post'].loc[93716.0]} ")
        print(f"CVD and CRC mortalities: {df_sim[f'CVD and CRC mortalities year {year} post'].loc[93716.0]} ")
        print(f"diabetes and CVD and CRC mortalities: {df_sim[f'diabetes and CVD and CRC mortalities year {year} post'].loc[93716.0]} ")


        #print(f"Mortalities no disease: {df_sim[f'Healthy mortalities year {year}'].loc[93716.0]}")

    #print(df_sim['New CVD cases year 1'].sum())
    #print(df_sim['CVD mortalities year 1 post'].sum())
    cases = df_sim['New CVD cases year 1'].sum() #-df_sim['CVD mortalities year 1 post'].sum()



    return cases


####################### Colorectal cancer ###################


def calibrate_CRC_model(df, filter, num_runs):
    df = df[filter].copy()
    CRC_cases = []
    average_risks = []
    for seed in range(num_runs):
        np.random.seed(seed)
        df['CRC family history'] = df.apply(lambda row: CRC_family_history(row), axis=1)

        df['PM_HR_CRC'] = df.apply(lambda row: Relative_risk_Zhao_CM(row, x_PM=1), axis=1)
        df['RM_HR_CRC'] = df.apply(lambda row: Relative_risk_Zhao_RM(row, x_RM=1), axis=1)

        df['CRC risk no diabetes'] = df.apply(lambda row: CRC_risk(row, with_diabetes=False), axis=1)
        df['CRC risk with diabetes'] = df.apply(lambda row: CRC_risk(row, with_diabetes=True), axis=1)

        avg_risk = (df['CRC risk no diabetes'] * df['Sample Weight']).sum() / df['Sample Weight'].sum()

        df['New CRC cases'] = df.apply(lambda row: expected_new_CRC_cases(row), axis=1)

        average_risks.append(avg_risk)

        CRC_cases.append(df['New CRC cases'].sum())

    print(f'average CRC risk: {np.mean(average_risks)}')

    return CRC_cases


def perform_CRC_calibration(df):
    males = df[df['Sex'] == 1].copy()
    #females = df[df['Sex'] == 2].copy()

    #filter = (df['Age'] < 50)
    #filter = (df['Age']>49) & (df['Age']<65)
    #filter = (df['Age']>64) & (df['Age']<80)
    #filter = (df['Age'] > 79)

    filter = (df['Age'] < 200)

    cases = calibrate_CRC_model(df=males, filter=filter, num_runs=20)
    print(f'Predicted new cases: {np.mean(cases)} +/- {np.std(cases)}')
    #new_CP = 1.67 * np.mean(cases) / 6700
    #print(f'New calibration parameter based on predicted number of new cases: {new_CP}')

    return


if __name__ == '__main__':
    df = pd.read_pickle('Data/mSHIFT_data_day2.plk')

    #print(df.columns)
    ind = df.loc[[93716.0, 93682.0	], :]
    #print(df['Sample Weight'].sum())
    #df = pd.read_pickle('Data/mSHIFT_data.plk')
    cases_baseline = test_sim(data=ind, years=2, seed=1, x_PM=1)
    #cases_int = test_sim(data=df, years=1, seed=36, x_PM=0.7)
    #print(cases_baseline)
    #print(cases_baseline-cases_int)
    #calibrate_CVD_model(data=df, num_runs=1, seed=1)



    #perform_CRC_calibration(df)
    #perform_diabetes_calibration(df, num_runs=20)
