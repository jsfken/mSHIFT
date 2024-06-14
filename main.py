import pandas as pd
import time
import sys
import os
from utils import *
from population import *


def run_sim(path_to_df, percent_reduction, seed, red_meat, processed_meat, years, one_day_recall, test_mode=False):

    if test_mode:
        output_directory = 'Output/Tests/'
    else:
        output_directory = 'Output/Final/'
        if one_day_recall:
            output_directory = 'Output/Final/One_day_recall/'
        else:
            output_directory = 'Output/Final/Two_day_recall/'






    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    if red_meat and not processed_meat:
        mdir = f'{percent_reduction}_reduction_RM_alone'
        file_name = f'df_seed_{seed}_RM.parquet'
    elif processed_meat and not red_meat:
        mdir = f'{percent_reduction}_reduction_PM_alone'
        file_name = f'df_seed_{seed}_PM.parquet'
    elif red_meat and processed_meat:
        mdir =f'{percent_reduction}_reduction'
        file_name = f'df_seed_{seed}.parquet'
    else:
        raise ValueError()


    if test_mode:
        mdir = mdir + '_test/'
    else:
        mdir = mdir + '/'

    path = os.path.join(output_directory, mdir)
    if not os.path.exists(path):
        os.mkdir(path)


    print('\n')
    print('#'*20)
    print(f'REDUCTION: {percent_reduction}%, Random Seed: {seed}, Processed meat: {processed_meat}, Red meat: {red_meat}')
    print('#'*20)
    print('\n')

    if red_meat:
        x_RM = (100-percent_reduction)/100
    else:
        x_RM = 1

    if processed_meat:
        x_PM = (100-percent_reduction) / 100
    else:
        x_PM=1

    if path_to_df.endswith('.plk'):
        df = pd.read_pickle(path_to_df)
    elif path_to_df.endswith('.parquet'):
        df = pd.read_parquet(path_to_df)
    elif path_to_df.endswith('.csv'):
        df = pd.read_csv(path_to_df)
    else:
        raise ValueError("Unsupported file format. Only pickle, parquet and csv files are accepted.")

    df_sim = df.copy()

    if test_mode:
        df_sim = df_sim.head(n=50)  # If test mode only select the first 50 individuals in the population.py

    df_sim = run_sampling(df_sim, x_PM=x_PM, x_RM=x_RM, seed=seed)
    df_sim = calculate_risks(df_sim, mortality_table=mortality_table, seed=seed)

    for year in range(1, years+1):
        df_sim = update_mortalities(df_sim, year=year, pre_new_cases=True)
        df_sim = update_cases(df_sim, year=year)
        df_sim = update_mortalities(df_sim, year=year, pre_new_cases=False)
        df_sim = apply_new_mortalities(df_sim, year=year)
        df_sim = update_df(df_sim)
        df_sim = calculate_risks(df_sim, mortality_table=mortality_table, seed=seed)

    df_sim.to_parquet(path=path+file_name)

    return


def parse_arguments(args=None):
    """
    Parse the arguments supplied
    """
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--path_to_df', default=os.getcwd(), type=str, required=True)
    parser.add_argument('--percent_reduction', default=0, type=float, required=True)
    parser.add_argument('--seed', default=0, type=int, required=True)
    parser.add_argument('--red_meat', default=False, type=str2bool, required=True)
    parser.add_argument('--processed_meat', default=False, type=str2bool, required=True)
    parser.add_argument('--years', default=10, type=int, required=False)
    parser.add_argument('--one_day_recall', default=False, type=str2bool, required=False)

    parser.add_argument('--test_mode', default=False, type=str2bool, required=False)

    options = parser.parse_args(args)
    return options

def main(args=None):
    options = parse_arguments(args)
    run_sim(**vars(options))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_time=time.time()
    main(sys.argv[1:])
    end_time=time.time()
    print(f'Total running time: {(end_time-start_time)/60} minutes')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
