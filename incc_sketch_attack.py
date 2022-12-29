#!/usr/bin/env python
# coding: utf-8

# In[10]:


import cv2
import random
import numpy as np


# In[11]:


random.seed(0)


# In[13]:


def incc_attack(image_name):
    img_file = image_name + '.tif'
    intensities = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    height = np.shape(intensities)[0]
    width = np.shape(intensities)[1]
    imf = np.float32(intensities)

    fi_intensities = np.zeros([height,width])
    nonzero_ac_nums = []
    for i in range(0,int(height/8)):
        for j in range(0,int(width/8)):
            blk = imf[8*i:8*(i+1), 8*j:8*(j+1)]
            shifted_blk = blk - 128 #level_shift for dct
            dct = cv2.dct(shifted_blk)
            nq_coef = np.round(dct)
            nq_coef_ac = np.delete(nq_coef, [0,0])
            nq_coef_dc = nq_coef[0,0]

            nonzero_ac_num = np.count_nonzero(nq_coef_ac)
            nonzero_ac_nums = np.append(nonzero_ac_nums, nonzero_ac_num)

    max_nonzero_ac_num = max(nonzero_ac_nums)
    k = 0
    for i in range(0,int(height/8)):
        for j in range(0,int(width/8)):        
            fi = np.floor(255*nonzero_ac_nums[k]/max_nonzero_ac_num)
            k += 1

            fi_blk = fi * np.ones([8, 8])
            fi_intensities [8*i:8*(i+1), 8*j:8*(j+1)] = fi_blk

    filename = 'incc_attack_'+image_name+'.png'
    cv2.imwrite(filename, fi_intensities)
    cv2.waitKey(1000)
    return fi_intensities


# In[4]:





# In[ ]:




