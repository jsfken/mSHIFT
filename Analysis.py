import pandas as pd
import numpy as np
from Plotting import demographic_bins



data_dir = 'Output/'


def cases_prevented_year(NCD, reduction, mortalities, year, data_dir):
    baseline_path = data_dir + '0.0_reduction/'
    int_path = data_dir + f'{reduction}_reduction/'

    cases_prevented_array = []

    for seed in range(1, 21):
        baseline_data = pd.read_pickle(baseline_path + f'df_seed_{seed}.plk')
        int_data = pd.read_pickle(int_path + f'df_seed_{seed}.plk')

        if mortalities:
            baseline_cases = baseline_data[f'{NCD} mortalities year {year} post'].sum()
        else:
            baseline_cases = baseline_data[f'New {NCD} cases year {year}'].sum()
            #baseline_cases = baseline_data[f'New {NCD} cases'].sum()

        if mortalities:
            int_cases = int_data[f'{NCD} mortalities year {year} post'].sum()
        else:
            int_cases = int_data[f'New {NCD} cases year {year}'].sum()
            #int_cases = int_data[f'New {NCD} cases'].sum()

        cases_prevented = baseline_cases - int_cases
        cases_prevented_array.append(cases_prevented)

    mean = np.mean(cases_prevented_array)
    lower = np.percentile(cases_prevented_array, 2.5)
    upper = np.percentile(cases_prevented_array, 97.5)
    # error = 1.96 * np.std(cases_prevented_array)
    # lower = mean - error
    # upper = mean + error

    return mean, lower, upper


def cumulative_cases_prevented_with_filter(NCD, reduction, red_meat, processed_meat, mortalities, years, with_filter, data_dir):

    baseline_path = data_dir + '0.0_reduction/'

    if red_meat and processed_meat:
        int_path = data_dir + f'{reduction}_reduction/'
    elif red_meat and not processed_meat:
        int_path = data_dir + f'{reduction}_reduction_RM_alone/'
    elif processed_meat and not red_meat:
        int_path = data_dir + f'{reduction}_reduction_PM_alone/'
    else:
        raise ValueError('Must specify a reduction in either red or processed meat')


    cases_prevented_total = []

    for seed in range(1, 51):
        baseline_data = pd.read_pickle(baseline_path + f'df_seed_{seed}.plk')

        if red_meat and processed_meat:
            int_data = pd.read_pickle(int_path + f'df_seed_{seed}.plk')
        elif red_meat and not processed_meat:
            int_data = pd.read_pickle(int_path + f'df_seed_{seed}_RM.plk')
        elif processed_meat and not red_meat:
            int_data = pd.read_pickle(int_path + f'df_seed_{seed}_PM.plk')
        else:
            raise ValueError('Must specify a reduction in either red or processed meat')


        ## Set the age to be that of the population.py at the start of the simulation
        baseline_data['Age']-= 10
        int_data['Age'] -= 10

        if with_filter:
            # baseline_data = baseline_data[baseline_data['Annual Household Income'] <= 6]
            # int_data = int_data[int_data['Annual Household Income'] <= 6]

            # baseline_data = baseline_data[baseline_data['Annual Household Income'] == 12]
            # int_data = int_data[int_data['Annual Household Income'] ==12]

            baseline_data = baseline_data[baseline_data['Sex'] == 1]
            int_data = int_data[int_data['Sex'] ==1]

            # Highest age quartile
            # baseline_data = baseline_data[baseline_data['Age'] >= 61]
            # int_data = int_data[int_data['Age'] >= 61]

            # Lowest age quartile
            # baseline_data = baseline_data[baseline_data['Age'] <= 32]
            # int_data = int_data[int_data['Age'] <= 32]



        cases_prevented_total_seed = 0

        for year in range(1, years + 1):
            if mortalities:
                baseline_cases = baseline_data[f'{NCD} mortalities year {year} post'].sum()
                int_cases = int_data[f'{NCD} mortalities year {year} post'].sum()
            else:
                baseline_cases = baseline_data[f'New {NCD} cases year {year}'].sum()
                int_cases = int_data[f'New {NCD} cases year {year}'].sum()

            cases_prevented_year = baseline_cases - int_cases
            cases_prevented_total_seed += cases_prevented_year

        cases_prevented_total.append(cases_prevented_total_seed)

    mean = np.mean(cases_prevented_total)
    lower = np.percentile(cases_prevented_total, 2.5)
    upper = np.percentile(cases_prevented_total, 97.5)


    return mean, lower, upper
#


def percentage_of_new_cases(NCD, reduction,red_meat, processed_meat ,mortalities, years, data_dir):

    mean_NF, lower_NF, upper_NF = cumulative_cases_prevented_with_filter(NCD=NCD, reduction=reduction, red_meat=red_meat, processed_meat=processed_meat, mortalities=mortalities, years=years, with_filter=False, data_dir=data_dir)

    mean_F, lower_F, upper_F = cumulative_cases_prevented_with_filter(NCD=NCD, reduction=reduction, red_meat=red_meat, processed_meat=processed_meat, mortalities=mortalities, years=years, with_filter=True, data_dir=data_dir)

    mean = np.round((mean_F/mean_NF)*100, 2)
    lower = np.round((lower_F/upper_NF)*100, 2)
    upper = np.round((upper_F/lower_NF)*100,2)

    print(f'{reduction}% reduction: % of prevented {NCD} cases: {mean}%, ({lower}%, {upper}%)')

    return


