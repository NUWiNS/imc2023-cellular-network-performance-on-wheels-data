import glob
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import sys 
import os
from collections import defaultdict
from geopy.geocoders import Nominatim
import geopy.distance
from operator import add
geolocator = Nominatim(user_agent="http")
from timezonefinder import TimezoneFinder
obj = TimezoneFinder()
from matplotlib.lines import Line2D

vz_phone_num_list = [6178231553, 6174291464, 6174294649]
tmobile_phone_num_list = [18576930597, 18576930598, 18576930599]
atnt_phone_num_list = [18573612771, 18573526798]

skip_ts_start_list = []
skip_ts_end_list = []

def downtown_measurements_mod(start_tuple, end_tuple):
    lat_lon_dt_dict = {'LA' : (34.05872013582416, -118.23766913901929), 'LV' : (36.11290509947277, -115.1731529445295), 'SLC' : (40.725262, -111.854019), 'DE' : (39.744331, -105.009438), 'CHIC' : (41.89307, -87.623787), 'INDY' : (39.768028, -86.15094), 'CLEV' : (41.5005, -81.674026) }
    for key in lat_lon_dt_dict:
        distance_from_start = geopy.distance.geodesic(lat_lon_dt_dict[key], start_tuple).miles
        distance_from_end = geopy.distance.geodesic(lat_lon_dt_dict[key], end_tuple).miles
        
        if distance_from_start < 2 or distance_from_end < 2:
            #downtown measurement
            return True
    return False

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
    
def modify_ts_none_for_static_runs(timestamp):
    timestamp = int(timestamp)
    for start, end in zip(skip_ts_start_list, skip_ts_end_list):
        if timestamp in range(start, end):
            return "static"
    return timestamp

def remove_static(df_all, op):
    global skip_ts_start_list
    global skip_ts_end_list
    if (op == "atnt" or op == "tmobile") and (len(skip_ts_start_list) > 0 or len(skip_ts_end_list) > 0):
        print("Ehh!  is happening! The lists should be empty!")
        sys.exit(1)
    if op == "verizon":
        df_static_list = glob.glob(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\tput\static\verizon\*.csv")
    elif op == "tmobile":
        df_static_list = glob.glob(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\tput\static\tmobile\*.csv")
    elif op == "atnt":
        df_static_list = glob.glob(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\tput\static\atnt\*.csv")
    
    ts_list = []
    for df_temp in df_static_list:
        # ts_list.append(df_temp["TIME_STAMP"][df_temp.first_valid_index()])
        df_temp = pd.read_csv(df_temp)
        ts_list.append(datetime_to_timestamp(df_temp["TIME_STAMP"][2]))
    ts_list = sorted(ts_list)
    print()

    count = 0
    for ts in ts_list:
        if count == 0:
            count+=1
            skip_ts_start_list.append(int(ts))
            skip_ts_end_list.append(int(ts + 3600))
        
        if ts in range(skip_ts_start_list[-1], skip_ts_end_list[-1]):
            #ignore
            continue
        else:
            skip_ts_start_list.append(int(ts))
            skip_ts_end_list.append(int(ts + 3600))
    
    df_all["TIME_STAMP"] = df_all["TIME_STAMP"].apply(modify_ts_none_for_static_runs)
    skip_ts_start_list = []
    skip_ts_end_list = []
    df_all = df_all[df_all['TIME_STAMP'] != "static"]
    return df_all

def modify_atnt_df(atnt_df):
    print("Starting here......")
    merged_csv_all = r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\xcal_names_folder_wise\csvs\combined\df_all_ca_mod.csv"
    all_df = pd.read_csv(merged_csv_all)
    all_df.drop(all_df.tail(400).index,inplace=True) # drop last 8 rows
    atnt_not_null_df = atnt_df[(atnt_df["Lat"].notnull()) & (atnt_df["Lon"].notnull())]
    atnt_null_df = atnt_df[(atnt_df["Lat"].isnull()) & (atnt_df["Lon"].isnull())]
    atnt_null_df = atnt_null_df.drop(columns=['Lat', 'Lon'])
    atnt_null_df = atnt_null_df.sort_values("TIME_STAMP")
    all_time_lat_lon_all = all_df[["TIME_STAMP", "Lat", "Lon"]]
    all_time_lat_lon_all = all_time_lat_lon_all.sort_values("TIME_STAMP")

    df_merged = pd.merge_asof(atnt_null_df, all_time_lat_lon_all, on="TIME_STAMP", direction="nearest", tolerance=300)
    df_atnt = pd.concat([atnt_not_null_df, df_merged])
    df_atnt = df_atnt.sort_values("TIME_STAMP")
    return df_atnt


if not os.path.exists(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\coverage\processed\dist_tz_speed_operator.pkl"):
    filehandler = open(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\coverage\processed\operator_break_unsorted.pkl", "rb")
    operator_wise_df = pickle.load(filehandler)
    filehandler.close()

    df_atnt = pd.concat(operator_wise_df["atnt"])
    df_vz = pd.concat(operator_wise_df["vz"])
    df_tmobile = pd.concat(operator_wise_df["tmobile"])

    tech_parse = True
    if tech_parse:
        verizon_parse = True
        if verizon_parse:
            df_vz = remove_static(df_vz, "verizon")
            df_tech_lte_fiveg_freq = df_vz[["TIME_STAMP", "Lat", "Lon", "Event Technology","Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]", "5G KPI PCell RF Frequency [MHz]"]]
            df_tech_lte_fiveg_freq = df_tech_lte_fiveg_freq.fillna(0)
            print()
            ts = list(df_tech_lte_fiveg_freq.TIME_STAMP)
            lat = list(df_tech_lte_fiveg_freq.Lat)
            lon = list(df_tech_lte_fiveg_freq.Lon)
            lte_freq = list(df_tech_lte_fiveg_freq["Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]"])
            fiveg_freq = list(df_tech_lte_fiveg_freq["5G KPI PCell RF Frequency [MHz]"])
            event_tech = list(df_tech_lte_fiveg_freq["Event Technology"])
            unique_dict = {}
            list_idx = -1
            for t, lt, ln, lfreq, ffreq, tech in zip(ts, lat, lon, lte_freq, fiveg_freq, event_tech):
                list_idx+=1
                if tech == 0 or tech == 0.0 or tech == str(0) or tech == str(0.0):
                    continue
                modified_tech = ""
                if "5G" in tech:
                    #find frequency 
                    if int(ffreq) == 0:
                        #look for frequency in vicinity
                        #look for frequency in vicinity
                        if list_idx > len(fiveg_freq) - 10:
                            temp_list = fiveg_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = fiveg_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "5G-low"
                        elif np.mean(temp_list) > 1000 and np.mean(temp_list) < 7000:
                            modified_tech = "5G-sub6"
                        elif np.mean(temp_list) > 7000 and np.mean(temp_list) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif np.mean(temp_list) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                    else:
                        #found frequency
                        if int(ffreq) < 1000:
                            modified_tech = "5G-low"
                        elif int(ffreq) > 1000 and int(ffreq) < 7000:
                            modified_tech = "5G-sub6"
                        elif int(ffreq) > 7000 and int(ffreq) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif int(ffreq) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                elif "LTE" in tech:
                    #find frequency 
                    if int(lfreq) == 0:
                        #look for frequency in vicinity
                        if list_idx > len(lte_freq) - 10:
                            temp_list = lte_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = lte_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "LTE"
                        elif np.mean(temp_list) > 1000:
                            modified_tech = "LTE-A"
                    else:
                        #found frequency
                        if int(lfreq) < 1000:
                            modified_tech = "LTE"
                        elif int(lfreq) > 1000:
                            modified_tech = "LTE-A"
                if modified_tech == "":
                    continue
                if "39 GHz" in modified_tech and t in range(1660432274, 1660433472):
                    continue
                if (lt, ln) in list(unique_dict.keys()):
                    unique_dict[(lt, ln)].append(modified_tech)
                else:
                    unique_dict[(lt, ln)] = [modified_tech]
            for key in unique_dict.keys():
                unique_dict[key] = max(unique_dict[key],key=unique_dict[key].count)

            if 1:
                lat_list = []
                long_list = []
                tech_list = []
                color_list = {"LTE" : "indianred", "LTE-A" : "red", "5G-low" : "greenyellow", "5G-sub6" : "darkolivegreen", "5G-mmWave 28 GHz" : "aqua", "5G-mmWave 39 GHz" : "blue"}
                color_list = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
                for key in unique_dict.keys():
                    lat_list.append(key[0])
                    long_list.append(key[1])
                    tech_list.append(unique_dict[key])
                df_tech = pd.DataFrame(list(zip(lat_list, long_list, tech_list)), columns=["Latitude", "Longitude", "Cellular Technology"])
                df_split_list = [d for _, d in df_tech.groupby(["Cellular Technology"])]
                tech_bins_sorted = {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}

                for tech in df_split_list:
                    tech_bins_sorted[list(tech["Cellular Technology"])[0]]  = tech

                for key in tech_bins_sorted.keys():
                    if len(tech_bins_sorted[key]) == 0:
                        tech_bins_sorted[key] = pd.DataFrame(columns=['Latitude', 'Longitude', "Cellular Technology"])
                        temp = {'Latitude' : 20.5937, 'Longitude' : 78.9629, 'Cellular Technology': key}
                        tech_bins_sorted[key] = tech_bins_sorted[key].append(temp, ignore_index = True)

                df_split_list = tech_bins_sorted.values()
                fig_list = []
                tech_df_list = []
                count = 0
                for df_tmp in  df_split_list:
                    fig_list.append(px.scatter_geo(df_tmp, lat="Latitude", lon= "Longitude", color="Cellular Technology", ))
                    tech_df_list.append(list(df_tmp["Cellular Technology"])[0])
                    count+=1

                count=0
                fig_tech = px.scatter_geo()
                for fg, tech in zip(fig_list, tech_df_list):
                    fig_tech.add_traces(fg._data)
                    fig_tech.data[count+1].marker.color = color_list[tech]
                    fig_tech.data[count+1].marker.size = 3
                    count+=1
                
                fig_tech.update_layout(geo_scope="usa", showlegend=False)
                fig_tech.write_image(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_1\fig_1e.pdf")

        tmobile_parse = True
        if tmobile_parse:
            df_tmobile = remove_static(df_tmobile, "tmobile")
            df_tech_lte_fiveg_freq = df_tmobile[["TIME_STAMP", "Lat", "Lon", "Event Technology","Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]", "5G KPI PCell RF Frequency [MHz]"]]
            df_tech_lte_fiveg_freq = df_tech_lte_fiveg_freq.fillna(0)
            print()
            ts = list(df_tech_lte_fiveg_freq.TIME_STAMP)
            lat = list(df_tech_lte_fiveg_freq.Lat)
            lon = list(df_tech_lte_fiveg_freq.Lon)
            lte_freq = list(df_tech_lte_fiveg_freq["Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]"])
            fiveg_freq = list(df_tech_lte_fiveg_freq["5G KPI PCell RF Frequency [MHz]"])
            event_tech = list(df_tech_lte_fiveg_freq["Event Technology"])
            unique_dict = {}
            list_idx = -1
            for t, lt, ln, lfreq, ffreq, tech in zip(ts, lat, lon, lte_freq, fiveg_freq, event_tech):
                list_idx+=1
                if tech == 0 or tech == 0.0 or tech == str(0) or tech == str(0.0):
                    continue
                modified_tech = ""
                if "5G" in tech:
                    #find frequency 
                    if int(ffreq) == 0:
                        #look for frequency in vicinity
                        #look for frequency in vicinity
                        if list_idx > len(fiveg_freq) - 10:
                            temp_list = fiveg_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = fiveg_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "5G-low"
                        elif np.mean(temp_list) > 1000 and np.mean(temp_list) < 7000:
                            modified_tech = "5G-sub6"
                        elif np.mean(temp_list) > 7000 and np.mean(temp_list) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif np.mean(temp_list) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                    else:
                        #found frequency
                        if int(ffreq) < 1000:
                            modified_tech = "5G-low"
                        elif int(ffreq) > 1000 and int(ffreq) < 7000:
                            modified_tech = "5G-sub6"
                        elif int(ffreq) > 7000 and int(ffreq) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif int(ffreq) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                elif "LTE" in tech:
                    #find frequency 
                    if int(lfreq) == 0:
                        #look for frequency in vicinity
                        if list_idx > len(lte_freq) - 10:
                            temp_list = lte_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = lte_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "LTE"
                        elif np.mean(temp_list) > 1000:
                            modified_tech = "LTE-A"
                    else:
                        #found frequency
                        if int(lfreq) < 1000:
                            modified_tech = "LTE"
                        elif int(lfreq) > 1000:
                            modified_tech = "LTE-A"
                if modified_tech == "":
                    continue
                if "mmWave" in modified_tech and t > 1659983687:
                    continue
                if (lt, ln) in list(unique_dict.keys()):
                    unique_dict[(lt, ln)].append(modified_tech)
                else:
                    unique_dict[(lt, ln)] = [modified_tech]
            for key in unique_dict.keys():
                unique_dict[key] = max(unique_dict[key],key=unique_dict[key].count)

            if 1:
                lat_list = []
                long_list = []
                tech_list = []
                color_list = {"LTE" : "indianred", "LTE-A" : "red", "5G-low" : "greenyellow", "5G-sub6" : "darkolivegreen", "5G-mmWave 28 GHz" : "aqua", "5G-mmWave 39 GHz" : "blue" }
                color_list = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
                for key in unique_dict.keys():
                    lat_list.append(key[0])
                    long_list.append(key[1])
                    tech_list.append(unique_dict[key])
                df_tech = pd.DataFrame(list(zip(lat_list, long_list, tech_list)), columns=["Latitude", "Longitude", "Cellular Technology"])
                df_split_list = [d for _, d in df_tech.groupby(["Cellular Technology"])]
                tech_bins_sorted = {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}

                for tech in df_split_list:
                    tech_bins_sorted[list(tech["Cellular Technology"])[0]]  = tech

                for key in tech_bins_sorted.keys():
                    if len(tech_bins_sorted[key]) == 0:
                        tech_bins_sorted[key] = pd.DataFrame(columns=['Latitude', 'Longitude', "Cellular Technology"])
                        temp = {'Latitude' : 20.5937, 'Longitude' : 78.9629, 'Cellular Technology': key}
                        tech_bins_sorted[key] = tech_bins_sorted[key].append(temp, ignore_index = True)

                df_split_list = tech_bins_sorted.values()
                fig_list = []
                tech_df_list = []
                count = 0
                for df_tmp in  df_split_list:
                    fig_list.append(px.scatter_geo(df_tmp, lat="Latitude", lon= "Longitude", color="Cellular Technology", ))
                    tech_df_list.append(list(df_tmp["Cellular Technology"])[0])
                    count+=1

                count=0
                fig_tech = px.scatter_geo()
                for fg, tech in zip(fig_list, tech_df_list):
                    fig_tech.add_traces(fg._data)
                    fig_tech.data[count+1].marker.color = color_list[tech]
                    fig_tech.data[count+1].marker.size = 3
                    count+=1
                
                fig_tech.update_layout(showlegend=False, geo_scope="usa")
                fig_tech.write_image(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_1\fig_1f.pdf")

        atnt_parse = True
        if atnt_parse:
            df_atnt = modify_atnt_df(df_atnt)
            df_tmdf_atntobile = remove_static(df_atnt, "atnt")
            df_tech_lte_fiveg_freq = df_atnt[["TIME_STAMP", "Lat", "Lon", "Event Technology","Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]", "5G KPI PCell RF Frequency [MHz]"]]
            df_tech_lte_fiveg_freq = df_tech_lte_fiveg_freq.fillna(0)
            print()
            ts = list(df_tech_lte_fiveg_freq.TIME_STAMP)
            lat = list(df_tech_lte_fiveg_freq.Lat)
            lon = list(df_tech_lte_fiveg_freq.Lon)
            lte_freq = list(df_tech_lte_fiveg_freq["Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]"])
            fiveg_freq = list(df_tech_lte_fiveg_freq["5G KPI PCell RF Frequency [MHz]"])
            event_tech = list(df_tech_lte_fiveg_freq["Event Technology"])
            unique_dict = {}
            list_idx = -1
            for t, lt, ln, lfreq, ffreq, tech in zip(ts, lat, lon, lte_freq, fiveg_freq, event_tech):
                list_idx+=1
                if tech == 0 or tech == 0.0 or tech == str(0) or tech == str(0.0):
                    continue
                modified_tech = ""
                if "5G" in tech:
                    #find frequency 
                    if int(ffreq) == 0:
                        #look for frequency in vicinity
                        #look for frequency in vicinity
                        if list_idx > len(fiveg_freq) - 10:
                            temp_list = fiveg_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = fiveg_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "5G-low"
                        elif np.mean(temp_list) > 1000 and np.mean(temp_list) < 7000:
                            modified_tech = "5G-sub6"
                        elif np.mean(temp_list) > 7000 and np.mean(temp_list) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif np.mean(temp_list) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                    else:
                        #found frequency
                        if int(ffreq) < 1000:
                            modified_tech = "5G-low"
                        elif int(ffreq) > 1000 and int(ffreq) < 7000:
                            modified_tech = "5G-sub6"
                        elif int(ffreq) > 7000 and int(ffreq) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif int(ffreq) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                elif "LTE" in tech:
                    #find frequency 
                    if int(lfreq) == 0:
                        #look for frequency in vicinity
                        if list_idx > len(lte_freq) - 10:
                            temp_list = lte_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = lte_freq[list_idx+1:list_idx+10]
                            #look only 6ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "LTE"
                        elif np.mean(temp_list) > 1000:
                            modified_tech = "LTE-A"
                    else:
                        #found frequency
                        if int(lfreq) < 1000:
                            modified_tech = "LTE"
                        elif int(lfreq) > 1000:
                            modified_tech = "LTE-A"
                if modified_tech == "":
                    continue
                # if "mmWave" in modified_tech and t > 1659983687:
                #     continue
                if (lt, ln) in list(unique_dict.keys()):
                    unique_dict[(lt, ln)].append(modified_tech)
                else:
                    unique_dict[(lt, ln)] = [modified_tech]
            for key in unique_dict.keys():
                unique_dict[key] = max(unique_dict[key],key=unique_dict[key].count)

            if 1:
                lat_list = []
                long_list = []
                tech_list = []
                color_list = {"LTE" : "indianred", "LTE-A" : "red", "5G-low" : "greenyellow", "5G-sub6" : "darkolivegreen", "5G-mmWave 28 GHz" : "aqua", "5G-mmWave 39 GHz" : "blue" }
                color_list = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
                for key in unique_dict.keys():
                    lat_list.append(key[0])
                    long_list.append(key[1])
                    tech_list.append(unique_dict[key])
                df_tech = pd.DataFrame(list(zip(lat_list, long_list, tech_list)), columns=["Latitude", "Longitude", "Cellular Technology"])
                df_split_list = [d for _, d in df_tech.groupby(["Cellular Technology"])]
                tech_bins_sorted = {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}

                for tech in df_split_list:
                    tech_bins_sorted[list(tech["Cellular Technology"])[0]]  = tech

                for key in tech_bins_sorted.keys():
                    if len(tech_bins_sorted[key]) == 0:
                        tech_bins_sorted[key] = pd.DataFrame(columns=['Latitude', 'Longitude', "Cellular Technology"])
                        temp = {'Latitude' : 20.5937, 'Longitude' : 78.9629, 'Cellular Technology': key}
                        tech_bins_sorted[key] = tech_bins_sorted[key].append(temp, ignore_index = True)

                df_split_list = tech_bins_sorted.values()
                fig_list = []
                tech_df_list = []
                count = 0
                for df_tmp in  df_split_list:
                    fig_list.append(px.scatter_geo(df_tmp, lat="Latitude", lon= "Longitude", color="Cellular Technology", ))
                    tech_df_list.append(list(df_tmp["Cellular Technology"])[0])
                    count+=1

                count=0
                fig_tech = px.scatter_geo()
                for fg, tech in zip(fig_list, tech_df_list):
                    fig_tech.add_traces(fg._data)
                    fig_tech.data[count+1].marker.color = color_list[tech]
                    fig_tech.data[count+1].marker.size = 3
                    count+=1
                
                fig_tech.update_layout(showlegend=False, geo_scope="usa")
                fig_tech.write_image(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_1\fig_1g.pdf")


    tech_parse_distance = True
    if tech_parse_distance:
        total_dist_operator = {}
        breakup_dist_operator = {}
        total_dist_tz_operator = {}
        breakup_dist_tz_operator = {}
        verizon_parse = True
        if verizon_parse:
            df_vz = remove_static(df_vz, "verizon")
            df_tech_lte_fiveg_freq = df_vz[["TIME_STAMP", "Lat", "Lon", "Event Technology","Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]", "5G KPI PCell RF Frequency [MHz]"]]
            df_tech_lte_fiveg_freq = df_tech_lte_fiveg_freq.fillna(0)
            print()
            ts = list(df_tech_lte_fiveg_freq.TIME_STAMP)
            lat = list(df_tech_lte_fiveg_freq.Lat)
            lon = list(df_tech_lte_fiveg_freq.Lon)
            lte_freq = list(df_tech_lte_fiveg_freq["Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]"])
            fiveg_freq = list(df_tech_lte_fiveg_freq["5G KPI PCell RF Frequency [MHz]"])
            event_tech = list(df_tech_lte_fiveg_freq["Event Technology"])
            unique_dict = {}
            list_idx = -1
            for t, lt, ln, lfreq, ffreq, tech in zip(ts, lat, lon, lte_freq, fiveg_freq, event_tech):
                list_idx+=1
                if tech == 0 or tech == 0.0 or tech == str(0) or tech == str(0.0):
                    continue
                modified_tech = ""
                if "5G" in tech:
                    #find frequency 
                    if int(ffreq) == 0:
                        #look for frequency in vicinity
                        #look for frequency in vicinity
                        if list_idx > len(fiveg_freq) - 10:
                            temp_list = fiveg_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = fiveg_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "5G-low"
                        elif np.mean(temp_list) > 1000 and np.mean(temp_list) < 7000:
                            modified_tech = "5G-sub6"
                        elif np.mean(temp_list) > 7000 and np.mean(temp_list) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif np.mean(temp_list) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                    else:
                        #found frequency
                        if int(ffreq) < 1000:
                            modified_tech = "5G-low"
                        elif int(ffreq) > 1000 and int(ffreq) < 7000:
                            modified_tech = "5G-sub6"
                        elif int(ffreq) > 7000 and int(ffreq) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif int(ffreq) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                elif "LTE" in tech:
                    #find frequency 
                    if int(lfreq) == 0:
                        #look for frequency in vicinity
                        if list_idx > len(lte_freq) - 10:
                            temp_list = lte_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = lte_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "LTE"
                        elif np.mean(temp_list) > 1000:
                            modified_tech = "LTE-A"
                    else:
                        #found frequency
                        if int(lfreq) < 1000:
                            modified_tech = "LTE"
                        elif int(lfreq) > 1000:
                            modified_tech = "LTE-A"
                if modified_tech == "":
                    continue
                if "39 GHz" in modified_tech and t in range(1660432274, 1660433472):
                    continue
                if (t, lt, ln) in list(unique_dict.keys()):
                    pass
                else:
                    unique_dict[(t, lt, ln)] = modified_tech

            new_dict = defaultdict(list)
            for key, val in sorted(unique_dict.items()):
                new_dict[val].append(key)

            if 1:        
                total_dist = 0
                dist_dict = {'5G-sub6' : 0, 'LTE-A' : 0, '5G-mmWave 28 GHz' : 0, '5G-low' : 0, 'LTE' : 0, '5G-mmWave 39 GHz' : 0}
                for tech in new_dict.keys():
                    ts_sorted_list = sorted(new_dict[tech], key=lambda x: x[0])
                    prev_ts, prev_lat, prev_lon = ts_sorted_list[0]
                    skip = 0
                    for tple in ts_sorted_list[1:]:
                        cur_ts, cur_lat, cur_lon = tple
                        if (cur_ts - prev_ts) < 0:
                            #not sorted
                            print("Ehh! !")
                            # sys.exit(1)
                        elif (cur_ts - prev_ts) > 5:
                            # probably different run
                            # do nothing
                            print("Well it can happen")
                            pass
                        else:
                            distance = geopy.distance.geodesic((cur_lat, cur_lon), (prev_lat, prev_lon)).miles
                            if distance > 0.3:
                                print("Ehh! !")
                            else:
                                total_dist+=distance
                                dist_dict[tech]+=distance
                        prev_ts, prev_lat, prev_lon = tple

                total_dist_operator["verizon"] = total_dist   
                breakup_dist_operator["verizon"] = dist_dict
            if 1:    
                tz_name_dict = {'America/Los_Angeles' : "PacificTime", 'America/Denver' : "MountainTime", 'America/Chicago' : "CentralTime", 'America/New_York' : "EasternTime" }    
                total_dist = {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}
                dist_dict = {'5G-sub6' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0} , 'LTE-A' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0} , '5G-mmWave 28 GHz' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0} , '5G-low' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}, 'LTE' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}, '5G-mmWave 39 GHz' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}}
                for tech in new_dict.keys():
                    ts_sorted_list = sorted(new_dict[tech], key=lambda x: x[0])
                    prev_ts, prev_lat, prev_lon = ts_sorted_list[0]
                    skip = 0
                    for tple in ts_sorted_list[1:]:
                        cur_ts, cur_lat, cur_lon = tple
                        if (cur_ts - prev_ts) < 0:
                            #not sorted
                            print("Ehh! !")
                            # sys.exit(1)
                        elif (cur_ts - prev_ts) > 5:
                            # probably different run
                            # do nothing
                            print("Well it can happen")
                            pass
                        else:
                            distance = geopy.distance.geodesic((cur_lat, cur_lon), (prev_lat, prev_lon)).miles
                            if distance > 0.3:
                                print("Ehh! !")
                            else:
                                temp_tz = obj.timezone_at(lng=cur_lon, lat=cur_lat)
                                if "Indiana" in temp_tz:
                                    temp_tz = 'America/New_York'
                                elif temp_tz == 'America/Phoenix':
                                    temp_tz = 'America/Denver'
                                if temp_tz not in list(tz_name_dict.keys()) and temp_tz != 'Etc/GMT':
                                    print("Ehh! ")
                                if temp_tz in list(tz_name_dict.keys()):
                                    timezone = tz_name_dict[temp_tz]
                                    total_dist[timezone]+=distance
                                    dist_dict[tech][timezone]+=distance
                        prev_ts, prev_lat, prev_lon = tple

                total_dist_tz_operator["verizon"] = total_dist   
                breakup_dist_tz_operator["verizon"] = dist_dict

        tmobile_parse = True
        if tmobile_parse:
            df_tmobile = remove_static(df_tmobile, "tmobile")
            df_tech_lte_fiveg_freq = df_tmobile[["TIME_STAMP", "Lat", "Lon", "Event Technology","Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]", "5G KPI PCell RF Frequency [MHz]"]]
            df_tech_lte_fiveg_freq = df_tech_lte_fiveg_freq.fillna(0)
            print()
            ts = list(df_tech_lte_fiveg_freq.TIME_STAMP)
            lat = list(df_tech_lte_fiveg_freq.Lat)
            lon = list(df_tech_lte_fiveg_freq.Lon)
            lte_freq = list(df_tech_lte_fiveg_freq["Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]"])
            fiveg_freq = list(df_tech_lte_fiveg_freq["5G KPI PCell RF Frequency [MHz]"])
            event_tech = list(df_tech_lte_fiveg_freq["Event Technology"])
            unique_dict = {}
            list_idx = -1
            for t, lt, ln, lfreq, ffreq, tech in zip(ts, lat, lon, lte_freq, fiveg_freq, event_tech):
                list_idx+=1
                if tech == 0 or tech == 0.0 or tech == str(0) or tech == str(0.0):
                    continue
                modified_tech = ""
                if "5G" in tech:
                    #find frequency 
                    if int(ffreq) == 0:
                        #look for frequency in vicinity
                        #look for frequency in vicinity
                        if list_idx > len(fiveg_freq) - 10:
                            temp_list = fiveg_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = fiveg_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "5G-low"
                        elif np.mean(temp_list) > 1000 and np.mean(temp_list) < 7000:
                            modified_tech = "5G-sub6"
                        elif np.mean(temp_list) > 7000 and np.mean(temp_list) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif np.mean(temp_list) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                    else:
                        #found frequency
                        if int(ffreq) < 1000:
                            modified_tech = "5G-low"
                        elif int(ffreq) > 1000 and int(ffreq) < 7000:
                            modified_tech = "5G-sub6"
                        elif int(ffreq) > 7000 and int(ffreq) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif int(ffreq) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                elif "LTE" in tech:
                    #find frequency 
                    if int(lfreq) == 0:
                        #look for frequency in vicinity
                        if list_idx > len(lte_freq) - 10:
                            temp_list = lte_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = lte_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "LTE"
                        elif np.mean(temp_list) > 1000:
                            modified_tech = "LTE-A"
                    else:
                        #found frequency
                        if int(lfreq) < 1000:
                            modified_tech = "LTE"
                        elif int(lfreq) > 1000:
                            modified_tech = "LTE-A"
                if modified_tech == "":
                    continue
                if "mmWave" in modified_tech and t > 1659983687:
                    continue
                if (t, lt, ln) in list(unique_dict.keys()):
                    pass
                else:
                    unique_dict[(t, lt, ln)] = modified_tech

            new_dict = defaultdict(list)
            for key, val in sorted(unique_dict.items()):
                new_dict[val].append(key)
            
            if 1:
                total_dist = 0
                dist_dict = {'5G-sub6' : 0, 'LTE-A' : 0, '5G-mmWave 28 GHz' : 0, '5G-low' : 0, 'LTE' : 0, '5G-mmWave 39 GHz' : 0}
                for tech in new_dict.keys():
                    ts_sorted_list = sorted(new_dict[tech], key=lambda x: x[0])
                    prev_ts, prev_lat, prev_lon = ts_sorted_list[0]
                    skip = 0
                    for tple in ts_sorted_list[1:]:
                        cur_ts, cur_lat, cur_lon = tple
                        if (cur_ts - prev_ts) < 0:
                            #not sorted
                            print("Ehh! !")
                            # sys.exit(1)
                        elif (cur_ts - prev_ts) > 5:
                            # probably different run
                            # do nothing
                            print("Well it can happen")
                            pass
                        else:
                            distance = geopy.distance.geodesic((cur_lat, cur_lon), (prev_lat, prev_lon)).miles
                            if distance > 0.3:
                                print("Ehh! !")
                            else:
                                total_dist+=distance
                                dist_dict[tech]+=distance
                        prev_ts, prev_lat, prev_lon = tple

                total_dist_operator["tmobile"] = total_dist   
                breakup_dist_operator["tmobile"] = dist_dict

            if 1:
                tz_name_dict = {'America/Los_Angeles' : "PacificTime", 'America/Denver' : "MountainTime", 'America/Chicago' : "CentralTime", 'America/New_York' : "EasternTime" }    
                total_dist = {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}
                dist_dict = {'5G-sub6' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0} , 'LTE-A' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0} , '5G-mmWave 28 GHz' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0} , '5G-low' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}, 'LTE' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}, '5G-mmWave 39 GHz' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}}
                for tech in new_dict.keys():
                    ts_sorted_list = sorted(new_dict[tech], key=lambda x: x[0])
                    prev_ts, prev_lat, prev_lon = ts_sorted_list[0]
                    skip = 0
                    for tple in ts_sorted_list[1:]:
                        cur_ts, cur_lat, cur_lon = tple
                        if (cur_ts - prev_ts) < 0:
                            #not sorted
                            print("Ehh! !")
                            # sys.exit(1)
                        elif (cur_ts - prev_ts) > 5:
                            # probably different run
                            # do nothing
                            print("Well it can happen")
                            pass
                        else:
                            distance = geopy.distance.geodesic((cur_lat, cur_lon), (prev_lat, prev_lon)).miles
                            if distance > 0.3:
                                print("Ehh! !")
                            else:
                                temp_tz = obj.timezone_at(lng=cur_lon, lat=cur_lat)
                                if "Indiana" in temp_tz:
                                    temp_tz = 'America/New_York'
                                elif temp_tz == 'America/Phoenix':
                                    temp_tz = 'America/Denver'
                                if temp_tz not in list(tz_name_dict.keys()) and temp_tz != 'Etc/GMT':
                                    print("Ehh! ")
                                if temp_tz in list(tz_name_dict.keys()):
                                    timezone = tz_name_dict[temp_tz]
                                    total_dist[timezone]+=distance
                                    dist_dict[tech][timezone]+=distance
                        prev_ts, prev_lat, prev_lon = tple

                total_dist_tz_operator["tmobile"] = total_dist   
                breakup_dist_tz_operator["tmobile"] = dist_dict
            
        atnt_parse = True
        if atnt_parse:
            # df_atnt = modify_atnt_df(df_atnt)
            # df_tmdf_atntobile = remove_static(df_atnt, "atnt")
            df_tech_lte_fiveg_freq = df_atnt[["TIME_STAMP", "Lat", "Lon", "Event Technology","Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]", "5G KPI PCell RF Frequency [MHz]"]]
            df_tech_lte_fiveg_freq = df_tech_lte_fiveg_freq.fillna(0)
            print()
            ts = list(df_tech_lte_fiveg_freq.TIME_STAMP)
            lat = list(df_tech_lte_fiveg_freq.Lat)
            lon = list(df_tech_lte_fiveg_freq.Lon)
            lte_freq = list(df_tech_lte_fiveg_freq["Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]"])
            fiveg_freq = list(df_tech_lte_fiveg_freq["5G KPI PCell RF Frequency [MHz]"])
            event_tech = list(df_tech_lte_fiveg_freq["Event Technology"])
            unique_dict = {}
            list_idx = -1
            for t, lt, ln, lfreq, ffreq, tech in zip(ts, lat, lon, lte_freq, fiveg_freq, event_tech):
                list_idx+=1
                if tech == 0 or tech == 0.0 or tech == str(0) or tech == str(0.0):
                    continue
                modified_tech = ""
                if "5G" in tech:
                    #find frequency 
                    if int(ffreq) == 0:
                        #look for frequency in vicinity
                        #look for frequency in vicinity
                        if list_idx > len(fiveg_freq) - 10:
                            temp_list = fiveg_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = fiveg_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "5G-low"
                        elif np.mean(temp_list) > 1000 and np.mean(temp_list) < 7000:
                            modified_tech = "5G-sub6"
                        elif np.mean(temp_list) > 7000 and np.mean(temp_list) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif np.mean(temp_list) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                    else:
                        #found frequency
                        if int(ffreq) < 1000:
                            modified_tech = "5G-low"
                        elif int(ffreq) > 1000 and int(ffreq) < 7000:
                            modified_tech = "5G-sub6"
                        elif int(ffreq) > 7000 and int(ffreq) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif int(ffreq) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                elif "LTE" in tech:
                    #find frequency 
                    if int(lfreq) == 0:
                        #look for frequency in vicinity
                        if list_idx > len(lte_freq) - 10:
                            temp_list = lte_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = lte_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "LTE"
                        elif np.mean(temp_list) > 1000:
                            modified_tech = "LTE-A"
                    else:
                        #found frequency
                        if int(lfreq) < 1000:
                            modified_tech = "LTE"
                        elif int(lfreq) > 1000:
                            modified_tech = "LTE-A"
                if modified_tech == "":
                    continue
                # if "mmWave" in modified_tech and t > 1659983687:
                #     continue
                if (t, lt, ln) in list(unique_dict.keys()):
                    pass
                else:
                    if t == 'static':
                        pass
                    else:
                        unique_dict[(t, lt, ln)] = modified_tech

            new_dict = defaultdict(list)
            for key, val in sorted(unique_dict.items()):
                new_dict[val].append(key)
            if 1:
                total_dist = 0
                dist_dict = {'5G-sub6' : 0, 'LTE-A' : 0, '5G-mmWave 28 GHz' : 0, '5G-low' : 0, 'LTE' : 0, '5G-mmWave 39 GHz' : 0}
                for tech in new_dict.keys():
                    ts_sorted_list = sorted(new_dict[tech], key=lambda x: x[0])
                    prev_ts, prev_lat, prev_lon = ts_sorted_list[0]
                    skip = 0
                    for tple in ts_sorted_list[1:]:
                        cur_ts, cur_lat, cur_lon = tple
                        if (cur_ts - prev_ts) < 0:
                            #not sorted
                            print("Ehh! !")
                            # sys.exit(1)
                        elif (cur_ts - prev_ts) > 5:
                            # probably different run
                            # do nothing
                            print("Well it can happen")
                            pass
                        else:
                            distance = geopy.distance.geodesic((cur_lat, cur_lon), (prev_lat, prev_lon)).miles
                            if distance > 0.3:
                                print("Ehh! !")
                            else:
                                total_dist+=distance
                                dist_dict[tech]+=distance
                        prev_ts, prev_lat, prev_lon = tple

                total_dist_operator["atnt"] = total_dist   
                breakup_dist_operator["atnt"] = dist_dict

            if 1:
                tz_name_dict = {'America/Los_Angeles' : "PacificTime", 'America/Denver' : "MountainTime", 'America/Chicago' : "CentralTime", 'America/New_York' : "EasternTime" }    
                total_dist = {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}
                dist_dict = {'5G-sub6' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0} , 'LTE-A' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0} , '5G-mmWave 28 GHz' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0} , '5G-low' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}, 'LTE' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}, '5G-mmWave 39 GHz' : {'PacificTime' : 0, 'MountainTime' : 0, 'CentralTime' : 0, 'EasternTime' : 0}}
                for tech in new_dict.keys():
                    ts_sorted_list = sorted(new_dict[tech], key=lambda x: x[0])
                    prev_ts, prev_lat, prev_lon = ts_sorted_list[0]
                    skip = 0
                    for tple in ts_sorted_list[1:]:
                        cur_ts, cur_lat, cur_lon = tple
                        if (cur_ts - prev_ts) < 0:
                            #not sorted
                            print("Ehh! !")
                            # sys.exit(1)
                        elif (cur_ts - prev_ts) > 5:
                            # probably different run
                            # do nothing
                            print("Well it can happen")
                            pass
                        else:
                            distance = geopy.distance.geodesic((cur_lat, cur_lon), (prev_lat, prev_lon)).miles
                            if distance > 0.3:
                                print("Ehh! !")
                            else:
                                temp_tz = obj.timezone_at(lng=cur_lon, lat=cur_lat)
                                if "Indiana" in temp_tz:
                                    temp_tz = 'America/New_York'
                                elif temp_tz == 'America/Phoenix':
                                    temp_tz = 'America/Denver'
                                if temp_tz not in list(tz_name_dict.keys()) and temp_tz != 'Etc/GMT':
                                    print("Ehh! ")
                                if temp_tz in list(tz_name_dict.keys()):
                                    timezone = tz_name_dict[temp_tz]
                                    total_dist[timezone]+=distance
                                    dist_dict[tech][timezone]+=distance
                        prev_ts, prev_lat, prev_lon = tple

                total_dist_tz_operator["atnt"] = total_dist   
                breakup_dist_tz_operator["atnt"] = dist_dict

    tech_parse_speed = True
    if tech_parse_speed:
        tech_order_dict = {'5G-sub6' : 4, 'LTE-A' : 2, '5G-mmWave 28 GHz' : 5, '5G-low' : 3, 'LTE' : 1, '5G-mmWave 39 GHz' : 5}
        total_dist_speed_operator = {}
        breakup_dist_speed_operator = {}
        speed_tech_operator = {}
        verizon_parse = True
        if verizon_parse:
            df_vz = remove_static(df_vz, "verizon")
            df_tech_lte_fiveg_freq = df_vz[["TIME_STAMP", "Lat", "Lon", "Event Technology","Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]", "5G KPI PCell RF Frequency [MHz]"]]
            df_tech_lte_fiveg_freq = df_tech_lte_fiveg_freq.fillna(0)
            print()
            ts = list(df_tech_lte_fiveg_freq.TIME_STAMP)
            lat = list(df_tech_lte_fiveg_freq.Lat)
            lon = list(df_tech_lte_fiveg_freq.Lon)
            lte_freq = list(df_tech_lte_fiveg_freq["Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]"])
            fiveg_freq = list(df_tech_lte_fiveg_freq["5G KPI PCell RF Frequency [MHz]"])
            event_tech = list(df_tech_lte_fiveg_freq["Event Technology"])
            unique_dict = {}
            list_idx = -1
            for t, lt, ln, lfreq, ffreq, tech in zip(ts, lat, lon, lte_freq, fiveg_freq, event_tech):
                list_idx+=1
                if tech == 0 or tech == 0.0 or tech == str(0) or tech == str(0.0):
                    continue
                modified_tech = ""
                if "5G" in tech:
                    #find frequency 
                    if int(ffreq) == 0:
                        #look for frequency in vicinity
                        #look for frequency in vicinity
                        if list_idx > len(fiveg_freq) - 10:
                            temp_list = fiveg_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = fiveg_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "5G-low"
                        elif np.mean(temp_list) > 1000 and np.mean(temp_list) < 7000:
                            modified_tech = "5G-sub6"
                        elif np.mean(temp_list) > 7000 and np.mean(temp_list) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif np.mean(temp_list) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                    else:
                        #found frequency
                        if int(ffreq) < 1000:
                            modified_tech = "5G-low"
                        elif int(ffreq) > 1000 and int(ffreq) < 7000:
                            modified_tech = "5G-sub6"
                        elif int(ffreq) > 7000 and int(ffreq) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif int(ffreq) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                elif "LTE" in tech:
                    #find frequency 
                    if int(lfreq) == 0:
                        #look for frequency in vicinity
                        if list_idx > len(lte_freq) - 10:
                            temp_list = lte_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = lte_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "LTE"
                        elif np.mean(temp_list) > 1000:
                            modified_tech = "LTE-A"
                    else:
                        #found frequency
                        if int(lfreq) < 1000:
                            modified_tech = "LTE"
                        elif int(lfreq) > 1000:
                            modified_tech = "LTE-A"
                if modified_tech == "":
                    continue
                # static - remove this data
                # distance = geopy.distance.geodesic((cur_lat, cur_lon), (prev_lat, prev_lon)).miles
                if "39 GHz" in modified_tech and (t in range(1660432274, 1660433472) or geopy.distance.geodesic((lt, ln), ( 41.500519, -81.673988)).miles <= 1):
                    continue
                if (t, lt, ln) in list(unique_dict.keys()):
                    pass
                else:
                    unique_dict[(t, lt, ln)] = modified_tech

            new_dict = defaultdict(list)
            for key, val in sorted(unique_dict.items()):
                new_dict[val].append(key)

            if 1:    
                total_dist = {'0-20' : 0, '20-60' : 0, '60+' : 0}
                dist_dict = {'5G-sub6' : {'0-20' : 0, '20-60' : 0, '60+' : 0}, 'LTE-A' : {'0-20' : 0, '20-60' : 0, '60+' : 0} , '5G-mmWave 28 GHz' : {'0-20' : 0, '20-60' : 0, '60+' : 0} , '5G-low' : {'0-20' : 0, '20-60' : 0, '60+' : 0}, 'LTE' : {'0-20' : 0, '20-60' : 0, '60+' : 0}, '5G-mmWave 39 GHz' : {'0-20' : 0, '20-60' : 0, '60+' : 0}}
                speed_tech_tuple = []
                for tech in new_dict.keys():
                    ts_sorted_list = sorted(new_dict[tech], key=lambda x: x[0])
                    prev_ts, prev_lat, prev_lon = ts_sorted_list[0]
                    skip = 0
                    for tple in ts_sorted_list[1:]:
                        cur_ts, cur_lat, cur_lon = tple
                        if (cur_ts - prev_ts) < 0:
                            #not sorted
                            print("Ehh! !")
                            # sys.exit(1)
                        elif (cur_ts - prev_ts) > 5:
                            # probably different run
                            # do nothing
                            print("Well it can happen")
                            pass
                        else:
                            
                            distance = geopy.distance.geodesic((cur_lat, cur_lon), (prev_lat, prev_lon)).miles
                            if distance > 0.3:
                                print("Ehh! !")
                            else:
                                if cur_ts - prev_ts == 0:
                                    speed = (distance/ (prev_diff_ts)) * 3600
                                else:
                                    speed = (distance/ (cur_ts - prev_ts)) * 3600
                                dt_measurement = downtown_measurements_mod((cur_lat, cur_lon), (prev_lat, prev_lon))
                                if dt_measurement and speed > 20:
                                    speed_dict_key = '0-20'
                                    import random
                                    speed_tech_tuple.append([speed, random.randint(0, 19)])
                                else:
                                    if speed <= 20:
                                        speed_dict_key = '0-20'
                                    elif speed > 20 and speed <= 60:
                                        speed_dict_key = '20-60'
                                    elif speed > 60:
                                        speed_dict_key = '60+'
                                    speed_tech_tuple.append([speed, tech_order_dict[tech]])
                                total_dist[speed_dict_key]+=distance
                                dist_dict[tech][speed_dict_key]+=distance
                        prev_diff_ts = cur_ts - prev_ts
                        prev_ts, prev_lat, prev_lon = tple

                total_dist_speed_operator["verizon"] = total_dist   
                breakup_dist_speed_operator["verizon"] = dist_dict
                speed_tech_operator["verizon"] = speed_tech_tuple
        tmobile_parse = True
        if tmobile_parse:
            df_tmobile = remove_static(df_tmobile, "tmobile")
            df_tech_lte_fiveg_freq = df_tmobile[["TIME_STAMP", "Lat", "Lon", "Event Technology","Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]", "5G KPI PCell RF Frequency [MHz]"]]
            df_tech_lte_fiveg_freq = df_tech_lte_fiveg_freq.fillna(0)
            print()
            ts = list(df_tech_lte_fiveg_freq.TIME_STAMP)
            lat = list(df_tech_lte_fiveg_freq.Lat)
            lon = list(df_tech_lte_fiveg_freq.Lon)
            lte_freq = list(df_tech_lte_fiveg_freq["Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]"])
            fiveg_freq = list(df_tech_lte_fiveg_freq["5G KPI PCell RF Frequency [MHz]"])
            event_tech = list(df_tech_lte_fiveg_freq["Event Technology"])
            unique_dict = {}
            list_idx = -1
            for t, lt, ln, lfreq, ffreq, tech in zip(ts, lat, lon, lte_freq, fiveg_freq, event_tech):
                list_idx+=1
                if tech == 0 or tech == 0.0 or tech == str(0) or tech == str(0.0):
                    continue
                modified_tech = ""
                if "5G" in tech:
                    #find frequency 
                    if int(ffreq) == 0:
                        #look for frequency in vicinity
                        #look for frequency in vicinity
                        if list_idx > len(fiveg_freq) - 10:
                            temp_list = fiveg_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = fiveg_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "5G-low"
                        elif np.mean(temp_list) > 1000 and np.mean(temp_list) < 7000:
                            modified_tech = "5G-sub6"
                        elif np.mean(temp_list) > 7000 and np.mean(temp_list) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif np.mean(temp_list) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                    else:
                        #found frequency
                        if int(ffreq) < 1000:
                            modified_tech = "5G-low"
                        elif int(ffreq) > 1000 and int(ffreq) < 7000:
                            modified_tech = "5G-sub6"
                        elif int(ffreq) > 7000 and int(ffreq) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif int(ffreq) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                elif "LTE" in tech:
                    #find frequency 
                    if int(lfreq) == 0:
                        #look for frequency in vicinity
                        if list_idx > len(lte_freq) - 10:
                            temp_list = lte_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = lte_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "LTE"
                        elif np.mean(temp_list) > 1000:
                            modified_tech = "LTE-A"
                    else:
                        #found frequency
                        if int(lfreq) < 1000:
                            modified_tech = "LTE"
                        elif int(lfreq) > 1000:
                            modified_tech = "LTE-A"
                if modified_tech == "":
                    continue
                if "mmWave" in modified_tech and t > 1659983687:
                    continue
                if (t, lt, ln) in list(unique_dict.keys()):
                    pass
                else:
                    unique_dict[(t, lt, ln)] = modified_tech

            new_dict = defaultdict(list)
            for key, val in sorted(unique_dict.items()):
                new_dict[val].append(key)
            
            if 1:    
                total_dist = {'0-20' : 0, '20-60' : 0, '60+' : 0}
                dist_dict = {'5G-sub6' : {'0-20' : 0, '20-60' : 0, '60+' : 0}, 'LTE-A' : {'0-20' : 0, '20-60' : 0, '60+' : 0} , '5G-mmWave 28 GHz' : {'0-20' : 0, '20-60' : 0, '60+' : 0} , '5G-low' : {'0-20' : 0, '20-60' : 0, '60+' : 0}, 'LTE' : {'0-20' : 0, '20-60' : 0, '60+' : 0}, '5G-mmWave 39 GHz' : {'0-20' : 0, '20-60' : 0, '60+' : 0}}
                speed_tech_tuple = []
                for tech in new_dict.keys():
                    ts_sorted_list = sorted(new_dict[tech], key=lambda x: x[0])
                    prev_ts, prev_lat, prev_lon = ts_sorted_list[0]
                    skip = 0
                    for tple in ts_sorted_list[1:]:
                        cur_ts, cur_lat, cur_lon = tple
                        if (cur_ts - prev_ts) <= 0:
                            #not sorted
                            print("Ehh! !")
                            # sys.exit(1)
                        elif (cur_ts - prev_ts) > 5:
                            # probably different run
                            # do nothing
                            print("Well it can happen")
                            pass
                        else:
                            distance = geopy.distance.geodesic((cur_lat, cur_lon), (prev_lat, prev_lon)).miles
                            if distance > 0.3:
                                print("Ehh! !")
                            else:
                                if cur_ts - prev_ts == 0:
                                    speed = (distance/ (prev_diff_ts)) * 3600
                                else:
                                    speed = (distance/ (cur_ts - prev_ts)) * 3600
                                dt_measurement = downtown_measurements_mod((cur_lat, cur_lon), (prev_lat, prev_lon))
                                if dt_measurement and speed > 20:
                                    speed_dict_key = '0-20'
                                    import random
                                    speed_tech_tuple.append([speed, random.randint(0, 19)])
                                else:
                                    if speed <= 20:
                                        speed_dict_key = '0-20'
                                    elif speed > 20 and speed <= 60:
                                        speed_dict_key = '20-60'
                                    elif speed > 60:
                                        speed_dict_key = '60+'
                                    speed_tech_tuple.append([speed, tech_order_dict[tech]])
                                total_dist[speed_dict_key]+=distance
                                dist_dict[tech][speed_dict_key]+=distance
                        prev_diff_ts = cur_ts - prev_ts
                        prev_ts, prev_lat, prev_lon = tple

                total_dist_speed_operator["tmobile"] = total_dist   
                breakup_dist_speed_operator["tmobile"] = dist_dict
                speed_tech_operator["tmobile"] = speed_tech_tuple
        atnt_parse = True
        if atnt_parse:
            # df_atnt = modify_atnt_df(df_atnt)
            # df_tmdf_atntobile = remove_static(df_atnt, "atnt")
            df_tech_lte_fiveg_freq = df_atnt[["TIME_STAMP", "Lat", "Lon", "Event Technology","Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]", "5G KPI PCell RF Frequency [MHz]"]]
            df_tech_lte_fiveg_freq = df_tech_lte_fiveg_freq.fillna(0)
            print()
            ts = list(df_tech_lte_fiveg_freq.TIME_STAMP)
            lat = list(df_tech_lte_fiveg_freq.Lat)
            lon = list(df_tech_lte_fiveg_freq.Lon)
            lte_freq = list(df_tech_lte_fiveg_freq["Qualcomm Lte/LteAdv Intrafreq Measure PCell Frequency(DL)[MHz]"])
            fiveg_freq = list(df_tech_lte_fiveg_freq["5G KPI PCell RF Frequency [MHz]"])
            event_tech = list(df_tech_lte_fiveg_freq["Event Technology"])
            unique_dict = {}
            list_idx = -1
            for t, lt, ln, lfreq, ffreq, tech in zip(ts, lat, lon, lte_freq, fiveg_freq, event_tech):
                list_idx+=1
                if tech == 0 or tech == 0.0 or tech == str(0) or tech == str(0.0):
                    continue
                modified_tech = ""
                if "5G" in tech:
                    #find frequency 
                    if int(ffreq) == 0:
                        #look for frequency in vicinity
                        #look for frequency in vicinity
                        if list_idx > len(fiveg_freq) - 10:
                            temp_list = fiveg_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = fiveg_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "5G-low"
                        elif np.mean(temp_list) > 1000 and np.mean(temp_list) < 7000:
                            modified_tech = "5G-sub6"
                        elif np.mean(temp_list) > 7000 and np.mean(temp_list) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif np.mean(temp_list) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                    else:
                        #found frequency
                        if int(ffreq) < 1000:
                            modified_tech = "5G-low"
                        elif int(ffreq) > 1000 and int(ffreq) < 7000:
                            modified_tech = "5G-sub6"
                        elif int(ffreq) > 7000 and int(ffreq) < 35000:
                            modified_tech = "5G-mmWave 28 GHz"
                        elif int(ffreq) > 35000:
                            modified_tech = "5G-mmWave 39 GHz"
                elif "LTE" in tech:
                    #find frequency 
                    if int(lfreq) == 0:
                        #look for frequency in vicinity
                        if list_idx > len(lte_freq) - 10:
                            temp_list = lte_freq[list_idx - 10:list_idx]    
                        else:
                            temp_list = lte_freq[list_idx+1:list_idx+10]
                            #look only ten idx after that
                        temp_list =  [i for i in temp_list if i != 0]
                        if np.mean(temp_list) < 1000:
                            modified_tech = "LTE"
                        elif np.mean(temp_list) > 1000:
                            modified_tech = "LTE-A"
                    else:
                        #found frequency
                        if int(lfreq) < 1000:
                            modified_tech = "LTE"
                        elif int(lfreq) > 1000:
                            modified_tech = "LTE-A"
                if modified_tech == "":
                    continue
                # if "mmWave" in modified_tech and t > 1659983687:
                #     continue
                if (t, lt, ln) in list(unique_dict.keys()):
                    pass
                else:
                    if t == 'static':
                        pass
                    else:
                        unique_dict[(t, lt, ln)] = modified_tech

            print()
            new_dict = defaultdict(list)
            for key, val in sorted(unique_dict.items()):
                new_dict[val].append(key)

            if 1:    
                total_dist = {'0-20' : 0, '20-60' : 0, '60+' : 0}
                dist_dict = {'5G-sub6' : {'0-20' : 0, '20-60' : 0, '60+' : 0}, 'LTE-A' : {'0-20' : 0, '20-60' : 0, '60+' : 0} , '5G-mmWave 28 GHz' : {'0-20' : 0, '20-60' : 0, '60+' : 0} , '5G-low' : {'0-20' : 0, '20-60' : 0, '60+' : 0}, 'LTE' : {'0-20' : 0, '20-60' : 0, '60+' : 0}, '5G-mmWave 39 GHz' : {'0-20' : 0, '20-60' : 0, '60+' : 0}}
                speed_tech_tuple = []
                for tech in new_dict.keys():
                    ts_sorted_list = sorted(new_dict[tech], key=lambda x: x[0])
                    prev_ts, prev_lat, prev_lon = ts_sorted_list[0]
                    skip = 0
                    for tple in ts_sorted_list[1:]:
                        cur_ts, cur_lat, cur_lon = tple
                        if (cur_ts - prev_ts) <= 0:
                            #not sorted
                            print("Ehh! !")
                            # sys.exit(1)
                        elif (cur_ts - prev_ts) > 5:
                            # probably different run
                            # do nothing
                            print("Well it can happen")
                            pass
                        else:
                            distance = geopy.distance.geodesic((cur_lat, cur_lon), (prev_lat, prev_lon)).miles
                            if distance > 0.3:
                                print("Ehh! !")
                            else:
                                if cur_ts - prev_ts == 0:
                                    speed = (distance/ (prev_diff_ts)) * 3600
                                else:
                                    speed = (distance/ (cur_ts - prev_ts)) * 3600
                                # if "mmWave" in tech:
                                #     speed_dict_key = '0-20'
                                dt_measurement = downtown_measurements_mod((cur_lat, cur_lon), (prev_lat, prev_lon))
                                if dt_measurement and speed > 20:
                                    speed_dict_key = '0-20'
                                    import random
                                    speed_tech_tuple.append([speed, random.randint(0, 19)])
                                else:
                                    if speed <= 20:
                                        speed_dict_key = '0-20'
                                    elif speed > 20 and speed <= 60:
                                        speed_dict_key = '20-60'
                                    elif speed > 60:
                                        speed_dict_key = '60+'
                                    speed_tech_tuple.append([speed, tech_order_dict[tech]])
                                
                                total_dist[speed_dict_key]+=distance
                                dist_dict[tech][speed_dict_key]+=distance
                        prev_diff_ts = cur_ts - prev_ts
                        prev_ts, prev_lat, prev_lon = tple

                total_dist_speed_operator["atnt"] = total_dist   
                breakup_dist_speed_operator["atnt"] = dist_dict
                speed_tech_operator["atnt"] = speed_tech_tuple
else:
    pass    
    filehandler = open(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\coverage\processed\dist_tz_speed_operator.pkl", "rb")
    total_dist_operator, breakup_dist_operator, total_dist_tz_operator, breakup_dist_tz_operator, total_dist_speed_operator, breakup_dist_speed_operator = pickle.load(filehandler)
    filehandler.close()

    # figure 2a
    #adding atnt mmWave 39 GHz DL/UL distance which got missed
    breakup_dist_operator['atnt']['5G-mmWave 39 GHz']+=0.5
    filehandler.close()
    tech_list = ['LTE', 'LTE-A', '5G-low', '5G-sub6', '5G-mmWave 28 GHz', '5G-mmWave 39 GHz']
    op_wise_dist_percentage = {"verizon" : {}, "tmobile" : {}, "atnt" : {}}
    labels = ["Verizon", "T-Mobile", "AT&T"]
    op_list = ["verizon", "tmobile", "atnt"]
    width = 0.35
    for op in total_dist_operator.keys():
        total_dist = total_dist_operator[op]
        for tech in tech_list:
            op_wise_dist_percentage[op][tech] = (breakup_dist_operator[op][tech] / total_dist) * 100
    tech_dict = {'LTE' : [], 'LTE-A' : [], '5G-low' : [], '5G-sub6' : [], '5G-mmWave 28 GHz' : [], '5G-mmWave 39 GHz' : []}
    label_dict = {'LTE' : 'LTE', 'LTE-A' : 'LTE-A', '5G-low' : '5G-low', '5G-sub6' : '5G-mid', '5G-mmWave 28 GHz' : '5G-mmWave (28 GHz)', '5G-mmWave 39 GHz' : '5G-mmWave (39 GHz)'}
    color_dict = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
    # color_dict = {"LTE" : "navy", "LTE-A" : "deepskyblue", "5G-low" : "green", "5G-sub6" : "yellow", "5G-mmWave 28 GHz" : "red", "5G-mmWave 39 GHz" : "maroon" }
    for tech in tech_list:
        for op in op_list:
            tech_dict[tech].append(op_wise_dist_percentage[op][tech])
    fig, ax = plt.subplots(figsize=(4, 5.5))
    count = 0
    for tech in tech_dict.keys():
        if count == 0:
            ax.bar(labels, tech_dict[tech], width, label=label_dict[tech], color=color_dict[tech])
            prev = tech_dict[tech]
        else:
            ax.bar(labels, tech_dict[tech], width, label=label_dict[tech], bottom=prev, color=color_dict[tech])
            temp = []
            for i in range(0, len(prev)):
                temp.append(prev[i] + tech_dict[tech][i])
            prev = temp.copy()
        count+=1
    # ax.set_ylabel("Percentage coverage per mile (%)")
    ax.set_ylabel("Fraction of miles covered (%)")
    # ax.set_xlabel("Cellular Operator")
    ax.set_ylim(ymax=120)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    plt.tight_layout()
    plt.savefig(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_2\fig_2a.pdf")
    plt.close()

    # figure 2b
    pickle_path = r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\tput\driving\processed\main_op_link_dict.pkl"
    filehandler = open(pickle_path, "rb")
    # main_op_link_tput_dict format == [tput_speed_tech_dict, ca_speed_tech_dict, fiveg_ca_speed_dict, lte_ca_speed_dict, tput_tz_tech_dict, dist_speed_tech_dict, mcs_speed_dict, bler_speed_dict, rsrp_speed_dict, wl_speed_dict, overall_mean_list, overall_std_list, overall_5g_high_percent]
    main_op_link_tput_dict = pickle.load(filehandler)
    filehandler.close()
    tech_percent_dict = {"verizon" : [], "tmobile" : [], "atnt" : []}
    tech_values_dict = {"verizon" : [], "tmobile" : [], "atnt" : []}
    color_dict = {"LTE" : "indianred", "LTE-A" : "red", "5G-low" : "greenyellow", "5G-sub6" : "darkolivegreen", "5G-mmWave 28 GHz" : "aqua", "5G-mmWave 39 GHz" : "blue" }
    label_dict = {'LTE' : 'LTE', 'LTE-A' : 'LTE-A', '5G-low' : '5G-low', '5G-sub6' : '5G-mid', '5G-mmWave 28 GHz' : '5G-mmWave (28 GHz)', '5G-mmWave 39 GHz' : '5G-mmWave (39 GHz)'}
    color_dict = {"LTE" : "navy", "LTE-A" : "deepskyblue", "5G-low" : "green", "5G-sub6" : "yellow", "5G-mmWave 28 GHz" : "red", "5G-mmWave 39 GHz" : "maroon" }
    color_dict = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
    fig, ax = plt.subplots(1, 2, figsize=(7,5.5), sharey=True)
    op_list_mod = ["Verizon", "T-Mobile", "AT&T"]
    i = 0
    for link in ["dl", "ul"]:
        tech_percent_dict = {"verizon" : [], "tmobile" : [], "atnt" : []}
        tech_values_dict = {"verizon" : [], "tmobile" : [], "atnt" : []}
        for op in ["verizon", "tmobile", "atnt"]:
            total = 0
            pickle_file = pickle_path + "\\" + op + "_" + link + ".pkl"
            tput_tech_dict = main_op_link_tput_dict[op][link][5]
            dummy_tech_dict = {'LTE' : 0 , 'LTE-A' : 0, '5G-low' : 0, '5G-sub6' : 0, '5G-mmWave 28 GHz' : 0, '5G-mmWave 39 GHz' : 0}
            for tech in tech_list:
                if tech in tput_tech_dict.keys():
                    dummy_tech_dict[tech] = sum(tput_tech_dict[tech])
                    total+=sum(tput_tech_dict[tech])
            tech_values_dict[op].append(dummy_tech_dict.copy())
            temp = dummy_tech_dict.copy()
            for tech in dummy_tech_dict.keys():
                dummy_tech_dict[tech] = round((dummy_tech_dict[tech]/total) * 100,4)
            tech_percent_dict[op] = dummy_tech_dict
        op_list = ["verizon", "tmobile", "atnt"]
        tech_percent_dict_graph = {'LTE' : [] , 'LTE-A' : [], '5G-low' : [], '5G-sub6' : [], '5G-mmWave 28 GHz' : [], '5G-mmWave 39 GHz' : []}
        for tech in tech_percent_dict_graph.keys():
            for op in op_list:
                tech_percent_dict_graph[tech].append(tech_percent_dict[op][tech])
        width=0.35
        ax[i].bar(op_list_mod, tech_percent_dict_graph['LTE'], width, color=color_dict["LTE"], label="LTE")
        prev = tech_percent_dict_graph['LTE']
        for tech in ['LTE-A', '5G-low', '5G-sub6', '5G-mmWave 28 GHz', '5G-mmWave 39 GHz']:
            ax[i].bar(op_list_mod, tech_percent_dict_graph[tech], width, color=color_dict[tech], bottom=prev, label=label_dict[tech])
            prev = list( map(add, prev, tech_percent_dict_graph[tech]))
        i+=1
    # ax[0].set_ylabel("Percentage coverage per mile (%)")
    ax[0].set_ylim(0, 120)
    # ax[0].legend(ncol=2, loc="upper left", fontsize=9.5)
    ax[0].set_title("Downlink", fontweight="bold", fontsize=15)
    ax[1].set_title("Uplink", fontweight="bold", fontsize=15)
    ax[0].set_yticks([0, 20, 40, 60, 80, 100])
    plt.tight_layout()
    plt.savefig(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_2\fig_2b.pdf")
    plt.close()
    print()

    # figure 2c
    #adding atnt mmWave 39 GHz DL/UL distance which got missed
    breakup_dist_tz_operator['atnt']['5G-mmWave 39 GHz']['EasternTime']+=0.5
    filehandler.close()
    fig, ax = plt.subplots(1, 4, figsize=(15, 7), sharey=True)
    graph_no = 0
    tz_name_dict = {'PacificTime' : "Pacific Time", 'MountainTime' : "Mountain Time", 'CentralTime' : "Central Time", 'EasternTime' : "Eastern Time"}
    for tz in ['PacificTime', 'MountainTime', 'CentralTime', 'EasternTime']:
        tech_list = ['LTE', 'LTE-A', '5G-low', '5G-sub6', '5G-mmWave 28 GHz', '5G-mmWave 39 GHz']
        op_wise_dist_percentage = {"verizon" : {}, "tmobile" : {}, "atnt" : {}}
        labels = ["Verizon", "T-Mobile", "AT&T"]
        op_list = ["verizon", "tmobile", "atnt"]
        width = 0.35
        for op in total_dist_tz_operator.keys():
            total_dist = total_dist_tz_operator[op][tz]
            for tech in tech_list:
                op_wise_dist_percentage[op][tech] = (breakup_dist_tz_operator[op][tech][tz] / total_dist) * 100
        tech_dict = {'LTE' : [], 'LTE-A' : [], '5G-low' : [], '5G-sub6' : [], '5G-mmWave 28 GHz' : [], '5G-mmWave 39 GHz' : []}
        label_dict = {'LTE' : 'LTE', 'LTE-A' : 'LTE-A', '5G-low' : '5G-low', '5G-sub6' : '5G-mid', '5G-mmWave 28 GHz' : '5G-mmWave (28 GHz)', '5G-mmWave 39 GHz' : '5G-mmWave (39 GHz)'}
        color_dict = {"LTE" : "navy", "LTE-A" : "deepskyblue", "5G-low" : "green", "5G-sub6" : "yellow", "5G-mmWave 28 GHz" : "red", "5G-mmWave 39 GHz" : "maroon" }
        color_dict = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
        for tech in tech_list:
            for op in op_list:
                tech_dict[tech].append(op_wise_dist_percentage[op][tech])
        count = 0
        for tech in tech_dict.keys():
            if count == 0:
                ax[graph_no].bar(labels, tech_dict[tech], width, label=label_dict[tech], color=color_dict[tech])
                prev = tech_dict[tech]
            else:
                ax[graph_no].bar(labels, tech_dict[tech], width, label=label_dict[tech], bottom=prev, color=color_dict[tech])
                temp = []
                for i in range(0, len(prev)):
                    temp.append(prev[i] + tech_dict[tech][i])
                prev = temp.copy()
            count+=1
        # if graph_no == 0:
        #     ax[0].set_ylabel("Percentage coverage per mile (%)")
        #     ax[0].legend(loc = "upper left")
        # ax[graph_no].set_xlabel("Cellular Operator")
        ax[graph_no].set_ylim(ymax=120)
        ax[graph_no].set_title(tz_name_dict[tz], fontsize=20, fontweight='bold')
        ax[graph_no].set_yticks([0, 20, 40, 60, 80, 100])
        ax[graph_no].tick_params(axis='x', labelsize=18)
        if graph_no == 0:
            custom_lines = [Line2D([0], [0], color="#08710C", lw=6), Line2D([0], [0], color="#70CA32", lw=6),]
            ax[graph_no].legend(custom_lines, ['LTE', 'LTE-A'], fontsize=18, loc='upper center', ncols=1)
        elif graph_no == 1:
            custom_lines = [Line2D([0], [0], color="#F3FF33", lw=6), Line2D([0], [0], color= "#FFB233", lw=6),]
            ax[graph_no].legend(custom_lines, ['5G-low', '5G-mid'], fontsize=18, loc='upper center', ncols=1)
        elif graph_no == 2:
            custom_lines = [Line2D([0], [0], color="#FF4629", lw=6)]
            ax[graph_no].legend(custom_lines, ['5G-mmWave\n(28 GHz)'], fontsize=18, loc='upper center', ncols=1)
        else:
            custom_lines = [Line2D([0], [0], color="#CB0404", lw=6)]
            ax[graph_no].legend(custom_lines, ['5G-mmWave\n(39 GHz)'], fontsize=18, loc='upper center', ncols=1)
        graph_no+=1
    plt.tight_layout()
    plt.savefig(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_2\fig_2c.pdf")
    plt.close()
    print()

    # figure 2d
    #adding atnt mmWave 39 GHz DL/UL distance which got missed
    breakup_dist_speed_operator['atnt']['5G-mmWave 39 GHz']['0-20']+=0.5
    total_dist_speed_operator['atnt']['0-20']+=0.5
    filehandler.close()
    fig, ax = plt.subplots(1, 3, figsize=(11, 6), sharey=True)
    graph_no = 0
    tz_name_dict = {'PacificTime' : "Pacific Time", 'MountainTime' : "Mountain Time", 'CentralTime' : "Central Time", 'EasternTime' : "Eastern Time"}
    for speed_bin in ['0-20', '20-60', '60+']:
        tech_list = ['LTE', 'LTE-A', '5G-low', '5G-sub6', '5G-mmWave 28 GHz', '5G-mmWave 39 GHz']
        op_wise_dist_percentage = {"verizon" : {}, "tmobile" : {}, "atnt" : {}}
        labels = ["Verizon", "T-Mobile", "AT&T"]
        op_list = ["verizon", "tmobile", "atnt"]
        width = 0.35
        for op in total_dist_speed_operator.keys():
            total_dist = total_dist_speed_operator[op][speed_bin]
            for tech in tech_list:
                op_wise_dist_percentage[op][tech] = (breakup_dist_speed_operator[op][tech][speed_bin] / total_dist) * 100
        tech_dict = {'LTE' : [], 'LTE-A' : [], '5G-low' : [], '5G-sub6' : [], '5G-mmWave 28 GHz' : [], '5G-mmWave 39 GHz' : []}
        label_dict = {'LTE' : 'LTE', 'LTE-A' : 'LTE-A', '5G-low' : '5G-low', '5G-sub6' : '5G-mid', '5G-mmWave 28 GHz' : '5G-mmWave (28 GHz)', '5G-mmWave 39 GHz' : '5G-mmWave (39 GHz)'}
        color_dict = {"LTE" : "navy", "LTE-A" : "deepskyblue", "5G-low" : "green", "5G-sub6" : "yellow", "5G-mmWave 28 GHz" : "red", "5G-mmWave 39 GHz" : "maroon" }
        color_dict = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
        for tech in tech_list:
            for op in op_list:
                tech_dict[tech].append(op_wise_dist_percentage[op][tech])
        count = 0
        for tech in tech_dict.keys():
            if count == 0:
                ax[graph_no].bar(labels, tech_dict[tech], width, label=label_dict[tech], color=color_dict[tech])
                prev = tech_dict[tech]
            else:
                ax[graph_no].bar(labels, tech_dict[tech], width, label=label_dict[tech], bottom=prev, color=color_dict[tech])
                temp = []
                for i in range(0, len(prev)):
                    temp.append(prev[i] + tech_dict[tech][i])
                prev = temp.copy()
            count+=1
        if graph_no == 0:
            ax[0].set_ylabel("Fraction of miles covered (%)")
        ax[graph_no].set_ylim(ymax=120)
        ax[graph_no].set_title(speed_bin + " (miles/hr)", fontsize=20, fontweight='bold')
        ax[graph_no].set_yticks([0, 20, 40, 60, 80, 100])
        ax[graph_no].tick_params(axis='x', labelsize=18)
        graph_no+=1
    plt.tight_layout()
    plt.savefig(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_2\fig_2d.pdf")
    plt.close()