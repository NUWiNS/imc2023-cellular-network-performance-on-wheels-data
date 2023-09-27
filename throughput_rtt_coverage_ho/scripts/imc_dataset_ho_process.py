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
import us 
from timezonefinder import TimezoneFinder
obj = TimezoneFinder()
import geopy.distance
import time
from collections import OrderedDict
import warnings
warnings.filterwarnings("ignore")


arfcn_freq_dict = {'177020' : 885.100, '2083329' : 28249.800, '2071667' : 27550.080, '648672' : 3730.080, '2078331' : 27949.920, '2073333' : 27650.040, '177000' : 885.000, '174800' : 874.000, '175000' : 875.000, '650004' : 3750.060, '2239999' : 37650.000, '125400' : 627.000, '125900' : 629.500, '126400' : 632.000, '126490' :632.450, '126510' : 632.550, '126530' : 632.650, '126900' : 634.500, '506280' : 2531.400, '508296' : 2541.480, '509202' : 2546.010, '514056' : 2570.280, '520020' : 2600.100, '525204' :2626.020, '526002' : 2630.010, '526404' : 2632.020, '527202' : 2636.010, '528000' : 2640.000, '528696' : 2643.480, '529998' : 2649.990, '530700' : 2653.500}

earfcn_freq_dict = {'1000' : 1970.00, '1025' :  1972.50, '1050' : 1975, '1075' : 1977.50, '1125' : 1982.50 , '2100' : 2125.00, '2450' : 874.0, '2460' : 875.0, '2559' : 884.90, '2560' : 885.00, '2561' : 885.10, '2600' : 889.00, '5230' : 751.00, '5780' : 739.00, '66486' : 2115.00, '66536' : 2120.00, '66561' : 2122.50, '66586' : 2125.00, '66611' : 2127.50, '66636' : 2130.0, '66686' : 2135.00, '66711' : 2137.50, '66761' : 2142.50, '66786' : 2145.00, '66811' : 2147.50, '66836' : 2150.00, '66911' : 2157.50, '66936' : 2160.00, '66986' : 2165.00, '67011' : 2167.50, '67086' : 2175.00, '750' : 1945.00, '775' : 1947.50, '825' : 1952.50, '925' : 1962.50, '950' : 1965.00, '975' : 1967.50, '800' : 1950, '1025' :  1972.50, '1075' : 1977.50, '1100' : 1980.00, '1125' : 1982.50, '1150' : 1985.00, '2175' : 2132.50, '41094' : 2640.40, '41490' : 2680.00, '5035' : 731.50, '5090' : 737.00, '5110' : 739.00, '5145' : 742.50, '5330' : 763.00, '625' : 1932.50, '650' : 1935.00, '66461' : 2112.50, '66486' : 2115.00, '66511' : 2117.50, '66611' : 2127.50, '66661' : 2132.50, '66686' : 2135.00, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66936' : 2160.00, '66985' : 2164.90, '66986' : 2165.00, '67086' : 2175.00, '675' : 1937.50, '700' : 1940.00, '800' : 1950.00, '850' : 1955.00, '875' : 1957.50, '900' : 1960.00, '925' : 1962.50, '950' : 1965, '9820' : 765.00, '1099' : 1979.90, '1100' : 1980.00, '1123' : 1982.30, '1125' : 1982.50, '1126' : 1982.60, '1148' : 1984.80, '1150' : 1985.00, '2000' : 2115.00, '2050' : 2120.00, '2125' : 2127.50, '2175' : 2132.50, '2200' : 2135.00, '2225' : 2137.50, '2300' : 2145.00, '2325' : 2147.50, '2460': 875.0,  '39750' : 2506.00, '39907' : 2521.70, '39948' : 2525.80, '40072' : 2538.20, '40384' : 2569.40, '40770' : 2608.00, '40810' : 2612.00, '41176' : 2648.60, '41238' : 2654.80, '41490' : 2680.00, '5035' : 731.50, '5090' : 737, '5095' : 737.50, '5110' : 739.00, '5330' : 763.00, '5780' : 739, '5815': 742.5, '66486': 2115.00, '66487' : 2115.10, '66536' : 2120.00, '66561' : 2122.5, '66586' : 2125, '66661' : 2132.50, '66686' : 2135, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66811': 2147.5, '66836': 2150, '66886': 2150, '66911': 2150, '66961': 2150, '66986' : 2165.00, '67011': 2167.5, '675' : 1937.50, '676': 1937.6, '677': 1937.7, '68611': 619.5, '68636': 622, '68661': 624.5, '68686': 627, '68786': 637, '68836': 637, '68861': 637, '68886': 637, '68911': 649.5, '700' : 1940.00, '725': 1942.5, '750': 1942.5, '775': 1942.5, '801': 1950.1, '8115': 1937.5, '825': 1952.5, '8264': 1952.4, '8290': 1952.4, '8315': 1952.4, '8465': 1972.5, '850' : 1955.00, '851': 1955.1, '852': 1955.1, '8539': 1979.9, '8562': 1982.2, '8640': 1982.2, '8665': 1992.5, '875' : 1957.50, '876': 1957.6, '8763': 866.3, '877': 1957.7, '8950': 885, '901': 1960.1, '925' : 1962.50, '41305' : 2661.50, '66761' : 2142.50, '132122' : 1747.5}

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
                print("!")
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
        print("2!")
        sys.exit(1)

    return mod_speed_list


base = r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\tput\driving"
main_op_link_ho_per_mile_dict = {"verizon" : {"dl" : 0, "ul" : 0}, "tmobile" : {"dl" : 0, "ul" : 0}, "atnt" : {"dl" : 0, "ul" : 0}}
main_op_link_ho_duration_dict = {"verizon" : {"dl" : 0, "ul" : 0}, "tmobile" : {"dl" : 0, "ul" : 0}, "atnt" : {"dl" : 0, "ul" : 0}}
main_op_link_ho_tput_dict = {"verizon" : {"dl" : 0, "ul" : 0}, "tmobile" : {"dl" : 0, "ul" : 0}, "atnt" : {"dl" : 0, "ul" : 0}}
for op in ["verizon", "tmobile", "atnt"]:
    for link in ["dl", "ul"]:
        csv_directory_list = glob.glob(base + "\\" + op + "\\" + link + "\\*.csv")
        global_idx = 1
        count = 0
        ho_count_list = []
        dist_list = []
        ho_per_mile_list = []
        lat_lon_list = []
        for csv in csv_directory_list:
            df_short = pd.read_csv(csv)
            if link == "dl":
                df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"].notna()]
                df_short_tput = df_short_tput[df_short_tput["Smart Phone Smart Throughput Mobile Network Rx Byte"] > 10000]
            else:
                df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].notna()]
                df_short_tput = df_short_tput[df_short_tput["Smart Phone Smart Throughput Mobile Network Tx Byte"] > 10000]
            df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
            if len(df_short_ho) != 0:
                df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].str.contains("Handover Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Success")]
            df_merged = pd.concat([df_short_tput, df_short_ho])
            df_merged = df_merged.sort_values(by=["TIME_STAMP"])
            df_merged.reset_index(inplace=True)
            # continue
            if len(df_merged) <5:
                # what's the point?
                global_idx+=1
                continue
            break_list = []
            event = -99
            start_flag = 0
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
            # now calculate technology - throughput
            issue_count = 0
            start = 1
            start_trace = 1
            jump_sequence = 0
            sum_dist = 0
            ho_count = len(break_list) - 1
            prev_lat = prev_lon = None
            for tput_df in break_list:
                if len(tput_df) == 0:
                    continue
                if len(tput_df) == 1:
                    if len(list(tput_df["Lat"].dropna())) > 0:
                        try:
                            prev_lat = list(tput_df["Lat"].dropna())[0]
                            prev_lon = list(tput_df["Lon"].dropna())[0]
                            continue
                        except:
                            prev_lat = prev_lon = None
                            continue
                    else:
                        continue

                if prev_lat != None and prev_lon != None:
                    lat_list = list(tput_df["Lat"].dropna())
                    lon_list = list(tput_df["Lon"].dropna())
                else:
                    try:
                        prev_lat = list(tput_df["Lat"].dropna())[0]
                        prev_lon = list(tput_df["Lon"].dropna())[0]
                    except:
                        prev_lat = prev_lon = None
                        continue
                    try:
                        lat_list = list(tput_df["Lat"].dropna())[1:]
                        lon_list = list(tput_df["Lon"].dropna())[1:]
                    except:
                        continue
                
                for current_lat, current_lon in zip(lat_list, lon_list):
                    dist = geopy.distance.geodesic((current_lat, current_lon), (prev_lat, prev_lon)).miles
                    if dist > 0.1:
                        # get a hint if it is static or gps error
                        prev_lat = current_lat
                        prev_lon = current_lon
                        continue
                    else:
                        sum_dist+=dist
                        prev_lat = current_lat
                        prev_lon = current_lon
                prev_lat = prev_lon = None

            if sum_dist >= 0.01:
                ho_count_list.append(ho_count)
                dist_list.append(sum_dist)
                ho_per_mile_list.append(round((ho_count / sum_dist), 2))
                lat_lon_list.append((df_merged.Lat.dropna().median(), df_merged.Lon.dropna().median()))

        main_op_link_ho_per_mile_dict[op][link] = [lat_lon_list, ho_count_list, dist_list, ho_per_mile_list]


