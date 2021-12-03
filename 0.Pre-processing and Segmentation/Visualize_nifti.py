#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 09:46:09 2021

@author: matteo99
"""

import nibabel as nib
import matplotlib.pyplot as plt
  
img_arr = nib.load('/home/matteo99/Scrivania/SUBJECT_229263_T1W3D.nii').get_data()
  
def show_plane(ax, plane, cmap="gray", title=None):
     ax.imshow(plane, cmap=cmap)
     ax.axis("off")
  
     if title:
         ax.set_title(title)
         
(n_plane, n_row, n_col) = img_arr.shape
_, (a, b, c) = plt.subplots(ncols=3, figsize=(15, 5))
  
show_plane(a, img_arr[n_plane // 2], title=f'Plane = {n_plane // 2}')
show_plane(b, img_arr[:, n_row // 2, :], title=f'Row = {n_row // 2}')
show_plane(c, img_arr[:, :, n_col // 2], title=f'Column = {n_col // 2}') 
