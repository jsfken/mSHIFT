#!/usr/bin/env bash


reductions=(5 10 30 50 75 100)
#reductions=(10 50 75 100)

start_seed=1
end_seed=4
red_meat=True
processed_meat=True
test_mode=False
years=10
path='Data/mSHIFT_data_day2.plk'
one_day_recall=False

#if [ $test_mode ]
#then
#  end_seed=5
#  reductions=(0 30)
#fi

echo 'mSHIFT -- micro-Simulation of the Health Impacts of Food Transformations'

### shellcheck disable=SC2068

#for reduction in ${reductions[@]}; do
#  for red_meat in True False; do
#    for processed_meat in True False; do
#      # Skip the combination where both are False
#      if [ "$red_meat" = "False" ] && [ "$processed_meat" = "False" ]; then
#        continue
#      fi
#      for seed in $(seq 0 50); do
#        python ./main.py --path_to_df $path --percent_reduction $reduction --seed "$seed" --red_meat $red_meat --processed_meat $processed_meat --years $years --one_day_recall $one_day_recall --test_mode $test_mode
#      done
#    done
#  done
#done

for seed in $(seq 0 1); do
    python ./main.py --path_to_df $path --percent_reduction 0 --seed "$seed" --red_meat $red_meat --processed_meat $processed_meat --years $years --one_day_recall $one_day_recall --test_mode $test_mode
  done

for seed in $(seq 0 1); do
    python ./main.py --path_to_df $path --percent_reduction 30 --seed "$seed" --red_meat $red_meat --processed_meat $processed_meat --years $years --one_day_recall $one_day_recall --test_mode $test_mode
  done



#
## shellcheck disable=SC2068
#for reduction in ${reductions[@]}; do
#  for seed in $(seq $start_seed $end_seed); do
#    python ./main.py --path_to_df $path --percent_reduction "$reduction" --seed "$seed" --red_meat $red_meat --processed_meat $processed_meat --years $years --test_mode $test_mode
#  done
#done

#for seed in $(seq $start_seed $end_seed); do
#  python ./main.py --path_to_df $path --percent_reduction 75 --seed "$seed" --red_meat $red_meat --processed_meat $processed_meat --years $years --test_mode $test_mode
#done

# shellcheck disable=SC2068
#for reduction in ${reductions[@]}; do
#  for seed in $(seq 1 30); do
#    python ./main.py --path_to_df $path --percent_reduction "$reduction" --seed "$seed" --red_meat $red_meat --processed_meat False --years $years --test_mode $test_mode
#  done
#done