for op in ["verizon", "tmobile", "atnt"]:
    for link in ["dl", "ul"]:
        csv_directory_list = glob.glob(base + "\\" + op + "\\" + link + "\\*.csv")
        count = 0
        ho_duration = []
        for csv in csv_directory_list:
            df_short = pd.read_csv(csv)
            count+=1
            if link == "dl":
                df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"].notna()]
                df_short_tput = df_short_tput[df_short_tput["Smart Phone Smart Throughput Mobile Network Rx Byte"] > 10000]
            else:
                df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].notna()]
                df_short_tput = df_short_tput[df_short_tput["Smart Phone Smart Throughput Mobile Network Tx Byte"] > 10000]
            df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
            if len(df_short_ho) != 0:
                df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].str.contains("Handover Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Success") | df_short['Event 5G-NR/LTE Events'].str.contains('PRACH: Msg4') | df_short['Event 5G-NR/LTE Events'].str.contains('PRACH: Msg2') | df_short['Event 5G-NR/LTE Events'].str.contains("Handover Attempt") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Attempt") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Attempt")]
            if len(df_short_ho) == 0:
                # no handover events observed
                continue
            df_merged = pd.concat([df_short_tput, df_short_ho])
            df_merged = df_merged.sort_values(by=["TIME_STAMP"])
            df_merged.reset_index(inplace=True)
            # continue
            if len(df_merged) <5:
                # what's the point?
                continue
            df_merged.to_clipboard()
            break_list = []
            break_ho_events_list = []
            break_ho_events_ts_list = []
            event = -99
            start_flag = 0
            temp_ho_events_break = []
            temp_ho_events_ts_break = []
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
                        temp_ho_events_break.append(row['Event 5G-NR/LTE Events'])
                        temp_ho_events_ts_break.append(row['TIME_STAMP'])
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
                        #add new event to event list
                        temp_ho_events_break.append(row['Event 5G-NR/LTE Events'])
                        temp_ho_events_ts_break.append(row['TIME_STAMP'])
                    elif event == 1 and pd.notnull(row['Event 5G-NR/LTE Events']):
                        # continue with event
                        temp_ho_events_break.append(row['Event 5G-NR/LTE Events'])
                        temp_ho_events_ts_break.append(row['TIME_STAMP'])
                        continue
                    elif event == 1 and pd.isnull(row['Event 5G-NR/LTE Events']):
                        # event stopped and throughput started
                        # set event to 0
                        # set start and end index count to current index + 1
                        event = 0
                        start_index_count = index
                        end_index_count = index
                        #add old event to break_ho_events_list
                        break_ho_events_list.append(temp_ho_events_break)
                        break_ho_events_ts_list.append(temp_ho_events_ts_break)
                        temp_ho_events_break = []
                        temp_ho_events_ts_break = []
            
            if event == 0:
                # add the last throughput value
                # if df_merged[start_index_count:end_index_count+1] != break_list[-1]:
                break_list.append(df_merged[start_index_count:end_index_count+1])
            if event == 1 and len(temp_ho_events_break) > 0:
                break_ho_events_list.append(temp_ho_events_break)
                break_ho_events_ts_list.append(temp_ho_events_ts_break)

            for event_cluster, time_stamp_list, tput_df in zip(break_ho_events_list, break_ho_events_ts_list, break_list):
                attempt_message = 0
                success_message = 0
                attempt_index_list = []
                msg2 = 0
                msg4 = 0
                event_idx = -1
                for events in event_cluster:
                    event_idx+=1
                    if "Attempt" in events:
                        attempt_message+=1
                        attempt_index_list.append(event_idx)
                    if "Success" in events:
                        success_message+=1
                    if "Msg2" in events:
                        msg2+=1
                    if "Msg4" in events:
                        msg4+=1
                
                if attempt_message == 0:
                    # not diff to calculate
                    continue
                if attempt_message == 0 and success_message == 0:
                    # not a handover
                    continue
                if (success_message > 1 and len(event_cluster) >= 10) or (len(event_cluster) >= 10):
                    # end of trace
                    last_ts_tput = list(tput_df["TIME_STAMP"])[-1]
                    if time_stamp_list[0] - last_ts_tput > 0.6:
                        # non contiguous point
                        # ignore this
                        continue
                    else:
                        # check the event duration
                        if time_stamp_list[-1] - time_stamp_list[0] > 2:
                            # non contiguous 
                            continue
                        else:
                            print()
                    continue
                if len(event_cluster) <= 1:
                    # cannot calculate diff
                    continue
                if msg2 == 0 and msg4 == 0:
                    # cannot calculate time diff
                    continue
                if attempt_message > 0 and success_message == 0:
                    # failed handover most probably
                    continue
                if attempt_message == 1 and success_message == 1:
                    # check the diff of  timestamp in this list
                    # if ts > 2 seconds, then the list is cut in between from some other handover - XCAL logging issue
                    if time_stamp_list[-1] - time_stamp_list[0] > 2:
                        continue
                # in all probability diff can be calculated now
                if (time_stamp_list[-1] - time_stamp_list[attempt_index_list[-1]]) > 0.5:
                    # last check to see if the df missed timestamps after throughput test or not
                    last_ts_tput = list(tput_df["TIME_STAMP"])[-1]
                    if time_stamp_list[0] - last_ts_tput > 0.6:
                        # non contiguous point
                        # ignore this
                        continue
                    else:
                        print()
                ho_duration.append(time_stamp_list[-1] - time_stamp_list[attempt_index_list[-1]])

        main_op_link_ho_duration_dict[op][link] = ho_duration


