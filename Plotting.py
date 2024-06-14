import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from itertools import cycle, islice
#import imageio
import os
# import pickle5 as pickle5
# import pickle

plt.rcParams["font.family"] = 'serif'
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.formatter.use_mathtext"] = True


def total_mortalities_prevented_year(reduction, years, red_meat, processed_meat, data_dir):
    if red_meat and processed_meat:
        int_path = data_dir + f'{reduction}_reduction/'
    elif red_meat and not processed_meat:
        int_path = data_dir + f'{reduction}_reduction_RM_alone/'
    elif not red_meat and processed_meat:
        int_path = data_dir + f'{reduction}_reduction_PM_alone/'
    else:
        raise Exception('Specify a reduction in either red meat, processed meat or both')

    baseline_path = data_dir + '0.0_reduction/'
    cases_prevented_total = []

    for seed in range(1, 51):

        file_name = f'df_seed_{seed}'

        if red_meat and not processed_meat:
            file_name += '_RM'
        elif not red_meat and processed_meat:
            file_name += '_PM'

        file_name += '.plk'

        baseline_data = pd.read_pickle(baseline_path + f'df_seed_{seed}.plk')
        int_data = pd.read_pickle(int_path + file_name)

        cases_prevented_total_seed = 0

        for year in range(1, years + 1):
            baseline_cases = baseline_data[f'Total mortalities year {year} post'].sum()
            int_cases = int_data[f'Total mortalities year {year} post'].sum()

            cases_prevented_year = baseline_cases - int_cases
            cases_prevented_total_seed += cases_prevented_year

        cases_prevented_total.append(cases_prevented_total_seed)

    mean = np.mean(cases_prevented_total)
    lower = np.percentile(cases_prevented_total, 2.5)
    upper = np.percentile(cases_prevented_total, 97.5)

    return mean, lower, upper

def plot_total_mortalities(red_meat, processed_meat, data_dir, save_fig):

    linestyles = ['solid', 'dotted', '-.']
    colours = ['#953b00', '#957300', '#67c600', '#006225', '#007c99', '#0350f0', '#5e0cfb']

    reductions = [5.0, 10.0, 30.0, 50.0, 75.0, 100.0]

    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(19, 15))
    plt.subplots_adjust(hspace=0.4)

    title_font_size = 40
    y_adustment = 0.95

    # if red_meat and not processed_meat:
    #     fig.suptitle('Prevented total mortalities, red meat reduction', y=y_adustment, fontsize=title_font_size)
    # elif processed_meat and not red_meat:
    #     fig.suptitle('Prevented total mortalities, processed meat reductions', y=y_adustment, fontsize=title_font_size)
    # else:
    #     fig.suptitle('Prevented total mortalities, red and processed meat reductions', y=y_adustment, fontsize=title_font_size)

    count = 0
    for year in [1, 5, 10]:
        cases_prevented_total = np.zeros(len(reductions))
        cases_error = np.zeros((2, len(reductions)))
        if year == 1:
            linestyle = 'solid'
        elif year == 5:
            linestyle = 'dashed'
        elif year == 10:
            linestyle = '-.'
        for i in range(len(reductions)):
            mean, lower, upper = total_mortalities_prevented_year(reduction=reductions[i],
                                                                  years=year,
                                                                  red_meat=red_meat,
                                                                  processed_meat=processed_meat,
                                                                  data_dir=data_dir)
            cases_prevented_total[i] = mean
            cases_error[0, i] = mean - lower
            cases_error[1, i] = upper - mean

        if year == 1:
            axs.plot(reductions, cases_prevented_total, color=colours[count],
                               label=f'{year} year',
                               linestyle=linestyles[count]
                               )
        else:
            axs.plot(reductions, cases_prevented_total, color=colours[count],
                               label=f'{year} years',
                               linestyle=linestyles[count]
                               )

        axs.errorbar(reductions, cases_prevented_total, yerr=cases_error, capsize=4,
                               color=colours[count], linestyle=linestyles[count])

        count += 1

        axs.tick_params(labelsize=20)
        axs.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        axs.yaxis.offsetText.set_fontsize(20)

    axs.set_xlim(4, 102)
    axs.set_xlabel('Red and processed meat reduction, %', fontsize=30)
    axs.set_ylabel('Prevented mortalities, total', fontsize=30)

    # handles, labels = axs.get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper left', prop={'size': 19})
    axs.legend(fontsize=19)

    if save_fig:
        plot_file_name = f'Prevented_total_mortalities'

        if processed_meat and not red_meat:
            plot_file_name += '_PM'
        elif red_meat and not processed_meat:
            plot_file_name += '_RM'

        plot_file_name += '.png'
        plot_path = 'Plots/' + plot_file_name
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')

    plt.show()

    return


def total_cases(NCD, reduction, years, red_meat, processed_meat, mortalities, data_dir):
    if reduction == 0.0:
        path = data_dir + '0.0_reduction/'
    else:
        if red_meat and processed_meat:
            path = data_dir + f'{reduction}_reduction/'
        elif red_meat and not processed_meat:
            path = data_dir + f'{reduction}_reduction_RM_alone/'
        elif not red_meat and processed_meat:
            path = data_dir + f'{reduction}_reduction_PM_alone/'
        else:
            raise Exception('Specify a reduction in either red meat, processed meat or both')

    cases_total = []
    mortalities_total = []

    for seed in range(1, 51):

        file_name = f'df_seed_{seed}'

        if red_meat and not processed_meat:
            file_name += '_RM'
        elif not red_meat and processed_meat:
            file_name += '_PM'

        file_name += '.plk'

        data = pd.read_pickle(path + f'df_seed_{seed}.plk')

        cases_total_seed = 0
        total_mortalities_seed = 0

        for year in range(1, years + 1):
            if mortalities:
                cases_year = data[f'{NCD} mortalities year {year} post'].sum()
            else:
                cases_year = data[f'New {NCD} cases year {year}'].sum()

            total_mortalities_year = data[f'Total mortalities year {year} post'].sum()

            total_mortalities_seed += total_mortalities_year
            cases_total_seed += cases_year

        cases_total.append(cases_total_seed)
        mortalities_total.append(total_mortalities_seed)

    mean_cases = np.mean(cases_total)
    lower_cases = np.percentile(cases_total, 2.5)
    upper_cases = np.percentile(cases_total, 97.5)

    mean_mortalities = np.mean(mortalities_total)
    lower_mortalities = np.percentile(mortalities_total, 2.5)
    upper_mortalities = np.percentile(mortalities_total, 97.5)

    print(f'Total number of new cases: {mean_cases}, ({lower_cases} , {upper_cases})')
    print(f'Total number of new mortalities: {mean_mortalities}, ({lower_mortalities} , {upper_mortalities}')

    return


def cases_prevented_year(NCD, reduction, mortalities, year, data_dir):
    baseline_path = data_dir + '0.0_reduction/'
    int_path = data_dir + f'{reduction}_reduction/'

    cases_prevented_array = []

    for seed in range(1, 51):
        baseline_data = pd.read_pickle(baseline_path + f'df_seed_{seed}.plk')
        int_data = pd.read_pickle(int_path + f'df_seed_{seed}.plk')

        if mortalities:
            baseline_cases = baseline_data[f'{NCD} mortalities year {year} post'].sum()
        else:
            baseline_cases = baseline_data[f'New {NCD} cases year {year}'].sum()

        if mortalities:
            int_cases = int_data[f'{NCD} mortalities year {year} post'].sum()
        else:
            int_cases = int_data[f'New {NCD} cases year {year}'].sum()

        cases_prevented = baseline_cases - int_cases
        cases_prevented_array.append(cases_prevented)

    mean = np.mean(cases_prevented_array)
    lower = np.percentile(cases_prevented_array, 2.5)
    upper = np.percentile(cases_prevented_array, 97.5)

    return mean, lower, upper


