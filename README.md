# Repository for BSc Biomedical Engineering Thesis

## 0.Pre-processing and Segmentation

This folder contain the script used for preprocessing T1-W images. It also contains a .txt file 
describing the workflow used for tissue segmentation using the ITKSNAP software CLI.

## 1. Segmentation Analysis

This folder contain the script used to exctract segmentation volumes and used to performed
statistical test. In particular, two different tests were carried out: ANOVA and T-test

## 2.Upload folder

This folder contains two script for the upload and storage of dataset of Benchmark in BrainLife.io
The final script used for the upload dataset is written in python and allow to to optimize and 
speed up the data loading step on the platform.

## 3.Example App for Reproducibility PRE-PROCESSING STEP

This folder contains an example of a script for Pre-processing dataset on BrainLife.io.

#### Input APP

There are two mandatory inputs:
    
	-i, --input         T1-w image to be preprocessed    
	-t, --template      template as reference space to be reoriented
   
and some optional inputs:

	-o, --outputdir     if not provided, the scripts create the folder 
	-a, --affine        affine matrix to perform rigid transformation to the template
	-m, --mask          brain mask to limit Bias-field correction on these voxels     
	-n, --nthreads      number of threads

#### Output APP

The results of app-MBB_preprocessing_t1w are:
     
     -T1-w reoriented.nii.gz
     -T1-w reoriented_N4BiasField.nii.gz

## 4.Example App for Comparison Segmentation Masks

This folder contains an example of script for calculate Dice Score between predicted mask and ground truth of each label.
The goal is to try to reproduce the comparison step through Dice Score between ground truth masks and predicted masks 
through the 3D-U-Net convolutional neural network


