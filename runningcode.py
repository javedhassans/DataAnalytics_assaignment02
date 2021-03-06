""""Read me:  this file runs the zip file and give out two files with the prefixs of
1) output --> this is the output of the zip file with all country codes after using log(n) search function
2) only_eu --> this is the output after filtering for all EU countries
"""
#%%
# importing the depending modules
import re
import time
import bz2
import os
import sys
import json
import time
import pickle
import pandas as pd
import sys
import lognsearch

#%%

# creating the ist of european countries
european_list_codes1 = ["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI",
                        "FR", "GB", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV",
                        "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK"]
#%%
# readign ipfile and puting headers as required
header_names = ['IPmin', 'IPmax', 'Countrycode', 'Countryname']
ip_locations = pd.read_csv('IP2LOCATION-LITE-DB1.CSV', header=0, names=header_names)

# creating prbe_id list of EU countries and are hosting
prb_ID_EU = pd.read_csv("m_AS_EU_hosting.csv")
prb_id_list = list(prb_ID_EU["prb_id"])

#%%

# asking for user to provide filenam to work with
filename = input("enter the filename you want to work with")
print("name of file you entered is", filename)
bz2Filename = str(filename)

# counting total number of lines and the time taken for reading the lines
## fname should be like "ping-2020-02-20T0000.bz2"
starttimereadinglines = time.time()
bz2File = bz2.open(bz2Filename, 'rt')
count_nrlines = 0
for line in bz2File:
    count_nrlines += 1
    if count_nrlines > 10000:  ## todo acts as counter to check
        break
print("Total number of lines is:", count_nrlines)
# closinf file
bz2File.close()
# creating end time variable
endtimereadingfiles = time.time()
# printing total times for reading lines
print("total times for reading ", str(count_nrlines), "lines is", endtimereadingfiles - starttimereadinglines,
      "in seconds")

#%%

# this will create variable output filename for saving the output
outputfile = bz2Filename + 'output' + '.json'
# opening the file with the filname entered by the user in above
bz2File = bz2.open(bz2Filename, 'rt')

# runing the main chuck
count = 0;
st = time.time()
for line in bz2File:
    count = count + 1
    if count > 10000:  # #todo this controls numner of lines you want to run or check
        break
    json_file = json.loads(line)
    if "af" not in json_file.keys(): continue
    if "dst_addr" not in json_file.keys(): continue
    # if json_file["af"] != 4: continue # todo not sure we need this or not
    prb_id = json_file["prb_id"]

    #  # Find the prb_id in in the prb_ID_EU dataset
    # added the filter to ensure only ipv4 are taken
    if prb_id in prb_id_list and json_file["af"] == 4:
        # # crearting variable names to use in writing file
        to_ip = json_file["dst_addr"]
        result_array = json_file["result"]
        avg_latency = json_file["avg"]
        #  # Find the ip_destination_address in the ip_location files
        target_ip = int(re.sub(r'\.', '', to_ip))
        country = lognsearch.binarySearch(target_ip, ip_locations)
        # # storing the output of the file in jason file
        data = dict(country_code=country, prb_id=prb_id, avg_latency=avg_latency)
        if data["country_code"] in european_list_codes1:
            with open(outputfile, 'a+') as outfile:
                json.dump(data, outfile)
                outfile.write('\n')

# finally close bz2File
bz2File.close()

end_time = time.time()
print("estimeated time for execution is ", end_time - st)

#%%
data = 'data_01.json'
df = pd.read_json(data,lines=True)

data = outputfile
df = pd.read_json(data,lines=True)
df = df[df.avg_latency > 0]
df_country = df.loc[df.country_code.isin(european_list_codes1)]

#%%
df_country.groupby(by='prb_id')