def cumulative_cases_prevented(NCD, reduction, processed_meat, red_meat, mortalities, years, data_dir):
    baseline_path = data_dir + '0.0_reduction/'

    if red_meat and processed_meat:
        int_path = data_dir + f'{reduction}_reduction/'
    elif red_meat and not processed_meat:
        int_path = data_dir + f'{reduction}_reduction_RM_alone/'
    elif not red_meat and processed_meat:
        int_path = data_dir + f'{reduction}_reduction_PM_alone/'
    else:
        raise Exception('Specify a reduction in either red meat, processed meat or both')

    cases_prevented_total = []
    #baseline_cases_seed = []


    for seed in range(1, 51):

        file_name = f'df_seed_{seed}'

        if red_meat and not processed_meat:
            file_name += '_RM'
        elif not red_meat and processed_meat:
            file_name += '_PM'

        file_name += '.plk'

        baseline_data = pd.read_pickle(baseline_path + f'df_seed_{seed}.plk')
        int_data = pd.read_pickle(int_path + file_name)

        cases_prevented_total_seed = 0

        for year in range(1, years + 1):
            if mortalities:
                baseline_cases = baseline_data[f'{NCD} mortalities year {year} post'].sum()
                int_cases = int_data[f'{NCD} mortalities year {year} post'].sum()

                # baseline_cases = baseline_data[f'Total mortalities year {year} post'].sum()
                # int_cases = int_data[f'Total mortalities year {year} post'].sum()

            else:
                baseline_cases = baseline_data[f'New {NCD} cases year {year}'].sum()
                int_cases = int_data[f'New {NCD} cases year {year}'].sum()

            #baseline_cases_seed.append(baseline_cases)
            cases_prevented_year = baseline_cases - int_cases
            cases_prevented_total_seed += cases_prevented_year

        cases_prevented_total.append(cases_prevented_total_seed)



    mean = np.mean(cases_prevented_total)
    lower = np.percentile(cases_prevented_total, 2.5)
    upper = np.percentile(cases_prevented_total, 97.5)

    # lower_baseline = np.percentile(baseline_cases_seed, 2.5)
    # upper_baseline = np.percentile(baseline_cases_seed, 97.5)
    # print(f'Total baseline cases: {np.mean(baseline_cases_seed)} ({lower_baseline}, {upper_baseline})')

    return mean, lower, upper


def plot_prevented_cases_shape(NCD, processed_meat, red_meat, mortalities, data_dir, save_fig):
    linestyles = ['solid', 'dotted', '-.']
    colours = ['#953b00', '#957300', '#67c600']

    reductions = [5.0, 10.0, 30.0, 50.0, 100.0]

    cases_prevented_total = np.zeros(len(reductions))
    cases_error = np.zeros((2, len(reductions)))

    c = 0
    for year in [1, 5, 10]:
        for i in range(len(reductions)):
            mean, lower, upper = cumulative_cases_prevented(NCD=NCD, reduction=reductions[i], mortalities=mortalities,
                                                            years=year, data_dir=data_dir)
            cases_prevented_total[i] = mean
            cases_error[0, i] = mean - lower
            cases_error[1, i] = upper - mean

        if year == 1:
            plt.plot(reductions, cases_prevented_total, color=colours[c], label=f'{year} year', linestyle=linestyles[c])
        else:
            plt.plot(reductions, cases_prevented_total, color=colours[c], label=f'{year} years',
                     linestyle=linestyles[c])

        plt.errorbar(reductions, cases_prevented_total, yerr=cases_error, capsize=4, color=colours[c])
        c += 1

    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.xlim(4, 102)
    plt.xlabel('Reduction, %', fontsize=15)

    if mortalities:
        if red_meat and not processed_meat:
            plt.title(f'{NCD}, red meat'.capitalize(), fontsize=15)
        elif processed_meat and not red_meat:
            plt.title(f'{NCD}, processed meat'.capitalize(), fontsize=15)
        else:
            plt.title(f'{NCD}, red and processed meat'.capitalize(), fontsize=15)

        plt.ylabel('Mortalities prevented', fontsize=15)
    else:
        plt.ylabel('Cases prevented', fontsize=15)
        if red_meat and not processed_meat:
            plt.title(f'{NCD}, red meat'.capitalize(), fontsize=15)
        elif processed_meat and not red_meat:
            plt.title(f'{NCD}, processed meat'.capitalize(), fontsize=15)
        else:
            plt.title(f'{NCD}, red and processed meat'.capitalize(), fontsize=15)

    plt.legend()

    if save_fig:
        plot_file_name = f'{NCD}_prevented_cases'

        if processed_meat and not red_meat:
            plot_file_name += '_PM'
        elif red_meat and not processed_meat:
            plot_file_name += '_RM'

        if mortalities:
            plot_file_name += '_mortalities'

        plot_file_name += '.png'
        plot_path = 'Plots/' + plot_file_name
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')

    return


