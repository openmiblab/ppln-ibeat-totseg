import os
import logging

# import stage_0_restore
# import stage_1_segment
# import stage_2_display
import stage_3_measure
import stage_4_edit
# import stage_5_measure
# import stage_6_archive


LOCALPATH = r"C:\Users\md1spsx\Documents\Data\iBEAt_Build"
SHAREDPATH = os.path.join("G:\\Shared drives", "iBEAt_Build")
os.makedirs(LOCALPATH, exist_ok=True)


# Set up logging
logging.basicConfig(
    filename=os.path.join(LOCALPATH, 'error.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# def restore():
    
#     stage_0_restore.segmentations(SHAREDPATH, LOCALPATH, 'Controls')
#     for site in ['Bari', 'Bordeaux', 'Exeter', 'Leeds', 'Sheffield', 'Turku']:
#         stage_0_restore.segmentations(SHAREDPATH, LOCALPATH, 'Patients', site)

def measure():

    group = 'Controls'
    stage_3_measure.organs(LOCALPATH, group, task='total_mr')
    stage_3_measure.organs(LOCALPATH, group, task='tissue_types_mr')

    sites = ['Bari', 'Bordeaux', 'Exeter', 'Leeds', 'Sheffield', 'Turku']
    group = 'Patients'
    for site in sites:
        stage_3_measure.organs(LOCALPATH, group, site, task='total_mr')
        stage_3_measure.organs(LOCALPATH, group, site, task='tissue_types_mr')
    
    stage_3_measure.concatenate(LOCALPATH)        


def run_totseg():

    group = 'Controls'
    #stage_0_restore.segmentations(SHAREDPATH, LOCALPATH, group)
    #stage_0_restore.dixons(SHAREDPATH, LOCALPATH, group)
    # stage_1_segment.segment(LOCALPATH, group, task='total_mr')
    # stage_2_display.mosaic(LOCALPATH, group, task='total_mr')
    # stage_2_display.mosaic(LOCALPATH, group, task='total_mr', organs='liver')
    #stage_3_measure.organs(LOCALPATH, group, task='total_mr')
    #stage_3_measure.organs(LOCALPATH, group, task='tissue_types_mr')
    #stage_3_measure.concatenate(LOCALPATH)
    stage_4_edit.organ_mask(LOCALPATH, group, task='total_mr', organ='pancreas')
    # stage_5_measure.edited_organ(LOCALPATH, group, task='total_mr', organ='pancreas')
    # stage_5_measure.concatenate(LOCALPATH)
    # stage_6_archive.autosegmentation(LOCALPATH, SHAREDPATH, group)
    # stage_6_archive.edited_segmentation(LOCALPATH, SHAREDPATH, group)
    # stage_6_archive.displays(LOCALPATH, SHAREDPATH, group)
    
    # sites = ['Bari', 'Bordeaux', 'Exeter', 'Leeds', 'Sheffield', 'Turku']
    group = 'Patients'
    site = 'Bordeaux'
    #stage_0_restore.segmentations(SHAREDPATH, LOCALPATH, group, site)
    #stage_0_restore.dixons(SHAREDPATH, LOCALPATH, group, site)
    # stage_1_segment.segment(LOCALPATH, group, site, task='total_mr')
    # stage_2_display.mosaic(LOCALPATH, group, site, task='total_mr')
    # stage_2_display.mosaic(LOCALPATH, group, site, task='total_mr', organs='liver')
    # stage_3_measure.all_organs(LOCALPATH, group, site, task='total_mr', organ='liver')
    # stage_3_measure.concatenate(LOCALPATH)
    # stage_4_edit.organ_mask(LOCALPATH, group, site, task='total_mr', organ='liver')
    # stage_5_measure.edited_organ(LOCALPATH, group, site, task='total_mr', organ='liver')
    # stage_5_measure.concatenate(LOCALPATH)        
    # stage_6_archive.autosegmentation(LOCALPATH, SHAREDPATH, group, site)
    # stage_6_archive.edited_segmentation(LOCALPATH, SHAREDPATH, group)
    # stage_6_archive.displays(LOCALPATH, SHAREDPATH, group, site)
        


if __name__ == '__main__':

    # restore()
    # measure()
    run_totseg()