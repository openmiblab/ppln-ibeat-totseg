import os
import logging
import shutil
from pathlib import Path
import time
import argparse

from tqdm import tqdm
import numpy as np
import pandas as pd
import dbdicom as db
import vreg
import pydmr
import dask

from utils import radiomics
from utils.total_segmentator_class_maps import class_map



def concatenate(measurepath):

    for group in ['Controls', 'Patients']:
        folder = os.path.join(measurepath, group) 
        folder = Path(folder)
        dmr_files = list(folder.rglob("*.dmr.zip"))  # change the pattern
        if dmr_files == []:
            continue
        dmr_files = [str(f) for f in dmr_files]
        dmr_file = os.path.join(measurepath, f'{group}_totseg_auto.dmr.zip')
        if os.path.exists(dmr_file):
            continue
        pydmr.concat(dmr_files, dmr_file)

        # Create some derived formats for convenience

        # 1. Long format with additional columns (units, type, description)
        long_format_file = os.path.join(measurepath, f'{group}_totseg_auto_long.csv')
        pydmr.pars_to_long(dmr_file, long_format_file)

        # 2. Wide format
        wide_format_file = os.path.join(measurepath, f'{group}_totseg_auto_wide.csv')
        pydmr.pars_to_wide(dmr_file, wide_format_file)
        


def measure_image(automask, sitemeasurepath, task, organ):

    patient, study, series = automask[1], automask[2][0], automask[3][0]

    # Skip if not the requested task
    if task != series:
        return

    # If the results already exist, skip
    dmr_file = os.path.join(sitemeasurepath, f'{patient}_{study}_{series}')
    if os.path.exists(f'{dmr_file}.dmr.zip'):
        return
    
    print(f'Measuring {patient}_{study}_{series}')

    # Get mask volume 
    vol = db.volume(automask, verbose=0)

    # Init results
    dmr = {'data':{}, 'pars':{}}
    
    # Loop over the classes
    for idx, roi in class_map[task].items():

        # Skip if not the requested organ
        if organ is not None:
            if organ != roi:
                continue

        # Binary mask
        mask = (vol.values==idx).astype(np.float32)
        if np.sum(mask) == 0:
            continue

        roi_vol = vreg.volume(mask, vol.affine)
        
        # Get skimage features
        try:
            results = radiomics.volume_features(roi_vol, roi)
        except Exception as e:
            logging.error(f"Patient {patient} {roi} - error computing ski-shapes: {e}")
        else:
            dmr['data'] = dmr['data'] | {p: v[1:] for p, v in results.items()}
            dmr['pars'] = dmr['pars'] | {(patient, study, p): v[0] for p, v in results.items()}

        # # Get radiomics shape features
        # # Take out for now because of installation issues
        # try:
        #     t = time.time()
        #     results = radiomics.shape_features(roi_vol, roi)
        #     print('pyrad time', time.time() - t)
        # except Exception as e:
        #     logging.error(f"Patient {patient} {roi} - error computing radiomics-shapes: {e}")
        # else:
        #     dmr['data'] = dmr['data'] | {p:v[1:] for p, v in results.items()}
        #     dmr['pars'] = dmr['pars'] | {(patient, study, p): v[0] for p, v in results.items()}

        # Get numpyradiomics shape features
        try:
            results = radiomics.shape_features_nprad(roi_vol, roi)
        except Exception as e:
            logging.error(f"Patient {patient} {roi} - error computing radiomics-shapes: {e}")
        else:
            dmr['data'] = dmr['data'] | {p:v[1:] for p, v in results.items()}
            dmr['pars'] = dmr['pars'] | {(patient, study, p): v[0] for p, v in results.items()}

    # Append parsed biomarkers in the dictionary for convenience
    dmr['columns'] = ['body_part', 'biomarker_category', 'biomarker']
    for p in dmr['data']:
        dmr['data'][p] += p.split('-')

    # Write results to file
    pydmr.write(dmr_file, dmr)


def measure_task(automaskpath, measurepath, group, site=None, task=None, organ=None):

    os.makedirs(measurepath, exist_ok=True)
    if group == 'Controls':
        siteautomaskpath = os.path.join(automaskpath, "Controls")
        sitemeasurepath = os.path.join(measurepath, "Controls")         
    else:
        siteautomaskpath = os.path.join(automaskpath, "Patients", site)
        sitemeasurepath = os.path.join(measurepath, "Patients", site)
    os.makedirs(sitemeasurepath, exist_ok=True)

    automasks = db.series(siteautomaskpath)
    tasks = [dask.delayed(measure_image)(mask, sitemeasurepath, task, organ) for mask in automasks]
    dask.compute(*tasks)



def measure(data, build):

    os.makedirs(build, exist_ok=True)

    group = 'Controls'
    measure_task(data, build, group, task='total_mr')
    measure_task(data, build, group, task='tissue_types_mr')

    sites = ['Bari', 'Bordeaux', 'Exeter', 'Leeds', 'Sheffield', 'Turku']
    group = 'Patients'
    for site in sites:
        measure_task(data, build, group, site, task='total_mr')
        measure_task(data, build, group, site, task='tissue_types_mr')
    
    concatenate(build)        


if __name__ == '__main__':

    PROJ_DIR=r"C:\Users\md1spsx\Documents\Data\iBEAt_Build\totseg"
    DATA_DIR=os.path.join(PROJ_DIR, "stage_1_segment")
    BUILD_DIR=os.path.join(PROJ_DIR, "stage_3_measure")

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default=DATA_DIR, help="Data folder")
    parser.add_argument("--build", type=str, default=BUILD_DIR, help="Build folder")
    args = parser.parse_args()

    measure(args.data, args.build)