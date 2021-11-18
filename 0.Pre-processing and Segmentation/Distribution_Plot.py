#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 10:54:50 2021

@author: matteo99
"""

#%% Libraries

import numpy as np
import cv2
import matplotlib.pyplot as plt
import seaborn as sns

#%% Path

path = '/home/matteo99/Scrivania/immagini_tesi/path_for_distribution/plot/'
img0 = cv2.imread(path+"brain_healthy_preview_GIUSTA.png")
img2 = cv2.imread(path+"sub2-dist-minor-crop.png")
img3 = cv2.imread(path+"sub1-dist-minor-crop.png")
img = cv2.imread(path+"brain_malformed_preview_GIUSTA.png")

#%% Main

## SUBJECT HEALTHY
# plot distribution intensity with 255 bins
sns.set(rc={'figure.figsize':(15,10)})
g = sns.distplot(img0, bins=42)
g.set(xlim=(0, 230))
g.set(ylim=(0,0.010))
g.set(xlabel='Intensity')
#plt.savefig("distribution_intensity_healthy.png")
#plt.show()

## SUBJECT DISTORTED
# plot distribution intensity with 255 bins
sns.set(rc={'figure.figsize':(15,10)})
g2 = sns.distplot(img2,bins=42)
g2.set(xlim=(0, 230))
g2.set(ylim=(0,0.010))
g2.set(xlabel='Intensity')
#plt.savefig("distribution_intensity_distorted_minor-sub2.png")
#plt.show()

## SUBJECT DISTORTED
# plot distribution intensity with 255 bins
sns.set(rc={'figure.figsize':(15,10)})
g3 = sns.distplot(img3,bins=42)
g3.set(xlim=(0, 230))
g3.set(ylim=(0,0.010))
g3.set(xlabel='Intensity')
#plt.savefig("distribution_intensity_distorted_minor-sub1.png")
#plt.show()

## SUBJECT HIGH DISTORTED
# plot distribution intensity with 255 bins
sns.set(rc={'figure.figsize':(15,10)})
g1 = sns.distplot(img,bins=42)
g1.set(xlim=(0, 230))
g1.set(ylim=(0,0.020))
g1.set(xlabel='Intensity')
#plt.savefig("distribution_intensity_distorted.png")
#plt.show()
plt.legend(title='Subjects', loc='upper right', labels=['HEALTHY CASE', 'DISTORTED CASE','HIGH DISTORTED CASE'])


#%% Clustering python
'''
## SUBJECT HEALTHY
#Convert MxNx3 image into Kx3 where K=MxN
img3 = img0.reshape((-1,3))  #-1 reshape means, in this case MxN

#We convert the unit8 values to float as it is a requirement of the k-means method of OpenCV
img3 = np.float32(img3)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

# Number of clusters
k = 5
attempts = 10
ret,label,center=cv2.kmeans(img3, k, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
center = np.uint8(center) 

#Next, we have to access the labels to regenerate the clustered image
res = center[label.flatten()]
res3 = res.reshape((img0.shape)) #Reshape labels to the size of original image
cv2.imwrite("images/segmented.jpg", res3)

#Now let us visualize the output result
figure_size = 15
plt.figure(figsize=(figure_size,figure_size))
plt.subplot(1,2,1),plt.imshow(img0)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(1,2,2),plt.imshow(res3)
plt.title('Segmented Image when K = %i' % k), plt.xticks([]), plt.yticks([])
plt.show()


## SUBJECT DISTORTED
#Convert MxNx3 image into Kx3 where K=MxN
img2 = img.reshape((-1,3))  #-1 reshape means, in this case MxN

#We convert the unit8 values to float as it is a requirement of the k-means method of OpenCV
img2 = np.float32(img2)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

# Number of clusters
k = 4
attempts = 10
ret,label,center=cv2.kmeans(img2, k, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
center = np.uint8(center) 

#Next, we have to access the labels to regenerate the clustered image
res = center[label.flatten()]
res2 = res.reshape((img.shape)) #Reshape labels to the size of original image

#Now let us visualize the output result
figure_size = 15
plt.figure(figsize=(figure_size,figure_size))
plt.subplot(1,2,1),plt.imshow(img)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(1,2,2),plt.imshow(res2)
plt.title('Segmented Image when K = %i' % k), plt.xticks([]), plt.yticks([])
plt.show()
'''














