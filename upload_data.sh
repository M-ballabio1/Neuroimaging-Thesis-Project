#!/bin/bash

bl login

project=60a14ca503bcad0ad27cada9
T1_full=/home/matteo99/mnt/nilabserver/home/matteoballabio/mnt/data/all_subjects_processed/SUBJECT_segmentated/SUBJECT_COMPLETED/SUBJECT_T1W3D_ACPC_BIAS
T1_brain=/home/matteo99/mnt/nilabserver/home/matteoballabio/mnt/data/all_subjects_processed/SUBJECT_segmentated/SUBJECT_COMPLETED/SUBJECT_T1W3D_BRAIN
T1_mask=/home/matteo99/mnt/nilabserver/home/matteoballabio/mnt/data/all_subjects_processed/SUBJECT_segmentated/SUBJECT_COMPLETED/SUBJECT_SEGMENTATION_COMPLETED

for type in $(ls T1_full); do
    for t1 in $(ls $type_*_T1W3D_reoriented_N4.nii.gz); do
        subject=${type}_${t1:4:3}
        bl data upload --project $project --datatype neuro/mask --subject $subject --t1 ${subject}_mask.nii.gz --tag "mask"
        bl data upload --project $project --datatype neuro/anat/t1w --subject $subject --t1 $t1 --tag "brain"
        bl data upload --project $project --datatype neuro/anat/t1w --subject $subject --t1 $t1 --tag "N4" --tag "acpc_aligned" "bias_corrected" 
    done
done
