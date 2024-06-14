import numpy as np
import pandas as pd
from colorectal_cancer import *
from CVD import *
from diabetes import *
from mortalities import *
from incidence import *






def run_sampling(df, x_PM, x_RM, seed):
  np.random.seed(seed)

  df['CRC family history']=df.apply(lambda row: CRC_family_history(row), axis=1)
  df['PM_HR_Diabetes']=df.apply(lambda row: Hazard_ratio_CM_Diabetes(row, x_PM=x_PM), axis=1)
  df['RM_HR_Diabetes']=df.apply(lambda row: Hazard_ratio_RM_Diabetes(row, x_RM=x_RM), axis=1)
  df['PM_HR_CVD']=df.apply(lambda row: Hazard_ratio_CM_CVD(row, x_PM=x_PM), axis=1)
  df['RM_HR_CVD']=df.apply(lambda row: Hazard_ratio_RM_CVD(row, x_RM=x_RM), axis=1)
  df['PM_HR_CRC']=df.apply(lambda row: Relative_risk_Zhao_CM(row, x_PM=x_PM), axis=1)
  df['RM_HR_CRC']=df.apply(lambda row: Relative_risk_Zhao_RM(row, x_RM=x_RM), axis=1)

  return df




def update_smoking_pack_years(row):

  smoking_pack_years=0

  if row['Smoking pack years']!=0:
    smoking_pack_years = row['Smoking pack years']
    smoking_pack_years += row['Daily Cigarettes']/20

  return smoking_pack_years

def update_SBP(row):

  SBP=row['Systolic Blood Pressure']

  if row['Sex'] == 0:
    if row['Age'] < 50:
        SBP += 0.288
    else:
        SBP += 0.308

  elif row['Sex'] ==1:
    if row['Age'] < 50:
          SBP += 0.430
    else:
        SBP += 0.613

  return SBP


def update_df(df):

  df['Age'] += 1
  df['Smoking pack years']=df.apply(lambda row: update_smoking_pack_years(row), axis =1)
  df['Systolic Blood Pressure']=df.apply(lambda row: update_SBP(row), axis =1)
  return df

def calculate_risks(df, mortality_table, seed):

  np.random.seed(seed)

  df['Diabetes risk']=df.apply(lambda row: Diabetes_risk_Alva(row, Diabetes_dict=Diabetes_dict), axis=1)
  df['CVD risk no diabetes']=df.apply(lambda row: updated_Framingham_CVD_risk(row, with_diabetes=False), axis=1)
  df['CVD risk with diabetes']=df.apply(lambda row: updated_Framingham_CVD_risk(row, with_diabetes=True), axis=1)

  df['CRC risk no diabetes']=df.apply(lambda row: CRC_risk(row, with_diabetes=False), axis=1)
  df['CRC risk with diabetes']=df.apply(lambda row: CRC_risk(row, with_diabetes=True), axis=1)

  df['Diabetes and CVD risk']=df['Diabetes risk']*df['CVD risk no diabetes']  ## Probability of getting both in one year from a starting healthy state
  df['Diabetes and CRC risk']=df['Diabetes risk']*df['CRC risk no diabetes']
  df['CVD and CRC risk with diabetes']=df['CVD risk with diabetes']*df['CRC risk with diabetes']
  df['CVD and CRC risk no diabetes']=df['CVD risk no diabetes']*df['CRC risk no diabetes']
  df['Diabetes and CVD and CRC risk'] =df['Diabetes risk']*df['CVD risk no diabetes']*df['CRC risk no diabetes']

  df['diabetes mortality risk']=df.apply(lambda row: mortality_prob(row, mortality_table=mortality_table, with_diabetes=True, with_CVD=False), axis=1)
  df['CVD mortality risk']=df.apply(lambda row: mortality_prob(row, mortality_table=mortality_table, with_diabetes=False, with_CVD=True), axis=1)
  df['diabetes and CVD mortality risk']=df.apply(lambda row: mortality_prob(row, mortality_table=mortality_table, with_diabetes=True, with_CVD=True), axis=1)
  df['CRC mortality risk'] = df.apply(lambda row: CRC_mortality_prob(row), axis=1)
  df['Healthy mortality risk'] = df.apply(lambda row: mortality_prob(row, mortality_table=mortality_table, with_diabetes=False, with_CVD=False), axis=1)

  return df

