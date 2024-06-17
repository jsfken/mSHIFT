#!/usr/bin/env bash

# Specify reduction scenarios
reductions=(5 10 30 50 75 100)

# set the number of random seed parameters which determines the number of simulations for each scenario.
start_seed=1
end_seed=5

# Reduction in unprocessed red meat
red_meat=True
#Reduction in processed meat
processed_meat=True

# Runs a simuation for 10 individuals from the simulation dataset to ensure that everything runs correctly
test_mode=False

# Set the numbre of years to run the simulation for
years=10

# set the path to the simulation dataset
path='Data/mSHIFT_two_day_recall_data.plk'

echo 'mSHIFT -- micro-Simulation of the Health Impacts of Food Transformations'

### shellcheck disable=SC2068

for seed in $(seq $start_seed $end_seed); do
    python ./main.py --path_to_df $path --percent_reduction 0 --seed "$seed" --red_meat $red_meat --processed_meat $processed_meat --years $years --test_mode $test_mode
  done








