import glob
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from datetime import datetime
import datetime
from datetime import timezone, timedelta
import pickle
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="http")
from timezonefinder import TimezoneFinder
obj = TimezoneFinder()
import geopy.distance

arfcn_freq_dict = {'177020' : 885.100, '2083329' : 28249.800, '2071667' : 27550.080, '648672' : 3730.080, '2078331' : 27949.920, '2073333' : 27650.040, '177000' : 885.000, '174800' : 874.000, '175000' : 875.000, '650004' : 3750.060, '2239999' : 37650.000, '125400' : 627.000, '125900' : 629.500, '126400' : 632.000, '126490' :632.450, '126510' : 632.550, '126530' : 632.650, '126900' : 634.500, '506280' : 2531.400, '508296' : 2541.480, '509202' : 2546.010, '514056' : 2570.280, '520020' : 2600.100, '525204' :2626.020, '526002' : 2630.010, '526404' : 2632.020, '527202' : 2636.010, '528000' : 2640.000, '528696' : 2643.480, '529998' : 2649.990, '530700' : 2653.500}

earfcn_freq_dict = {'1000' : 1970.00, '1025' :  1972.50, '1050' : 1975, '1075' : 1977.50, '1125' : 1982.50 , '2100' : 2125.00, '2450' : 874.0, '2460' : 875.0, '2559' : 884.90, '2560' : 885.00, '2561' : 885.10, '2600' : 889.00, '5230' : 751.00, '5780' : 739.00, '66486' : 2115.00, '66536' : 2120.00, '66561' : 2122.50, '66586' : 2125.00, '66611' : 2127.50, '66636' : 2130.0, '66686' : 2135.00, '66711' : 2137.50, '66761' : 2142.50, '66786' : 2145.00, '66811' : 2147.50, '66836' : 2150.00, '66911' : 2157.50, '66936' : 2160.00, '66986' : 2165.00, '67011' : 2167.50, '67086' : 2175.00, '750' : 1945.00, '775' : 1947.50, '825' : 1952.50, '925' : 1962.50, '950' : 1965.00, '975' : 1967.50, '800' : 1950, '1025' :  1972.50, '1075' : 1977.50, '1100' : 1980.00, '1125' : 1982.50, '1150' : 1985.00, '2175' : 2132.50, '41094' : 2640.40, '41490' : 2680.00, '5035' : 731.50, '5090' : 737.00, '5110' : 739.00, '5145' : 742.50, '5330' : 763.00, '625' : 1932.50, '650' : 1935.00, '66461' : 2112.50, '66486' : 2115.00, '66511' : 2117.50, '66611' : 2127.50, '66661' : 2132.50, '66686' : 2135.00, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66936' : 2160.00, '66985' : 2164.90, '66986' : 2165.00, '67086' : 2175.00, '675' : 1937.50, '700' : 1940.00, '800' : 1950.00, '850' : 1955.00, '875' : 1957.50, '900' : 1960.00, '925' : 1962.50, '950' : 1965, '9820' : 765.00, '1099' : 1979.90, '1100' : 1980.00, '1123' : 1982.30, '1125' : 1982.50, '1126' : 1982.60, '1148' : 1984.80, '1150' : 1985.00, '2000' : 2115.00, '2050' : 2120.00, '2125' : 2127.50, '2175' : 2132.50, '2200' : 2135.00, '2225' : 2137.50, '2300' : 2145.00, '2325' : 2147.50, '2460': 875.0,  '39750' : 2506.00, '39907' : 2521.70, '39948' : 2525.80, '40072' : 2538.20, '40384' : 2569.40, '40770' : 2608.00, '40810' : 2612.00, '41176' : 2648.60, '41238' : 2654.80, '41490' : 2680.00, '5035' : 731.50, '5090' : 737, '5095' : 737.50, '5110' : 739.00, '5330' : 763.00, '5780' : 739, '5815': 742.5, '66486': 2115.00, '66487' : 2115.10, '66536' : 2120.00, '66561' : 2122.5, '66586' : 2125, '66661' : 2132.50, '66686' : 2135, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66811': 2147.5, '66836': 2150, '66886': 2150, '66911': 2150, '66961': 2150, '66986' : 2165.00, '67011': 2167.5, '675' : 1937.50, '676': 1937.6, '677': 1937.7, '68611': 619.5, '68636': 622, '68661': 624.5, '68686': 627, '68786': 637, '68836': 637, '68861': 637, '68886': 637, '68911': 649.5, '700' : 1940.00, '725': 1942.5, '750': 1942.5, '775': 1942.5, '801': 1950.1, '8115': 1937.5, '825': 1952.5, '8264': 1952.4, '8290': 1952.4, '8315': 1952.4, '8465': 1972.5, '850' : 1955.00, '851': 1955.1, '852': 1955.1, '8539': 1979.9, '8562': 1982.2, '8640': 1982.2, '8665': 1992.5, '875' : 1957.50, '876': 1957.6, '8763': 866.3, '877': 1957.7, '8950': 885, '901': 1960.1, '925' : 1962.50, '41305' : 2661.50, '66761' : 2142.50, '132122' : 1747.5}