def update_mortalities(df, year, pre_new_cases):

  if pre_new_cases:
    df[f'Healthy mortalities year {year} pre'] = df.apply(lambda row: expected_healthy_mortalities(row), axis=1)
    df[f'diabetes mortalities year {year} pre']=df.apply(lambda row: expected_diabetes_mortalities(row), axis=1)
    df[f'CVD mortalities year {year} pre']=df.apply(lambda row: expected_CVD_mortalities(row), axis=1)
    df[f'CRC mortalities year {year} pre']=df.apply(lambda row: expected_CRC_mortalities(row), axis=1)
    df[f'diabetes and CVD mortalities year {year} pre']=df.apply(lambda row: expected_diabetes_CVD_mortalities(row),axis=1)
    df[f'diabetes and CRC mortalities year {year} pre']=df.apply(lambda row: expected_diabetes_CRC_mortalities(row), axis=1)
    df[f'CVD and CRC mortalities year {year} pre']=df.apply(lambda row: expected_CVD_CRC_mortalities(row), axis=1)
    df[f'diabetes and CVD and CRC mortalities year {year} pre']=df.apply(lambda row: expected_diabetes_CVD_CRC_mortalities(row), axis=1)
    df[f'Total mortalities year {year} pre']= df[f'Healthy mortalities year {year} pre'] + df[f'diabetes mortalities year {year} pre'] + df[f'CVD mortalities year {year} pre']+df[f'CRC mortalities year {year} pre']-df[f'diabetes and CVD mortalities year {year} pre']-df[f'diabetes and CRC mortalities year {year} pre']-df[f'CVD and CRC mortalities year {year} pre']+df[f'diabetes and CVD and CRC mortalities year {year} pre']

  else:
    df[f'Healthy mortalities year {year} post'] = df.apply(lambda row: expected_healthy_mortalities(row), axis=1)
    df[f'diabetes mortalities year {year} post']=df.apply(lambda row: expected_diabetes_mortalities(row), axis=1)
    df[f'CVD mortalities year {year} post']=df.apply(lambda row: expected_CVD_mortalities(row), axis=1)
    df[f'CRC mortalities year {year} post']=df.apply(lambda row: expected_CRC_mortalities(row), axis=1)
    df[f'diabetes and CVD mortalities year {year} post']=df.apply(lambda row: expected_diabetes_CVD_mortalities(row),axis=1)
    df[f'diabetes and CRC mortalities year {year} post']=df.apply(lambda row: expected_diabetes_CRC_mortalities(row), axis=1)
    df[f'CVD and CRC mortalities year {year} post']=df.apply(lambda row: expected_CVD_CRC_mortalities(row), axis=1)
    df[f'diabetes and CVD and CRC mortalities year {year} post']=df.apply(lambda row: expected_diabetes_CVD_CRC_mortalities(row), axis=1)
    df[f'Total mortalities year {year} post']= df[f'Healthy mortalities year {year} post'] + df[f'diabetes mortalities year {year} post'] + df[f'CVD mortalities year {year} post']+df[f'CRC mortalities year {year} post']-df[f'diabetes and CVD mortalities year {year} post']-df[f'diabetes and CRC mortalities year {year} post']-df[f'CVD and CRC mortalities year {year} post']+df[f'diabetes and CVD and CRC mortalities year {year} post']

  return df


