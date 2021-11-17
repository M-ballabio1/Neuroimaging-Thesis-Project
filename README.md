# Repository for BSc Biomedical Engineering Thesis

## 0.Pre-processing and Segmentation

This folder contain the script used for preprocessing T1-W images. It also contains a .txt file 
describing the workflow used for tissue segmentation using the ITKSNAP software CLI.

![Preprocessing_giusto drawio](https://user-images.githubusercontent.com/78934727/142078775-1a50e3ad-7be1-4b12-bf15-ff93dcb0eb70.png)

![segmentation](https://user-images.githubusercontent.com/78934727/142191006-f16cdb4e-0eef-48f1-bf62-bd1b57f991d8.png)

![clustering](https://user-images.githubusercontent.com/78934727/142191087-ec51bbe9-c201-4bfa-8368-c3516a9d5caf.png)




## 1. Segmentation Analysis

This folder contain the script used to exctract segmentation volumes and used to performed
statistical test. In particular, two different tests were carried out: ANOVA and T-test

![tessuti_tot](https://user-images.githubusercontent.com/78934727/142190412-eb69ded9-c777-4706-bef1-8641929ab1ad.png)

![anova](https://user-images.githubusercontent.com/78934727/142190454-bb1e51af-122e-4f52-becd-5bf3ecc33be4.png)

![t-test3](https://user-images.githubusercontent.com/78934727/142190837-4ced7b17-e33d-4809-afe5-000659137fd3.png)




## 2.Upload folder

This folder contains two script for the upload and storage of dataset of Benchmark in BrainLife.io
The final script used for the upload dataset is written in python and allow to to optimize and 
speed up the data loading step on the platform.

![Upload data_giusto drawio](https://user-images.githubusercontent.com/78934727/142075402-437669ee-49af-4d63-b515-b07e07c40878.png)

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

![dice](https://user-images.githubusercontent.com/78934727/142238239-fa45584b-ced7-491a-a67b-46532628066b.png)

#### Example of SUBJECT ACC:

First image is the ground truth mask segmentation
Second image is the 3D-U-Net excellent mask segmentation

![gt_284617](https://user-images.githubusercontent.com/78934727/142241237-8edbedce-a102-47bc-9e66-fb383bb423d2.png)
![unet_284617](https://user-images.githubusercontent.com/78934727/142241557-c4e24262-f578-46ca-8804-8c93f3fa8536.png)

#### Example of SUBJECT HD:

First image is the ground truth mask segmentation
Second image is the 3D-U-Net excellent mask segmentation

![gt_MAFF](https://user-images.githubusercontent.com/78934727/142241684-2b9449ed-552b-470d-87ff-9dccf428ee52.png)
![unet_MAFF](https://user-images.githubusercontent.com/78934727/142241700-7c65fbfa-395b-4ef4-94dd-d22815b1ce4f.png)

The results of GM and WM is very good, CEREBELLUM's result is good, on the other hand, the CSF is discrete when compared
with the classic segmentation methods.
