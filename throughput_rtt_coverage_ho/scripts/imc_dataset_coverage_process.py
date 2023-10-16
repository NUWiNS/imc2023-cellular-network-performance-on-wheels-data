import pandas as pd
import pickle
import sys 
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="http")
from timezonefinder import TimezoneFinder
obj = TimezoneFinder()

vz_phone_num_list = [6178231553, 6174291464, 6174294649]
tmobile_phone_num_list = [18576930597, 18576930598, 18576930599]
atnt_phone_num_list = [18573612771, 18573526798]

df_all = pd.read_csv(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\coverage\all_tests_combined.csv")
df_all.drop(df_all.head(5).index,inplace=True)
df_all = df_all.reset_index()
not_yet_started = 0
df_dict = {}
current_line = 0
current_op = 0
start_idx = 0
start_flag = False
count = -1
for index, row in df_all.iterrows():
    count+=1
    if count % 100 == 0:
        print("Parsing row == " + str(count))
    if start_flag == False:
        current_line = int(float((row['Smart Phone Android Mobile Info Line1 Number'])))
        current_op = "AT&T"
        start_flag = True
        continue
    elif pd.isnull(row['Smart Phone Android Mobile Info Line1 Number']) and pd.isnull(row['Smart Phone Android System Info Operator']):
        continue
    else:
        if pd.notnull(row['Smart Phone Android Mobile Info Line1 Number']):
            if row['Smart Phone Android Mobile Info Line1 Number'] == 'unknown':
                # it is tmobile
                # check if previous value was tmobile 
                if current_line in tmobile_phone_num_list:
                    # previous value was tmobile. no change then
                    continue
                else:
                    #previous value was not tmobile
                    # change observed
                    if current_line in vz_phone_num_list:
                        tech = "vz"
                    elif current_line in atnt_phone_num_list:
                        tech = "atnt"
                    else:
                        print("[2] Holy !")
                        import sys
                        sys.exit(1)
                    if tech not in df_dict.keys():
                        df_dict[tech] = [df_all[start_idx:index]]
                    else:
                        df_dict[tech].append(df_all[start_idx:index])
                    
                    current_line = tmobile_phone_num_list[0]
                    start_idx = index
            elif int(float(row['Smart Phone Android Mobile Info Line1 Number'])) == current_line:
                continue
            elif int(float(row['Smart Phone Android Mobile Info Line1 Number'])) != current_line:
                #change noticed
                if current_line in vz_phone_num_list:
                    tech = "vz"
                elif current_line in atnt_phone_num_list:
                    tech = "atnt"
                elif current_line in tmobile_phone_num_list:
                    tech = "tmobile"
                else:
                    print("Holy !")
                    import sys
                    sys.exit(1)
                if tech not in df_dict.keys():
                    df_dict[tech] = [df_all[start_idx:index]]
                else:
                    df_dict[tech].append(df_all[start_idx:index])

                current_line = int(float(row['Smart Phone Android Mobile Info Line1 Number']))
                start_idx = index
        elif pd.notnull(row['Smart Phone Android System Info Operator']):
            # {'T-Mobile', 'AT&T', 'Verizon ', 'Viaero Wireless', 'No service', '(Searching)'}
            # viaero wireless = T-Mobile
            # (searching) = T-Mobile
            # No service = ATnT

            # check if the operator detected now matches with the current_line's operator value
            # if it matches, then it is the same operator
            # or else , the operator has changed
            # changed to 
            if row['Smart Phone Android System Info Operator'] in ['Verizon ']:
                # verizon operator detected
                if current_line in vz_phone_num_list:
                    # previous operator matches
                    # do nothing 
                    continue
                else:
                    #previous operator do not match
                    #check which operator it is if 
                    if current_line in atnt_phone_num_list:
                        tech = "atnt"
                    elif current_line in tmobile_phone_num_list:
                        tech = "tmobile"
                    
                    if tech not in df_dict.keys():
                        df_dict[tech] = [df_all[start_idx:index]]
                    else:
                        df_dict[tech].append(df_all[start_idx:index])

                    start_idx = index
                    # change line to one of vz line now
                    current_line = vz_phone_num_list[0]
            elif row['Smart Phone Android System Info Operator'] in ['AT&T', 'No service']:
                # atnt detected 
                if current_line in atnt_phone_num_list:
                    # previous operator matches
                    # do nothing 
                    continue
                else:
                    #previous operator do not match
                    #check which operator it is if 
                    if current_line in vz_phone_num_list:
                        tech = "vz"
                    elif current_line in tmobile_phone_num_list:
                        tech = "tmobile"
                    
                    if tech not in df_dict.keys():
                        df_dict[tech] = [df_all[start_idx:index]]
                    else:
                        df_dict[tech].append(df_all[start_idx:index])

                    start_idx = index
                    # change line to one of atnt line now
                    current_line = atnt_phone_num_list[0]
            elif row['Smart Phone Android System Info Operator'] in ['T-Mobile', 'Viaero Wireless', '(Searching)']:
                # tmobile detected
                if current_line in tmobile_phone_num_list:
                    # previous operator matches
                    # do nothing 
                    continue
                else:
                    #previous operator do not match
                    #check which operator it is if 
                    if current_line in atnt_phone_num_list:
                        tech = "atnt"
                    elif current_line in vz_phone_num_list:
                        tech = "vz"
                    
                    if tech not in df_dict.keys():
                        df_dict[tech] = [df_all[start_idx:index]]
                    else:
                        df_dict[tech].append(df_all[start_idx:index])

                    start_idx = index
                    # change line to one of tmobile line now
                    current_line = tmobile_phone_num_list[0]


filehandler = open(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\coverage\processed\operator_break_unsorted.pkl", "wb")
pickle.dump(df_dict,filehandler)
filehandler.close()