def subplots(red_meat, processed_meat, mortalities, save_fig):
    NCDs = ['diabetes', 'CVD', 'CRC', 'diabetes and CVD', 'diabetes and CRC', 'CVD and CRC']

    linestyles = ['solid', 'dotted', '-.']
    colours = ['#953b00', '#957300', '#67c600', '#006225', '#007c99', '#0350f0', '#5e0cfb']

    reductions = [5.0, 10.0, 30.0, 50.0, 75.0, 100.0]

    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(20, 16))
    plt.subplots_adjust(hspace=0.3)

    #title_font_size = 40
    #y_adustment = 1.06

    # if mortalities:
    #     if red_meat and not processed_meat:
    #         fig.suptitle('Prevented mortalities, red meat reduction', y=y_adustment, fontsize=title_font_size)
    #     elif processed_meat and not red_meat:
    #         fig.suptitle('Prevented mortalities, processed meat reductions',  y=y_adustment, fontsize=title_font_size)
    #     else:
    #         fig.suptitle('Prevented mortalities, red and processed meat reductions',  y=y_adustment, x=0.54, fontsize=title_font_size)
    # else:
    #     if red_meat and not processed_meat:
    #         fig.suptitle('Prevented cases, red meat reduction',  y=y_adustment, fontsize=title_font_size)
    #     elif processed_meat and not red_meat:
    #         fig.suptitle('Prevented cases, processed meat reduction', y=y_adustment ,fontsize=title_font_size)
    #     else:
    #         fig.suptitle('Prevented cases, red and processed meat reduction', y=y_adustment, fontsize=title_font_size)

    NCD_count = 0
    for row in range(2):
        for col in range(3):
            count = 0
            for year in [1, 5, 10]:
                cases_prevented_total = np.zeros(len(reductions))
                cases_error = np.zeros((2, len(reductions)))
                if year == 1:
                    linestyle = 'solid'
                elif year == 5:
                    linestyle = 'dashed'
                elif year == 10:
                    linestyle = '-.'
                for i in range(len(reductions)):
                    mean, lower, upper = cumulative_cases_prevented(NCD=NCDs[NCD_count], reduction=reductions[i],
                                                                    red_meat=red_meat,
                                                                    processed_meat=processed_meat,
                                                                    mortalities=mortalities,
                                                                    years=year, data_dir=data_dir)
                    cases_prevented_total[i] = mean
                    cases_error[0, i] = mean - lower
                    cases_error[1, i] = upper - mean

                if year == 1:
                    axs[row, col].plot(reductions, cases_prevented_total, color=colours[count],
                                       label=f'{year} year',
                                       linestyle=linestyles[count]
                                       )
                else:
                    axs[row, col].plot(reductions, cases_prevented_total, color=colours[count],
                                       label=f'{year} years',
                                       linestyle=linestyles[count]
                                       )

                axs[row, col].errorbar(reductions, cases_prevented_total, yerr=cases_error, capsize=4,
                                       color=colours[count], linestyle=linestyles[count])

                count += 1

                title = f"{NCDs[NCD_count]}".capitalize()
                title = title.replace("cvd", "CVD")
                title = title.replace("Cvd", "CVD")
                title = title.replace("Crc", "Colorectal cancer")
                title = title.replace("crc", "colorectal cancer")
                axs[row, col].set_title(title, y=1.08, fontsize=23)

                axs[row, col].tick_params(labelsize=15)
                axs[row, col].ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
                axs[row, col].yaxis.offsetText.set_fontsize(23)

            NCD_count += 1

            axs[row, col].set_xlim(4, 102)
            if col == 1 and row == 1:
                if red_meat and processed_meat:
                    axs[row, col].set_xlabel('Reduction in both red and processed meat, %', fontsize=23)
                elif red_meat and not processed_meat:
                    axs[row, col].set_xlabel('Reduction in red meat, %', fontsize=23)
                elif processed_meat and not red_meat:
                    axs[row, col].set_xlabel('Reduction in processed meat, %', fontsize=23)
            else:
                axs[row, col].set(xlabel=None)

            if col == 0:
                axs[row, col].set_ylabel('Prevented cases', fontsize=23)
            else:
                axs[row, col].set_ylabel(ylabel=None)

    handles, labels = axs[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper left', prop={'size': 19})

    if save_fig:
        if mortalities:
            plot_file_name = f'Prevented_mortalities'
        else:
            plot_file_name = f'Prevented_cases'

        if processed_meat and not red_meat:
            plot_file_name += '_PM'
        elif red_meat and not processed_meat:
            plot_file_name += '_RM'

        plot_file_name += '.png'
        plot_path = 'Plots/' + plot_file_name
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')

    plt.show()

    return

def subplots_same_scale(red_meat, processed_meat, mortalities, save_fig):

    NCDs = ['diabetes', 'CVD', 'diabetes and CVD', 'CRC', 'diabetes and CRC', 'CVD and CRC']

    linestyles = ['solid', 'dotted', '-.']
    colours = ['#953b00', '#957300', '#67c600', '#006225', '#007c99', '#0350f0', '#5e0cfb']

    reductions = [5.0, 10.0, 30.0, 50.0, 75.0, 100.0]

    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(20, 16))
    plt.subplots_adjust(hspace=0.3)


    NCD_count = 0
    for row in range(2):
        for col in range(3):
            count = 0
            for year in [1, 5, 10]:
                cases_prevented_total = np.zeros(len(reductions))
                cases_error = np.zeros((2, len(reductions)))
                if year == 1:
                    linestyle = 'solid'
                elif year == 5:
                    linestyle = 'dashed'
                elif year == 10:
                    linestyle = '-.'
                for i in range(len(reductions)):
                    mean, lower, upper = cumulative_cases_prevented(NCD=NCDs[NCD_count], reduction=reductions[i],
                                                                    red_meat=red_meat,
                                                                    processed_meat=processed_meat,
                                                                    mortalities=mortalities,
                                                                    years=year, data_dir=data_dir)
                    cases_prevented_total[i] = mean
                    cases_error[0, i] = mean - lower
                    cases_error[1, i] = upper - mean

                if year == 1:
                    axs[row, col].plot(reductions, cases_prevented_total, color=colours[count],
                                       label=f'{year} year',
                                       linestyle=linestyles[count]
                                       )
                else:
                    axs[row, col].plot(reductions, cases_prevented_total, color=colours[count],
                                       label=f'{year} years',
                                       linestyle=linestyles[count]
                                       )

                axs[row, col].errorbar(reductions, cases_prevented_total, yerr=cases_error, capsize=4,
                                       color=colours[count], linestyle=linestyles[count])

                count += 1


                if mortalities:
                    if row == 0:
                        axs[row, col].set_ylim(0, 5e05)
                    else:
                        axs[row, col].set_ylim(0, 5e04)
                else:
                    if row == 0:
                        axs[row, col].set_ylim(0, 3e06)
                    else:
                        axs[row, col].set_ylim(0, 2e05)




                title = f"{NCDs[NCD_count]}".capitalize()
                title = title.replace("cvd", "CVD")
                title = title.replace("Cvd", "CVD")
                title = title.replace("Crc", "Colorectal cancer")
                title = title.replace("crc", "colorectal cancer")
                axs[row, col].set_title(title, y=1.08, fontsize=23)

                axs[row, col].tick_params(labelsize=15)
                axs[row, col].ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
                axs[row, col].yaxis.offsetText.set_fontsize(23)

            NCD_count += 1

            axs[row, col].set_xlim(4, 102)
            if col == 1 and row == 1:
                if red_meat and processed_meat:
                    axs[row, col].set_xlabel('Reduction in both red and processed meat, %', fontsize=23)
                elif red_meat and not processed_meat:
                    axs[row, col].set_xlabel('Reduction in red meat, %', fontsize=23)
                elif processed_meat and not red_meat:
                    axs[row, col].set_xlabel('Reduction in processed meat, %', fontsize=23)
            else:
                axs[row, col].set(xlabel=None)


            if mortalities:
                if col == 0:
                    axs[row, col].set_ylabel('Prevented mortalities', fontsize=23)
                else:
                    axs[row, col].set_ylabel(ylabel=None)
            else:
                if col == 0:
                    axs[row, col].set_ylabel('Prevented cases', fontsize=23)
                else:
                    axs[row, col].set_ylabel(ylabel=None)

    handles, labels = axs[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper left', prop={'size': 19})

    if save_fig:
        if mortalities:
            plot_file_name = f'Prevented_mortalities'
        else:
            plot_file_name = f'Prevented_cases'

        if processed_meat and not red_meat:
            plot_file_name += '_PM'
        elif red_meat and not processed_meat:
            plot_file_name += '_RM'

        plot_file_name += '.png'
        plot_path = 'Plots/' + plot_file_name
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')

    #plt.show()

    return


def table_values(year, reductions, red_meat, processed_meat, mortalities, comorbidity=False):

    # #reductions = [5.0, 10.0, 30.0, 50.0, 75.0, 100.0]
    # reductions = [10.0]

    comorbidities = ['diabetes and CVD', 'diabetes and CRC', 'CVD and CRC']
    one_disease = ['diabetes', 'CVD', 'CRC']

    for reduction in reductions:
        if comorbidity:
            NCDs=comorbidities
        else:
            NCDs=one_disease

        for NCD in NCDs:

            mean, lower, upper = cumulative_cases_prevented(NCD=NCD, reduction=reduction,
                                                            red_meat=red_meat,
                                                            processed_meat=processed_meat,
                                                            mortalities=mortalities,
                                                            years=year, data_dir=data_dir)
            print(NCD)
            if red_meat and processed_meat:
                print(f'Reduction {reduction} both: {mean} ({lower}, {upper})')
            elif red_meat and not processed_meat:
                print(f'Reduction {reduction} red meat alone: {mean} ({lower}, {upper})')
            elif not red_meat and processed_meat:
                print(f'Reduction {reduction} processed meat alone: {mean} ({lower}, {upper})')
            print('\n')

    return


def cases_prevented_per_SW(df, baseline_path, int_path, NCD, red_meat, processed_meat, year, reduction, mortalities):
    prevented_cases = pd.DataFrame(index=df.index)

    for seed in range(1, 51):

        file_name = f'df_seed_{seed}'

        if red_meat and not processed_meat:
            file_name += '_RM'
        elif not red_meat and processed_meat:
            file_name += '_PM'

        file_name += '.plk'

        baseline_data = pd.read_pickle(baseline_path + f'df_seed_{seed}.plk')
        int_data = pd.read_pickle(int_path + file_name)

        if mortalities:
            baseline_cases = baseline_data[f'{NCD} mortalities year {year} post']
        else:
            baseline_cases = baseline_data[f'New {NCD} cases year {year}']

        if mortalities:
            int_cases = int_data[f'{NCD} mortalities year {year} post']
        else:
            int_cases = int_data[f'New {NCD} cases year {year}']

        prevented_cases_seed = baseline_cases - int_cases
        prevented_cases[
            f'{NCD} cases prevented: year {year}, reduction {reduction}, seed {seed}'] = prevented_cases_seed

    mean = prevented_cases.mean(axis=1)
    df[f'mean {NCD} cases prevented: year {year}, reduction {reduction}'] = mean

    lower = prevented_cases.quantile(0.025, axis=1)
    df[f'lower {NCD} cases prevented: year {year}, reduction {reduction}'] = lower

    upper = prevented_cases.quantile(0.975, axis=1)
    df[f'upper {NCD} cases prevented: year {year}, reduction {reduction}'] = upper

    return df


def demographic_bins(df):
    sex_mapping = {1.0: 'Male', 2.0: 'Female'}

    ethnicity_mapping = {1.0: 'Mexican American', 2.0: 'Other Hispanic', 3.0: 'Non-hispanic white',
                         4.0: 'Non-hispanic black', 6.0: 'Non-hispanic Asian', 7.0: 'Other, including multi-racial'}

    income_mapping = {1: "AHI<25k", 2: "AHI<25k", 3: "AHI<25k", 4: "AHI<25k", 5: "AHI<25k",
                      6: "25k<AHI<55k", 7: "25k<AHI<55k", 8: "$25k<AHI<55k", 9: "55k<AHI<100k",
                      10: "55k<AHI<100k", 11: "55k<AHI<100k", 12: "AHI>100k"}

    df = df.replace({'Sex': sex_mapping, 'Ethnicity': ethnicity_mapping, 'Annual Household Income': income_mapping})

    for i in df.index:
        if df.loc[i, 'Age'] in range(18, 50):
            df.loc[i, 'Age'] = "18-49"
        elif df.loc[i, 'Age'] in range(50, 65):
            df.loc[i, 'Age'] = "50-64"
        elif df.loc[i, 'Age'] in range(65, 80):
            df.loc[i, 'Age'] = "65-79"
        else:
            df.loc[i, 'Age'] = ">80"

    return df


## Write a function that outputs cumulative prevented cases in a particular subpopulation
def percentage_cases_prevented_filter(filter, NCD, reduction, processed_meat, red_meat, mortalities, years, data_dir):
    baseline_path = data_dir + '0.0_reduction/'

    if red_meat and processed_meat:
        int_path = data_dir + f'{reduction}_reduction/'
    elif red_meat and not processed_meat:
        int_path = data_dir + f'{reduction}_reduction_RM_alone/'
    elif not red_meat and processed_meat:
        int_path = data_dir + f'{reduction}_reduction_PM_alone/'
    else:
        raise Exception('Specify a reduction in either red meat, processed meat or both')

    cases_prevented_total = []
    cases_prevented_total_filt = []

    for seed in range(1, 51):

        file_name = f'df_seed_{seed}'

        if red_meat and not processed_meat:
            file_name += '_RM'
        elif not red_meat and processed_meat:
            file_name += '_PM'

        file_name += '.plk'

        baseline_data = pd.read_pickle(baseline_path + f'df_seed_{seed}.plk')
        int_data = pd.read_pickle(int_path + file_name)

        baseline_data = demographic_bins(baseline_data)
        int_data = demographic_bins(int_data)

        baseline_data_filt = baseline_data.query(filter)
        int_data_filt = int_data.query(filter)

        cases_prevented_total_seed = 0
        cases_prevented_total_seed_filt = 0

        for year in range(1, years + 1):

            if mortalities:
                baseline_cases = baseline_data[f'{NCD} mortalities year {year} post'].sum()
                int_cases = int_data[f'{NCD} mortalities year {year} post'].sum()
                baseline_cases_filt = baseline_data_filt[f'{NCD} mortalities year {year} post'].sum()
                int_cases_filt = int_data_filt[f'{NCD} mortalities year {year} post'].sum()

            else:
                baseline_cases = baseline_data[f'New {NCD} cases year {year}'].sum()
                int_cases = int_data[f'New {NCD} cases year {year}'].sum()
                baseline_cases_filt = baseline_data_filt[f'New {NCD} cases year {year}'].sum()
                int_cases_filt = int_data_filt[f'New {NCD} cases year {year}'].sum()

            cases_prevented_year = baseline_cases - int_cases
            cases_prevented_total_seed += cases_prevented_year

            cases_prevented_year_filt = baseline_cases_filt - int_cases_filt
            cases_prevented_total_seed_filt += cases_prevented_year_filt

        cases_prevented_total.append(cases_prevented_total_seed)
        cases_prevented_total_filt.append(cases_prevented_total_seed_filt)

    percentage_prevented_cases = 100 * np.array(cases_prevented_total_filt) / np.array(cases_prevented_total)

    mean = np.mean(percentage_prevented_cases)
    lower = np.percentile(percentage_prevented_cases, 2.5)
    upper = np.percentile(percentage_prevented_cases, 97.5)

    return mean, lower, upper


def percentage_pop_df(NCD, year, reduction, by_income=False, by_age=False, by_sex_eth=False):
    if not (by_income ^ by_age ^ by_sex_eth):
        raise Exception("Only one of the binning conditions can be true")

    if by_income:

        index = ['prevented cases']
        columns = ["AHI<25k", "25k<AHI<55k", "55k<AHI<100k", "AHI>100k"]

        df_mean = pd.DataFrame(index=index, columns=columns)
        df_lower = pd.DataFrame(index=index, columns=columns)
        df_upper = pd.DataFrame(index=index, columns=columns)

        filters = ["`Annual Household Income` == 'AHI<25k'",
                   "`Annual Household Income` == '25k<AHI<55k'",
                   "`Annual Household Income` == '55k<AHI<100k'",
                   "`Annual Household Income`== 'AHI>100k'"]

        for filter in filters:
            mean, lower, upper = percentage_cases_prevented_filter(filter=filter,
                                                                   NCD=NCD,
                                                                   reduction=reduction,
                                                                   processed_meat=processed_meat,
                                                                   red_meat=red_meat,
                                                                   mortalities=mortalities,
                                                                   years=year,
                                                                   data_dir=data_dir)
            col = filters.index(filter)
            df_mean.iloc[0, col] = mean
            df_lower.iloc[0, col] = lower
            df_upper.iloc[0, col] = upper

            df_mean.to_pickle(path=f'Data/Plots/mean_{NCD}_{year}_{reduction}_income.plk')
            df_lower.to_pickle(path=f'Data/Plots/lower_{NCD}_{year}_{reduction}_income.plk')
            df_upper.to_pickle(path=f'Data/Plots/upper_{NCD}_{year}_{reduction}_income.plk')

    if by_age:

        index = ['prevented cases']
        columns = ["18-49", "50-64", "65-79", ">80"]

        df_mean = pd.DataFrame(index=index, columns=columns)
        df_lower = pd.DataFrame(index=index, columns=columns)
        df_upper = pd.DataFrame(index=index, columns=columns)

        filters = ["Age == '18-49'",
                   "Age == '50-64'",
                   "Age == '65-79'",
                   "Age == '>80'"]

        for filter in filters:
            mean, lower, upper = percentage_cases_prevented_filter(filter=filter,
                                                                   NCD=NCD,
                                                                   reduction=reduction,
                                                                   processed_meat=processed_meat,
                                                                   red_meat=red_meat,
                                                                   mortalities=mortalities,
                                                                   years=year,
                                                                   data_dir=data_dir)
            col = filters.index(filter)
            df_mean.iloc[0, col] = mean
            df_lower.iloc[0, col] = lower
            df_upper.iloc[0, col] = upper

            df_mean.to_pickle(path=f'Data/Plots/mean_{NCD}_{year}_{reduction}_age.plk')
            df_lower.to_pickle(path=f'Data/Plots/lower_{NCD}_{year}_{reduction}_age.plk')
            df_upper.to_pickle(path=f'Data/Plots/upper_{NCD}_{year}_{reduction}_age.plk')

    if by_sex_eth:

        index = ['Male', 'Female']
        columns = ['Mexican American', 'Other Hispanic', 'Non-hispanic white',
                   'Non-hispanic black', 'Non-hispanic Asian', 'Other, including multi-racial']

        df_mean = pd.DataFrame(index=index, columns=columns)
        df_lower = pd.DataFrame(index=index, columns=columns)
        df_upper = pd.DataFrame(index=index, columns=columns)

        filters_male = ["Sex == 'Male' and Ethnicity == 'Mexican American'",
                        "Sex == 'Male' and Ethnicity == 'Other Hispanic'",
                        "Sex == 'Male' and Ethnicity == 'Non-hispanic white'",
                        "Sex == 'Male' and Ethnicity == 'Non-hispanic black'",
                        "Sex == 'Male' and Ethnicity == 'Non-hispanic Asian'",
                        "Sex == 'Male' and Ethnicity == 'Other, including multi-racial'"
                        ]

        filters_female = ["Sex == 'Female' and Ethnicity == 'Mexican American'",
                          "Sex == 'Female' and Ethnicity == 'Other Hispanic'",
                          "Sex == 'Female' and Ethnicity == 'Non-hispanic white'",
                          "Sex == 'Female' and Ethnicity == 'Non-hispanic black'",
                          "Sex == 'Female' and Ethnicity == 'Non-hispanic Asian'",
                          "Sex == 'Female' and Ethnicity == 'Other, including multi-racial'"
                          ]

        for filter in filters_male:
            mean, lower, upper = percentage_cases_prevented_filter(filter=filter,
                                                                   NCD=NCD,
                                                                   reduction=reduction,
                                                                   processed_meat=processed_meat,
                                                                   red_meat=red_meat,
                                                                   mortalities=mortalities,
                                                                   years=year,
                                                                   data_dir=data_dir)
            col = filters_male.index(filter)
            df_mean.iloc[0, col] = mean
            df_lower.iloc[0, col] = lower
            df_upper.iloc[0, col] = upper

        for filter in filters_female:
            mean, lower, upper = percentage_cases_prevented_filter(filter=filter,
                                                                   NCD=NCD,
                                                                   reduction=reduction,
                                                                   processed_meat=processed_meat,
                                                                   red_meat=red_meat,
                                                                   mortalities=mortalities,
                                                                   years=year,
                                                                   data_dir=data_dir)
            col = filters_female.index(filter)
            df_mean.iloc[1, col] = mean
            df_lower.iloc[1, col] = lower
            df_upper.iloc[1, col] = upper

        df_mean.to_pickle(path=f'Data/Plots/mean_{NCD}_{year}_{reduction}_sex_eth.plk')
        df_lower.to_pickle(path=f'Data/Plots/lower_{NCD}_{year}_{reduction}_sex_eth.plk')
        df_upper.to_pickle(path=f'Data/Plots/upper_{NCD}_{year}_{reduction}_sex_eth.plk')

    return


def total_percentage_dem_groups(by_income=False, by_age=False, by_sex=False, by_eth=False):
    if not (by_income ^ by_age ^ by_sex ^ by_eth):
        raise Exception("Only one of the binning conditions can be true")

    index = ['prevented cases']
    data = pd.read_pickle('Data/mSHIFT_data.plk')
    data = demographic_bins(data)
    total_pop = data['Sample Weight'].sum()

    if by_income:
        columns = ["AHI<25k", "25k<AHI<55k", "55k<AHI<100k", "AHI>100k"]

        df_tot = pd.DataFrame(index=index, columns=columns)

        data_col1 = data[data['Annual Household Income'] == "AHI<25k"]
        df_tot["AHI<25k"] = 100 * (data_col1['Sample Weight'].sum() / total_pop)

        data_col2 = data[data['Annual Household Income'] == "25k<AHI<55k"]
        df_tot["25k<AHI<55k"] = 100 * (data_col2['Sample Weight'].sum() / total_pop)

        data_col3 = data[data['Annual Household Income'] == "55k<AHI<100k"]
        df_tot["55k<AHI<100k"] = 100 * (data_col3['Sample Weight'].sum() / total_pop)

        data_col4 = data[data['Annual Household Income'] == "AHI>100k"]
        df_tot["AHI>100k"] = 100 * (data_col4['Sample Weight'].sum() / total_pop)

    if by_age:
        index = ['prevented cases']
        columns = ["18-49", "50-64", "65-79", ">80"]
        df_tot = pd.DataFrame(index=index, columns=columns)

        data_col1 = data[data['Age'] == "18-49"]
        df_tot["18-49"] = 100 * (data_col1['Sample Weight'].sum() / total_pop)

        data_col2 = data[data['Age'] == "50-64"]
        df_tot["50-64"] = 100 * (data_col2['Sample Weight'].sum() / total_pop)

        data_col3 = data[data['Age'] == "65-79"]
        df_tot["65-79"] = 100 * (data_col3['Sample Weight'].sum() / total_pop)

        data_col4 = data[data['Age'] == ">80"]
        df_tot[">80"] = 100 * (data_col4['Sample Weight'].sum() / total_pop)

    if by_sex:
        index = ['prevented cases']
        columns = ["Male", "Female"]
        df_tot = pd.DataFrame(index=index, columns=columns)

        data_col1 = data[data['Sex'] == 'Male']
        df_tot["Male"] = 100 * (data_col1['Sample Weight'].sum() / total_pop)

        data_col2 = data[data['Sex'] == 'Female']
        df_tot["Female"] = 100 * (data_col2['Sample Weight'].sum() / total_pop)

    if by_eth:
        index = ['prevented cases']
        columns = ['Mexican American', 'Other Hispanic', 'Non-hispanic white',
                   'Non-hispanic black', 'Non-hispanic Asian', 'Other, including multi-racial']
        df_tot = pd.DataFrame(index=index, columns=columns)

        data_col1 = data[data['Ethnicity'] == 'Mexican American']
        df_tot["Mexican American"] = 100 * (data_col1['Sample Weight'].sum() / total_pop)

        data_col2 = data[data['Ethnicity'] == 'Other Hispanic']
        df_tot['Other Hispanic'] = 100 * (data_col2['Sample Weight'].sum() / total_pop)

        data_col3 = data[data['Ethnicity'] == 'Non-hispanic white']
        df_tot['Non-hispanic white'] = 100 * (data_col3['Sample Weight'].sum() / total_pop)

        data_col4 = data[data['Ethnicity'] == 'Non-hispanic black']
        df_tot['Non-hispanic black'] = 100 * (data_col4['Sample Weight'].sum() / total_pop)

        data_col5 = data[data['Ethnicity'] == 'Non-hispanic Asian']
        df_tot['Non-hispanic Asian'] = 100 * (data_col5['Sample Weight'].sum() / total_pop)

        data_col6 = data[data['Ethnicity'] == 'Other, including multi-racial']
        df_tot['Other, including multi-racial'] = 100 * (data_col6['Sample Weight'].sum() / total_pop)

    return df_tot


def compute_mean_error(NCD, year, reduction, by_income=False, by_age=False, by_sex=False, by_ethnicity=False,
                       normalised=False):
    if not (by_income ^ by_age ^ by_sex ^ by_ethnicity):
        raise Exception("Only one of the binning conditions can be true")

    if by_income:
        df_mean = pd.read_pickle(f'Data/Plots/mean_{NCD}_{year}_{reduction}_income.plk')
        df_lower = pd.read_pickle(f'Data/Plots/lower_{NCD}_{year}_{reduction}_income.plk')
        df_upper = pd.read_pickle(f'Data/Plots/upper_{NCD}_{year}_{reduction}_income.plk')

        # with open(f'Data/Plots/mean_{NCD}_{year}_{reduction}_income.plk', "rb") as f:
        #     df_mean = pickle.load(f, protocol=4)
        # with open(f'Data/Plots/lower_{NCD}_{year}_{reduction}_income.plk', "rb") as f:
        #     df_lower = pickle.load(f)
        # with open(f'Data/Plots/upper_{NCD}_{year}_{reduction}_income.plk', "rb") as f:
        #     df_upper = pickle.load(f)

        if normalised:
            norm_df = total_percentage_dem_groups(by_income=True)
            df_mean /= norm_df
            df_lower /= norm_df
            df_upper /= norm_df

    if by_sex:
        df_mean = pd.read_pickle(f'Data/Plots/mean_{NCD}_{year}_{reduction}_sex_eth.plk')
        df_lower = pd.read_pickle(f'Data/Plots/lower_{NCD}_{year}_{reduction}_sex_eth.plk')
        df_upper = pd.read_pickle(f'Data/Plots/upper_{NCD}_{year}_{reduction}_sex_eth.plk')

        # with open(f'Data/Plots/mean_{NCD}_{year}_{reduction}_sex_eth.plk', "rb") as f:
        #     df_mean = pickle.load(f)
        # with open(f'Data/Plots/lower_{NCD}_{year}_{reduction}_sex_eth.plk', "rb") as f:
        #     df_lower = pickle.load(f)
        # with open(f'Data/Plots/upper_{NCD}_{year}_{reduction}_sex_eth.plk', "rb") as f:
        #     df_upper = pickle.load(f)

        df_mean = df_mean.sum(axis=1)
        df_lower = df_lower.sum(axis=1)
        df_upper = df_upper.sum(axis=1)

        df_mean = df_mean.to_frame()
        df_mean = df_mean.T

        df_lower = df_lower.to_frame()
        df_lower = df_lower.T

        df_upper = df_upper.to_frame()
        df_upper = df_upper.T

        df_mean = df_mean.rename(index={0: "prevented cases"})
        df_lower = df_lower.rename(index={0: "prevented cases"})
        df_upper = df_upper.rename(index={0: "prevented cases"})

        if normalised:
            norm_df = total_percentage_dem_groups(by_sex=True)
            df_mean /= norm_df
            df_lower /= norm_df
            df_upper /= norm_df

    if by_ethnicity:
        df_mean = pd.read_pickle(f'Data/Plots/mean_{NCD}_{year}_{reduction}_sex_eth.plk')
        df_lower = pd.read_pickle(f'Data/Plots/lower_{NCD}_{year}_{reduction}_sex_eth.plk')
        df_upper = pd.read_pickle(f'Data/Plots/upper_{NCD}_{year}_{reduction}_sex_eth.plk')

        # with open(f'Data/Plots/mean_{NCD}_{year}_{reduction}_sex_eth.plk', "rb") as f:
        #     df_mean = pickle.load(f)
        # with open(f'Data/Plots/lower_{NCD}_{year}_{reduction}_sex_eth.plk', "rb") as f:
        #     df_lower = pickle.load(f)
        # with open(f'Data/Plots/upper_{NCD}_{year}_{reduction}_sex_eth.plk', "rb") as f:
        #     df_upper = pickle.load(f)

        df_mean = df_mean.sum(axis=0)
        df_lower = df_lower.sum(axis=0)
        df_upper = df_upper.sum(axis=0)

        df_mean = df_mean.to_frame()
        df_mean = df_mean.T

        df_lower = df_lower.to_frame()
        df_lower = df_lower.T

        df_upper = df_upper.to_frame()
        df_upper = df_upper.T

        df_mean = df_mean.rename(index={0: "prevented cases"})
        df_lower = df_lower.rename(index={0: "prevented cases"})
        df_upper = df_upper.rename(index={0: "prevented cases"})

        if normalised:
            norm_df = total_percentage_dem_groups(by_eth=True)
            df_mean /= norm_df
            df_lower /= norm_df
            df_upper /= norm_df

    if by_age:
        df_mean = pd.read_pickle(f'Data/Plots/mean_{NCD}_{year}_{reduction}_age.plk')
        df_lower = pd.read_pickle(f'Data/Plots/lower_{NCD}_{year}_{reduction}_age.plk')
        df_upper = pd.read_pickle(f'Data/Plots/upper_{NCD}_{year}_{reduction}_age.plk')

        # with open(f'Data/Plots/mean_{NCD}_{year}_{reduction}_age.plk', "rb") as f:
        #     df_mean = pickle.load(f)
        # with open(f'Data/Plots/lower_{NCD}_{year}_{reduction}_age.plk', "rb") as f:
        #     df_lower = pickle.load(f)
        # with open(f'Data/Plots/upper_{NCD}_{year}_{reduction}_age.plk', "rb") as f:
        #     df_upper = pickle.load(f)

        if normalised:
            norm_df = total_percentage_dem_groups(by_age=True)
            df_mean /= norm_df
            df_lower /= norm_df
            df_upper /= norm_df

    error = np.array([[df_mean - df_lower], [df_upper - df_mean]])

    if by_income or by_age:
        error = error.reshape(4, 2, 1)
    elif by_sex:
        error = error.reshape(2, 2, 1)
    elif by_ethnicity:
        error = error.reshape(6, 2, 1)

    # else:
    #     error = error.reshape(6, 2, 2)

    return df_mean, error


def pivot_df(df, NCD, year, reduction, by_income=False, by_age=False, by_sex_eth=False):
    if not (by_income ^ by_age ^ by_sex_eth):
        raise Exception("Only one of the binning conditions can be true")

    mean = df['mean ' + NCD + f' cases prevented: year {year}, reduction {reduction}']
    lower = df['lower ' + NCD + f' cases prevented: year {year}, reduction {reduction}']
    upper = df['upper ' + NCD + f' cases prevented: year {year}, reduction {reduction}']

    mean_total = mean.sum()
    lower_total = lower.sum()
    upper_total = upper.sum()

    if by_income:
        df_pivot = pd.pivot_table(
            df,
            values=mean.name,
            columns="Annual Household Income",
            aggfunc=np.sum
        )
        df_pivot = df_pivot[["AHI<\$25k", "\$25<AHI<\$55k", "\$55<AHI<\$100k", "AHI>\$100k"]]

        df_pivot_lower = pd.pivot_table(
            df,
            values=lower.name,
            columns="Annual Household Income",
            aggfunc=np.sum
        )

        df_pivot_lower = df_pivot_lower[["AHI<\$25k", "\$25<AHI<\$55k", "\$55<AHI<\$100k", "AHI>\$100k"]]

        df_pivot_upper = pd.pivot_table(
            df,
            values=upper.name,
            columns="Annual Household Income",
            aggfunc=np.sum
        )

        df_pivot_upper = df_pivot_upper[["AHI<\$25k", "\$25<AHI<\$55k", "\$55<AHI<\$100k", "AHI>\$100k"]]

    if by_sex_eth:
        df_pivot = pd.pivot_table(
            df,
            values=mean.name,
            index="Sex",
            columns="Ethnicity",
            aggfunc=np.sum
        )

        df_pivot_lower = pd.pivot_table(
            df,
            values=lower.name,
            index="Sex",
            columns="Ethnicity",
            aggfunc=np.sum
        )

        df_pivot_upper = pd.pivot_table(
            df,
            values=upper.name,
            index="Sex",
            columns="Ethnicity",
            aggfunc=np.sum
        )

    if by_age:
        df_pivot = pd.pivot_table(
            df,
            values=mean.name,
            columns="Age",
            aggfunc=np.sum
        )
        df_pivot = df_pivot[["18-49", "50-64", "65-79", ">80"]]

        df_pivot_lower = pd.pivot_table(
            df,
            values=lower.name,
            columns="Age",
            aggfunc=np.sum
        )

        df_pivot_lower = df_pivot_lower[["18-49", "50-64", "65-79", ">80"]]

        df_pivot_upper = pd.pivot_table(
            df,
            values=upper.name,
            columns="Age",
            aggfunc=np.sum
        )

        df_pivot_upper = df_pivot_upper[["18-49", "50-64", "65-79", ">80"]]

    if by_income or by_age:
        df_pivot = df_pivot.rename(index={mean.name: 'preventions'})
        df_pivot_lower = df_pivot_lower.rename(index={lower.name: 'preventions'})
        df_pivot_upper = df_pivot_upper.rename(index={upper.name: 'preventions'})

    df_pivot = (df_pivot / mean_total) * 100
    df_pivot_lower = (df_pivot_lower / lower_total) * 100
    df_pivot_upper = (df_pivot_upper / upper_total) * 100

    return df_pivot, df_pivot_lower, df_pivot_upper


def bin_results(df, NCD, reduction, year, red_meat, processed_meat, mortalities, data_dir, by_income=False, by_age=False, by_sex_eth=False):
    if not (by_income ^ by_age ^ by_sex_eth):
        raise Exception("One and only one of grouping conditions can be true")

    baseline_path = data_dir + '0.0_reduction/'

    if red_meat and processed_meat:
        int_path = data_dir + f'{reduction}_reduction/'
    elif red_meat and not processed_meat:
        int_path = data_dir + f'{reduction}_reduction_RM_alone/'
    elif not red_meat and processed_meat:
        int_path = data_dir + f'{reduction}_reduction_PM_alone/'
    else:
        raise Exception('Specify a reduction in either red meat, processed meat or both')

    df = cases_prevented_per_SW(df, baseline_path, int_path, NCD, red_meat, processed_meat, year, reduction,
                                mortalities)
    df = demographic_bins(df)

    # Return three data frames with the mean percentage cases, the lower percentage cases and the upper percenatage cases in each demographic group

    df_mean, df_lower, df_upper = perctange_pop_df(NCD=NCD, year=year, reduction=reduction, by_income=by_income,
                                                   by_age=by_age, by_sex_eth=by_sex_eth)

    df_mean, df_lower, df_upper = pivot_df(df=df, NCD=NCD, year=year, reduction=reduction, by_income=by_income,
                                           by_age=by_age, by_sex_eth=by_sex_eth)

    df_error = np.array([df_mean - df_lower, df_upper - df_mean])

    if by_income or by_age:
        df_error = df_error.reshape(4, 2, 1)
    else:
        df_error = df_error.reshape(6, 2, 2)

    return df_mean, df_error


def demographic_bar_plots(reduction, year, red_meat, processed_meat,  normalised, save_fig):
    nrows = 4
    ncols = 3

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(18, 18))
    plt.subplots_adjust(hspace=0.15)

    mSHIFT_data = pd.read_pickle('Data/mSHIFT_data.plk')
    # with open("Data/mSHIFT_data.plk", "rb") as f:
    #     mSHIFT_data = pickle5.load(f)

    #SHIFT_data = pickle.load('Data/mSHIFT_data.plk')

    my_colors = list(
        islice(cycle(['#ffffcc', '#c7e9b4', '#7fcdbb', '#41b6c4', '#2c7fb8', '#253494']), None, len(mSHIFT_data)))

    NCDs = ['diabetes', 'CVD', 'CRC']

    dem_bins = {0: {'by_income': True, 'normalised': normalised},
                1: {'by_age': True, 'normalised': normalised},
                2: {'by_sex': True, 'normalised': normalised},
                3: {'by_ethnicity': True, 'normalised': normalised}
                }

    for row in range(nrows):
        for col in range(ncols):

            mean, error = compute_mean_error(NCD=NCDs[col], year=year, reduction=reduction, **dem_bins[row])
            # print(NCDs[col])
            # print(mean.to_string())
            # print(error)
            # print('\n')

            mean.plot(ax=axs[row, col], kind="bar", yerr=error, color=my_colors, capsize=8, xticks=[])

            axs[row, col].legend().set_visible(False)
            axs[row, col].tick_params(labelsize=15)

            if col == 0:
                if normalised:
                    axs[0, col].set_ylabel("Annual Household \n Income ", fontsize=20)
                    axs[1, col].set_ylabel("Age", fontsize=20)
                    axs[2, col].set_ylabel("Sex", fontsize=20)
                    axs[3, col].set_ylabel("Ethnicity", fontsize=20)

                else:
                    axs[0, col].set_ylabel("Annual Household \n Income \n % prevented \n cases", fontsize=20)
                    axs[1, col].set_ylabel("Age \n % prevented \n cases", fontsize=20)
                    axs[2, col].set_ylabel("Sex \n % prevented \n cases", fontsize=20)
                    axs[3, col].set_ylabel("Ethnicity \n % prevented \n cases", fontsize=20)

            if row == 0:
                title = f"{NCDs[col]}".capitalize()
                title = title.replace("cvd", "CVD")
                title = title.replace("Cvd", "CVD")
                title = title.replace("Crc", "Colorectal cancer")
                title = title.replace("crc", "colorectal cancer")
                axs[row, col].set_title(title, fontsize=15)

            if col == 2:

                axs[0, col].legend(bbox_to_anchor=(2.4, 0.5), loc='center right', fontsize='20')
                axs[1, col].legend(bbox_to_anchor=(2, 0.5), loc='center right', fontsize='20')
                axs[2, col].legend(bbox_to_anchor=(2, 0.5), loc='center right', fontsize='20')
                axs[3, col].legend(bbox_to_anchor=(2.9, 0.5), loc='center right', fontsize='20')
            else:
                pass

    #
    #
    # print(len(texts))
    #
    # print(isinstance(texts[2], matplotlib.text.Text))

    # get the original legend object
    legend = axs[3, 2].legend()

    # modify the text of the legend labels
    texts = legend.get_texts()
    texts[2].set_text('Non-Hispanic White')
    texts[3].set_text('Non-Hispanic Black')
    texts[4].set_text('Non-Hispanic Asian')
    texts[5].set_text('Other - Including Multi-Racial')

    # create a new legend object with the modified handles and labels
    handles, labels = legend.legend_handles, [t.get_text() for t in texts]
    modified_legend = axs[3, 2].legend(handles, labels, bbox_to_anchor=(3, 0.5), loc='center right', fontsize=20)

    # add the new legend object to the plot
    axs[3, 2].add_artist(modified_legend)

    # legend_eth = axs[3, 2].legend()
    # texts = legend_eth.texts
    # print(len(texts))
    #
    # if len(texts) == 6:
    #     texts[2].set_text('Non-Hispanic White')
    #     texts[3].set_text('Non-Hispanic Black')
    #     texts[4].set_text('Non-Hispanic Asian')
    #     texts[5].set_text('Other - Including Multi-Racial')
    # else:
    #     print('Not enough text elements in the legend.')
    #
    # modified_legend = axs[3, 2].legend(*legend_eth.legendHandles)
    # axs[3, 2].add_artist(modified_legend)
    #
    # axs[3, 2].legend(bbox_to_anchor=(2.9, 0.5), loc='center right', fontsize='20')





    if red_meat and processed_meat:
        fig.suptitle(f'{reduction}% reduction, year {year} \n Red and processed meat', fontsize=25)
    elif not processed_meat and red_meat:
        fig.suptitle(f'{reduction}% reduction, year {year} \n  Red meat alone', fontsize=25)
    elif processed_meat and not red_meat:
        fig.suptitle(f'{reduction}% reduction, year {year} \n Processed meat alone', fontsize=25)
    else:
        raise Exception('Must specify a reduction in one food group')


    if save_fig:
        plt.subplots_adjust(right=0.65)
        if normalised:
            plt.savefig(f'Plots/prevented_cases_demographics_normalised_year_{year}.png', dpi=300)
        else:
            plt.savefig(f'Plots/prevented_cases_demographics_year_{year}.png', dpi=300)

    return


