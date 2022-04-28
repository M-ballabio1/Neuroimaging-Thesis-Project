# -*- coding: utf-8 -*-
"""
Spyder Editor
Statistical  Analysis 
author: matte99
"""


#%% Import Modules

import nibabel as nib
from pathlib import Path               #combine path elements with /
import numpy as np                     #numeric python
from scipy import stats                #operate on N-dimensional images
import nibabel.testing                 #for fetching test data
import pandas as pd
import os


#%% Define Functions

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

#%% Define paths

data_segmentation = '/home/matteoballabio/data/all_subjects_processed/SUBJECT_segmentated/SUBJECT_SEGMENTATION_COMPLETED/'
data_analysis = '/home/matteoballabio/data/stat_results/'
xls_file_paz=data_analysis+"/stat.xlsx"

#%% Main

if __name__ == '__main__':
	
	seg_list=os.listdir(data_segmentation)
	npaz=len(seg_list)
	nlabels=len(np.unique(loadArray(data_segmentation+'/'+seg_list[0])))-1		#Num lables == unique element of Nii whitout background
	Vol=np.zeros([npaz,nlabels])
	pat_list=[]
	for idx,seg in enumerate(seg_list):
		pat_id=seg[0:seg.rfind('T1W3D')]									    #crop at subject id
		print(pat_id)
		
		NiiArray1 = loadArray(data_segmentation+'/'+seg)                        #load segmentation
		# calculate volumes for each label
		for i in range(nlabels):
				lindex=(i+1)
				NiiArray_i = (NiiArray1==lindex).astype(int)
				Vol[idx,i] = np.count_nonzero(NiiArray_i)						#spacing=1mm --> nvoxel == volume
				print('vol label'+str(lindex)+': '+str(Vol[idx,i]))
		pat_list.append(pat_id)
	
	# Write Excel file
	writer = pd.ExcelWriter(xls_file_paz) 										#create a excel file from pandas dataframe
	with pd.ExcelWriter(xls_file_paz) as writer:
		sheet_name="Volumes"					
		df = pd.DataFrame(Vol)
		#df = df[1:] 
		hlist=["CSF","GM","WM","DGM","Trunk","Cerebellum"]
		df.index = pat_list 
		df.columns= hlist
		df.to_excel(writer,sheet_name=sheet_name ) #,  header=hlist)
	
