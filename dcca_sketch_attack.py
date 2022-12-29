#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''dcca attack based on Minemura 2016
and scrambling DCs by assigning random number from (-2048, 2047)(inclusive)'''

import cv2
import random
import numpy as np


# In[2]:


random.seed(0)


# In[3]:


def dcca_attack(image_name):

    img_file = image_name + '.tif'
    intensities = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    height = np.shape(intensities)[0]
    width = np.shape(intensities)[1]
    imf = np.float32(intensities)
    fsketch_intensities = np.zeros([height,width])
    
    for i in range(0,1):
        for j in range(0,1):
            blk = imf[8*i:8*(i+1), 8*j:8*(j+1)]
            shifted_blk = blk - 128 #level_shift for dct
            dct = cv2.dct(shifted_blk)
            nq_coef = np.round(dct)
            nq_coef_ac = np.delete(nq_coef, [0,0])
            nq_coef_dc = nq_coef[0,0]
        
    previous_dc = nq_coef_dc
    for i in range(0,int(height/8)):
        for j in range(0,int(width/8)):
            '''DC encryption'''
            enc_dc = random.randint(-1023, 1023)
            
            dc_difference = enc_dc - previous_dc
            previous_dc = enc_dc
            
            if dc_difference == 0:
                fsketch = 0
            else:
                fsketch_temp = np.floor(np.log2(abs(dc_difference)))
                fsketch = 2 ** fsketch_temp * 3
            
            fsketch_blk = fsketch * np.ones([8, 8])
            fsketch_intensities [8*i:8*(i+1), 8*j:8*(j+1)]= fsketch_blk

    fsketch_modified = fsketch_intensities.copy()
    fsketch_modified[fsketch_modified>255] = 255

    filename = 'dcca_attack_'+image_name+'.png'
    cv2.imwrite(filename, fsketch_modified)
    cv2.waitKey(1000)

    return fsketch_modified


# In[ ]:




