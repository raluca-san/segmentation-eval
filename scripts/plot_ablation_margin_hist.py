# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:15:51 2017

@author: Raluca Sandu
"""
import os
from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
matplotlib.use('Agg')

np.seterr(divide='ignore', invalid='ignore')


# %%


def plot_histogram_surface_distances(pat_name, lesion_id, rootdir, distance_map, num_voxels, title, ablation_date,
                                     flag_to_plot=True):

    cmap = sns.color_palette("colorblind")  # colorblind friendly palette
    fontsize = 20
    try:
            lesion_id_str = str(lesion_id)
            lesion_id = lesion_id_str.split('.')[0]
    except Exception:
        pass
        # lesion id is either not a string, nor it contains numerical characters. do nothing
    min_val = int(np.floor(min(distance_map)))
    max_val = int(np.ceil(max(distance_map)))
    fig, ax = plt.subplots(figsize=(12, 10))

    col_height, bins, patches = ax.hist(distance_map, ec='black', bins=range(min_val - 1, max_val + 1))

    voxels_nonablated = []
    voxels_insuffablated = []
    voxels_ablated = []

    for b, p, col_val in zip(bins, patches, col_height):
        if b < 0:
            voxels_nonablated.append(col_val)
        elif 0 <= b < 5:
            voxels_insuffablated.append(col_val)
        elif b >= 5:
            voxels_ablated.append(col_val)
    # %%
    '''calculate the total percentage of surface for ablated, non-ablated, insufficiently ablated'''

    voxels_nonablated = np.asarray(voxels_nonablated)
    voxels_insuffablated = np.asarray(voxels_insuffablated)
    voxels_ablated = np.asarray(voxels_ablated)

    sum_perc_nonablated = ((voxels_nonablated / num_voxels) * 100).sum()
    sum_perc_insuffablated = ((voxels_insuffablated / num_voxels) * 100).sum()
    sum_perc_ablated = ((voxels_ablated / num_voxels) * 100).sum()
    # %%

    if flag_to_plot is True:
        '''iterate through the bins to change the colors of the patches bases on the range [mm]'''
        for b, p, col_val in zip(bins, patches, col_height):
            if b < 0:
                plt.setp(p, 'facecolor', cmap[3],
                         label='Ablation Margin ' + r'$x < 0$' + 'mm :' + " %.2f" % sum_perc_nonablated + '%')
            elif 0 <= b < 5:
                plt.setp(p, 'facecolor', cmap[8],
                         label='Ablation Margin ' + r'$0 \leq x < 5$' + 'mm: ' + "%.2f" % sum_perc_insuffablated + '%')
            elif b >= 5:  # fixed color in histogram
                plt.setp(p, 'facecolor', cmap[2],
                         label='Ablation Margin ' + r'$x \geq 5$' + 'mm: ' + " %.2f" % sum_perc_ablated + '%')
        # %%
        '''edit the axes limits and labels'''
        # csfont = {'fontname': 'Times New Roman'}
        plt.xlabel('Surface-to-Surface Euclidean Distances (mm)', fontsize=fontsize, color='black')
        plt.tick_params(labelsize=fontsize, color='black')
        ax.tick_params(colors='black', labelsize=fontsize)
        ax.set_xlim([-15, 15])

        # edit the y-ticks: change to percentage of surface
        yticks, locs = plt.yticks()
        percent = (yticks / num_voxels) * 100
        percentage_surface_rounded = np.round(percent)
        yticks_percent = [str(x) + '%' for x in percentage_surface_rounded]
        new_yticks = (percentage_surface_rounded * yticks) / percent
        new_yticks[0] = 0
        plt.yticks(new_yticks, yticks_percent)

        plt.ylabel('Tumor surface covered (%)', fontsize=fontsize, color='black')

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        # font = font_manager.FontProperties(family='Times New Roman',
        #                                    style='normal', size=30)
        # plt.legend(by_label.values(), by_label.keys(), fontsize=30, loc='best', prop=font)
        # ax.legend(prop=font)
        plt.legend(by_label.values(), by_label.keys(), fontsize=fontsize, loc='best')
        plt.xticks(fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=fontsize)
        ax.grid(False)
        #%% save the fig to disk as png and eps
        figName_hist = 'Pat_' + str(pat_name) + '_Lesion' + str(
            lesion_id) + '_AblationDate_' + ablation_date + '_histogram'
        plt.title(title + '. Patient ' + str(pat_name) + '. Lesion ' + str(lesion_id), fontsize=fontsize)
        figpathHist = os.path.join(rootdir, figName_hist)
        ax.set_rasterized(True)

        plt.savefig(figpathHist, dpi=600, bbox_inches='tight')
        plt.savefig(figpathHist + '.eps', dpi=600)
        plt.savefig(figpathHist + '.svg', dpi=600)
        plt.savefig(figpathHist + '.pdf', dpi=600)

        plt.close()
        return sum_perc_nonablated, sum_perc_insuffablated, sum_perc_ablated
    else:
        # return the percentages of tumor surface covered
        return sum_perc_nonablated, sum_perc_insuffablated, sum_perc_ablated
