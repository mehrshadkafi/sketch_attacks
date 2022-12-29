#!/usr/bin/env python
# coding: utf-8

# In[35]:


import cv2
import random
import numpy as np


# In[36]:


random.seed(0)


# In[37]:


def eac_attack(image_name, msb0_fellows, msb1_fellows):
    img_file = image_name + '.tif'
    intensities = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    height = np.shape(intensities)[0]
    width = np.shape(intensities)[1]
    imf = np.float32(intensities)

    e_prime_ijs = []
    for i in range(0,int(height/8)):
        for j in range(0,int(width/8)):
            blk = imf[8*i:8*(i+1), 8*j:8*(j+1)]
            shifted_blk = blk - 128 #level_shift for dct
            dct = cv2.dct(shifted_blk)
            nq_coef = np.round(dct)
            nq_coef_ac = np.delete(nq_coef, [0,0])
            nq_coef_dc = nq_coef[0,0]

            '''ACs msb encryption'''
            enc_ac = nq_coef_ac.copy()
            for m in range(np.size(nq_coef_ac)):
                if nq_coef_ac[m] != 0:
                    if random.randint(0,1): # set msb to 1
                        if nq_coef_ac[m] in msb1_fellows:
                            enc_ac[m] = nq_coef_ac[m]
                        if nq_coef_ac[m] in msb0_fellows:
                            ind = np.where(msb0_fellows == nq_coef_ac[m])[0][0]
                            enc_ac[m] = msb1_fellows[ind]
                    else: # set msb to 0
                        if nq_coef_ac[m] in msb0_fellows:
                            enc_ac[m] = nq_coef_ac[m]
                        if nq_coef_ac[m] in msb1_fellows:
                            ind = np.where(msb1_fellows == nq_coef_ac[m])[0][0]
                            enc_ac[m] = msb0_fellows[ind]

            e_prime_ij = sum(abs(enc_ac))
            e_prime_ijs = np.append(e_prime_ijs, e_prime_ij)

    e_prime_avg = sum(e_prime_ijs)/(height * width)

    fe_intensities = np.zeros([height,width])
    k = 0
    for i in range(0,int(height/8)):
        for j in range(0,int(width/8)):        
            fe = np.floor(e_prime_ijs[k]/e_prime_avg)
            k += 1

            fe_blk = fe * np.ones([8, 8])
            fe_intensities [8*i:8*(i+1), 8*j:8*(j+1)] = fe_blk

    fe_intensities_modified = fe_intensities.copy()
    fe_intensities_modified[fe_intensities_modified>255] = 255
    filename = 'eac_attack_'+image_name+'.png'
    cv2.imwrite(filename, fe_intensities_modified)
    cv2.waitKey(1000)
    return fe_intensities


# In[ ]:




