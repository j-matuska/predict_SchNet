#! /bin/bash

# PaiNN20_3_5Ang_train80

source_dir=`pwd` ;
destination_dir=${source_dir}/PaiNN20_3_5Ang_train80 ;

mkdir -p ${destination_dir}

for s in 01 02 03 04 05 ; do
    cp ${source_dir}/80_${s}_painn_b/best_model ${destination_dir}/${s}/;
    echo `sha256sum ${source_dir}/80_${s}_painn_b/best_model`;
    echo `sha256sum ${destination_dir}/${s}/best_model`;
done;
# then copy folder PaiNN20_3_5Ang_train80 to trained_models