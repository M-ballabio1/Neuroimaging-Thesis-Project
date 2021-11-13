#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 10:53:01 2021

@author: matteo99
"""

import nibabel as nib
import numpy as np
import pandas as pd
from IPython.display import display, HTML

#%% Path

path = '/home/matteo99/Scrivania/confronto_segm'
mask_pth = path+'/predicted_folder/predicted.nii.gz'
grou_pth = path+'/ground_truth_folder/ground_truth.nii.gz'

#%% Dice Score

mask_p = nib.load(mask_pth)
gt_p = nib.load(grou_pth)
mask = np.array(mask_p.dataobj)
gt = np.array(gt_p.dataobj)

# Calculate class-wise dice similarity coefficient
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

# Calculate the total Dice Score
def dice_coef(img, img2):
        if img.shape != img2.shape:
            raise ValueError("Shape mismatch: img and img2 must have to be of the same shape.")
        else:
            lenIntersection=0
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if ( np.array_equal(img[i][j],img2[i][j]) ):
                        lenIntersection+=1
            lenimg=img.shape[0]*img.shape[1]
            lenimg2=img2.shape[0]*img2.shape[1]  
            value = (2. * lenIntersection  / (lenimg + lenimg2))
        return value

#%% Main

Dice = compute_dice(gt, mask, 7)
print(Dice)
dice_tot = dice_coef(gt, mask)
print(dice_tot)

Dice_new1 = np.append(Dice,dice_tot)
Dice_new2 = np.delete(Dice_new1,[0])
Dice_new = np.reshape(Dice_new2, (1,7))

# Graft our results matrix into pandas data frames 
overlap_results_df = pd.DataFrame(data=Dice_new, columns=('CSF','GM',
                                                          'WM','DGM','TRUNK','CEREBELLUM',
                                                          'TOTAL'), index=['Sub1'])

# Display the data as HTML tables and graphs
display(HTML(overlap_results_df.to_html(float_format=lambda x: '%.3f' % x)))
overlap_results_df.plot(kind='bar').legend(bbox_to_anchor=(1.4,0.9))

