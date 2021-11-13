#!/bin/bash

#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:05:00

#parse config.json for input parameters (here, we are pulling "t1") --> communication with BL
t1=$(jq -r .t1 config.json)
affine=$(jq -r .affine config.json)
mask=$(jq -r .mask config.json)

echo ${mask}
echo ${affine}
if [ -n "${affine}" ]; then
	affine_opt=" --affine ${affine} "

fi
mask=$(jq -r .mask config.json)
if [ -n "${mask}" ]; then
	mask_opt=" --mask ${mask} "
fi


template='./data/MNI152_T1_1mm.nii.gz'
singularity exec -e docker://brainlife/ants:2.2.0.1 bash T1Wbasicpreproc.sh -i $t1 -t ${template} ${affine_opt}  ${mask_opt} --outputdir ./outputdir

mkdir -p ./T1_reoriented
mkdir -p ./T1_reoriented_N4

cp ./outputdir/*reoriented.nii.gz ./T1_reoriented
cp ./outputdir/*reoriented_N4.nii.gz ./T1_reoriented_N4
