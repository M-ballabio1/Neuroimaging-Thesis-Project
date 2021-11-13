#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Apr 11 10:53:01 2021
@author: matteo99
Segmentation Analysis 
"""

#%% Import Modules

import nibabel as nib
from pathlib import Path               #combine path elements with /
import numpy as np                     #numeric python
from matplotlib import pyplot as plt   #mat_lab plotting commands
#from nilearn import plotting as nlp    #nice neuroimage plotting
import scipy.stats as stats        #operate on N-dimensional images
from statsmodels.stats.multicomp import pairwise_tukeyhsd            
import nibabel.testing                 #for fetching test data
import pandas as pd
import os
from statistics import mean, stdev
import matplotlib.mlab as mlab
import seaborn as sns

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
data_segmentation = '/home/matteoballabio/data/all_subjects_processed/SUBJECT_segmentated/SUBJECT_COMPLETED/SUBJECT_SEGMENTATION_COMPLETED/SUBJECT_FINAL_FOR_SCRIPT/'
data_agenesiaCC = data_segmentation+"/SUBJECT_AGENESIA_CC"
data_polimicrogiria = data_segmentation+"/SUBJECT_POLIMICROGIRIA"
data_fossaetronco = data_segmentation+"/SUBJECT_FOSSA_POSTERIORE-TRONCO"
data_highdistorted = data_segmentation+"/SUBJECT_HIGH_DISTORTED"
data_analysis = '/home/matteoballabio/data/stat_results/'
xls_file_paz=data_analysis+"/Vols/FINAL/statALL_SUBJECTS.xlsx"
xls_file_paz1=data_analysis+"/Vols/FINAL/stat2.xlsx"
xls_file_paz2=data_analysis+"/Vols/FINAL/statPOLIMICROGIRIA.xlsx"
xls_file_paz3=data_analysis+"/Vols/FINAL/statFOSSA_E_TRONCO.xlsx"
xls_file_paz4=data_analysis+"/Vols/FINAL/statHIGHDISTORTED.xlsx"
xls_file_paz_describe=data_analysis+"/Vols/FINAL/stat2_sumarized.xlsx"
xls_file_paz_describe11=data_analysis+"/Vols/FINAL/statAGENESIA.xlsx"
xls_file_paz_describe21=data_analysis+"/Vols/FINAL/stat2_sumarized_POLIMICROGIRIA.xlsx"
xls_file_paz_describe31=data_analysis+"/Vols/FINAL/stat2_sumarized_FOSSA_E_TRONCO.xlsx"
data_information = data_analysis+'/Info_pazienti/soggetti_con_malformazioni_anonymized.xlsx'
data_plots = data_analysis+'/Plots'
file_summarized_info = data_analysis+'/Info_pazienti/summarized_pathologies_subjects.txt'
file_stats_info = data_analysis+'/Tests/FINAL_T/stats_test_subjects.txt'

subjjj = ('/home/matteoballabio/data/all_subjects_processed/PROVE')


#%% Main

if __name__ == '__main__':
	
    ## SUBJECTS AGENESIA CC
    
	seg_list1=os.listdir(data_agenesiaCC)
	npaz1=len(seg_list1)
	nlabels1=len(np.unique(loadArray(data_agenesiaCC+'/'+seg_list1[0])))-1		#Num lables == unique element of Nii whitout background
	Vol_Agenesia=np.zeros([npaz1,nlabels1])
	pat_list1=[]
	for idx1,seg1 in enumerate(seg_list1):
		pat_id1=seg1[0:seg1.rfind('_T1W3D')]									    #crop at subject id
		print(pat_id1)
		
		NiiArray1 = loadArray(data_agenesiaCC+'/'+seg1)                        #load segmentation
		# calculate volumes for each label
		for i1 in range(nlabels1):
				lindex1=(i1+1)
				NiiArray_i1 = (NiiArray1==lindex1).astype(int)
				Vol_Agenesia[idx1,i1] = np.count_nonzero(NiiArray_i1)						#spacing=1mm --> nvoxel == volume
				print('vol label'+str(lindex1)+': '+str(Vol_Agenesia[idx1,i1]))
		pat_list1.append(pat_id1)
        
            # Write Excel file
	writer1 = pd.ExcelWriter(xls_file_paz1) 										#create a excel file from pandas dataframe
	with pd.ExcelWriter(xls_file_paz1) as writer1:
		sheet_name1="Volumes SUBJECT AGENESIA in mm^3"					
		df1 = pd.DataFrame(Vol_Agenesia)
		hlist=["CSF","GM","WM","DGM","Trunk","Cerebellum"]
		df1.index = pat_list1
		df1.columns= hlist
		df1.to_excel(writer1,sheet_name=sheet_name1) #,  header=hlist)
 
#create a summarized excel file
writer11 = pd.ExcelWriter(xls_file_paz_describe11) 										
with pd.ExcelWriter(xls_file_paz_describe11) as writer11:
    for row1 in df1:
        mean1=(df1.describe())
        ds1 = pd.DataFrame(mean1)
        sheet_name11="Summarized Volumes SUBJECT AGENESIA in mm^3"
        df1.to_excel(writer11,sheet_name=sheet_name1)
        ds1.to_excel(writer11,sheet_name=sheet_name11)

## SUBJECTS POLIMICROGIRIA
    
seg_list2=os.listdir(data_polimicrogiria)
npaz2=len(seg_list2)
nlabels2=len(np.unique(loadArray(data_polimicrogiria+'/'+seg_list2[0])))-1		#Num lables == unique element of Nii whitout background
Vol_polimicrogiria=np.zeros([npaz2,nlabels2])
pat_list2=[]
for idx2,seg2 in enumerate(seg_list2):
	pat_id2=seg2[0:seg2.rfind('_T1W3D')]									    #crop at subject id
	print(pat_id2)
		
	NiiArray2 = loadArray(data_polimicrogiria+'/'+seg2)                        #load segmentation
		# calculate volumes for each label
	for i2 in range(nlabels2):
			lindex2=(i2+1)
			NiiArray_i2 = (NiiArray2==lindex2).astype(int)
			Vol_polimicrogiria[idx2,i2] = np.count_nonzero(NiiArray_i2)						#spacing=1mm --> nvoxel == volume
			print('vol label'+str(lindex2)+': '+str(Vol_polimicrogiria[idx2,i2]))
	pat_list2.append(pat_id2)
    
# Write Excel file
writer2 = pd.ExcelWriter(xls_file_paz2) 										#create a excel file from pandas dataframe
with pd.ExcelWriter(xls_file_paz2) as writer2:
    sheet_name2="Volumes SUBJECT POLIMICROGIRIA in mm^3"
    df2 = pd.DataFrame(Vol_polimicrogiria)
    hlist=["CSF","GM","WM","DGM","Trunk","Cerebellum"]
    df2.index = pat_list2
    df2.columns= hlist
    mean2=(df2.describe())
    ds2 = pd.DataFrame(mean2)
    sheet_name21="Summarized Volumes SUBJECT POLIMICROGIRIA in mm^3"
    df2.to_excel(writer2,sheet_name=sheet_name2) #,  header=hlist)
    ds2.to_excel(writer2,sheet_name=sheet_name21)
    
## SUBJECTS FOSSA POSTERIORE E TRONCO

seg_list3=os.listdir(data_fossaetronco)
npaz3=len(seg_list3)
nlabels3=len(np.unique(loadArray(data_fossaetronco+'/'+seg_list3[0])))-1		#Num lables == unique element of Nii whitout background
Vol_fossaetronco=np.zeros([npaz3,nlabels3])
pat_list3=[]
for idx3,seg3 in enumerate(seg_list3):
	pat_id3=seg3[0:seg3.rfind('_T1W3D')]									    #crop at subject id
	print(pat_id3)
		
	NiiArray3 = loadArray(data_fossaetronco+'/'+seg3)                        #load segmentation
		# calculate volumes for each label
	for i3 in range(nlabels3):
			lindex3=(i3+1)
			NiiArray_i3 = (NiiArray3==lindex3).astype(int)
			Vol_fossaetronco[idx3,i3] = np.count_nonzero(NiiArray_i3)						#spacing=1mm --> nvoxel == volume
			print('vol label'+str(lindex3)+': '+str(Vol_fossaetronco[idx3,i3]))
	pat_list3.append(pat_id3)

# Write Excel file
writer3 = pd.ExcelWriter(xls_file_paz3) 										#create a excel file from pandas dataframe
with pd.ExcelWriter(xls_file_paz3) as writer3:
    sheet_name3="Volumes SUBJECT FOSSA POSTERIORE E TRONCO in mm^3"
    df3 = pd.DataFrame(Vol_fossaetronco)
    hlist=["CSF","GM","WM","DGM","Trunk","Cerebellum"]
    df3.index = pat_list3
    df3.columns= hlist
    mean3=(df3.describe())
    ds3 = pd.DataFrame(mean3)
    sheet_name31="Summarized Volumes SUBJECT FOSSA POSTERIORE E TRONCO in mm^3"
    df3.to_excel(writer3,sheet_name=sheet_name3) #,  header=hlist)
    ds3.to_excel(writer3,sheet_name=sheet_name31)

## SUBJECTS HIGH DISTORTED

seg_list4=os.listdir(data_highdistorted)
npaz4=len(seg_list4)
nlabels4=len(np.unique(loadArray(data_highdistorted+'/'+seg_list4[0])))-1		#Num lables == unique element of Nii whitout background
Vol_highdistorted=np.zeros([npaz4,nlabels4])
pat_list4=[]
for idx4,seg4 in enumerate(seg_list4):
	pat_id4=seg4[0:seg4.rfind('_T1W3D')]									    #crop at subject id
	print(pat_id4)
		
	NiiArray4 = loadArray(data_highdistorted+'/'+seg4)                        #load segmentation
		# calculate volumes for each label
	for i4 in range(nlabels4):
			lindex4=(i4+1)
			NiiArray_i4 = (NiiArray4==lindex4).astype(int)
			Vol_highdistorted[idx4,i4] = np.count_nonzero(NiiArray_i4)						#spacing=1mm --> nvoxel == volume
			print('vol label'+str(lindex4)+': '+str(Vol_highdistorted[idx4,i4]))
	pat_list4.append(pat_id4)

# Write Excel file
writer4 = pd.ExcelWriter(xls_file_paz4) 										#create a excel file from pandas dataframe
with pd.ExcelWriter(xls_file_paz4) as writer4:
    sheet_name4="Volumes HIGH DISTORTED in mm^3"
    df4 = pd.DataFrame(Vol_highdistorted)
    hlist=["CSF","GM","WM","DGM","Trunk","Cerebellum"]
    df4.index = pat_list4
    df4.columns= hlist
    mean4=(df4.describe())
    ds4 = pd.DataFrame(mean4)
    sheet_name41="Summarized Volumes SUBJECT HIGH DISTORTED in mm^3"
    df4.to_excel(writer4,sheet_name=sheet_name4) #,  header=hlist)
    ds4.to_excel(writer4,sheet_name=sheet_name41)

## SUBJECTS TOTALI

writer = pd.ExcelWriter(xls_file_paz) 										#create a excel file from pandas dataframe
with pd.ExcelWriter(xls_file_paz) as writer:
    sheet_name="Volumes SUBJECT in mm^3"
    df = pd.concat([df1, df2, df3, df4], ignore_index=False)
    mean0=(df.describe())
    ds = pd.DataFrame(mean0)
    sheet_name0="Summarized Volumes in mm^3"
    df.to_excel(writer,sheet_name=sheet_name)
    ds.to_excel(writer,sheet_name=sheet_name0)
              

#%%

def Informazioni():      
    excel_data_df = pd.read_excel(data_information,
                                  usecols=["MRI ID","EXAM AGE","BIRTH DATE","EXAM DATE","DIAGNOSIS"], nrows=31)
    print(excel_data_df)
    
    
    #summary about informations of pathological subjects
    mean_age_subjects = excel_data_df['EXAM AGE'].mean()
    std_age_subjects = excel_data_df['EXAM AGE'].std()
    pathologies = excel_data_df['DIAGNOSIS'].value_counts(normalize=True)
    max_date_acquisition = excel_data_df['EXAM DATE'].max()    
    min_date_acquisition = excel_data_df['EXAM DATE'].min()
    
    mean_age_groups = excel_data_df.groupby('DIAGNOSIS', as_index=False)['EXAM AGE'].mean()
    std_age_groups = excel_data_df.groupby('DIAGNOSIS', as_index=False)['EXAM AGE'].std()

    with open(file_summarized_info,'w',encoding = 'utf-8') as f:
        f.write('\nAge All Subjects: \n\n''Mean and Std Age Subjects: '+str(round(mean_age_subjects,1)))
        f.write(' ± '+str(round(std_age_subjects,1)))
        f.write(' years')
    
        f.write('\n\nPercentage of subjects with different type of pathology: \n\n'+str(pathologies))
        f.write('\n\nMean Age different type of pathologies: \n\n'+str(mean_age_groups))
        f.write('\n\nStd Age different type of pathologies: \n\n'+str(std_age_groups))
        
        f.write('\n\nAcquisition MRI IMAGES: \n')
        f.write('\nFirst acqusition: '+str(min_date_acquisition))
        f.write('\nLast acquisition: '+str(max_date_acquisition))


print(Informazioni())

#%%

#Visualization plot summarized
def Visualization():
    #error-plot mean and std structures pathological subjects
    #FOUR subplots mean/std volumes for different pathological diseases
    x0=hlist
    y0=ds.iloc[1]
    y1=ds1.iloc[1]
    y2=ds2.iloc[1]
    y3=ds3.iloc[1]
    error0=ds.iloc[2]
    error1=ds1.iloc[2]
    error2=ds2.iloc[2]
    error3=ds3.iloc[2]

    fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, figsize=(10,15), sharex=True)

    ax0.errorbar(x0, y0, error0, fmt='o', ecolor='red', capsize=5)
    ax0.set_ylabel('Volume mm^3')
    ax0.set_title('Plot_Mean_Std_structures - ALL SUBJECTS')
    ax0.grid(True)

    ax1.errorbar(x0, y1, error1, fmt='o', ecolor='red', capsize=5)
    ax1.set_ylabel('Volume mm^3')
    ax1.set_title('Plot_Mean_Std_structures - SUBJECTS AGENESIA CC')
    ax1.grid(True)

    ax2.errorbar(x0, y2, error2, fmt='o', ecolor='red', capsize=5)
    ax2.set_ylabel('Volume mm^3')
    ax2.set_title('Plot_Mean_Std_structures - SUBJECTS POLIMICROGIRIA')
    ax2.grid(True)

    ax3.errorbar(x0, y3, error3, fmt='o', ecolor='red', capsize=5)
    ax3.set_ylabel('Volume mm^3')
    ax3.set_title('Plot_Mean_Std_structures - SUBJECTS FOSSA POSTERIORE E TRONCO')
    ax3.grid(True)

    plt.savefig(data_plots +'/Plot_Pathologies_Mean_Std_structures.png')
    
    
    #grid-plot double structures pathological subjects
    columns = ["CSF","GM","WM","DGM","Trunk","Cerebellum"]
    df[columns].head()
    fd = df[columns].dropna()
    g = sns.PairGrid(fd,
                     size=2)
    g.map_diag(plt.hist, alpha=0.5, color=".3")
    g.map_offdiag(plt.scatter, alpha=0.75, s=20);
    g.savefig(data_plots+"/grid_plot_double_structures.png")

print(Visualization())

#%%
def Stat_Analyis():
    #CSF - ANOVA e T-test
    anova_csf = stats.f_oneway(df1.iloc[:,0], df2.iloc[:,0], df3.iloc[:,0], df4.iloc[:,0])
    print(anova_csf)
    t, p = stats.ttest_ind(df1.iloc[:,0], df2.iloc[:,0])
    print('CSF1 vs CSF2:', t, p)
    t1, p1 = stats.ttest_ind(df2.iloc[:,0], df3.iloc[:,0])
    print('CSF2 vs CSF3:', t1, p1)
    t2, p2 = stats.ttest_ind(df3.iloc[:,0], df1.iloc[:,0])
    print('CSF3 vs CSF1:', t2, p2)
    t3, p3 = stats.ttest_ind(df4.iloc[:,0], df1.iloc[:,0])
    print('CSF1 vs CSF4:', t3, p3)
    t4, p4 = stats.ttest_ind(df4.iloc[:,0], df2.iloc[:,0])
    print('CSF2 vs CSF4:', t4, p4)
    t5, p5 = stats.ttest_ind(df4.iloc[:,0], df3.iloc[:,0])
    print('CSF3 vs CSF4:', t5, p5)
    
    #GM - ANOVA e T-Test
    anova_gm = stats.f_oneway(df1.iloc[:,1], df2.iloc[:,1], df3.iloc[:,1])
    print(anova_gm)
    y, u = stats.ttest_ind(df1.iloc[:,1], df2.iloc[:,1])
    print('GM1 vs GM2:', y, u)
    y1, u1 = stats.ttest_ind(df2.iloc[:,1], df3.iloc[:,1])
    print('GM2 vs GM3:', y1, u1)
    y2, u2 = stats.ttest_ind(df3.iloc[:,1], df1.iloc[:,1])
    print('GM3 vs GM1:', y2, u2)
    
    #WM - ANOVA e T-Test
    anova_wm = stats.f_oneway(df1.iloc[:,2], df2.iloc[:,2], df3.iloc[:,2])
    print(anova_wm)
    k, q = stats.ttest_ind(df1.iloc[:,2], df2.iloc[:,2])
    print('WM1 vs WM2:', k, q)
    k1, q1 = stats.ttest_ind(df2.iloc[:,2], df3.iloc[:,2])
    print('WM2 vs WM3:', k1, q1)
    k2, q2 = stats.ttest_ind(df3.iloc[:,2], df1.iloc[:,2])
    print('WM3 vs WM1:', k2, q2)
    
    #DGM - ANOVA e T-Test
    anova_dgm = stats.f_oneway(df1.iloc[:,3], df2.iloc[:,3], df3.iloc[:,3])
    print(anova_dgm)
    m, o = stats.ttest_ind(df1.iloc[:,3], df2.iloc[:,3])
    print('DGM1 vs DGM2:', m, o)
    m1, o1 = stats.ttest_ind(df2.iloc[:,3], df3.iloc[:,3])
    print('DGM2 vs DG3:', m1, o1)
    m2, o2 = stats.ttest_ind(df3.iloc[:,3], df1.iloc[:,3])
    print('DGM3 vs DGM1:', m2, o2)

    #TRUNK - ANOVA e T-Test
    anova_trunk = stats.f_oneway(df1.iloc[:,4], df2.iloc[:,4], df3.iloc[:,4])
    print(anova_trunk)
    n, r = stats.ttest_ind(df1.iloc[:,4], df2.iloc[:,4])
    print('TRUNK1 vs TRUNK2:', n, r)
    n1, r1 = stats.ttest_ind(df2.iloc[:,4], df3.iloc[:,4])
    print('TRUNK2 vs TRUNK3:', n1, r1)
    n2, r2 = stats.ttest_ind(df3.iloc[:,4], df1.iloc[:,4])
    print('TRUNK3 vs TRUNK1:', n2, r2)
    
    #CEREBELLUM - ANOVA e T-Test
    anova_cerebellum = stats.f_oneway(df1.iloc[:,5], df2.iloc[:,5], df3.iloc[:,5])
    print(anova_cerebellum)
    s, x = stats.ttest_ind(df1.iloc[:,5], df2.iloc[:,5])
    print('CEREBELLUM1 vs CEREBELLUM2:', s, x)
    s1, x1 = stats.ttest_ind(df2.iloc[:,5], df3.iloc[:,5])
    print('CERELLUM2 vs CEREBELLUM3:', s1, x1)
    s2, x2 = stats.ttest_ind(df3.iloc[:,5], df1.iloc[:,5])
    print('CEREBELLUM3 vs CEREBELLUM1:', s2, x2)
    
    with open(file_stats_info,'w',encoding = 'utf-8') as f1:
        f1.write('\nCSF')
        f1.write('\n\nANOVA one way: \n\n'+str(anova_csf))
        f1.write('\n\nT-TEST')
        f1.write('\nCSF_GROUP1 vs CSF_GROUP2: t='+str(round(t,3))+' p-value='+str(round(p,3)))
        f1.write('\nCSF_GROUP2 vs CSF_GROUP3: t='+str(round(t1,3))+' p-value='+str(round(p1,3)))
        f1.write('\nCSF_GROUP3 vs CSF_GROUP1: t='+str(round(t2,3))+' p-value='+str(round(p2,3)))
        
        f1.write('\n\nGM')
        f1.write('\n\nANOVA one way: \n\n'+str(anova_gm))
        f1.write('\n\nT-TEST')
        f1.write('\nGM_GROUP1 vs GM_GROUP2: t='+str(round(y,3))+' p-value='+str(round(u,3)))
        f1.write('\nGM_GROUP2 vs GM_GROUP3: t='+str(round(y1,3))+' p-value='+str(round(u1,3)))
        f1.write('\nGM_GROUP3 vs GM_GROUP1: t='+str(round(y2,3))+' p-value='+str(round(u2,3)))
        
        f1.write('\n\nWM')
        f1.write('\n\nANOVA one way: \n\n'+str(anova_wm))
        f1.write('\n\nT-TEST')
        f1.write('\nWM_GROUP1 vs WM_GROUP2: t='+str(round(k,3))+' p-value='+str(round(q,3)))
        f1.write('\nWM_GROUP2 vs WM_GROUP3: t='+str(round(k1,3))+' p-value='+str(round(q1,3)))
        f1.write('\nWM_GROUP3 vs WM_GROUP1: t='+str(round(k2,3))+' p-value='+str(round(q2,3)))
        
        f1.write('\n\nDGM')
        f1.write('\n\nANOVA one way: \n\n'+str(anova_dgm))
        f1.write('\n\nT-TEST')
        f1.write('\nDGM_GROUP1 vs DGM_GROUP2: t='+str(round(m,3))+' p-value='+str(round(o,3)))
        f1.write('\nDGM_GROUP2 vs DGM_GROUP3: t='+str(round(m1,3))+' p-value='+str(round(o1,3)))
        f1.write('\nDGM_GROUP3 vs DGM_GROUP1: t='+str(round(m2,3))+' p-value='+str(round(o2,3)))
        
        f1.write('\n\nTRUNK')
        f1.write('\n\nANOVA one way: \n\n'+str(anova_trunk))
        f1.write('\n\nT-TEST')
        f1.write('\nTRUNK_GROUP1 vs TRUNK_GROUP2: t='+str(round(n,3))+' p-value='+str(round(r,3)))
        f1.write('\nTRUNK_GROUP2 vs TRUNK_GROUP3: t='+str(round(n1,3))+' p-value='+str(round(r1,3)))
        f1.write('\nTRUNK_GROUP3 vs TRUNK_GROUP1: t='+str(round(n2,3))+' p-value='+str(round(r2,3)))
        
        f1.write('\n\nCEREBELLUM')
        f1.write('\n\nANOVA one way: \n\n'+str(anova_cerebellum))
        f1.write('\n\nT-TEST')
        f1.write('\nCEREBELLUM_GROUP1 vs CEREBELLUM_GROUP2: t='+str(round(s,3))+' p-value='+str(round(x,3)))
        f1.write('\nCEREBELLUM_GROUP2 vs CEREBELLUM_GROUP3: t='+str(round(s1,3))+' p-value='+str(round(x1,3)))
        f1.write('\nCEREBELLUM_GROUP3 vs CEREBELLUM_GROUP1: t='+str(round(s2,3))+' p-value='+str(round(x2,3)))
        
    
print(Stat_Analyis())
