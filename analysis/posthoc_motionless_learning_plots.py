from pathlib import Path

import numpy as np

from utils import utils_plots as ut_plots


def plot_masks(folder_path: Path, masks: np.array, new_com: np.array, nerden, rad_neur: int = 20, thres: float = 0.1):
    """ Function to plot the masks after cleaning """
    for neur in np.arange(masks.shape[0]):
        if (new_com[0] + rad_neur) > masks.shape[1]:
            x2 = masks.shape[1]
        else:
            x2 = int(new_com[0] + rad_neur)
        if (new_com[0] - rad_neur) < 0:
            x1 = 0
        else:
            x1 = int(new_com[0] - rad_neur)
        if (new_com[1] + rad_neur) > masks.shape[2]:
            y2 = masks.shape[2]
        else:
            y2 = int(new_com[1] + rad_neur)
        if (new_com[1] - rad_neur) < 0:
            y1 = 0
        else:
            y1 = int(new_com[1] - rad_neur)
        img = masks[x1:x2, y1:y2, neur]
        fig, ax, bx = ut_plots.open_2subplots()
        ax.imshow(np.transpose(img))
        ax.set_xlabel('nd: ' + str(nerden[neur]))
        bx.imshow(np.transpose(img > thres))
        bx.set_xlabel('neuron: ' + str(neur))
        ut_plots.save_plot(fig, folder_path=folder_path, var_y='masks_', var_x=str(neur), set_labels=False)


def plot_ensemble_pos(folder_path: Path, b: np.array, com_online: np.array, new_com: np.array, masks: np.array):
    fig, ax, bx = ut_plots.open_2subplots()
    online_mask = np.zeros(b.shape[1:])
    offline_mask = np.zeros(b.shape[1:])
    for neur in np.arange(com_online.shape[0]):
        online_mask[com_online[neur, 1], com_online[neur, 0]] = 1
    for neur in np.arange(new_com.shape[0]):
        offline_mask[new_com[neur, 0].astype(int), new_com[neur, 1].astype(int)] = 1
    ax.imshow(np.stack((online_mask, offline_mask, np.nansum(b, 0))/np.nanmax(b)*2, 2))
    bx.imshow(np.stack((online_mask, offline_mask, np.nansum(masks, 0))/np.nanmax(masks)*2, 2))

    plt.savefig(fanal + 'ens_masks.png', bbox_inches="tight")

    fig1 = plt.figure(figsize=(16, 6))
    for un in np.arange(dff.shape[0]):
        ax = fig1.add_subplot(dff.shape[0], 1, un + 1)
        ens = (online_data.keys())[2 + un]
        frames = (np.asarray(online_data['frameNumber']) / number_planes_total).astype('int') + len_base
        auxonline = (np.asarray(online_data[ens]) - np.nanmean(online_data[ens])) / np.nanmean(online_data[ens])
        auxonline[np.isnan(auxonline)] = 0
        ax.plot(zscore(auxonline[-5000:]))
        if ~np.isnan(finalneur[un]):
            auxdd = dff[finalneur[un].astype('int'), frames]
            ax.plot(zscore(auxdd[-5000:]))

    plt.savefig(fanal + 'ens_online_offline.png', bbox_inches="tight")