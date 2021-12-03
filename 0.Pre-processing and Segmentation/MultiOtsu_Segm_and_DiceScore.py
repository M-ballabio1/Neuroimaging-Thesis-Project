#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 09:15:49 2021

@author: matteo99
"""

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from skimage.filters import threshold_multiotsu
import cv2
import os
import nibabel as nib
from nibabel.testing import data_path

#%% Path

#img = cv2.imread("/home/matteo99/Scaricati/maff_whole_brain_Crop.png", 0)
immagine_ni1 = os.path.join('/home/matteo99/Scrivania/SUBJECT_for_otsu_script/SUBJECT_323340_T1W3D_reoriented_N4.nii.gz')
gt = os.path.join('/home/matteo99/Scrivania/SUBJECT_for_otsu_script/SUBJECT_323340_T1W3D_Segmentazione_Completa_4_labels.nii.gz')

#%% Load nifti file and histogram

n1_img = nib.load(immagine_ni1)
array_nifti = n1_img.get_fdata()
#n = int(array_nifti.shape[2]/2)
array2D = array_nifti[:,:,90]  #Permette di estrarre una slices assiale (bastava cambiare posizione del 90 per estrarre assiale)
#plt.grid(b=None)
plt.axis('off')
plt.imshow(array2D, cmap='gray')
Array_flattizzato = array2D.flatten()

'''
plt.figure(figsize=(30,20))
plt.hist(Array_flattizzato, bins=40, density=True)
plt.grid()
plt.xlim(0,145000)
plt.ylim(0,0.00012)
plt.show()
'''


#%% Segmentation method Multi-Otsu threshold 

thresholds = threshold_multiotsu(array2D, classes=4)
colors = ['g', 'c', 'm']

# Digitize (segment) original image into multiple classes.
#np.digitize assign values 0, 1, 2, 3, ... to pixels in each class.
regions = np.digitize(array2D, bins=thresholds)
#plt.imshow(regions)

segm1 = (regions == 0)
segm2 = (regions == 1)
segm3 = (regions == 2)
segm4 = (regions == 3)

plt.figure(figsize=(30,20))
plt.hist(Array_flattizzato, bins=40, density=True)
for p, c in zip(thresholds, colors):
    plt.axvline(p,  label='line: {}'.format(p), c=c, linewidth=3)
plt.grid()
plt.xlim(0,array2D.max())
plt.ylim(0,0.00012)
plt.show()


#We can use binary opening and closing operations to clean up. 
#Open takes care of isolated pixels within the window
#Closing takes care of isolated holes within the defined window

from scipy import ndimage as nd

segm1_opened = nd.binary_opening(segm1, np.ones((1,1)))     #Definizione grandezza voxels segmentations
segm1_closed = nd.binary_closing(segm1_opened, np.ones((1,1)))

segm2_opened = nd.binary_opening(segm2, np.ones((1,1)))
segm2_closed = nd.binary_closing(segm2_opened, np.ones((1,1)))

segm3_opened = nd.binary_opening(segm3, np.ones((1,1)))
segm3_closed = nd.binary_closing(segm3_opened, np.ones((1,1)))

segm4_opened = nd.binary_opening(segm4, np.ones((1,1)))
segm4_closed = nd.binary_closing(segm4_opened, np.ones((1,1)))

all_segments_cleaned = np.zeros((array2D.shape[0], array2D.shape[1], 3)) 

all_segments_cleaned[segm1_closed] = (0,0,0)
all_segments_cleaned[segm2_closed] = (1,0,0)
all_segments_cleaned[segm3_closed] = (0,1,0)
all_segments_cleaned[segm4_closed] = (0,0,1)

#plt.axis('off')
plt.figure(figsize=(100,100))
plt.imshow(all_segments_cleaned)  #All the noise should be cleaned now
plt.imsave("/home/matteo99/Scrivania/Segm_otsu.jpg", all_segments_cleaned)

#%% Load Segmentation ground truth

def loadArray(fullpath):    
	file_ext=fullpath[fullpath.rfind('.'):]
	if file_ext == ".gz" or file_ext == ".nii":
	    	
		NiiStructure = nib.load(fullpath)
		Array = NiiStructure.get_data()
	    		
	elif file_ext == ".npy":
	    	
	 	Array=np.load(fullpath)
	else:	
		print("not valid extension")
		return []
	return Array

NiiArray1 = loadArray(gt)
Segm_array2D = NiiArray1[:,:,90] #estrae stessa slices

#%% Dice Score

def compute_dice(truth, pred, classes):
    dice_scores = []
    # Compute Dice for each class
    for i in range(classes):
        try:
            pd = np.equal(pred, i)
            gtr = np.equal(truth, i)
            dice = 2*np.logical_and(pd, gtr).sum()/(pd.sum() + gtr.sum())
            dice_scores.append(dice)
        except ZeroDivisionError:
            dice_scores.append(0.0)
    # Return computed Dice scores
    return dice_scores

Dice = compute_dice(Segm_array2D, regions, 4)
print(Dice)
Dice_new = np.reshape(Dice, (1,4))

# Graft our results matrix into pandas data frames 
overlap_results_df = pd.DataFrame(data=Dice, columns=('background','CSF','GM',
                                                          'WM'), index=['Sub1'])
