#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 09:15:49 2021

@author: matteo99
"""

# Image segmentation and morphological operators

from matplotlib import pyplot as plt
import numpy as np
from skimage.filters import threshold_multiotsu
import cv2
import os
import seaborn as sns
import nibabel as nib
from nibabel.testing import data_path

#img = cv2.imread("/home/matteo99/Scaricati/maff_whole_brain_Crop.png", 0)

immagine_ni1 = os.path.join('/home/matteo99/Scrivania/MAFF_T1W3D_N4_reoriented.nii.gz')
n1_img = nib.load(immagine_ni1)
array_nifti = n1_img.get_fdata()
#n = int(array_nifti.shape[2]/2)
array2D = array_nifti[:,:,90]
#plt.grid(b=None)
plt.axis('off')
plt.imshow(array2D, cmap='gray')

Array_flattizzato = array2D.flatten()
'''
plt.figure(figsize=(30,20))
plt.hist(Array_flattizzato, bins=40, density=True)
plt.xlim(9500,70000)
plt.ylim(0,0.00002)
plt.show()
'''

####AUTO###########################
# Apply multi-Otsu threshold 

thresholds = threshold_multiotsu(array2D, classes=4)

# Digitize (segment) original image into multiple classes.
#np.digitize assign values 0, 1, 2, 3, ... to pixels in each class.
regions = np.digitize(array2D, bins=thresholds)
plt.imshow(regions)

segm1 = (regions == 0)
segm2 = (regions == 1)
segm3 = (regions == 2)
segm4 = (regions == 3)


#We can use binary opening and closing operations to clean up. 
#Open takes care of isolated pixels within the window
#Closing takes care of isolated holes within the defined window

from scipy import ndimage as nd

segm1_opened = nd.binary_opening(segm1, np.ones((1,1)))
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

plt.axis('off')
plt.figure(figsize=(100,100))
plt.imshow(all_segments_cleaned)  #All the noise should be cleaned now
plt.imsave("/home/matteo99/Scrivania/Segm_otsu.jpg", all_segments_cleaned) 