def datetime_to_timestamp(datetime_str):
    from datetime import datetime
    date, time_all = datetime_str.split()
    temp_year = date.split("-")[0]
    temp_month = date.split("-")[1]
    temp_date = date.split("-")[2]
    datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
    dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
    sec = dt_obj.timestamp() 
    return sec

def get_avg_ping(filename):
    edge_found = 0
    edge_list = ['155.146.178.233', '161.188.33.26', '155.146.118.158', '155.146.144.24']
    fh = open(filename, "r")
    data = fh.readlines()
    rtt_list = []
    for d in data:
        if "46 bytes from" in d:
            #ping data found
            d = d.strip()
            d = d.split()
            ms_idx = d.index("ms")
            rtt_list.append(float(d[ms_idx - 1].split("=")[-1]))
        elif "PING" in d and "bytes of data." in d:
            for edge in edge_list:
                if edge in d:
                    edge_found = 1
    return [edge_found, rtt_list]

def downtown_measurements_mod(start_tuple, end_tuple):
    lat_lon_dt_dict = {'LA' : (34.05872013582416, -118.23766913901929), 'LV' : (36.11290509947277, -115.1731529445295), 'SLC' : (40.725262, -111.854019), 'DE' : (39.744331, -105.009438), 'CHIC' : (41.89307, -87.623787), 'INDY' : (39.768028, -86.15094), 'CLEV' : (41.5005, -81.674026) }
    for key in lat_lon_dt_dict:
        distance_from_start = geopy.distance.geodesic(lat_lon_dt_dict[key], start_tuple).miles
        distance_from_end = geopy.distance.geodesic(lat_lon_dt_dict[key], end_tuple).miles
        
        if distance_from_start < 2 or distance_from_end < 2:
            #downtown measurement
            return True
    return False
def modify_speed_list(speed_list):
    if len(speed_list) == 0:
        return
    elif len(speed_list) <= 10:
        # too small a length for handover segment
        # average all speed values
        return [np.mean(speed_list)] * len(speed_list)
    prev_speed = speed_list[0]
    prev_idx = 0
    current_idx = 1
    mod_speed_list = [prev_speed]
    crap_found = 0
    for current_speed in speed_list[1:]:
        if crap_found and current_idx in ignore_indices:
            prev_speed = current_speed
            prev_idx = current_idx
            current_idx+=1
            continue
        if abs(current_speed - prev_speed) <= 12:
            crap_found = 0
            mod_speed_list.append(current_speed)
            prev_speed = current_speed
            prev_idx = current_idx
            current_idx+=1
        else:
            # next 10 speed vals
            next_10_speed_vals = speed_list[current_idx:current_idx+11]
            next_10_speed_vals_diff = [abs(next_val - prev_speed) for next_val in next_10_speed_vals]
            idx = 0
            recovery_speed = None
            for diff in next_10_speed_vals_diff:
                if diff > 12:
                    idx+=1
                else:
                    recovery_speed = next_10_speed_vals[idx]
                    break
            if recovery_speed == None:
                print("WTF!")
                # replace with the average
                mod_speed_list.append(np.mean(speed_list))
                prev_speed = current_speed
                prev_idx = current_idx
                current_idx+=1
                continue
            mod_list = [np.mean([prev_speed, recovery_speed])] * idx
            mod_speed_list.extend(mod_list)
            mod_speed_list.append(recovery_speed)
            crap_found = 1
            ignore_indices = list(range(current_idx, current_idx+len(mod_list) + 1))
            prev_speed = current_speed
            prev_idx = current_idx
            current_idx+=1
    
    if len(speed_list) != len(mod_speed_list):
        print("WTF 2!")
        sys.exit(1)

    return mod_speed_list
 