def update_cases(df, year):
    df[f'New diabetes cases year {year}'] = df.apply(lambda row: expected_new_diabetes_cases(row), axis=1)
    df[f'New CVD cases year {year}'] = df.apply(lambda row: expected_new_CVD_cases(row), axis=1)
    df[f'New CRC cases year {year}'] = df.apply(lambda row: expected_new_CRC_cases(row), axis=1)
    df[f'New diabetes and CVD cases year {year}'] = df.apply(lambda row: expected_new_diabetes_CVD_cases(row), axis=1)
    df[f'New diabetes and CRC cases year {year}'] = df.apply(lambda row: expected_new_diabetes_CRC_cases(row), axis=1)
    df[f'New CVD and CRC cases year {year}'] = df.apply(lambda row: expected_new_CVD_CRC_cases(row), axis=1)
    df[f'New diabetes and CVD and CRC cases year {year}'] = df.apply(lambda row: expected_new_diabetes_CVD_CRC_cases(row), axis=1)

    df['New diabetes cases'] += df[f'New diabetes cases year {year}']
    df['New CVD cases'] += df[f'New CVD cases year {year}']
    df['New CRC cases'] += df[f'New CRC cases year {year}']
    df['New diabetes and CVD cases'] += df[f'New diabetes and CVD cases year {year}']
    df['New diabetes and CRC cases'] += df[f'New diabetes and CRC cases year {year}']
    df['New CVD and CRC cases'] += df[f'New CVD and CRC cases year {year}']
    df['New diabetes and CVD and CRC cases'] += df[f'New diabetes and CVD and CRC cases year {year}']

    df['healthy'] = df.apply(lambda row: healthy_pop(row), axis=1)

    return df


def update_sample_weight(row, year):
    SW = row['Sample Weight']
    SW -= row[f'Total mortalities year {year} post']
    return SW


## Update the diabetes cases

def update_new_diabetes_cases(row, year):
    new_cases = row['New diabetes cases']

    if row['Diabetes'] != 1:
        new_cases -= row[f'diabetes mortalities year {year} post']
        if new_cases < 0:
            new_cases = 0
    else:
        pass

    return new_cases


def update_new_CVD_cases(row, year):
    new_cases = row['New CVD cases']

    if row['CVD'] != 1:
        new_cases -= row[f'CVD mortalities year {year} post']
        if new_cases < 0:
            new_cases = 0
    else:
        pass

    return new_cases


def update_new_CRC_cases(row, year):
    new_cases = row['New CRC cases']

    if row['CRC'] != 1:
        new_cases -= row[f'CRC mortalities year {year} post']
        if new_cases < 0:
            new_cases = 0
    else:
        pass

    return new_cases


def update_new_diabetes_CVD_cases(row, year):
    new_cases = row['New diabetes and CVD cases']

    if row['Diabetes'] != 1 and row['CVD'] != 1:
        new_cases -= row[f'diabetes and CVD mortalities year {year} post']
        if new_cases < 0:
            new_cases = 0

    return new_cases


def update_new_diabetes_CRC_cases(row, year):
    new_cases = row['New diabetes and CRC cases']

    if row['Diabetes'] != 1 and row['CRC'] != 1:
        new_cases -= row[f'diabetes and CRC mortalities year {year} post']
        if new_cases < 0:
            new_cases = 0

    return new_cases


def update_new_CVD_CRC_cases(row, year):
    new_cases = row['New CVD and CRC cases']

    if row['CVD'] != 1 and row['CRC'] != 1:
        new_cases -= row[f'CVD and CRC mortalities year {year} post']
        if new_cases < 0:
            new_cases = 0

    return new_cases


def update_new_diabetes_CVD_CRC_cases(row, year):
    new_cases = row['New diabetes and CVD and CRC cases']

    if row['Diabetes'] != 1 and row['CVD'] != 1 and row['CRC'] != 1:
        new_cases -= row[f'diabetes and CVD and CRC mortalities year {year} post']
        if new_cases < 0:
            new_cases = 0

    return new_cases


def apply_new_mortalities(df, year):
    df['Sample Weight'] = df.apply(lambda row: update_sample_weight(row, year), axis=1)
    df['New diabetes cases'] = df.apply(lambda row: update_new_diabetes_cases(row, year), axis=1)
    df['New CVD cases'] = df.apply(lambda row: update_new_CVD_cases(row, year), axis=1)
    df['New CRC cases'] = df.apply(lambda row: update_new_CRC_cases(row, year), axis=1)
    df['New diabetes and CVD cases'] = df.apply(lambda row: update_new_diabetes_CVD_cases(row, year), axis=1)
    df['New diabetes and CRC cases'] = df.apply(lambda row: update_new_diabetes_CRC_cases(row, year), axis=1)
    df['New CVD and CRC cases'] = df.apply(lambda row: update_new_CVD_CRC_cases(row, year), axis=1)
    df['New diabetes and CVD and CRC cases'] = df.apply(lambda row: update_new_diabetes_CVD_CRC_cases(row, year),
                                                        axis=1)

    return df