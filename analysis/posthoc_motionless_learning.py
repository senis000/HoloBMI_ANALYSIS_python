import copy
import h5py
import pickle
import numpy as np
import pandas as pd
from scipy import signal, sparse, ndimage, spatial
from pathlib import Path
from PIL import Image

from utils.loader import SessionLoader
from analysis.analysis_constants import caiman_analysis_results_directory, caiman_full_directory, voltage_rec_filename, \
    caiman_analysis_file_path, motion_file_path, raw_folder, raw_files
from utils.general_constants import caiman_directory, raw_data_directory


def open_caiman_files(loader: SessionLoader):
    """ Function to open the hdf5 file with the results from caiman """
    # get the directories names
    caiman_dir = caiman_full_directory(caiman_directory(), loader.mice_name, loader.session_date, loader.day)
    analysis_file = caiman_analysis_file_path(caiman_analysis_results_directory(caiman_dir))
    # get the frames from online data
    voltage_file = voltage_rec_filename(caiman_dir)
    f = h5py.File(analysis_file, 'r')
    dims = np.asarray(f['dims'])
    estimates = f['estimates']
    strc_mask = loader.experiment_variables.dict_strc_mask()['strcMask']
    x_pos = strc_mask['xctr']
    y_pos = strc_mask['yctr']
    com_online = np.asarray([x_pos, y_pos]).transpose()
    online_data = loader.experiment_variables.dict_training()['data']['bmiAct']
    dff = np.asarray(estimates['F_dff'])
    A = estimates['A']
    b_aux = np.asarray(estimates['b'])
    cnn_pred = np.asarray(estimates['cnn_preds'])
    A_full = sparse.csc_matrix((A['data'][:], A['indices'][:], A['indptr'][:]), A['shape']).toarray()
    f.close()
    masks = np.asarray([np.reshape(np.array(A_full[:, i]), dims, order='F') for i in range(A_full.shape[1])])
    b = np.asarray([np.reshape(b_aux[:, i], dims, order='F') for i in range(b_aux.shape[1])])

    nerden = np.ones(A_full.shape[1]).astype('bool')
    nerden[np.where(cnn_pred < 0.65)] = False
    new_com = obtain_real_com(masks)

    finalneur, b_mod = detect_ensemble_neurons(dff, online_data, new_com, com_online, np.nansum(b, 0))


def motion_reconstruction(loader: SessionLoader, dims: np.array):
    """ function to reconstruct the video of motion correction given by caiman"""
    # open the files
    caiman_dir = caiman_full_directory(caiman_directory(), loader.mice_name, loader.session_date, loader.day)
    raw_dir = raw_folder(raw_data_directory(), loader.mice_name, loader.session_date, loader.day)
    motion_file = motion_file_path(caiman_analysis_results_directory(caiman_dir))
    # files to motion_correct
    list_raw_files = raw_files(raw_dir)
    # motion correct shifts
    motion_dict = pickle.load(open(motion_file, 'rb'))
    motion_shift = motion_dict['rigid']
    motion_corrected_video = np.full(([len(list_raw_files), dims[0], dims[1]]), -999, dtype=int)
    for ind, file in enumerate(list_raw_files):
        im = np.asarray(Image.open(raw_dir / file))
        if motion_shift[ind][0] > 0:
            x_im_min = 0
            x_im_max = np.int(dims[0] - motion_shift[ind][0])
            x_v_min = np.int(motion_shift[ind][0])
            x_v_max = dims[0]
        else:
            x_im_min = np.int(motion_shift[ind][0])
            x_im_max = dims[0]
            x_v_min = 0
            x_v_max = np.int(dims[0] + motion_shift[ind][0])
        if motion_shift[ind][1] > 0:
            y_im_min = 0
            y_im_max = np.int(dims[1] - motion_shift[ind][1])
            y_v_min = np.int(motion_shift[ind][1])
            y_v_max = dims[1]
        else:
            y_im_min = np.int(motion_shift[ind][1])
            y_im_max = dims[1]
            y_v_min = 0
            y_v_max = np.int(dims[1] + motion_shift[ind][1])
        motion_corrected_video[ind, x_v_min:x_v_max, y_v_min:y_v_max] = im[x_im_min:x_im_max, y_im_min:y_im_max]






def synchronize_frames(voltage_file: Path):
    voltage_rec = pd.read_csv(voltage_file)
    frames_bmi, _ = signal.find_peaks(voltage_rec[' Input 7'], 1, distance=20)
    frames_prairie, _ = signal.find_peaks(voltage_rec[' Input 3'], 1, distance=10)
    frames_im = frames_prairie[1::2]
    sync_time = voltage_rec['Time(ms)']
    indices_bmi = np.zeros(frames_bmi.shape, dtype=int)
    for ind, frame in enumerate(frames_bmi):
        indices_bmi[ind] = np.where(frames_im <= frame)[0][-1]