def plot_gif(path):
    png_files = [f.name for f in os.scandir(path) if f.is_file()]

    images = []

    png_files.append(png_files.pop(png_files.index('prevented_diabetes_income_year_10.png')))

    # Loop through the PNG files and add them to the images list
    for file_name in png_files:
        images.append(imageio.imread(path + file_name))

    # Save the images as a GIF
    imageio.mimsave('Plots/gifs/animation.gif', images, duration=1)

    return


def plot_bar_fig1(reduction, year, mortalities, data_dir):
    mean_diabetes, lower_diabetes, upper_diabetes = cumulative_cases_prevented(NCD='diabetes',
                                                                               reduction=reduction,
                                                                               processed_meat=True,
                                                                               red_meat=True,
                                                                               mortalities=mortalities,
                                                                               years=year,
                                                                               data_dir=data_dir)

    mean_CVD, lower_CVD, upper_CVD = cumulative_cases_prevented(NCD='CVD',
                                                                reduction=reduction,
                                                                processed_meat=True,
                                                                red_meat=True,
                                                                mortalities=mortalities,
                                                                years=year,
                                                                data_dir=data_dir)

    mean_CRC, lower_CRC, upper_CRC = cumulative_cases_prevented(NCD='CRC',
                                                                reduction=reduction,
                                                                processed_meat=True,
                                                                red_meat=True,
                                                                mortalities=mortalities,
                                                                years=year,
                                                                data_dir=data_dir)

    mean_diabetes_RM, lower_diabetes_RM, upper_diabetes_RM = cumulative_cases_prevented(NCD='diabetes',
                                                                                        reduction=reduction,
                                                                                        processed_meat=False,
                                                                                        red_meat=True,
                                                                                        mortalities=mortalities,
                                                                                        years=year,
                                                                                        data_dir=data_dir)

    mean_diabetes_PM, lower_diabetes_PM, upper_diabetes_PM = cumulative_cases_prevented(NCD='diabetes',
                                                                                        reduction=reduction,
                                                                                        processed_meat=True,
                                                                                        red_meat=False,
                                                                                        mortalities=mortalities,
                                                                                        years=year,
                                                                                        data_dir=data_dir)

    mean_CVD_RM, lower_CVD_RM, upper_CVD_RM = cumulative_cases_prevented(NCD='CVD',
                                                                         reduction=reduction,
                                                                         processed_meat=False,
                                                                         red_meat=True,
                                                                         mortalities=mortalities,
                                                                         years=year,
                                                                         data_dir=data_dir)

    mean_CVD_PM, lower_CVD_PM, upper_CVD_PM = cumulative_cases_prevented(NCD='CVD',
                                                                         reduction=reduction,
                                                                         processed_meat=True,
                                                                         red_meat=False,
                                                                         mortalities=mortalities,
                                                                         years=year,
                                                                         data_dir=data_dir)

    mean_CRC_RM, lower_CRC_RM, upper_CRC_RM = cumulative_cases_prevented(NCD='CRC',
                                                                         reduction=reduction,
                                                                         processed_meat=False,
                                                                         red_meat=True,
                                                                         mortalities=mortalities,
                                                                         years=year,
                                                                         data_dir=data_dir)

    mean_CRC_PM, lower_CRC_PM, upper_CRC_PM = cumulative_cases_prevented(NCD='CRC',
                                                                         reduction=reduction,
                                                                         processed_meat=True,
                                                                         red_meat=False,
                                                                         mortalities=mortalities,
                                                                         years=year,
                                                                         data_dir=data_dir)

    labels = ['Diabetes', 'CVD', 'Colorectal cancer']

    means_total = [mean_diabetes, mean_CVD, mean_CRC]
    means_RM = [mean_diabetes_RM, mean_CVD_RM, mean_CRC_RM]
    means_PM = [mean_diabetes_PM, mean_CVD_PM, mean_CRC_PM]

    std_total = [[mean_diabetes - lower_diabetes, mean_CVD - lower_CVD, mean_CRC - lower_CRC],
                 [upper_diabetes - mean_diabetes, upper_CVD - mean_CVD, upper_CRC - mean_CRC]]

    std_RM = [[mean_diabetes_RM - lower_diabetes_RM, mean_CVD_RM - lower_CVD_RM, mean_CRC_RM - lower_CRC_RM],
              [upper_diabetes_RM - mean_diabetes_RM, upper_CVD_RM - mean_CVD_RM, upper_CRC_RM - mean_CRC_RM]]

    std_PM = [[mean_diabetes_PM - lower_diabetes_PM, mean_CVD_PM - lower_CVD_PM, mean_CRC_PM - lower_CRC_PM],
              [upper_diabetes_PM - mean_diabetes_PM, upper_CVD_PM - mean_CVD_PM, upper_CRC_PM - mean_CRC_PM]]

    # colours = ['#953b00', '#957300', '#67c600']
    colours = ['#c7e9b4', '#7fcdbb', '#41b6c4']

    x = np.arange(len(labels))
    width = 0.2  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()
    ax.bar(x - width / 2, means_RM, yerr=std_RM, width=width, capsize=6, label='Red meat', color=colours[0],
           alpha=0.9)
    ax.bar(x + width / 2, means_PM, yerr=std_PM, width=width, capsize=6, label='Processed meat', color=colours[1],
           alpha=0.9)
    ax.bar(x + 1.5 * width, means_total, yerr=std_total, capsize=6, width=width, label='Total meat', color=colours[2],
           alpha=0.6)

    # ax.bar(labels, means_RM, width, label='Red meat')
    # ax.bar(labels, means_PM, width, bottom=means_RM, label='Processed meat')

    if mortalities:
        ax.set_ylabel('Prevented mortalities', fontsize=14)
    else:
        ax.set_ylabel('Prevented cases', fontsize=14)

    ax.set_title(f'{reduction}% reduction, year {year}', fontsize=14)
    ax.set_xticks(x + width / 2, labels)
    ax.legend(fontsize=14)

    fig.tight_layout()

    plt.yscale('log')
    #plt.ylim(0, 1e04)
    if mortalities:
        plot_path = f'Plots/Bar_prevented_mortalities_{reduction}_{year}.png'
    else:
        plot_path = f'Plots/Bar_prevented_cases_{reduction}_{year}.png'

    plt.savefig(plot_path, dpi=300, bbox_inches='tight')

    plt.show()

    return


