#!/usr/bin/env python
# coding: utf-8

# In[16]:


import numpy as np
import cv2


# In[17]:


def swap_fellows_assigner(image, x, sH):
    img_file = image + '.tif'
    intensities = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    height = np.shape(intensities)[0]
    width = np.shape(intensities)[1]
    imf = np.float32(intensities)

    all_nq_ac = []
    for i in range(0,int(height/8)):
        for j in range(0,int(width/8)):
            blk = imf[8*i:8*(i+1), 8*j:8*(j+1)]
            shifted_blk = blk - 128 #level_shift for dct
            dct = cv2.dct(shifted_blk)
            nq_coef = np.round(dct)
            nq_coef_ac = np.delete(nq_coef, [0,0])

            all_nq_ac = np.append(all_nq_ac, nq_coef_ac)

    ac_values, ac_counts = np.unique(all_nq_ac, return_counts=True)

    pos_all_vals = []
    neg_all_vals_paired = []
    counts_all_pos = []
    counts_all_neg_paired = []

    ac_values_dic = {}
    ac_counts_dic = {}

    for i in range(1,11):
        neg_part = range(-(2**i-1), -2**(i-1)+1)
        pos_part = range(2**(i-1), 2**i)

        pos_all_vals = np.append(pos_all_vals, pos_part)
        neg_all_vals_paired = np.append(neg_all_vals_paired, neg_part)

        values_in_size = np.append(neg_part,pos_part)
        ac_values_dic[i] = values_in_size

        counts_in_size = np.zeros(np.size(values_in_size))
        for j in range(np.size(values_in_size)):
            if values_in_size[j] in ac_values:
                position_in_counts = np.where(
                    ac_values == values_in_size[j])
                counts_in_size[j] = ac_counts[position_in_counts]

        ac_counts_dic[i] = counts_in_size

        counts_in_size_pos = np.zeros(np.size(pos_part))
        for m in range(np.size(pos_part)):
            if pos_part[m] in ac_values:
                position_in_counts = np.where(
                    ac_values == pos_part[m])
                counts_in_size_pos[m] = ac_counts[position_in_counts]
        counts_all_pos = np.append(counts_all_pos, counts_in_size_pos)

        counts_in_size_neg = np.zeros(np.size(neg_part))
        for n in range(np.size(neg_part)):
            if neg_part[n] in ac_values:
                position_in_counts = np.where(
                    ac_values == neg_part[n])
                counts_in_size_neg[n] = ac_counts[position_in_counts]

        counts_all_neg_paired = np.append(counts_all_neg_paired, counts_in_size_neg)

    n0 = 0
    pos0 = np.where(ac_values == 0)
    ac_values_n0 = ac_values.copy()
    ac_counts_n0 = ac_counts.copy()
    ac_values_n0 = np.delete(ac_values_n0, pos0)
    ac_counts_n0 = np.delete(ac_counts_n0, pos0)

    counts_each_pair = counts_all_pos + counts_all_neg_paired



    zeq_theories = []
    # for x in [+1, +2, +3, +4]:
    #     print(x)
#     #     for sH in [8, 9, 10]:
#     x = +1
#     sH = 10

    sL = np.floor(np.log2(x))+1
    deltasL = 2**sL -1 + 2**(sL-1)
    indx = np.where(pos_all_vals == x)
    prbx = counts_all_pos [indx]/sum(ac_counts_n0)

    xbar = deltasL - x
    indxbar = np.where(pos_all_vals == xbar)
    prbxbar = counts_all_pos [indxbar]/sum(ac_counts_n0)


    deltasH = 2**sH - 1 + 2** (sH-1)

    '''find zeq #######################################################################''' 
    if x != 1:
        zeq_theory1 = deltasH * (prbx - np.sqrt(prbx * prbxbar))/(prbx-prbxbar)
        zeq_theory = np.floor(zeq_theory1)

    if x ==1:
        zeq_theory =  np.floor(deltasH/2)

    if zeq_theory > (2**sH-1):
        z = 2**sH-1
    else:
        z = zeq_theory

    zeq_theories = np.append(zeq_theories, zeq_theory)

    '''SWAPING ########################################################################'''
    x_bspair = x -(2**sL -1 + 2**(sL-1))
    new_pair = [x_bspair, z] # (x-dlta, z)

    msb0_elements = []
    msb1_elements = []

    p1 = new_pair[0]
    p2 = new_pair[1]

    ind_p1 = np.where(neg_all_vals_paired == p1)
    p1_bs_pair = pos_all_vals[ind_p1]

    p1_counts = counts_all_neg_paired[ind_p1]
    p1_bs_pair_counts = counts_all_pos [ind_p1]

    new_all_pos = np.delete(pos_all_vals, ind_p1)
    new_all_neg = np.delete(neg_all_vals_paired, ind_p1)

    new_counts_all_pos = np.delete(counts_all_pos, ind_p1)
    new_counts_all_neg_paired = np.delete(counts_all_neg_paired, ind_p1)

    new_counts_each_pair = np.delete(counts_each_pair, ind_p1)


    new_ind_p2 = np.where(new_all_pos == p2)
    p2_bs_pair = new_all_neg[new_ind_p2]

    ind_p2 = np.where(pos_all_vals == p2)    
    p2_counts = counts_all_pos[ind_p2]
    p2_bs_pair_counts = counts_all_neg_paired [ind_p2]


    new_pair_counts = p1_counts + p2_counts
    new_pair_pair_counts = p1_bs_pair_counts + p2_bs_pair_counts

    new_pair_pair = [p2_bs_pair, p1_bs_pair]

    newer_all_pos = np.delete(new_all_pos, new_ind_p2)
    newer_all_neg = np.delete(new_all_neg, new_ind_p2)
    newer_counts_all_pos = np.delete(new_counts_all_pos, new_ind_p2)
    newer_counts_all_neg_paired = np.delete(new_counts_all_neg_paired, new_ind_p2)

    newer_counts_each_pair = np.delete(new_counts_each_pair, new_ind_p2)


    # substitution
    for i in range(len(newer_counts_each_pair)):
        if new_pair_counts > newer_counts_each_pair[i]:
            break
    new_1st_fellows = np.insert(newer_all_neg, i, p1)
    new_1st_fellows_counts = np.insert(newer_counts_all_neg_paired, i, p1_counts)

    new_2nd_fellows = np.insert(newer_all_pos, i, p2)
    new_2nd_fellows_counts = np.insert(newer_counts_all_pos, i, p2_counts)

    new_pairs_counts = np.insert(newer_counts_each_pair, i, new_pair_counts)

    for i in range(len(new_pairs_counts)):
        if new_pair_pair_counts > new_pairs_counts[i]:
            break
    newer_1st_fellows = np.insert(new_1st_fellows, i, p2_bs_pair)
    newer_1st_fellows_counts = np.insert(new_1st_fellows_counts, i, p2_bs_pair_counts)

    newer_2nd_fellows = np.insert(new_2nd_fellows, i, p1_bs_pair)
    newer_2nd_fellows_counts = np.insert(new_2nd_fellows_counts, i, p1_bs_pair_counts)

    newer_pairs_counts = np.insert(new_pairs_counts, i, new_pair_pair_counts)


    msb0_fellows = newer_1st_fellows
    msb1_fellows = newer_2nd_fellows
    
    return msb0_fellows, msb1_fellows


# In[ ]:




