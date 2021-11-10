#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 16:11:58 2021
@author: matteoballabio
Data Upload on BrainLife.io
"""

#%% Import Modules

import pandas as pd
import os
import time
import sys
import subprocess

#%% Define Path

#path_data= '/home/matteoballabio/data/DBB_Dataset'
path_data=sys.argv[1]
csv_file= path_data+'/participants.csv'
seg_path= path_data+'/segmentations/'
images_path= path_data+'/images/'
mask_path= path_data+'/raw_masks/'
affine_path= path_data+'/affines/affines_txt/'
label_file= path_data+'/label.json'

#%% Define Main

activity=time.time()

if os.path.exists(csv_file):
    print ("File exist")
    dataset=pd.read_csv(csv_file)
    print(dataset)
else:
    print ("File not exist")

sb_id_v=dataset.iloc[:,0].values
tag_1_v=dataset.iloc[:,4].values
tag_2_v=dataset.iloc[:,5].values
tag_3_v=dataset.iloc[:,6].values
t1_condi_v=dataset.iloc[:,8].values
seg_condi_v=dataset.iloc[:,9].values
mask_cond_v=dataset.iloc[:,10].values
affine_cond_v=dataset.iloc[:,11].values

project='60a14ca503bcad0ad27cada9'

subjects_uploaded=subprocess.check_output(["bl data query --project 60a14ca503bcad0ad27cada9 -l 10000 --datatype neuro/parcellation/volume | grep Subject"], shell=True )
subjects_uploaded_r=str(subjects_uploaded).replace('Subject:','')
subjects_uploaded_r=str(subjects_uploaded_r).rstrip('\n')
subjects_uploaded_list=str(subjects_uploaded_r).split()
last_uploaded_sbj=subjects_uploaded_list[-1]
last_uploaded_sbj=str(last_uploaded_sbj).replace("""\\n'""",'')
print("last subject uploaded: "+last_uploaded_sbj)


start = False

for i in range(len(sb_id_v)):
    sbj_id_i=sb_id_v[i]
    
    if sbj_id_i == last_uploaded_sbj:
        start = True
        continue
    if start == False:
        continue
    
    command0=' -i '+sbj_id_i
    tag1= tag_1_v[i]
    tag2= tag_2_v[i]
    tag3= tag_3_v[i]
    
    file_seg_name=sbj_id_i.replace('sub-','SEGMENTATION_')
    file_seg=seg_path+file_seg_name+'.nii.gz'
    if os.path.exists(file_seg):
        print('The file'+file_seg+' exists')
        file_seg_temp='/tmp/'+os.path.basename(file_seg)
        start=time.time()
        os.system('cp '+file_seg+' '+file_seg_temp)
        commandseg='bl data upload --project '+project+' --datatype "neuro/parcellation/volume" --subject '+sbj_id_i+' --parc '+file_seg_temp+'  --label '+label_file+' --tag '+tag1+' --tag '+tag2+' --tag '+tag3
        os.system(commandseg)
        os.system('rm '+file_seg_temp)
        end=time.time()
        print("Time for completion",end-start)
    else:
        print('The file'+file_seg+' does not exist')
        pass
   
    if t1_condi_v[i] == 'YES':
        file_t1_name=sbj_id_i.replace('sub-','IMAGE_')
        file_t1=images_path+file_t1_name+'.nii.gz'
        if os.path.exists(file_t1):
            print('The file'+file_t1+' exists')
            file_t1_temp='/tmp/'+os.path.basename(file_t1)
            os.system('cp '+file_t1+' '+file_t1_temp)
            commandt1='bl data upload --project '+project+' --datatype "neuro/anat/t1w" --subject '+sbj_id_i+' --t1 '+file_t1_temp+' --tag '+tag1+' --tag '+tag2+' --tag '+tag3
            os.system(commandt1)
            os.system('rm '+file_t1_temp)
        else:
            print('The file'+file_t1+' does not exist')
            pass

    if mask_cond_v[i] == 'YES':
        file_mask_name=sbj_id_i.replace('sub-','BRAIN_MASK_')
        file_mask=mask_path+file_mask_name+'.nii.gz'
        if os.path.exists(file_mask):
            print('The file'+file_mask+' exists')
            file_mask_temp='/tmp/'+os.path.basename(file_mask)
            os.system('cp '+file_mask+' '+file_mask_temp)
            commandmask='bl data upload --project '+project+' --datatype "neuro/mask" --subject '+sbj_id_i+' --mask '+file_mask_temp+' --tag '+tag1+' --tag '+tag2+' --tag '+tag3
            os.system(commandmask)
            os.system('rm '+file_mask_temp)
        else:
            print('The file'+file_mask+' does not exist')
            pass
    
    if affine_cond_v[i] == 'YES':
        file_aff_name=sbj_id_i.replace('sub-','AFFINE_')
        file_affine=affine_path+file_aff_name+'.txt'
        if os.path.exists(file_affine):
            print('The file'+file_affine+' exists')
            file_affine_temp='/tmp/'+os.path.basename(file_affine)
            os.system('cp '+file_affine+' '+file_affine_temp)
            commandaffine='bl data upload --project '+project+' --datatype "neuro/transform" --subject '+sbj_id_i+' --affine '+file_affine_temp+' --datatype_tag "linear" --tag '+tag1+' --tag '+tag2+' --tag '+tag3
            os.system(commandaffine)
            os.system('rm '+file_affine_temp)
        else:
            print('The file'+file_affine+' does not exist')
            pass

ending=time.time()
print("The total time to complete the upload process is: ",ending-activity)
