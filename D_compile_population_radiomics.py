# -*- coding: utf-8 -*-
"""
@author: Raluca Sandu
"""

import argparse
import os
import time

import pandas as pd

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--rootdir", required=True,
                    help="path to the patient folder with Radiomics XLSX to be processed")
    ap.add_argument("-b", "--input_batch_proc_paths", required=True, help="input XLSX file for batch processing")
    args = vars(ap.parse_args())

    if args["rootdir"] is not None:
        print("Path to folder with Radiomics Files for each patient and each lesion: ", args["rootdir"])
    if (args["input_batch_proc_paths"]) is not None:
        print("Path to Excel file that has (RedCap) lesion info: ", args["input_batch_proc_paths"])

    df_download_db_all_info = pd.read_excel(args["input_batch_proc_paths"])
    frames = []  # list to store all df per lesion.

    for subdir, dirs, files in os.walk(args["rootdir"]):
        for file in sorted(files):
            if file.endswith('.xlsx'):
                # check file extension is xlsx
                excel_input_file_per_lesion = os.path.join(subdir, file)
                df_single_lesion = pd.read_excel(excel_input_file_per_lesion)
                df_single_lesion.rename(columns={'lesion_id': 'Lesion_ID', 'patient_id': 'Patient_ID'}, inplace=True)
                # MAV - B01 - L1
                try:
                    patient_id = df_single_lesion.loc[0]['Patient_ID']
                except Exception as e:
                    print(repr(e))
                    print("Path to bad excel file:", excel_input_file_per_lesion)
                    continue
                try:
                    df_single_lesion['Lesion_ID'] = df_single_lesion['Lesion_ID'].apply(
                        lambda x: 'MAV-' + patient_id + '-L' + str(x))
                except Exception as e:
                    print(repr(e))
                    print("Path to bad excel file:", excel_input_file_per_lesion)
                    continue
                frames.append(df_single_lesion)
                # concatenate on patient_id and lesion_id
                # rename the columns
                # concatenate the rest of the pandas dataframe based on the lesion id.
                # first edit the lesion id.
#
# result = pd.concat(frames, axis=1, keys=['Patient ID', 'Lesion id', 'ablation_date'], ignore_index=True)
# df_final = result
# print(len(frames))
result = pd.concat(frames, ignore_index=True)
result_inner_ellipsoid = pd.DataFrame()
result_inner_ellipsoid['Patient_ID'] = result['Patient_ID']
result_inner_ellipsoid['Lesion_ID'] = result['Lesion_ID']
result_inner_ellipsoid['Inner Ellipsoid Volume'] = result['Inner Ellipsoid Volume']
df_final = pd.merge(df_download_db_all_info, result_inner_ellipsoid, how="left", on=['Patient_ID', 'Lesion_ID'])
timestr = time.strftime("%H%M%S-%Y%m%d")
filepath_excel = 'Radiomics_MAVERRIC----' + timestr + '_.xlsx'
writer = pd.ExcelWriter(filepath_excel)
df_final.to_excel(writer, sheet_name='radiomics', index=False, float_format='%.4f')
writer.save()