for op in ["verizon", "tmobile", "atnt"]:
    for link in ["dl", "ul"]:
        csv_directory_list = glob.glob(base + "\\" + op + "\\" + link + "\\*.csv")
        count = 0
        ho_vector = []
        tput_vector = []
        speed_vector = []
        tech_vector = []
        pre_post_ho_tput_diff = {"4G->5G" : [], "5G->4G" : [], "4G->4G" : [], "5G->5G" : [], "5G->4G->5G" : []}
        pre_ho_list = {"4G->5G" : [], "5G->4G" : [], "4G->4G" : [], "5G->5G" : [], "5G->4G->5G" : []}
        post_ho_list = {"4G->5G" : [], "5G->4G" : [], "4G->4G" : [], "5G->5G" : [], "5G->4G->5G" : []}
        all_ho_t_list = []
        for csv in csv_directory_list:
            df_short = pd.read_csv(csv)
            count+=1
            if "atnt" in csv and 'ul' in csv and 'trial_57' in csv:
                print()
            if link == "dl":
                df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"].notna()]
                df_short_tput = df_short_tput[df_short_tput["Smart Phone Smart Throughput Mobile Network Rx Byte"] > 10000]
            else:
                df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].notna()]
                df_short_tput = df_short_tput[df_short_tput["Smart Phone Smart Throughput Mobile Network Tx Byte"] > 10000]
            df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
            if len(df_short_ho) != 0:
                df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].str.contains("Handover Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Success")]
            # df_short_ho = df_short_ho[df_short_ho['Event 5G-NR/LTE Events'].str.contains("Failure") == False]
            if len(df_short_ho) == 0:
                # no handover events observed
                continue
            df_merged = pd.concat([df_short_tput, df_short_ho])
            df_merged = df_merged.sort_values(by=["TIME_STAMP"])
            df_merged.reset_index(inplace=True)
            # continue
            if len(df_merged) <5:
                # what's the point?
                continue
            if len(df_merged["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) == 0:
                continue
            break_list = []
            event = -99
            start_flag = 0
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
            # now calculate technology - throughput
            issue_count = 0
            start = 1
            ho_count = 0
            start_trace = 1
            jump_sequence = 0
            prev_cell = break_list[0]

            for tput_df in break_list[1:]:
                current_cell = tput_df
                #first check if the time difference between the prev df last val and the current df first val is within 1 second
                if list(current_cell["TIME_STAMP"].dropna())[0] - list(prev_cell["TIME_STAMP"].dropna())[-1] > 0.5:
                    if jump_sequence == 1:
                        # does not really make sense to carry on with jump sequence as the previous value of t3 is meaningless now to calculate handover diff
                        jump_sequence = 0
                    prev_cell = current_cell.copy()
                    continue
                # first check if both the list has more than 1 value or not 
                if start_trace == 1:
                    if len(prev_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) == 1:
                        # do not consider that fragment
                        prev_cell = current_cell.copy()
                        continue
                    elif len(prev_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) > 1:
                        start_trace = 0 

                if not jump_sequence:
                    t1 = t2 = t3 = t4 = t5 = None
                    if len(prev_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) == 1:
                        t1 = list(prev_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[0]
                        t2 = list(prev_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[0]
                    elif len(prev_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) > 1:
                        t1 = list(prev_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[-2]
                        t2 = list(prev_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[-1]
                    else:
                        t2 = 0
                        t2 = 0

                    if len(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) == 1:
                        # average it with next t3 - jump
                        jump_sequence = 1
                        t3 = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())
                        prev_cell = current_cell.copy()
                        continue
                    elif len(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) == 2:
                        t3 = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[0]
                        t4 = t5 = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[1]
                    elif len(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) > 2:
                        t3 = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[0]
                        t4 = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[1]
                        t5 = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[2]
                    else:
                        t3 = 0
                        t4 = 0
                        t5 = 0
                else:
                    # jump sequence, we just need a new t3 to be averaged
                    if len(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) == 1:
                        #still one value, average it
                        t3.append(list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[0])
                        continue
                    else:
                        jump_sequence = 0
                        if len(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) == 2:
                            t3 = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[0]
                            t4 = t5 = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[1]
                        elif len(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna()) > 2:
                            t3.append(list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[0])
                            t3 = np.mean(t3)
                            t4 = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[1]
                            t5 = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())[2]

                #check type of handover
                try:
                    lte_cell_1 = list(prev_cell["LTE KPI PCell Serving PCI"].dropna())
                    if len(lte_cell_1) == 0:
                        lte_cell_1 = None
                    else:
                        lte_cell_1 = int(max(set(lte_cell_1), key=lte_cell_1.count))
                except:
                    lte_cell_1 = None
                try:
                    lte_cell_2 = list(current_cell["LTE KPI PCell Serving PCI"].dropna())
                    if len(lte_cell_2) == 0:
                        lte_cell_2 = None
                    else:
                        lte_cell_2 = int(max(set(lte_cell_2), key=lte_cell_2.count))
                except:
                    lte_cell_2 = None

                try:
                    fiveg_cell_1 = list(prev_cell["5G KPI PCell RF Serving PCI"].dropna())
                    if len(fiveg_cell_1) == 0:
                        fiveg_cell_1 = None
                    else:
                        fiveg_cell_1 = int(max(set(fiveg_cell_1), key=fiveg_cell_1.count))
                except:
                    fiveg_cell_1 = None
                try:
                    fiveg_cell_2 = list(current_cell["5G KPI PCell RF Serving PCI"].dropna())
                    if len(fiveg_cell_2) == 0:
                        fiveg_cell_2 = None
                    else:
                        fiveg_cell_2 = int(max(set(fiveg_cell_2), key=fiveg_cell_2.count))
                except:
                    fiveg_cell_2 = None

                # pre_post_ho_tput_diff = {"only-4G-changed" : [], "only-5G-changed" : [], "both-4G-5G-changed" : []}
                if (lte_cell_1 != lte_cell_2) and  (fiveg_cell_1 != fiveg_cell_2):
                    # both 4g and 5g changed
                    if fiveg_cell_1 == None and fiveg_cell_2 != None:
                        key="4G->5G"
                    elif fiveg_cell_1 != None and fiveg_cell_2 == None:
                        key="5G->4G"
                    else:
                        key="5G->4G->5G"
                elif (lte_cell_1 == lte_cell_2) and  (fiveg_cell_1 != fiveg_cell_2):
                    # only 5g changed
                    if fiveg_cell_1 == None and fiveg_cell_2 != None:
                        # 4G -> 5G
                        key="4G->5G"
                    elif fiveg_cell_1 != None and fiveg_cell_2 == None:
                        # 4G <- 5G
                        key="5G->4G"
                    elif fiveg_cell_1 != None and fiveg_cell_2 != None:
                        # 5G -> 5G
                        key="5G->5G"
                elif (lte_cell_1 != lte_cell_2) and  (fiveg_cell_1 == fiveg_cell_2):
                    # only 4g changed changed
                    key = "4G->4G"

                elif (lte_cell_1 == lte_cell_2) and  (fiveg_cell_1 == fiveg_cell_2):
                    #nothing changed
                    #not a handover
                    key = "no-change"
                    prev_cell = current_cell
                    continue
                else:
                    print("!")
                prev_cell = current_cell.copy()

                pre_post_ho_tput_diff[key].append(float(np.mean([t5, t4])) - float(np.mean([t2, t1])))
                pre_ho_list[key].append(np.mean([t5, t4]))
                post_ho_list[key].append(np.mean([t2, t1]))
                all_ho_t_list.append([t1, t2, t3, t4, t5])


                current_cell_tput_list = list(current_cell["Smart Phone Smart Throughput Mobile Network %s Throughput [Mbps]" %str(link.upper())].dropna())
                # remove first value as that was part of t3 or was t3
                current_cell_tput_list = current_cell_tput_list[1:]

        all_list = [pre_ho_list, post_ho_list, pre_post_ho_tput_diff, all_ho_t_list]
        main_op_link_ho_tput_dict[op][link] = all_list

filehandler = open(r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\ho\processed\main_op_link_ho_per_mile_dict.pkl", "wb")
pickle.dump(main_op_link_ho_per_mile_dict, filehandler)
filehandler.close()

filehandler = open(r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\ho\processed\main_op_link_ho_duration_dict.pkl", "wb")
pickle.dump(main_op_link_ho_duration_dict, filehandler)
filehandler.close()

filehandler = open(r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\ho\processed\main_op_link_ho_tput_dict.pkl", "wb")
pickle.dump(main_op_link_ho_tput_dict, filehandler)
filehandler.close()