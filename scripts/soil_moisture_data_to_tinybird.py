import h5py
import requests
import pandas as pd

import json
import subprocess

import os
from dotenv import load_dotenv
load_dotenv()

UID = os.getenv('UID', None)
PASSWORD = os.getenv('PASSWORD', None)
TOKEN = os.getenv('TOKEN', None)

def runcmd(cmd, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    pass

def process_data(data, data_date, am_or_pm):
    
    # prepare the data we want to send to tinybird
    df=pd.DataFrame(data)

    # storing positive integers takes less space
    df=df.replace(-9999.000000, 0)
    df=df * 1000000
    df=df.astype('int')

    # column values as an array
    df['columns'] = [[] for _ in range(len(df))] 
    for i in range(len(df)):
        df.at[i,'columns']=df.iloc[i].to_list()[:-1]
        
    df['date'] = data_date
    df['am_0_pm_1'] = am_or_pm
    df.reset_index(inplace=True)
    df.rename(columns={'index':'row'}, inplace=True)
    df[['date','am_0_pm_1','row','columns']].to_json('soil_moisture.json', orient="records", lines=True)   

    # build an ndjson batch
    with open("soil_moisture.json") as file:
        batch = []
        for record in file.readlines():
            batch.append(record)
        data = "\n".join(batch)
        file.close()

    # post the batch into tinybird
    r = requests.post(
        'https://api.tinybird.co/v0/events',
        params={
            'name': 'soil_moisture',
            'token': {TOKEN},
        },
        data=data
    ) 
    return r, data_date, am_or_pm

def main():
  for day in range(6,27):

    url_start = "https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP.008/2022.10."
    url_end = "_R18290_001.h5"
    fn = url_start+("0"+str(day))[-2:]+"/SMAP_L3_SM_P_202210"+("0"+str(day))[-2:]+url_end
    
    wget_call = 'wget --http-user='+UID+' --http-password='+PASSWORD+' --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off '+fn
    runcmd(wget_call)
    
    filename = fn[8:]
    data_date = filename[-22:-14]
    f = h5py.File(filename, "r")

    group = f['Soil_Moisture_Retrieval_Data_AM']
    data_am = group['soil_moisture'][()]
    print('events api ', process_data(data_am, data_date, 0))

    group = f['Soil_Moisture_Retrieval_Data_PM']
    data_pm = group['soil_moisture_pm'][()]
    print('events api ', process_data(data_pm, data_date, 1))

    f.close() 

if __name__ == '__main__':
    main()
    