path = 'Plots/bar/'
data_dir = 'Output/Final/'
reduction = 30.0
year = 1
processed_meat = True
red_meat = False
mortalities = False
#mSHIFT_data = pd.read_pickle('Data/mSHIFT_data.plk')
reductions = [5.0, 10.0, 30.0, 50.0, 75.0, 100.0]
#reductions = [75.0]


def Figs3_5():

    for red_meat in [True, False]:
        for processed_meat in [True, False]:
            for mortalities in [True, False]:
                print(f'Red meat: {red_meat}, Processed meat: {processed_meat}, Mortalities: {mortalities}')
                subplots_same_scale(red_meat=red_meat, processed_meat=processed_meat, mortalities=mortalities, save_fig=True)

    return

if __name__ == '__main__':
    #subplots_same_scale(red_meat=red_meat, processed_meat=processed_meat, mortalities=mortalities, save_fig=True)
    #Figs3_5()


    #plot_bar_fig1(reduction=reduction, year=year, mortalities=mortalities, data_dir=data_dir)
    #x, y, z = total_mortalities_prevented_year(reduction=30.0, years=10, red_meat=True, processed_meat=True, data_dir=data_dir)
    #print(x)

    #demographic_bar_plots(reduction=reduction, year=year, red_meat=red_meat, processed_meat=processed_meat, normalised=False, save_fig=True)

    #plot_total_mortalities(red_meat=red_meat, processed_meat=processed_meat, data_dir=data_dir, save_fig=True)



    plot_total_mortalities(red_meat=True, processed_meat=True, data_dir=data_dir, save_fig=True)
    #subplots(red_meat=True, processed_meat=True, mortalities=False, save_fig=True)
    #table_values(year=year, reductions=reductions, red_meat=red_meat, processed_meat=processed_meat, mortalities=mortalities, comorbidity=True)

    #table_values(year=year, reductions=reductions, red_meat=red_meat, processed_meat=processed_meat, mortalities=mortalities, comorbidity=False)




    #table_values(year=year, red_meat=red_meat, processed_meat=processed_meat, mortalities=mortalities, comorbidity=False)

    # mean, lower, upper = cumulative_cases_prevented(NCD='diabetes', reduction=30.0,
    #                            red_meat=red_meat,
    #                            processed_meat=processed_meat,
    #                            mortalities=mortalities,
    #                            years=10, data_dir=data_dir)
    #
    # print(mean, lower, upper)
    #
    # mean, lower, upper = cumulative_cases_prevented(NCD='CVD', reduction=30.0,
    #                            red_meat=red_meat,
    #                            processed_meat=processed_meat,
    #                            mortalities=mortalities,
    #                            years=10, data_dir=data_dir)
    #
    # print(mean, lower, upper)
    #
    # mean, lower, upper = cumulative_cases_prevented(NCD='CRC', reduction=30.0,
    #                                                 red_meat=red_meat,
    #                                                 processed_meat=processed_meat,
    #                                                 mortalities=mortalities,
    #                                                 years=10, data_dir=data_dir)
    #


    # total_cases(NCD='CRC', reduction=reduction, years=year, red_meat=red_meat, processed_meat=processed_meat, mortalities=mortalities, data_dir=data_dir)

    # mean, lower, upper = total_mortalities_prevented_year(reduction=reduction, years=year, red_meat=red_meat, processed_meat=processed_meat, data_dir=data_dir)
    # print(mean, lower, upper)

    #
    #for year in range(1, 11):



    # mean, error = bin_results(df=mSHIFT_data, NCD='CVD',
    #                           reduction=reduction,
    #                           year=year,
    #                           red_meat=red_meat,
    #                           processed_meat=processed_meat,
    #                           mortalities=mortalities,
    #                           data_dir=data_dir,
    #                           by_income=True)

    # for year in range(1, 11):
    #     for NCD in ['CVD', 'CRC']:
    #         percentage_pop_df(NCD=NCD, year=year, reduction=30.0, by_income=True)
    #         percentage_pop_df(NCD=NCD, year=year, reduction=30.0, by_age=True)
    #         percentage_pop_df(NCD=NCD, year=year, reduction=30.0, by_sex_eth=True)

    #
    # for year in range(4,11):
    #     demographic_bar_plots(reduction=reduction, year=year, red_meat=red_meat, processed_meat=processed_meat,
    #                           mortalities=mortalities, data_dir=data_dir)

    # plot_gif(path=path)
