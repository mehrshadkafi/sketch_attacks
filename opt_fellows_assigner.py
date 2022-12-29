#!/usr/bin/env python
# coding: utf-8

# In[54]:


import numpy as np


# In[55]:


def opt_fellows_assigner(Lambda):
#     Lambda = 149847 # Lena threshold
    pairs_show_file_name = 'pulp_pairs_'+str(Lambda)+'.npy'
    mip_pairs_show = np.load(pairs_show_file_name)
    pairs_show = np.transpose(mip_pairs_show)
    # Better MSB 0 and 1 assignment ##################################### 
    abs_pairs_show = abs(pairs_show)
    pair_diff = abs(abs_pairs_show [:,0] - abs_pairs_show [:,1])
    pair_diff = pair_diff[..., None]
    pairs_diff = np.append(pairs_show, pair_diff, axis = 1)
    pairs_diff_sort = pairs_diff[pairs_diff[:,2].argsort()[::-1]]

    msb0_fellows = []
    msb1_fellows = []
    for i in range(0, len(pairs_diff_sort)):
        msb0_fellow = pairs_diff_sort[i][i%2]
        msb1_fellow = pairs_diff_sort[i][(i+1)%2]
        msb0_fellows.append(msb0_fellow)
        msb1_fellows.append(msb1_fellow)
        
    return msb0_fellows, msb1_fellows