def get_speed_for_df(df_short_tput):
    speed_tput_tuple = {}
    lat_list = list(df_short_tput["Lat"])
    lon_list = list(df_short_tput["Lon"])
    ts_list = list(df_short_tput["TIME_STAMP"])
    prev_lat_lon = (lat_list[0], lon_list[0])
    prev_ts = ts_list[0]
    dist_list = []
    speed_list = []
    dt_measurement = downtown_measurements_mod((lat_list[0], lon_list[0]), (lat_list[-1], lon_list[-1]))
    for lat, lon, ts in zip(lat_list[1:], lon_list[1:], ts_list[1:]):
        current_lat_lon = (lat, lon)
        distance_current = geopy.distance.geodesic(current_lat_lon, prev_lat_lon).miles
        # assuming we drove max of 150 miles/hour, we cannot have more than 0.021 miles in 0.5 sec
        # check if distance current > 0.03
        if distance_current > 0.03:
            # check timestamp diff
            ts_diff = ts - prev_ts
            # ideally each point should be 0.5 seconds apart
            # with some tolerance, each point should not be more than 5 seconds apart? 
            if ts_diff <= 5:
                # if tolerance of 5 seconds is achieved, check if the distance complies with it or not
                # if 0.021 miles in 0.5 sec is normal, what happens for ts_diff?
                # is (0.021 * 2 * ts_diff) within range of distance_current?
                if distance_current <= ((0.021 * 2 * ts_diff)):
                    # value can be accepted
                    speed = (distance_current / ts_diff) * 3600
                else:
                    prev_lat_lon = (lat, lon)
                    prev_ts = ts
                    continue

            else:
                prev_lat_lon = (lat, lon)
                prev_ts = ts
                continue

        elif distance_current == 0:
            speed = 0
        else:
            # speed = (distance_current / 0.5) * 3600
            ts_diff = ts - prev_ts
            speed = (distance_current / ts_diff) * 3600
        if round(speed) > 150:
            prev_lat_lon = (lat, lon)
            prev_ts = ts
            continue

        if dt_measurement and speed > 20:
            import random
            # speed = 10
            speed = random.randint(0, 20)

        dist_list.append(distance_current)
        speed_list.append(speed)
        prev_lat_lon = (lat, lon)
        prev_ts = ts
    old_speed_list = speed_list.copy()
    if len(old_speed_list) == 0:
        return []
    speed_list = modify_speed_list(speed_list)
    uniques, counts = np.unique(speed_list, return_counts=True)
    percentages = dict(zip(uniques, counts * 100 / len(speed_list)))
    
    if len(percentages) != 0:
        if 0 in percentages.keys():
            if percentages[0] > 85:
                #static run
                return speed_list                          
            else:
                return speed_list
                
        else:
            return speed_list
