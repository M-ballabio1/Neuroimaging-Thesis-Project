# Repository for BSc Biomedical Engineering Thesis

## 0.Pre-processing and Segmentation

### Semi-automatic method for Pre-processing 

This folder contain the workflow used for preprocessing T1-W images. 

![Preprocessing_giusto drawio](https://user-images.githubusercontent.com/78934727/142078775-1a50e3ad-7be1-4b12-bf15-ff93dcb0eb70.png)

### Plot histogram subjects (without background)

In this plot, there is a comparison between the different distribution curve of categorical subjects.
In particular, we observe a big curve distribution difference in the case of high distorted case.
Furthermore, it is interesting to note that in the case of a distorted subject from another 
category the tissue distribution curve is quite similar to that of a healthy subject.

![Untitled Diagram drawio](https://user-images.githubusercontent.com/78934727/143457592-504aa93f-05f3-4dc1-af7f-a5ff125a93f3.png)

### Why use a thresholding method with manual selection of the thresholds?

Why was it necessary to use a Threshold segmentation method with choice of manual thresholds compared for example to the Otsu segmentation method (automatic thresholds that minimize intra-class variance)?
The script multi-otsu creates a segmentation based on Otsu method.

![COMPARAZIONE_288618_totale](https://user-images.githubusercontent.com/78934727/144195381-34d38aae-2ca7-4fa9-9a72-a874568b148a.png)

The comparison between the two segmentation methods highlights a gross segmentation by the automatic segmentation algorithm in the case of subjects with severe brain malformations. This is confirmed by the calculation of the Dice Score metric which reports very low results for the Otsu segmentation, in particular for the recognition of background and csf.

![comparison_method2 drawio](https://user-images.githubusercontent.com/78934727/144581503-b270da5f-ed2b-4652-934f-ea7ab42e9273.png)

### Semi-automatic method for Segmentation 

It also contains a .txt file describing the workflow used for tissue segmentation using 
the ITKSNAP software CLI. In particular, using two different algorithms: Thresholding and Clustering.

![segmentation](https://user-images.githubusercontent.com/78934727/142191006-f16cdb4e-0eef-48f1-bf62-bd1b57f991d8.png)

![clustering](https://user-images.githubusercontent.com/78934727/142191087-ec51bbe9-c201-4bfa-8368-c3516a9d5caf.png)

![Trunk_Cerebellum_Segmentation drawio](https://user-images.githubusercontent.com/78934727/143455141-9688d757-23a8-4869-8b80-dd9e8859d3d7.png)



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

![Upload data drawio(2) drawio](https://user-images.githubusercontent.com/78934727/143455235-5185e523-b6cb-477b-bfeb-1cbd8d8b771a.png)

In the following screens, it's possible to see the execution of script to upload the full DBB-dataset. In particular, if the loading is blocked, then by running the script, it restarts from the last point.
![Foto da Matteo](https://user-images.githubusercontent.com/78934727/167823403-ec77d76e-bf4d-4d18-b986-a93521401a73.jpg)
![Foto da Matteo (1)](https://user-images.githubusercontent.com/78934727/167823417-7715a0c7-fb8b-4408-a9eb-12e248564fd2.jpg)


## 3.Example App for Reproducibility PRE-PROCESSING STEP with Docker container

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

### There are two methods to execute apps:

-Execute app from GUI on the subjects present in BrainLife project.

![EXECUTE_APP_FROM_BL drawio](https://user-images.githubusercontent.com/78934727/143466171-5d521a14-38ac-436b-9bb8-caffe7fbd667.png)

-Execute app from CLI using app on all possible subjects.
 (only two details: install singularity and create a config.json file for path local file).
 
 ![USING_APP_FROM_CLI drawio](https://user-images.githubusercontent.com/78934727/143466188-8366266b-8ba6-4c31-85e0-ff6b0940689c.png)
 
 #### Why is the dual functionality of the DBB Preprocessing t1w app essential in the case of subjects with distorted brain anatomy?
 
 The reason is that the automatic reorientation performed by ANTs is efficient in the 
 case of subjects with healthy brain anatomy. In the case of distorted subjects, 
 the automatic AC-PC alignment is not correct and it is necessary to apply the 
 affine.txt file (obtained manually) for a correct reorientation.
 
 This processed image of pathological subject obtained with automatic reorientation
 
![automatic reorie](https://user-images.githubusercontent.com/78934727/143769496-3ac8c650-001e-41a3-894b-de54803a799d.png)

This processed image of pathological subject obtained applying affine trasformation file

![apply_reorient](https://user-images.githubusercontent.com/78934727/143769381-a54af32d-4826-4096-a4ad-ef1b69365a8c.png)

The reference template is MNI_152_T1W_brain.nii.gz

![TEMPLATE](https://user-images.githubusercontent.com/78934727/143769760-eacbd0c4-9856-49a3-8d00-74fc105b1f4f.png)


## 4.Example script for Comparison Segmentation Masks

This folder contains an example of script for calculate Dice Score between predicted mask and ground truth of each label.
The goal is to try to reproduce the comparison step through Dice Score between ground truth masks and predicted masks 
through the 3D-U-Net convolutional neural network

![dice](https://user-images.githubusercontent.com/78934727/142238239-fa45584b-ced7-491a-a67b-46532628066b.png)


#### How does the Dice Score metric work?

Let's take two examples:

- first SUBJECT ACC (DOWN) with ground truth segmentation mask and 3D-U-Net mask segmentation
- second SUBJECT HD (UP) ground truth segmentation mask and 3D-U-Net mask segmentation

![Dicedrawio](https://user-images.githubusercontent.com/78934727/142252594-4a9b2c6f-acd2-4363-a799-03c51f6b47bf.png)