def obtain_real_com(masks, thres=0.1):
    """
    Function to obtain the "real" position of the neuron regarding the spatial filter
    masks(array): matrix with all the spatial components
    thres(int): tolerance to identify the soma of the spatial filter
    Returns
    new_com(array): matrix with new position of the neurons
    """
    # function to obtain the real values of com

    new_com = np.zeros((masks.shape[0], 2))
    for neur in np.arange(masks.shape[0]):
        center_mass = ndimage.measurements.center_of_mass(masks[neur, :, :] > thres)
        if np.nansum(center_mass) == 0:
            center_mass = ndimage.measurements.center_of_mass(masks[neur, :, :])
        new_com[neur, :] = [center_mass[0], center_mass[1]]
    return new_com


def detect_ensemble_neurons(dff: np.array, online_data: np.array, com: np.array, com_online: np.array, b: np.array,
                            aux_tol: int = 10, cor_min: float = 0.5, iterations: int = 40) -> np.array:
    """
    Function to identify the ensemble neurons across all components
    dff: Dff values of the components. given by caiman
    online_data: activity of the ensemble neurons registered on the online bmi experiment
    com: position of the neurons
    com_online: position of the ensemble neurons as given by the experiment
    b: background image
    aux_tol: max difference distance for ensemble neurons
    cor_min: minimum correlation between neuronal activity from caiman DFF and online recording
    returns
    final_neur: index of the ensemble neurons"""

    # initialize vars
    neurcor = np.full([online_data.shape[0], dff.shape[0]], np.nan)
    finalcorr = np.zeros(online_data.shape[0])
    finalneur = np.zeros(online_data.shape[0])
    finaldist = np.zeros(online_data.shape[0])

    for un in np.arange(online_data.shape[0]):
        print(['finding neuron: ' + str(un)])

        tol = copy.deepcopy(aux_tol)
        temp_cor_min = copy.deepcopy(cor_min)

        for n_pro in np.arange(dff.shape[0]):
            neurcor[un, n_pro] = np.corrcoef(online_data[n_pro, :], dff)

        auxneur = copy.deepcopy(neurcor)
        neurcor[neurcor < temp_cor_min] = np.nan

        # extract position from metadata

        not_good_enough = True
        aux_com_online = np.reshape(com_online[un, :], [1, 2])
        while not_good_enough:
            if np.nansum(neurcor[un, :]) != 0:
                if np.nansum(np.abs(neurcor[un, :])) > 0:
                    maxcor = np.nanmax(neurcor[un, :])
                    indx = np.where(neurcor[un, :] == maxcor)[0][0]
                    aux_com = np.reshape(com[indx, :], [1, 2])
                    dist = spatial.distance.cdist(aux_com_online, aux_com)[0][0]
                    not_good_enough = dist > tol

                    finalcorr[un] = neurcor[un, indx]
                    finalneur[un] = indx
                    finaldist[un] = dist
                    neurcor[un, indx] = np.nan
                else:
                    print('Error couldnt find neuron' + str(un) + ' with this tolerance. Increasing tolerance')
                    if iterations > 0:
                        neurcor = auxneur
                        tol *= 1.1
                        iterations -= 1
                    else:
                        print('wtf??')
            #                         break
            elif temp_cor_min > 0:
                print('Error couldnt find neuron' + str(un) + ' reducing minimum correlation')
                neurcor = auxneur
                temp_cor_min -= 0.1
                neurcor[neurcor < temp_cor_min] = np.nan
                tol -= 2  # If reduced correlation reduce distance
                not_good_enough = True
            else:
                print('No luck, finding neurons by distance')
                auxcom = com
                dist = spatial.distance.cdist(aux_com_online, auxcom)[0]
                indx = np.where(dist == np.nanmin(dist))[0][0]
                finalcorr[un] = np.nan
                if np.nanmin(dist) < aux_tol:
                    finaldist[un] = np.nanmin(dist)
                    finalneur[un] = indx
                else:
                    print('where are my neurons??')
                    finalneur[un] = np.nan
                    finaldist[un] = np.nan
                not_good_enough = False
        print('tol value at: ', str(tol), 'correlation thres at: ', str(temp_cor_min))
        print('Correlated with value: ', str(finalcorr[un]), ' with a distance: ', str(finaldist[un]))

        if ~np.isnan(finalneur[un]):
            auxp = com[finalneur[un].astype(int)].astype(int)
            b[auxp[1], auxp[0]] = 0.01  # to detect
            b[com_online[un, 0], com_online[un, 1]] = 0.01  # to detect

    return finalneur, b
