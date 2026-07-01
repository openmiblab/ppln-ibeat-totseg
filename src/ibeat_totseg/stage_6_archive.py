import os
import logging

import dbdicom as db

from utils.files import copy_new_files


def edited_segmentation(local_path, shared_path, group, site=None):
    datapath = os.path.join(local_path, 'totseg', 'stage_4_edit')
    archivepath = os.path.join(shared_path, 'totseg', 'stage_4_edit')
    if group == 'Controls':
        sitedatapath = os.path.join(datapath, "Controls") 
        sitearchivepath = os.path.join(archivepath, 'Controls')
    else:
        sitedatapath = os.path.join(datapath, "Patients", site) 
        sitearchivepath = os.path.join(archivepath, "Patients", site)
    db.archive(sitedatapath, sitearchivepath)


def autosegmentation(local_path, shared_path, group, site=None):
    datapath = os.path.join(local_path, 'totseg', 'stage_1_segment')
    archivepath = os.path.join(shared_path, 'totseg', 'stage_1_segment')
    if group == 'Controls':
        sitedatapath = os.path.join(datapath, "Controls") 
        sitearchivepath = os.path.join(archivepath, 'Controls')
    else:
        sitedatapath = os.path.join(datapath, "Patients", site) 
        sitearchivepath = os.path.join(archivepath, "Patients", site)
    db.archive(sitedatapath, sitearchivepath)


def displays(local_path, shared_path, group, site=None):
    datapath = os.path.join(local_path, 'totseg', 'stage_2_display')
    archivepath = os.path.join(shared_path, 'totseg', 'stage_2_display')
    if group == 'Controls':
        sitedatapath = os.path.join(datapath, "Controls") 
        sitearchivepath = os.path.join(archivepath, 'Controls')
    else:
        sitedatapath = os.path.join(datapath, "Patients", site) 
        sitearchivepath = os.path.join(archivepath, "Patients", site)
    copy_new_files(sitedatapath, sitearchivepath)
    

if __name__=='__main__':

    LOCALPATH = r"C:\Users\md1spsx\Documents\Data\iBEAt_Build"
    SHAREDPATH = r"G:\\Shared drives\iBEAt_Build"
    os.makedirs(LOCALPATH, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(LOCALPATH, 'error.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    autosegmentation(LOCALPATH, SHAREDPATH, 'Controls')
    # autosegmentation(LOCALPATH, SHAREDPATH, 'Patients', site='Sheffield')