def compute_incidence(NCD, reduction, red_meat, processed_meat, mortalities, years, data_dir):

    if reduction == 0.0:
        path = data_dir + '0.0_reduction/'
    else:
        if red_meat and processed_meat:
            path = data_dir + f'{reduction}_reduction/'
        elif red_meat and not processed_meat:
            path = data_dir + f'{reduction}_reduction_RM_alone/'
        elif processed_meat and not red_meat:
            path = data_dir + f'{reduction}_reduction_PM_alone/'
        else:
            raise ValueError('Must specify a reduction in either red or processed meat')

    cases_total = []

    for seed in range(1, 51):

        if red_meat and processed_meat:
            data = pd.read_parquet(path + f'df_seed_{seed}.parquet')
        elif red_meat and not processed_meat:
            data = pd.read_parquet(path + f'df_seed_{seed}_RM.parquet')
        elif processed_meat and not red_meat:
            data = pd.read_parquet(path + f'df_seed_{seed}_PM.parquet')
        else:
            raise ValueError('Must specify a reduction in either red or processed meat')

        cases_seed = 0

        for year in range(1, years + 1):
            if mortalities:
                #cases = data[f'{NCD} mortalities year {year} pre'].sum()
                cases = data[f'Total mortalities year {year} pre'].sum()
            else:
                cases = data[f'New {NCD} cases year {year}'].sum()

            cases_seed += cases

        cases_total.append(cases_seed)

    mean = np.mean(cases_total)
    lower = np.percentile(cases_total, 2.5)
    upper = np.percentile(cases_total, 97.5)

    return mean, lower, upper

def cumulative_cases_prevented(NCD, red_meat, processed_meat, mortalities, years,  int_path):

    baseline_path = 'Output/Final/Two_day_recall/0.0_reduction/'



    # if red_meat and processed_meat:
    #     int_path = data_dir + f'{reduction}_reduction/'
    # elif red_meat and not processed_meat:
    #     int_path = data_dir + f'{reduction}_reduction_RM_alone/'
    # elif processed_meat and not red_meat:
    #     int_path = data_dir + f'{reduction}_reduction_PM_alone/'
    # else:
    #     raise ValueError('Must specify a reduction in either red or processed meat')


    cases_prevented_total = []
    BMI_mean_total = []


    for seed in range(0, 2):
        baseline_data = pd.read_parquet(baseline_path + f'df_seed_{seed}.parquet')

        if red_meat and processed_meat:
            int_data = pd.read_parquet(int_path + f'df_seed_{seed}.parquet')
        elif red_meat and not processed_meat:
            int_data = pd.read_parquet(int_path + f'df_seed_{seed}_RM.parquet')
        elif processed_meat and not red_meat:
            int_data = pd.read_parquet(int_path + f'df_seed_{seed}_PM.parquet')
        else:
            raise ValueError('Must specify a reduction in either red or processed meat')


        # ## Set the age to be that of the population.py at the start of the simulation
        # baseline_data['Age']-= 10
        # int_data['Age'] -= 10

        cases_prevented_total_seed = 0


        for year in range(1, years + 1):
            if mortalities:
                baseline_cases = baseline_data[f'{NCD} mortalities year {year} post'].sum()
                int_cases = int_data[f'{NCD} mortalities year {year} post'].sum()
            else:
                baseline_cases = baseline_data[f'New {NCD} cases year {year}'].sum()
                int_cases = int_data[f'New {NCD} cases year {year}'].sum()

            # baseline_BMI = (baseline_data[f'BMI year {year}'] * baseline_data['Sample Weight']).sum() / baseline_data['Sample Weight'].sum()
            # int_BMI = (int_data[f'BMI year {year}'] * int_data['Sample Weight']).sum() / int_data['Sample Weight'].sum()

            cases_prevented_year = baseline_cases - int_cases
            cases_prevented_total_seed += cases_prevented_year

        cases_prevented_total.append(cases_prevented_total_seed)

    mean = np.mean(cases_prevented_total)
    lower = np.percentile(cases_prevented_total, 2.5)
    upper = np.percentile(cases_prevented_total, 97.5)


    return mean, lower, upper

if __name__ == '__main__':
    years =1

    int_path = 'Output/Final/Two_day_recall/30.0_reduction/'
    for NCD in ['diabetes', 'CVD', 'CRC']:
        x,y,z = cumulative_cases_prevented(NCD=NCD, red_meat=True, processed_meat=True, mortalities=False, years=years, int_path=int_path)
        print(f'{NCD} cases prevented by year {years}: {x} ({y}, {z})')