main_op_dict = {}
main_rtt_5g_dict = {}
main_rtt_tech_dict = {}
main_avg_rtt_tech_dict = {}
main_std_rtt_tech_dict = {}
main_edge_tech_dict = {}
op_speed_dict = {'verizon' : [], 'tmobile' : [], 'atnt' : []}
op_rtt_dict = {'verizon' : [], 'tmobile' : [], 'atnt' : []}
op_tech_dict = {'verizon' : [], 'tmobile' : [], 'atnt' : []}
for op in ['verizon', 'tmobile', 'atnt']:
    rtt_tech_dict = {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}
    edge_tech_dict = {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}
    rtt_5g_percent_dict = {}
    color_dict = {"LTE" : "indianred", "LTE-A" : "red", "5G-low" : "greenyellow", "5G-sub6" : "darkolivegreen", "5G-mmWave 28 GHz" : "aqua", "5G-mmWave 39 GHz" : "blue" }
    ping_path = r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc_dataset\rtt\\" + op
    ping_folders = glob.glob(ping_path + "\\run-*")
    ping_lat_lon_dict = []
    for ping_folder in ping_folders:
        if "atnt" in ping_folder and "run-4" in ping_folder:
            print()
        lte_only = 0
        print("*******************")
        print("Parsing " + ping_folder)
        out_file = glob.glob(ping_folder + "\\*.out")
        df_file = glob.glob(ping_folder + "\\xcal.csv")
        edge_found, rtt_list = get_avg_ping(out_file[0])
        edge_found   = [edge_found]  * len(rtt_list)
        avg_rtt = rtt_list[5:]
        df = pd.read_csv(df_file[-1])
        try:
            df_tech = df[["TIME_STAMP", "5G KPI PCell RF Frequency [MHz]", "LTE KPI PCell Serving EARFCN(DL)"]]
        except:
            lte_only = 1
        df_tech.drop(df_tech.tail(8).index,inplace=True)
        percentage = None
        if lte_only == 0 and (len(list(df_tech["5G KPI PCell RF Frequency [MHz]"].dropna())) > 0):
            # it is a 5G run
            event_tech = list(df['Event Technology'].dropna())
            if any("LTE" in item for item in event_tech) == False:
                total_count = df_tech[(df_tech['5G KPI PCell RF Frequency [MHz]'].notna())].shape[0]
                count_greater_than_1000 = df_tech['5G KPI PCell RF Frequency [MHz]'].gt(1000).sum()
                percentage = count_greater_than_1000/total_count
            else:
                try:
                    df_short_ho = df[df['Event 5G-NR/LTE Events'].notna()]
                    df_short_ho = df[df['Event 5G-NR/LTE Events'].str.contains("Handover Success") | df['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Success") | df['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Success")]

                    if len(df_short_ho) == 0:
                        print("No HO!")
                        total_count = df_tech[(df_tech['5G KPI PCell RF Frequency [MHz]'].notna())].shape[0]
                        count_greater_than_1000 = df_tech['5G KPI PCell RF Frequency [MHz]'].gt(1000).sum()
                        percentage = count_greater_than_1000/total_count
                    else:
                        df_merged = pd.concat([df_tech, df_short_ho])
                        df_merged = df_merged.sort_values(by=["TIME_STAMP"])
                        df_merged.reset_index(inplace=True)
                            
                        break_list = []
                        event = -99
                        start_flag = 0
                        
                        #create break list --> tput_df 
                        for index, row in df_merged.iterrows():
                            if start_flag == 0:
                                # first entry
                                # check if event is empty or not
                                if pd.isnull(row['Event 5G-NR/LTE Events']):
                                    event = 0
                                    start_flag = 1
                                    start_index_count = 0 
                                    end_index_count = 0 
                                else:
                                    #first entry is event
                                    event = 1
                                    start_flag = 1
                            else:
                                #row scan in progress 
                                if event == 0 and pd.isnull(row['Event 5G-NR/LTE Events']):
                                    #keep increasing index count
                                    end_index_count+=1
                                elif event == 0 and pd.notnull(row['Event 5G-NR/LTE Events']):
                                    # set event to 1 : new event started
                                    event = 1
                                    # add truncated df to break list
                                    break_list.append(df_merged[start_index_count:end_index_count+1])
                                elif event == 1 and pd.notnull(row['Event 5G-NR/LTE Events']):
                                    # continue with event
                                    continue
                                elif event == 1 and pd.isnull(row['Event 5G-NR/LTE Events']):
                                    # event stopped and throughput started
                                    # set event to 0
                                    # set start and end index count to current index + 1
                                    event = 0
                                    start_index_count = index
                                    end_index_count = index
                        
                        if event == 0:
                            # add the last throughput value
                            # if df_merged[start_index_count:end_index_count+1] != break_list[-1]:
                            break_list.append(df_merged[start_index_count:end_index_count+1])
                        total_count = 0
                        fiveg_high_count = 0
                        for tput_df in break_list:
                            modified_tech = ""
                            # check if 5G frequency or 5G PCI  is empty
                            if len(list(tput_df["5G KPI PCell RF Frequency [MHz]"].dropna())) > 0 or len(list(tput_df["5G KPI PCell RF Serving PCI"].dropna())) > 0:
                                # it is a 5G run 
                                # get type of 5G 
                                # max(set(freq_list), key=freq_list.count)
                                freq_list = list(tput_df["5G KPI PCell RF Frequency [MHz]"].dropna())
                                ffreq = float(max(set(freq_list), key=freq_list.count))
                                if ffreq > 1000:
                                    fiveg_high_count+=len(tput_df)
                                modified_tech = ""

                            total_count+=len(tput_df)
                        percentage = fiveg_high_count / total_count
                except:
                    # revert back to old way - as event lte/5g is not recorded by xcal
                    total_count = df_tech[(df_tech['5G KPI PCell RF Frequency [MHz]'].notna())].shape[0]
                    count_greater_than_1000 = df_tech['5G KPI PCell RF Frequency [MHz]'].gt(1000).sum()
                    percentage = count_greater_than_1000/total_count
            freq_list = list(df_tech["5G KPI PCell RF Frequency [MHz]"].dropna())
            ffreq = float(max(set(freq_list), key=freq_list.count))
            if int(ffreq) < 1000:
                modified_tech = "5G-low"
            elif int(ffreq) > 1000 and int(ffreq) < 7000:
                modified_tech = "5G-sub6"
            elif int(ffreq) > 7000 and int(ffreq) < 35000:
                modified_tech = "5G-mmWave 28 GHz"
            elif int(ffreq) > 35000:
                modified_tech = "5G-mmWave 39 GHz"
        else:
            # it is lte probably
            earfcn_list = list(df_tech["LTE KPI PCell Serving EARFCN(DL)"].dropna())
            if len(earfcn_list) == 0:
                continue
            percentage = 0
            lfreq = str(int(max(set(earfcn_list), key=earfcn_list.count)))
            if lfreq not in earfcn_freq_dict.keys():
                print("EARFCN not present in dict. Need to add." + str(lfreq))
                sys.exit(1)
            else:
                lfreq = earfcn_freq_dict[lfreq]
            
            if int(lfreq) < 1000:
                modified_tech = "LTE"
            elif int(lfreq) > 1000:
                modified_tech = "LTE-A"  
        
        rtt_tech_dict[modified_tech].extend(avg_rtt)
        edge_tech_dict[modified_tech].extend(edge_found)
        
        if percentage in rtt_5g_percent_dict.keys():
            rtt_5g_percent_dict[percentage].append(np.mean(avg_rtt))
        else:
            rtt_5g_percent_dict[percentage] = [np.mean(avg_rtt)]

        lat_lon_df = df[["TIME_STAMP", "Lat", "Lon"]]
        lat_lon_df = lat_lon_df.dropna()
        break_point = 5
        count = -1
        for index, row in lat_lon_df.iterrows():
            count+=1
            if count < break_point:
                continue
            else:
                lat = row['Lat']
                lon = row['Lon']
                break
        
        if lat != None and lon != None and avg_rtt != None:
            ping_lat_lon_dict.append([lat, lon, avg_rtt, ping_folder])
            lat_lon_df.drop(lat_lon_df.tail(8).index, inplace=True)
            lat_lon_df["TIME_STAMP"] = lat_lon_df["TIME_STAMP"].apply(datetime_to_timestamp)
        else:
            if avg_rtt != None:
                # lat lon not found 
                # match it with all dict
                # if still None, nothing can be done
                merged_csv_all = r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc_dataset\coverage\all_tests_combined.csv"
                lat_lon_df = df[["TIME_STAMP", "Lat", "Lon"]]
                lat_lon_df.drop(lat_lon_df.tail(8).index, inplace=True)
                atnt_df = lat_lon_df
                all_df = pd.read_csv(merged_csv_all)
                all_df.drop(all_df.tail(400).index,inplace=True) # drop last 8 rows
                atnt_not_null_df = atnt_df[(atnt_df["Lat"].notnull()) & (atnt_df["Lon"].notnull())]
                atnt_null_df = atnt_df[(atnt_df["Lat"].isnull()) & (atnt_df["Lon"].isnull())]
                atnt_null_df["TIME_STAMP"] = atnt_null_df["TIME_STAMP"].apply(datetime_to_timestamp)
                atnt_null_df = atnt_null_df.drop(columns=['Lat', 'Lon'])
                atnt_null_df = atnt_null_df.sort_values("TIME_STAMP")
                all_time_lat_lon_all = all_df[["TIME_STAMP", "Lat", "Lon"]]
                all_time_lat_lon_all = all_time_lat_lon_all.sort_values("TIME_STAMP")

                df_merged = pd.merge_asof(atnt_null_df, all_time_lat_lon_all, on="TIME_STAMP", direction="nearest", tolerance=300)
                df_merged = pd.concat([atnt_not_null_df, df_merged])
                df_merged = df_merged.sort_values("TIME_STAMP")
                df_merged = df_merged.dropna()
                # check again 
                break_point = 5
                count = -1
                for index, row in df_merged.iterrows():
                    count+=1
                    if count < break_point:
                        continue
                    else:
                        if pd.isnull(row['Lat']) or pd.isnull(row['Lon']):
                            continue
                        lat = row['Lat']
                        lon = row['Lon']
                        break
                
                if lat != None and lon != None and avg_rtt != None:
                    ping_lat_lon_dict.append([lat, lon, avg_rtt, ping_folder])
                    lat_lon_df = df_merged.copy()
                else:
                    print("Hopeless data! Wtf!")
                    print("try once more ")
                    lat_lon_fh = open(ping_folder + "\\lat_lon.txt", "rb")
                    data = lat_lon_fh.readlines()
                    lat, lon = data[0].decode().strip().split(",")
                    lat_lon_fh.close()
                    ping_lat_lon_dict.append([lat, lon, avg_rtt, ping_folder])
                    lat_lon_df = []
        
        if len(lat_lon_df) != 0:
            speed_list = get_speed_for_df(lat_lon_df)
            rtt_len = len(rtt_list)
            if len(speed_list) > rtt_len:
                # Calculate the start index for the subset
                start_index = max(0, (len(speed_list) - len(rtt_list)) // 2)
                # Extract the subset from list_n
                sub_list = speed_list[start_index:start_index + len(rtt_list)]
                op_speed_dict[op].extend(sub_list)
                op_rtt_dict[op].extend(rtt_list)
                op_tech_dict[op].extend([modified_tech] * len(rtt_list))
            elif len(speed_list) == rtt_len:
                op_speed_dict[op].extend(speed_list)
                op_rtt_dict[op].extend(rtt_list)
                op_tech_dict[op].extend([modified_tech] * len(rtt_list))
            elif len(speed_list) < rtt_len:
                if len(speed_list) != 0:
                    op_rtt_dict[op].extend(rtt_list)
                    op_tech_dict[op].extend([modified_tech] * len(rtt_list))
                    op_speed_dict[op].extend(speed_list)
                    op_speed_dict[op].extend([speed_list[-1]] * (len(rtt_list) - len(speed_list)))

        lat = None
        lon = None
        avg_rtt = None
        modified_tech = ""
    main_rtt_5g_dict[op] = rtt_5g_percent_dict

    main_rtt_tech_dict[op] = rtt_tech_dict
    main_edge_tech_dict[op] = edge_tech_dict
    main_op_dict[op] = ping_lat_lon_dict
    # include the Vegas missed run 
    if "verizon" in op:
        vegas_county_lat = 36.2333
        vegas_county_lon = -115.2654
        vegas_vz_driving_ping = [84.1, \
                                16.0, \
                                15.1, \
                                14.8, \
                                34.4, \
                                32.9, \
                                31.9, \
                                31.3, \
                                30.9, \
                                30.6, \
                                30.1, \
                                23.8, \
                                29.0, \
                                23.3, \
                                17.8, \
                                16.8, \
                                22.6, \
                                41.1, \
                                46.2, \
                                41.4, \
                                44.8, \
                                28.6, \
                                37.3, \
                                37.8, \
                                32.4, \
                                28.6, \
                                28.8, \
                                33.6, \
                                38.9, \
                                38.1, \
                                32.5, \
                                27.1, \
                                25.4, \
                                29.9, \
                                23.6, \
                                63.3, \
                                30.9, \
                                35.3, \
                                28.9, \
                                27.6, \
                                27.7, \
                                27.4, \
                                31.7, \
                                24.8, \
                                24.3, \
                                34.6, \
                                22.9, \
                                27.6, \
                                20.2, \
                                25.2, \
                                20.5, \
                                21.6, \
                                21.2, \
                                23.4, \
                                34.6, \
                                75.2, \
                                32.8, \
                                32.7, \
                                32.0, \
                                31.3, \
                                32.5, \
                                49.8, \
                                29.3, \
                                39.2, \
                                38.2, \
                                17.3, \
                                42.1, \
                                41.0, \
                                36.4, \
                                32.9, \
                                32.5, \
                                31.7, \
                                11.4, \
                                34.6, \
                                33.4, \
                                34.3, \
                                32.2, \
                                32.3, \
                                31.5, \
                                40.7, \
                                44.7, \
                                38.8, \
                                35.1, \
                                27.9, \
                                20.8, \
                                19.8, \
                                21.2, \
                                18.8, \
                                18.9, \
                                17.7, \
                                16.5, \
                                15.0, \
                                37.3, \
                                38.9, \
                                38.0, \
                                37.2, \
                                34.7, \
                                53.0, \
                                40.8, \
                                10.7]
        main_op_dict[op].append([vegas_county_lat, vegas_county_lon, vegas_vz_driving_ping])
        # for this vegas run, get speed
        ping_vegas_df = pd.read_csv(r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc_dataset\rtt\verizon\vegas_ping.csv")
        ping_vegas_df.drop(ping_vegas_df.tail(8).index,inplace=True)
        ping_vegas_df["TIME_STAMP"] = ping_vegas_df["TIME_STAMP"].apply(datetime_to_timestamp)
        speed_list = get_speed_for_df(ping_vegas_df)
        rtt_list = vegas_vz_driving_ping.copy()
        rtt_len = len(rtt_list)
        if len(speed_list) > rtt_len:
            # Calculate the start index for the subset
            start_index = max(0, (len(speed_list) - len(rtt_list)) // 2)
            # Extract the subset from list_n
            sub_list = speed_list[start_index:start_index + len(rtt_list)]
            op_speed_dict[op].extend(sub_list)
            op_rtt_dict[op].extend(rtt_list)
            op_tech_dict[op].extend([modified_tech] * len(rtt_list))
        elif len(speed_list) == rtt_len:
            op_speed_dict[op].extend(speed_list)
            op_rtt_dict[op].extend(rtt_list)
            op_tech_dict[op].extend([modified_tech] * len(rtt_list))

    if "atnt" in op:
        # missed Indianapolis run with 0 speed
        # car stalled 0 speed
        indy_ping = [93.4, 131.0, 92.2, 129.0, 90.4, 130.0, 89.4, 128.0, 88.0, 126.0, 87.3, 127.0, 85.7, 126.0, 83.9, 124.0, 83.4, 122.0, 81.1, 120.0, 80.4, 119.0, 78.2, 117.0, 75.8, 116.0, 76.3, 115.0, 73.6, 113.0, 73.4, 112.0, 152.0, 111.0, 150.0, 110.0, 149.0, 108.0, 147.0, 106.0, 147.0, 106.0, 145.0, 105.0, 144.0, 104.0, 143.0, 103.0, 142.0, 101.0, 141.0, 101.0, 140.0, 99.2, 138.0, 99.3, 138.0, 97.3, 136.0, 95.3, 135.0, 94.7, 134.0, 93.7, 132.0, 91.8, 131.0, 90.2, 129.0, 89.5, 129.0, 88.0, 127.0, 86.6, 127.0, 84.4, 123.0, 83.5, 123.0, 83.9, 122.0, 81.7, 121.0, 80.4, 120.0, 78.9, 118.0, 77.5, 118.0, 76.4, 115.0, 73.8, 114.0, 73.0, 113.0]
        rtt_list = indy_ping.copy()
        op_speed_dict[op].extend([0] * len(rtt_list))
        op_rtt_dict[op].extend(rtt_list)
        op_tech_dict[op].extend(['5G-mmWave 39 GHz'] * len(rtt_list))
filehandler = open(r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc_dataset\rtt\processed\rtt_all.pkl", "wb")
lst = [main_op_dict, main_rtt_5g_dict, main_rtt_tech_dict, main_edge_tech_dict, op_speed_dict, op_rtt_dict, op_tech_dict]
pickle.dump(lst, filehandler)
filehandler.close()
