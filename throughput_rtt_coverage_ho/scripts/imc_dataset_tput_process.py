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
import scipy.stats
import warnings
warnings.filterwarnings("ignore")

earfcn_freq_dict = {'1099' : 1979.90, '1100' : 1980.00, '1123' : 1982.30, '1125' : 1982.50, '1126' : 1982.60, '1148' : 1984.80, '1150' : 1985.00, '2000' : 2115.00, '2050' : 2120.00, '2125' : 2127.50, '2175' : 2132.50, '2200' : 2135.00, '2225' : 2137.50, '2300' : 2145.00, '2325' : 2147.50, '2460': 875.0,  '39750' : 2506.00, '39907' : 2521.70, '39948' : 2525.80, '40072' : 2538.20, '40384' : 2569.40, '40770' : 2608.00, '40810' : 2612.00, '41176' : 2648.60, '41238' : 2654.80, '41490' : 2680.00, '5035' : 731.50, '5090' : 737, '5095' : 737.50, '5110' : 739.00, '5330' : 763.00, '5780' : 739, '5815': 742.5, '66486': 2115.00, '66487' : 2115.10, '66536' : 2120.00, '66561' : 2122.5, '66586' : 2125, '66661' : 2132.50, '66686' : 2135, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66811': 2147.5, '66836': 2150, '66886': 2150, '66911': 2150, '66961': 2150, '66986' : 2165.00, '67011': 2167.5, '675' : 1937.50, '676': 1937.6, '677': 1937.7, '68611': 619.5, '68636': 622, '68661': 624.5, '68686': 627, '68786': 637, '68836': 637, '68861': 637, '68886': 637, '68911': 649.5, '700' : 1940.00, '725': 1942.5, '750': 1942.5, '775': 1942.5, '801': 1950.1, '8115': 1937.5, '825': 1952.5, '8264': 1952.4, '8290': 1952.4, '8315': 1952.4, '8465': 1972.5, '850' : 1955.00, '851': 1955.1, '852': 1955.1, '8539': 1979.9, '8562': 1982.2, '8640': 1982.2, '8665': 1992.5, '875' : 1957.50, '876': 1957.6, '8763': 866.3, '877': 1957.7, '8950': 885, '901': 1960.1, '925' : 1962.50, '41305' : 2661.50, '66761' : 2142.50, '1000' : 1970.00, '1025' :  1972.50, '1050' : 1975, '1075' : 1977.50, '1125' : 1982.50 , '2100' : 2125.00, '2450' : 874.0, '2460' : 875.0, '2559' : 884.90, '2560' : 885.00, '2561' : 885.10, '2600' : 889.00, '5230' : 751.00, '5780' : 739.00, '66486' : 2115.00, '66536' : 2120.00, '66561' : 2122.50, '66586' : 2125.00, '66611' : 2127.50, '66636' : 2130.0, '66686' : 2135.00, '66711' : 2137.50, '66761' : 2142.50, '66786' : 2145.00, '66811' : 2147.50, '66836' : 2150.00, '66911' : 2157.50, '66936' : 2160.00, '66986' : 2165.00, '67011' : 2167.50, '67086' : 2175.00, '750' : 1945.00, '775' : 1947.50, '825' : 1952.50, '925' : 1962.50, '950' : 1965.00, '975' : 1967.50, '800' : 1950, '1025' :  1972.50, '1075' : 1977.50, '1100' : 1980.00, '1125' : 1982.50, '1150' : 1985.00, '2175' : 2132.50, '41094' : 2640.40, '41490' : 2680.00, '5035' : 731.50, '5090' : 737.00, '5110' : 739.00, '5145' : 742.50, '5330' : 763.00, '625' : 1932.50, '650' : 1935.00, '66461' : 2112.50, '66486' : 2115.00, '66511' : 2117.50, '66611' : 2127.50, '66661' : 2132.50, '66686' : 2135.00, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66936' : 2160.00, '66985' : 2164.90, '66986' : 2165.00, '67086' : 2175.00, '675' : 1937.50, '700' : 1940.00, '800' : 1950.00, '850' : 1955.00, '875' : 1957.50, '900' : 1960.00, '925' : 1962.50, '950' : 1965, '9820' : 765.00}

arfcn_freq_dict = {'125400' : 627.000, '125900' : 629.500, '126400' : 632.000, '126490' :632.450, '126510' : 632.550, '126530' : 632.650, '126900' : 634.500, '506280' : 2531.400, '508296' : 2541.480, '509202' : 2546.010, '514056' : 2570.280, '520020' : 2600.100, '525204' :2626.020, '526002' : 2630.010, '526404' : 2632.020, '527202' : 2636.010, '528000' : 2640.000, '528696' : 2643.480, '529998' : 2649.990, '530700' : 2653.500, '177020' : 885.100, '2083329' : 28249.800, '2071667' : 27550.080, '648672' : 3730.080, '2078331' : 27949.920, '2073333' : 27650.040, '177000' : 885.000, '174800' : 874.000, '175000' : 875.000, '650004' : 3750.060, '2239999' : 37650.000}


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
        sys.exit(1)

    return mod_speed_list

def is_wavelength(lat, lon): 
    """ Given a run, return whether a run is with AWS Wavelength. Assume edge server is used when the run is near the cities. """ 
    coord_city_arr = [ [34.058479, -118.237534], [39.74691, -105.004723], [39.74435, -105.00943], [39.76627, -104.999107], [40.061871, -104.654373], [34.058441, -118.237549], [34.068748, -118.22921], [41.893082, -87.623756], [36.113411, -115.173218], ] 
    coord = [lat, lon] 
    for coord_city in coord_city_arr: 
        if geopy.distance.geodesic(coord, coord_city).miles < 3: 
            return 1 
        
    return 0


def get_tz_info(first_lat_lon, last_lat_lon):
    try:
        temp_first_tz = obj.timezone_at(lng=first_lat_lon[-1], lat=first_lat_lon[0])
        temp_last_tz = obj.timezone_at(lng=last_lat_lon[-1], lat=last_lat_lon[0])
        if "Indiana" in temp_first_tz:
            temp_first_tz = 'America/New_York'
        if "Indiana" in temp_last_tz:
            temp_last_tz = 'America/New_York'
        
        if temp_first_tz != temp_last_tz:
            print("Return start TZ")
        
        return temp_first_tz
    except Exception as ex:
        print("TZ cannot be fetched! Why?????")
        print(str(ex))
        return None
       

def downtown_measurements_mod(start_tuple, end_tuple):
    lat_lon_dt_dict = {'LA' : (34.05872013582416, -118.23766913901929), 'LV' : (36.11290509947277, -115.1731529445295), 'SLC' : (40.725262, -111.854019), 'DE' : (39.744331, -105.009438), 'CHIC' : (41.89307, -87.623787), 'INDY' : (39.768028, -86.15094), 'CLEV' : (41.5005, -81.674026) }
    for key in lat_lon_dt_dict:
        distance_from_start = geopy.distance.geodesic(lat_lon_dt_dict[key], start_tuple).miles
        distance_from_end = geopy.distance.geodesic(lat_lon_dt_dict[key], end_tuple).miles
        
        if distance_from_start < 2 or distance_from_end < 2:
            #downtown measurement
            return True
    return False

def remove_values(lst, val):
    new_list = []
    for l in lst:
        if l < val:
            new_list.append(l)
    return new_list

def get_speed_dl_tput_ca_verizon(df_main, df_short_tput):
    speed_tput_tuple = {}
    speed_ca_tuple = {}
    speed_fiveg_ca_tuple = {}
    speed_lte_ca_tuple = {}
    speed_tz_tuple = {}
    speed_dist_tuple = {}
    speed_mcs_tuple = {}
    speed_bler_tuple = {}
    speed_rsrp_tuple = {}
    speed_wl_tuple = {}
    short_index_list = list(df_short_tput["index"])
    lat_list = list(df_short_tput["Lat"])
    lon_list = list(df_short_tput["Lon"])
    ts_list = list(df_short_tput["TIME_STAMP"])
    cols = ["LTE KPI PCell DL MCS0", "5G KPI PCell Layer1 DL MCS (Avg)", "LTE KPI PDSCH BLER[%]", "5G KPI PCell Layer1 DL BLER [%]", 'LTE KPI PCell Serving RSRP[dBm]', '5G KPI PCell RF Serving SS-RSRP [dBm]']
    df_short_tput.loc[:,cols] = df_short_tput.loc[:,cols].ffill().bfill()
    lte_bler_list = list(df_short_tput["LTE KPI PDSCH BLER[%]"]) 
    fiveg_bler_list = list(df_short_tput["5G KPI PCell Layer1 DL BLER [%]"]) 
    lte_mcs_list = list(df_short_tput["LTE KPI PCell DL MCS0"])
    fiveg_mcs_list = list(df_short_tput["5G KPI PCell Layer1 DL MCS (Avg)"])
    lte_rsrp_list = list(df_short_tput['LTE KPI PCell Serving RSRP[dBm]'])
    fiveg_rsrp_list = list(df_short_tput['5G KPI PCell RF Serving SS-RSRP [dBm]'])
    tput_list = list(df_short_tput["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"])
    fiveg_cell_tput_list = df_short_tput[["5G KPI PCell Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC DL Throughput [Mbps]"]].values.tolist()
    lte_cell_tput_list = df_short_tput[["LTE KPI PCell MAC DL Throughput[Mbps]", "LTE KPI SCell[1] MAC DL Throughput[Mbps]", "LTE KPI SCell[2] MAC DL Throughput[Mbps]", "LTE KPI SCell[3] MAC DL Throughput[Mbps]", "LTE KPI SCell[4] MAC DL Throughput[Mbps]"]].values.tolist()
    prev_lat_lon = (lat_list[0], lon_list[0])
    prev_ts = ts_list[0]
    tz_list = []
    dist_list = []
    speed_list = []
    ca_list = []
    mcs_list = []
    rsrp_list = []
    fiveg_ca_list = []
    lte_ca_list = []
    tput_current_list = []
    lat_lon_30_60_list = []
    ts_new_list = []
    tput_new_list = []
    bler_list = []
    wl_list = []
    dt_measurement = downtown_measurements_mod((lat_list[0], lon_list[0]), (lat_list[-1], lon_list[-1]))
    for short_index, lat, lon, ts, tput, fiveg_cells, lte_cells, lte_mcs, fiveg_mcs, lte_bler, fiveg_bler, lte_rsrp, fiveg_rsrp in zip(short_index_list[1:], lat_list[1:], lon_list[1:], ts_list[1:], tput_list[1:], fiveg_cell_tput_list[1:], lte_cell_tput_list[1:], lte_mcs_list[1:], fiveg_mcs_list[1:], lte_bler_list[1:], fiveg_bler_list[1:], lte_rsrp_list[1:], fiveg_rsrp_list[1:]):
        #check nans in lte/five g cells list
        fiveg_cell_count = 0
        lte_cell_count = 0
        nan_count = 0
        for cell in fiveg_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                fiveg_cell_count+=1
        if nan_count == len(fiveg_cells):
            fiveg_empty = True
        else:
            fiveg_empty = False

        nan_count = 0
        for cell in lte_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                lte_cell_count+=1
        if nan_count == len(lte_cells):
            lte_empty = True
        else:
            lte_empty = False
        if lte_empty == True and fiveg_empty == True:
            # let's backtrack 1 second
            main_index = short_index - 1
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_cell_list_main = df_main.iloc[main_index][["5G KPI PCell Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC DL Throughput [Mbps]"]]
                lte_cell_list_main = df_main.iloc[main_index][["LTE KPI PCell MAC DL Throughput[Mbps]", "LTE KPI SCell[1] MAC DL Throughput[Mbps]", "LTE KPI SCell[2] MAC DL Throughput[Mbps]", "LTE KPI SCell[3] MAC DL Throughput[Mbps]", "LTE KPI SCell[4] MAC DL Throughput[Mbps]"]]
                fiveg_cell_count = 0
                lte_cell_count = 0
                nan_count = 0
                for cell in fiveg_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        fiveg_cell_count+=1
                if nan_count == len(fiveg_cell_list_main):
                    fiveg_empty = True
                else:
                    fiveg_empty = False

                nan_count = 0
                for cell in lte_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        lte_cell_count+=1
                if nan_count == len(lte_cell_list_main):
                    lte_empty = True
                else:
                    lte_empty = False
                
                if lte_empty == True and fiveg_empty == True:
                    main_index-=1
                else:
                    # match found
                    break

                    
            # last check -> if still empty continue
            if lte_empty == True and fiveg_empty == True:
                continue
        total_cell_count = fiveg_cell_count + lte_cell_count
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
        
        # if speed > 0 and speed < 1:
        #     speed = 1

        if dt_measurement and speed > 20:
            import random
            # speed = 10
            speed = random.randint(0, 20)

        if pd.isnull(fiveg_mcs) and pd.isnull(lte_mcs):
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_mcs_main = df_main.iloc[main_index][["5G KPI PCell Layer1 DL MCS (Avg)"]][0]
                lte_mcs_main = df_main.iloc[main_index][["LTE KPI PCell DL MCS0"]][0]
                fiveg_mcs_count = 0
                lte_mcs_count = 0

                if pd.isnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(lte_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                mcs_list.append(fiveg_mcs)
        elif pd.isnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(lte_mcs)
        elif pd.notnull(fiveg_mcs) and pd.isnull(lte_mcs):
            mcs_list.append(fiveg_mcs)
        elif pd.notnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(fiveg_mcs)

        if pd.isnull(fiveg_bler) and pd.isnull(lte_bler):
            # let's backtrack 1 second - bler
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_bler_main = df_main.iloc[main_index][["5G KPI PCell Layer1 DL BLER [%]"]][0]
                lte_bler_main = df_main.iloc[main_index][["LTE KPI PDSCH BLER[%]"]][0]
                fiveg_bler_count = 0
                lte_bler_count = 0

                if pd.isnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(lte_bler_count)
                elif pd.notnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                elif pd.notnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                bler_list.append(fiveg_bler)
        elif pd.isnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(lte_bler)
        elif pd.notnull(fiveg_bler) and pd.isnull(lte_bler):
            bler_list.append(fiveg_bler)
        elif pd.notnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(fiveg_bler)

        if pd.isnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            # let's backtrack 1 second - rsrp
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_rsrp_main = df_main.iloc[main_index][['5G KPI PCell RF Serving SS-RSRP [dBm]']][0]
                lte_rsrp_main = df_main.iloc[main_index][['LTE KPI PCell Serving RSRP[dBm]']][0]
                fiveg_rsrp_count = 0
                lte_rsrp_count = 0

                if pd.isnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(lte_rsrp_count)
                elif pd.notnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                elif pd.notnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                rsrp_list.append(fiveg_rsrp)
        elif pd.isnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(lte_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)


        #get timezone
        tz = get_tz_info(prev_lat_lon, current_lat_lon)
        tz_list.append(tz)
        wl_list.append(is_wavelength(lat, lon))
        dist_list.append(distance_current)
        speed_list.append(speed)
        tput_current_list.append(tput)
        ca_list.append(total_cell_count)
        fiveg_ca_list.append(fiveg_cell_count)
        lte_ca_list.append(lte_cell_count)
        prev_lat_lon = (lat, lon)
        if speed >= 30 and speed <= 60:
            lat_lon_30_60_list.append(prev_lat_lon)
            ts_new_list.append(ts)
            tput_new_list.append(tput)
        prev_ts = ts
    uniques, counts = np.unique(speed_list, return_counts=True)
    percentages = dict(zip(uniques, counts * 100 / len(speed_list)))
    speed_list = modify_speed_list(speed_list)
    if len(percentages) != 0:
        if 0 in percentages.keys():
            if percentages[0] > 85:
                #static run
                pass                            
            else:
                for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp, wl in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list, wl_list):
                    if speed not in speed_tput_tuple.keys():
                        speed_tput_tuple[speed] = [tput]
                    else:
                        speed_tput_tuple[speed].append(tput)

                    if speed not in speed_ca_tuple.keys():
                            speed_ca_tuple[speed] = [ca]
                    else:
                        speed_ca_tuple[speed].append(ca)
                    
                    if speed not in speed_fiveg_ca_tuple.keys():
                            speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                    else:
                        speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                    if speed not in speed_lte_ca_tuple.keys():
                            speed_lte_ca_tuple[speed] = [lte_ca]
                    else:
                        speed_lte_ca_tuple[speed].append(lte_ca)
                    
                    if speed not in speed_tz_tuple.keys():
                        speed_tz_tuple[speed] = [tz_temp]
                    else:
                        speed_tz_tuple[speed].append(tz_temp)

                    if speed not in speed_dist_tuple.keys():
                        speed_dist_tuple[speed] = [dist]
                    else:
                        speed_dist_tuple[speed].append(dist)
                    
                    if speed not in speed_mcs_tuple.keys():
                        speed_mcs_tuple[speed] = [mcs]
                    else:
                        speed_mcs_tuple[speed].append(mcs)
                    
                    if speed not in speed_bler_tuple.keys():
                        speed_bler_tuple[speed] = [bler]
                    else:
                        speed_bler_tuple[speed].append(bler)

                    if speed not in speed_rsrp_tuple.keys():
                        speed_rsrp_tuple[speed] = [rsrp]
                    else:
                        speed_rsrp_tuple[speed].append(rsrp)
                    if speed not in speed_wl_tuple.keys():
                        speed_wl_tuple[speed] = [wl]
                    else:
                        speed_wl_tuple[speed].append(wl)

                
        else:
            for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp, wl in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list, wl_list):
                if speed not in speed_tput_tuple.keys():
                        speed_tput_tuple[speed] = [tput]
                else:
                    speed_tput_tuple[speed].append(tput)

                if speed not in speed_ca_tuple.keys():
                    speed_ca_tuple[speed] = [ca]
                else:
                    speed_ca_tuple[speed].append(ca)

                if speed not in speed_fiveg_ca_tuple.keys():
                        speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                else:
                    speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                if speed not in speed_lte_ca_tuple.keys():
                        speed_lte_ca_tuple[speed] = [lte_ca]
                else:
                    speed_lte_ca_tuple[speed].append(lte_ca)
                
                if speed not in speed_tz_tuple.keys():
                    speed_tz_tuple[speed] = [tz_temp]
                else:
                    speed_tz_tuple[speed].append(tz_temp)

                if speed not in speed_dist_tuple.keys():
                    speed_dist_tuple[speed] = [dist]
                else:
                    speed_dist_tuple[speed].append(dist)

                if speed not in speed_mcs_tuple.keys():
                    speed_mcs_tuple[speed] = [mcs]
                else:
                    speed_mcs_tuple[speed].append(mcs)
    
                if speed not in speed_bler_tuple.keys():
                    speed_bler_tuple[speed] = [bler]
                else:
                    speed_bler_tuple[speed].append(bler)

                if speed not in speed_rsrp_tuple.keys():
                    speed_rsrp_tuple[speed] = [rsrp]
                else:
                    speed_rsrp_tuple[speed].append(rsrp)
                
                if speed not in speed_wl_tuple.keys():
                    speed_wl_tuple[speed] = [wl]
                else:
                    speed_wl_tuple[speed].append(wl)

    if len(speed_tput_tuple) == 0:
        lat_lon_30_60_list = []
        percent = 0
        ts_new_list = []
        tput_new_list = []
    else:
        percent = len(lat_lon_30_60_list)/len(speed_tput_tuple)
    return [speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple, speed_wl_tuple]

def get_speed_ul_tput_ca_verizon(df_main, df_short_tput):
    speed_tput_tuple = {}
    speed_ca_tuple = {}
    speed_fiveg_ca_tuple = {}
    speed_dist_tuple = {}
    speed_lte_ca_tuple = {}
    speed_tz_tuple = {}
    speed_mcs_tuple = {}
    speed_bler_tuple = {}
    speed_rsrp_tuple = {}
    speed_wl_tuple = {}
    short_index_list = list(df_short_tput["index"])
    lat_list = list(df_short_tput["Lat"])
    lon_list = list(df_short_tput["Lon"])
    ts_list = list(df_short_tput["TIME_STAMP"])
    cols = ["LTE KPI PCell UL MCS", "5G KPI PCell Layer1 UL MCS (Avg)", "LTE KPI PUSCH BLER[%]", "5G KPI PCell Layer1 UL BLER [%]", 'LTE KPI PCell Serving RSRP[dBm]', '5G KPI PCell RF Serving SS-RSRP [dBm]']
    df_short_tput.loc[:,cols] = df_short_tput.loc[:,cols].ffill().bfill()
    lte_bler_list = list(df_short_tput["LTE KPI PUSCH BLER[%]"]) 
    fiveg_bler_list = list(df_short_tput["5G KPI PCell Layer1 UL BLER [%]"]) 
    lte_mcs_list = list(df_short_tput["LTE KPI PCell UL MCS"])
    fiveg_mcs_list = list(df_short_tput["5G KPI PCell Layer1 UL MCS (Avg)"])
    lte_rsrp_list = list(df_short_tput['LTE KPI PCell Serving RSRP[dBm]'])
    fiveg_rsrp_list = list(df_short_tput['5G KPI PCell RF Serving SS-RSRP [dBm]'])
    tput_list = list(df_short_tput["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"])
    fiveg_cell_tput_list = df_short_tput[["5G KPI PCell Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC UL Throughput [Mbps]"]].values.tolist()
    lte_cell_tput_list = df_short_tput[["LTE KPI PCell MAC UL Throughput[Mbps]", "LTE KPI SCell[1] MAC UL Throughput[Mbps]", "LTE KPI SCell[2] MAC UL Throughput[Mbps]", "LTE KPI SCell[3] MAC UL Throughput[Mbps]", "LTE KPI SCell[4] MAC UL Throughput[Mbps]"]].values.tolist()
    prev_lat_lon = (lat_list[0], lon_list[0])
    prev_ts = ts_list[0]
    dist_list = []
    speed_list = []
    tz_list = []
    ca_list = []
    mcs_list = []
    bler_list = []
    rsrp_list = []
    fiveg_ca_list = []
    lte_ca_list = []
    tput_current_list = []
    wl_list = []
    dt_measurement = downtown_measurements_mod((lat_list[0], lon_list[0]), (lat_list[-1], lon_list[-1]))
    for short_index, lat, lon, ts, tput, fiveg_cells, lte_cells, lte_mcs, fiveg_mcs, lte_bler, fiveg_bler, lte_rsrp, fiveg_rsrp in zip(short_index_list[1:], lat_list[1:], lon_list[1:], ts_list[1:], tput_list[1:], fiveg_cell_tput_list[1:], lte_cell_tput_list[1:], lte_mcs_list[1:], fiveg_mcs_list[1:], lte_bler_list[1:], fiveg_bler_list[1:], lte_rsrp_list[1:], fiveg_rsrp_list[1:]):
        #check nans in lte/five g cells list
        fiveg_cell_count = 0
        lte_cell_count = 0
        nan_count = 0
        for cell in fiveg_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                fiveg_cell_count+=1
        if nan_count == len(fiveg_cells):
            fiveg_empty = True
        else:
            fiveg_empty = False

        nan_count = 0
        for cell in lte_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                lte_cell_count+=1
        if nan_count == len(lte_cells):
            lte_empty = True
        else:
            lte_empty = False
        if lte_empty == True and fiveg_empty == True:
            # let's backtrack 1 second
            main_index = short_index - 1
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_cell_list_main = df_main.iloc[main_index][["5G KPI PCell Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC UL Throughput [Mbps]"]]
                lte_cell_list_main = df_main.iloc[main_index][["LTE KPI PCell MAC UL Throughput[Mbps]", "LTE KPI SCell[1] MAC UL Throughput[Mbps]", "LTE KPI SCell[2] MAC UL Throughput[Mbps]", "LTE KPI SCell[3] MAC UL Throughput[Mbps]", "LTE KPI SCell[4] MAC UL Throughput[Mbps]"]]
                fiveg_cell_count = 0
                lte_cell_count = 0
                nan_count = 0
                for cell in fiveg_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        fiveg_cell_count+=1
                if nan_count == len(fiveg_cell_list_main):
                    fiveg_empty = True
                else:
                    fiveg_empty = False

                nan_count = 0
                for cell in lte_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        lte_cell_count+=1
                if nan_count == len(lte_cell_list_main):
                    lte_empty = True
                else:
                    lte_empty = False
                
                if lte_empty == True and fiveg_empty == True:
                    main_index-=1
                else:
                    # match found
                    break

                    
            # last check -> if still empty continue
            if lte_empty == True and fiveg_empty == True:
                continue
        total_cell_count = fiveg_cell_count + lte_cell_count
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
        
        # if speed > 0 and speed < 1:
        #     speed = 1

        if dt_measurement and speed > 20:
            import random
            # speed = 10
            speed = random.randint(0, 20)

        if pd.isnull(fiveg_mcs) and pd.isnull(lte_mcs):
            # let's backtrack 1 second - mcs
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_mcs_main = df_main.iloc[main_index][["5G KPI PCell Layer1 UL MCS (Avg)"]][0]
                lte_mcs_main = df_main.iloc[main_index][["LTE KPI PCell UL MCS"]][0]
                fiveg_mcs_count = 0
                lte_mcs_count = 0

                if pd.isnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(lte_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                mcs_list.append(fiveg_mcs)
        elif pd.isnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(lte_mcs)
        elif pd.notnull(fiveg_mcs) and pd.isnull(lte_mcs):
            mcs_list.append(fiveg_mcs)
        elif pd.notnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(fiveg_mcs)

        if pd.isnull(fiveg_bler) and pd.isnull(lte_bler):
            # let's backtrack 1 second - bler
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_bler_main = df_main.iloc[main_index][["5G KPI PCell Layer1 UL BLER [%]"]][0]
                lte_bler_main = df_main.iloc[main_index][["LTE KPI PUSCH BLER[%]"]][0]
                fiveg_bler_count = 0
                lte_bler_count = 0

                if pd.isnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(lte_bler_count)
                elif pd.notnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                elif pd.notnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                bler_list.append(fiveg_bler)
        elif pd.isnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(lte_bler)
        elif pd.notnull(fiveg_bler) and pd.isnull(lte_bler):
            bler_list.append(fiveg_bler)
        elif pd.notnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(fiveg_bler)

        if pd.isnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            # let's backtrack 1 second - rsrp
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_rsrp_main = df_main.iloc[main_index][['5G KPI PCell RF Serving SS-RSRP [dBm]']][0]
                lte_rsrp_main = df_main.iloc[main_index][['LTE KPI PCell Serving RSRP[dBm]']][0]
                fiveg_rsrp_count = 0
                lte_rsrp_count = 0

                if pd.isnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(lte_rsrp_count)
                elif pd.notnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                elif pd.notnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                rsrp_list.append(fiveg_rsrp)
        elif pd.isnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(lte_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)


        #get timezone
        tz = get_tz_info(prev_lat_lon, current_lat_lon)
        tz_list.append(tz)
        wl_list.append(is_wavelength(lat, lon))
        dist_list.append(distance_current)
        speed_list.append(speed)
        tput_current_list.append(tput)
        ca_list.append(total_cell_count)
        fiveg_ca_list.append(fiveg_cell_count)
        lte_ca_list.append(lte_cell_count)
        prev_lat_lon = (lat, lon)
        prev_ts = ts
    
    uniques, counts = np.unique(speed_list, return_counts=True)
    percentages = dict(zip(uniques, counts * 100 / len(speed_list)))
    speed_list = modify_speed_list(speed_list)
    if len(percentages) != 0:
        if 0 in percentages.keys():
            if percentages[0] > 85:
                #static run
                pass                            
            else:
                for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp, wl in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list, wl_list):
                    if speed not in speed_tput_tuple.keys():
                            speed_tput_tuple[speed] = [tput]
                    else:
                        speed_tput_tuple[speed].append(tput)

                    if speed not in speed_ca_tuple.keys():
                            speed_ca_tuple[speed] = [ca]
                    else:
                        speed_ca_tuple[speed].append(ca)
                    
                    if speed not in speed_fiveg_ca_tuple.keys():
                            speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                    else:
                        speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                    if speed not in speed_lte_ca_tuple.keys():
                            speed_lte_ca_tuple[speed] = [lte_ca]
                    else:
                        speed_lte_ca_tuple[speed].append(lte_ca)

                    if speed not in speed_tz_tuple.keys():
                        speed_tz_tuple[speed] = [tz_temp]
                    else:
                        speed_tz_tuple[speed].append(tz_temp)

                    if speed not in speed_dist_tuple.keys():
                        speed_dist_tuple[speed] = [dist]
                    else:
                        speed_dist_tuple[speed].append(dist)
                    
                    if speed not in speed_mcs_tuple.keys():
                        speed_mcs_tuple[speed] = [mcs]
                    else:
                        speed_mcs_tuple[speed].append(mcs)
                    if speed not in speed_bler_tuple.keys():
                        speed_bler_tuple[speed] = [bler]
                    else:
                        speed_bler_tuple[speed].append(bler)
                    if speed not in speed_rsrp_tuple.keys():
                        speed_rsrp_tuple[speed] = [rsrp]
                    else:
                        speed_rsrp_tuple[speed].append(rsrp)
                    if speed not in speed_wl_tuple.keys():
                        speed_wl_tuple[speed] = [wl]
                    else:
                        speed_wl_tuple[speed].append(wl)
        else:
            for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp, wl in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list, wl_list):
                if speed not in speed_tput_tuple.keys():
                        speed_tput_tuple[speed] = [tput]
                else:
                    speed_tput_tuple[speed].append(tput)

                if speed not in speed_ca_tuple.keys():
                    speed_ca_tuple[speed] = [ca]
                else:
                    speed_ca_tuple[speed].append(ca)

                if speed not in speed_fiveg_ca_tuple.keys():
                        speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                else:
                    speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                if speed not in speed_lte_ca_tuple.keys():
                        speed_lte_ca_tuple[speed] = [lte_ca]
                else:
                    speed_lte_ca_tuple[speed].append(lte_ca)

                if speed not in speed_tz_tuple.keys():
                    speed_tz_tuple[speed] = [tz_temp]
                else:
                    speed_tz_tuple[speed].append(tz_temp)

                if speed not in speed_dist_tuple.keys():
                    speed_dist_tuple[speed] = [dist]
                else:
                    speed_dist_tuple[speed].append(dist)
                
                if speed not in speed_mcs_tuple.keys():
                    speed_mcs_tuple[speed] = [mcs]
                else:
                    speed_mcs_tuple[speed].append(mcs)
                if speed not in speed_bler_tuple.keys():
                    speed_bler_tuple[speed] = [bler]
                else:
                    speed_bler_tuple[speed].append(bler)
                if speed not in speed_rsrp_tuple.keys():
                    speed_rsrp_tuple[speed] = [rsrp]
                else:
                    speed_rsrp_tuple[speed].append(rsrp)
                if speed not in speed_wl_tuple.keys():
                    speed_wl_tuple[speed] = [wl]
                else:
                    speed_wl_tuple[speed].append(wl)
    
    return [speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple, speed_wl_tuple]

def get_speed_dl_tput_ca_tmobile(df_main, df_short_tput):
    speed_tput_tuple = {}
    speed_ca_tuple = {}
    speed_fiveg_ca_tuple = {}
    speed_lte_ca_tuple = {}
    speed_tz_tuple = {}
    speed_dist_tuple = {}
    speed_mcs_tuple = {}
    speed_bler_tuple = {}
    speed_rsrp_tuple = {}
    short_index_list = list(df_short_tput["index"])
    lat_list = list(df_short_tput["Lat"])
    lon_list = list(df_short_tput["Lon"])
    ts_list = list(df_short_tput["TIME_STAMP"])
    cols = ["LTE KPI PCell DL MCS0", "5G KPI PCell Layer1 DL MCS (Avg)", "LTE KPI PDSCH BLER[%]", "5G KPI PCell Layer1 DL BLER [%]", 'LTE KPI PCell Serving RSRP[dBm]', '5G KPI PCell RF Serving SS-RSRP [dBm]']
    df_short_tput.loc[:,cols] = df_short_tput.loc[:,cols].ffill().bfill()
    lte_bler_list = list(df_short_tput["LTE KPI PDSCH BLER[%]"]) 
    fiveg_bler_list = list(df_short_tput["5G KPI PCell Layer1 DL BLER [%]"]) 
    lte_mcs_list = list(df_short_tput["LTE KPI PCell DL MCS0"])
    fiveg_mcs_list = list(df_short_tput["5G KPI PCell Layer1 DL MCS (Avg)"])
    lte_rsrp_list = list(df_short_tput['LTE KPI PCell Serving RSRP[dBm]'])
    fiveg_rsrp_list = list(df_short_tput['5G KPI PCell RF Serving SS-RSRP [dBm]'])
    tput_list = list(df_short_tput["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"])
    fiveg_cell_tput_list = df_short_tput[["5G KPI PCell Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC DL Throughput [Mbps]"]].values.tolist()
    lte_cell_tput_list = df_short_tput[["LTE KPI PCell MAC DL Throughput[Mbps]", "LTE KPI SCell[1] MAC DL Throughput[Mbps]", "LTE KPI SCell[2] MAC DL Throughput[Mbps]", "LTE KPI SCell[3] MAC DL Throughput[Mbps]", "LTE KPI SCell[4] MAC DL Throughput[Mbps]"]].values.tolist()
    prev_lat_lon = (lat_list[0], lon_list[0])
    prev_ts = ts_list[0]
    tz_list = []
    dist_list = []
    speed_list = []
    ca_list = []
    mcs_list = []
    rsrp_list = []
    fiveg_ca_list = []
    lte_ca_list = []
    tput_current_list = []
    lat_lon_30_60_list = []
    ts_new_list = []
    tput_new_list = []
    bler_list = []
    dt_measurement = downtown_measurements_mod((lat_list[0], lon_list[0]), (lat_list[-1], lon_list[-1]))
    for short_index, lat, lon, ts, tput, fiveg_cells, lte_cells, lte_mcs, fiveg_mcs, lte_bler, fiveg_bler, lte_rsrp, fiveg_rsrp in zip(short_index_list[1:], lat_list[1:], lon_list[1:], ts_list[1:], tput_list[1:], fiveg_cell_tput_list[1:], lte_cell_tput_list[1:], lte_mcs_list[1:], fiveg_mcs_list[1:], lte_bler_list[1:], fiveg_bler_list[1:], lte_rsrp_list[1:], fiveg_rsrp_list[1:]):
        #check nans in lte/five g cells list
        fiveg_cell_count = 0
        lte_cell_count = 0
        nan_count = 0
        for cell in fiveg_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                fiveg_cell_count+=1
        if nan_count == len(fiveg_cells):
            fiveg_empty = True
        else:
            fiveg_empty = False

        nan_count = 0
        for cell in lte_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                lte_cell_count+=1
        if nan_count == len(lte_cells):
            lte_empty = True
        else:
            lte_empty = False
        if lte_empty == True and fiveg_empty == True:
            # let's backtrack 1 second
            main_index = short_index - 1
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_cell_list_main = df_main.iloc[main_index][["5G KPI PCell Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC DL Throughput [Mbps]"]]
                lte_cell_list_main = df_main.iloc[main_index][["LTE KPI PCell MAC DL Throughput[Mbps]", "LTE KPI SCell[1] MAC DL Throughput[Mbps]", "LTE KPI SCell[2] MAC DL Throughput[Mbps]", "LTE KPI SCell[3] MAC DL Throughput[Mbps]", "LTE KPI SCell[4] MAC DL Throughput[Mbps]"]]
                fiveg_cell_count = 0
                lte_cell_count = 0
                nan_count = 0
                for cell in fiveg_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        fiveg_cell_count+=1
                if nan_count == len(fiveg_cell_list_main):
                    fiveg_empty = True
                else:
                    fiveg_empty = False

                nan_count = 0
                for cell in lte_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        lte_cell_count+=1
                if nan_count == len(lte_cell_list_main):
                    lte_empty = True
                else:
                    lte_empty = False
                
                if lte_empty == True and fiveg_empty == True:
                    main_index-=1
                else:
                    # match found
                    break

                    
            # last check -> if still empty continue
            if lte_empty == True and fiveg_empty == True:
                continue
        total_cell_count = fiveg_cell_count + lte_cell_count
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
        
        # if speed > 0 and speed < 1:
        #     speed = 1

        if dt_measurement and speed > 20:
            import random
            # speed = 10
            speed = random.randint(0, 20)

        if pd.isnull(fiveg_mcs) and pd.isnull(lte_mcs):
            # let's backtrack 1 second - mcs
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_mcs_main = df_main.iloc[main_index][["5G KPI PCell Layer1 DL MCS (Avg)"]][0]
                lte_mcs_main = df_main.iloc[main_index][["LTE KPI PCell DL MCS0"]][0]
                fiveg_mcs_count = 0
                lte_mcs_count = 0

                if pd.isnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(lte_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                mcs_list.append(fiveg_mcs)
        elif pd.isnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(lte_mcs)
        elif pd.notnull(fiveg_mcs) and pd.isnull(lte_mcs):
            mcs_list.append(fiveg_mcs)
        elif pd.notnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(fiveg_mcs)


        if pd.isnull(fiveg_bler) and pd.isnull(lte_bler):
            # let's backtrack 1 second - bler
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_bler_main = df_main.iloc[main_index][["5G KPI PCell Layer1 DL BLER [%]"]][0]
                lte_bler_main = df_main.iloc[main_index][["LTE KPI PDSCH BLER[%]"]][0]
                fiveg_bler_count = 0
                lte_bler_count = 0

                if pd.isnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(lte_bler_count)
                elif pd.notnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                elif pd.notnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                bler_list.append(fiveg_bler)
        elif pd.isnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(lte_bler)
        elif pd.notnull(fiveg_bler) and pd.isnull(lte_bler):
            bler_list.append(fiveg_bler)
        elif pd.notnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(fiveg_bler)

        if pd.isnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            # let's backtrack 1 second - rsrp
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_rsrp_main = df_main.iloc[main_index][['5G KPI PCell RF Serving SS-RSRP [dBm]']][0]
                lte_rsrp_main = df_main.iloc[main_index][['LTE KPI PCell Serving RSRP[dBm]']][0]
                fiveg_rsrp_count = 0
                lte_rsrp_count = 0

                if pd.isnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(lte_rsrp_count)
                elif pd.notnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                elif pd.notnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                rsrp_list.append(fiveg_rsrp)
        elif pd.isnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(lte_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)

        #get timezone
        tz = get_tz_info(prev_lat_lon, current_lat_lon)
        tz_list.append(tz)
        dist_list.append(distance_current)
        speed_list.append(speed)
        tput_current_list.append(tput)
        ca_list.append(total_cell_count)
        fiveg_ca_list.append(fiveg_cell_count)
        lte_ca_list.append(lte_cell_count)
        prev_lat_lon = (lat, lon)
        if speed >= 30 and speed <= 60:
            lat_lon_30_60_list.append(prev_lat_lon)
            ts_new_list.append(ts)
            tput_new_list.append(tput)
        prev_ts = ts
    uniques, counts = np.unique(speed_list, return_counts=True)
    percentages = dict(zip(uniques, counts * 100 / len(speed_list)))
    speed_list = modify_speed_list(speed_list)
    if len(percentages) != 0:
        if 0 in percentages.keys():
            if percentages[0] > 85:
                #static run
                # global_static_removed_dl_df.append(df_current)
                pass                            
            else:
                for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list):
                    # let's prune those tput data that are greater than 5000 Mbps (not possible!)
                    if tput > 5000:
                        continue
                    if speed not in speed_tput_tuple.keys():
                        speed_tput_tuple[speed] = [tput]
                    else:
                        speed_tput_tuple[speed].append(tput)

                    if speed not in speed_ca_tuple.keys():
                            speed_ca_tuple[speed] = [ca]
                    else:
                        speed_ca_tuple[speed].append(ca)
                    
                    if speed not in speed_fiveg_ca_tuple.keys():
                            speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                    else:
                        speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                    if speed not in speed_lte_ca_tuple.keys():
                            speed_lte_ca_tuple[speed] = [lte_ca]
                    else:
                        speed_lte_ca_tuple[speed].append(lte_ca)
                    
                    if speed not in speed_tz_tuple.keys():
                        speed_tz_tuple[speed] = [tz_temp]
                    else:
                        speed_tz_tuple[speed].append(tz_temp)

                    if speed not in speed_dist_tuple.keys():
                        speed_dist_tuple[speed] = [dist]
                    else:
                        speed_dist_tuple[speed].append(dist)
                    
                    if speed not in speed_mcs_tuple.keys():
                        speed_mcs_tuple[speed] = [mcs]
                    else:
                        speed_mcs_tuple[speed].append(mcs)
                    
                    if speed not in speed_bler_tuple.keys():
                        speed_bler_tuple[speed] = [bler]
                    else:
                        speed_bler_tuple[speed].append(bler)
                    
                    if speed not in speed_rsrp_tuple.keys():
                        speed_rsrp_tuple[speed] = [rsrp]
                    else:
                        speed_rsrp_tuple[speed].append(rsrp)
                
        else:
            for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list):
                # let's prune those tput data that are greater than 5000 Mbps (not possible!)
                if tput > 5000:
                    continue
                if speed not in speed_tput_tuple.keys():
                        speed_tput_tuple[speed] = [tput]
                else:
                    speed_tput_tuple[speed].append(tput)

                if speed not in speed_ca_tuple.keys():
                    speed_ca_tuple[speed] = [ca]
                else:
                    speed_ca_tuple[speed].append(ca)

                if speed not in speed_fiveg_ca_tuple.keys():
                        speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                else:
                    speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                if speed not in speed_lte_ca_tuple.keys():
                        speed_lte_ca_tuple[speed] = [lte_ca]
                else:
                    speed_lte_ca_tuple[speed].append(lte_ca)
                
                if speed not in speed_tz_tuple.keys():
                    speed_tz_tuple[speed] = [tz_temp]
                else:
                    speed_tz_tuple[speed].append(tz_temp)

                if speed not in speed_dist_tuple.keys():
                    speed_dist_tuple[speed] = [dist]
                else:
                    speed_dist_tuple[speed].append(dist)

                if speed not in speed_mcs_tuple.keys():
                    speed_mcs_tuple[speed] = [mcs]
                else:
                    speed_mcs_tuple[speed].append(mcs)
                if speed not in speed_bler_tuple.keys():
                    speed_bler_tuple[speed] = [bler]
                else:
                    speed_bler_tuple[speed].append(bler)
                if speed not in speed_rsrp_tuple.keys():
                    speed_rsrp_tuple[speed] = [rsrp]
                else:
                    speed_rsrp_tuple[speed].append(rsrp)

    if len(speed_tput_tuple) == 0:
        lat_lon_30_60_list = []
        percent = 0
        ts_new_list = []
        tput_new_list = []
    else:
        percent = len(lat_lon_30_60_list)/len(speed_tput_tuple)
    return [speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple]

def get_speed_ul_tput_ca_tmobile(df_main, df_short_tput):
    speed_tput_tuple = {}
    speed_ca_tuple = {}
    speed_fiveg_ca_tuple = {}
    speed_dist_tuple = {}
    speed_lte_ca_tuple = {}
    speed_tz_tuple = {}
    speed_mcs_tuple = {}
    speed_bler_tuple = {}
    speed_rsrp_tuple = {}
    short_index_list = list(df_short_tput["index"])
    lat_list = list(df_short_tput["Lat"])
    lon_list = list(df_short_tput["Lon"])
    ts_list = list(df_short_tput["TIME_STAMP"])
    cols = ["LTE KPI PCell UL MCS", "5G KPI PCell Layer1 UL MCS (Avg)", "LTE KPI PUSCH BLER[%]", "5G KPI PCell Layer1 UL BLER [%]", 'LTE KPI PCell Serving RSRP[dBm]', '5G KPI PCell RF Serving SS-RSRP [dBm]']
    df_short_tput.loc[:,cols] = df_short_tput.loc[:,cols].ffill().bfill()
    lte_bler_list = list(df_short_tput["LTE KPI PUSCH BLER[%]"]) 
    fiveg_bler_list = list(df_short_tput["5G KPI PCell Layer1 UL BLER [%]"]) 
    lte_mcs_list = list(df_short_tput["LTE KPI PCell UL MCS"])
    fiveg_mcs_list = list(df_short_tput["5G KPI PCell Layer1 UL MCS (Avg)"])
    lte_rsrp_list = list(df_short_tput['LTE KPI PCell Serving RSRP[dBm]'])
    fiveg_rsrp_list = list(df_short_tput['5G KPI PCell RF Serving SS-RSRP [dBm]'])
    tput_list = list(df_short_tput["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"])
    fiveg_cell_tput_list = df_short_tput[["5G KPI PCell Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC UL Throughput [Mbps]"]].values.tolist()
    lte_cell_tput_list = df_short_tput[["LTE KPI PCell MAC UL Throughput[Mbps]", "LTE KPI SCell[1] MAC UL Throughput[Mbps]", "LTE KPI SCell[2] MAC UL Throughput[Mbps]", "LTE KPI SCell[3] MAC UL Throughput[Mbps]", "LTE KPI SCell[4] MAC UL Throughput[Mbps]"]].values.tolist()
    prev_lat_lon = (lat_list[0], lon_list[0])
    prev_ts = ts_list[0]
    dist_list = []
    speed_list = []
    tz_list = []
    ca_list = []
    mcs_list = []
    rsrp_list = []
    fiveg_ca_list = []
    lte_ca_list = []
    tput_current_list = []
    bler_list = []
    dt_measurement = downtown_measurements_mod((lat_list[0], lon_list[0]), (lat_list[-1], lon_list[-1]))
    for short_index, lat, lon, ts, tput, fiveg_cells, lte_cells, lte_mcs, fiveg_mcs, lte_bler, fiveg_bler, lte_rsrp, fiveg_rsrp in zip(short_index_list[1:], lat_list[1:], lon_list[1:], ts_list[1:], tput_list[1:], fiveg_cell_tput_list[1:], lte_cell_tput_list[1:], lte_mcs_list[1:], fiveg_mcs_list[1:], lte_bler_list[1:], fiveg_bler_list[1:], lte_rsrp_list[1:], fiveg_rsrp_list[1:]):
        #check nans in lte/five g cells list
        fiveg_cell_count = 0
        lte_cell_count = 0
        nan_count = 0
        for cell in fiveg_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                fiveg_cell_count+=1
        if nan_count == len(fiveg_cells):
            fiveg_empty = True
        else:
            fiveg_empty = False

        nan_count = 0
        for cell in lte_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                lte_cell_count+=1
        if nan_count == len(lte_cells):
            lte_empty = True
        else:
            lte_empty = False
        if lte_empty == True and fiveg_empty == True:
            # let's backtrack 1 second
            main_index = short_index - 1
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_cell_list_main = df_main.iloc[main_index][["5G KPI PCell Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC UL Throughput [Mbps]"]]
                lte_cell_list_main = df_main.iloc[main_index][["LTE KPI PCell MAC UL Throughput[Mbps]", "LTE KPI SCell[1] MAC UL Throughput[Mbps]", "LTE KPI SCell[2] MAC UL Throughput[Mbps]", "LTE KPI SCell[3] MAC UL Throughput[Mbps]", "LTE KPI SCell[4] MAC UL Throughput[Mbps]"]]
                fiveg_cell_count = 0
                lte_cell_count = 0
                nan_count = 0
                for cell in fiveg_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        fiveg_cell_count+=1
                if nan_count == len(fiveg_cell_list_main):
                    fiveg_empty = True
                else:
                    fiveg_empty = False

                nan_count = 0
                for cell in lte_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        lte_cell_count+=1
                if nan_count == len(lte_cell_list_main):
                    lte_empty = True
                else:
                    lte_empty = False
                
                if lte_empty == True and fiveg_empty == True:
                    main_index-=1
                else:
                    # match found
                    break

                    
            # last check -> if still empty continue
            if lte_empty == True and fiveg_empty == True:
                continue
        total_cell_count = fiveg_cell_count + lte_cell_count
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
        
        # if speed > 0 and speed < 1:
        #     speed = 1

        if dt_measurement and speed > 20:
            import random
            # speed = 10
            speed = random.randint(0, 20)

        if pd.isnull(fiveg_mcs) and pd.isnull(lte_mcs):
            # let's backtrack 1 second - mcs
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_mcs_main = df_main.iloc[main_index][["5G KPI PCell Layer1 UL MCS (Avg)"]][0]
                lte_mcs_main = df_main.iloc[main_index][["LTE KPI PCell UL MCS"]][0]
                fiveg_mcs_count = 0
                lte_mcs_count = 0

                if pd.isnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(lte_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                mcs_list.append(fiveg_mcs)
        elif pd.isnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(lte_mcs)
        elif pd.notnull(fiveg_mcs) and pd.isnull(lte_mcs):
            mcs_list.append(fiveg_mcs)
        elif pd.notnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(fiveg_mcs)

        if pd.isnull(fiveg_bler) and pd.isnull(lte_bler):
            # let's backtrack 1 second - bler
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_bler_main = df_main.iloc[main_index][["5G KPI PCell Layer1 UL BLER [%]"]][0]
                lte_bler_main = df_main.iloc[main_index][["LTE KPI PUSCH BLER[%]"]][0]
                fiveg_bler_count = 0
                lte_bler_count = 0

                if pd.isnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(lte_bler_count)
                elif pd.notnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                elif pd.notnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                bler_list.append(fiveg_bler)
        elif pd.isnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(lte_bler)
        elif pd.notnull(fiveg_bler) and pd.isnull(lte_bler):
            bler_list.append(fiveg_bler)
        elif pd.notnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(fiveg_bler)

        if pd.isnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            # let's backtrack 1 second - rsrp
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_rsrp_main = df_main.iloc[main_index][['5G KPI PCell RF Serving SS-RSRP [dBm]']][0]
                lte_rsrp_main = df_main.iloc[main_index][['LTE KPI PCell Serving RSRP[dBm]']][0]
                fiveg_rsrp_count = 0
                lte_rsrp_count = 0

                if pd.isnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(lte_rsrp_count)
                elif pd.notnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                elif pd.notnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                rsrp_list.append(fiveg_rsrp)
        elif pd.isnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(lte_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)

        #get timezone
        tz = get_tz_info(prev_lat_lon, current_lat_lon)
        tz_list.append(tz)
        dist_list.append(distance_current)
        speed_list.append(speed)
        tput_current_list.append(tput)
        ca_list.append(total_cell_count)
        fiveg_ca_list.append(fiveg_cell_count)
        lte_ca_list.append(lte_cell_count)
        prev_lat_lon = (lat, lon)
        prev_ts = ts
    uniques, counts = np.unique(speed_list, return_counts=True)
    percentages = dict(zip(uniques, counts * 100 / len(speed_list)))
    speed_list = modify_speed_list(speed_list)
    if len(percentages) != 0:
        if 0 in percentages.keys():
            if percentages[0] > 85:
                #static run
                pass                            
            else:
                for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list):
                    if speed not in speed_tput_tuple.keys():
                            speed_tput_tuple[speed] = [tput]
                    else:
                        speed_tput_tuple[speed].append(tput)

                    if speed not in speed_ca_tuple.keys():
                            speed_ca_tuple[speed] = [ca]
                    else:
                        speed_ca_tuple[speed].append(ca)
                    
                    if speed not in speed_fiveg_ca_tuple.keys():
                            speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                    else:
                        speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                    if speed not in speed_lte_ca_tuple.keys():
                            speed_lte_ca_tuple[speed] = [lte_ca]
                    else:
                        speed_lte_ca_tuple[speed].append(lte_ca)

                    if speed not in speed_tz_tuple.keys():
                        speed_tz_tuple[speed] = [tz_temp]
                    else:
                        speed_tz_tuple[speed].append(tz_temp)

                    if speed not in speed_dist_tuple.keys():
                        speed_dist_tuple[speed] = [dist]
                    else:
                        speed_dist_tuple[speed].append(dist)
                    
                    if speed not in speed_mcs_tuple.keys():
                        speed_mcs_tuple[speed] = [mcs]
                    else:
                        speed_mcs_tuple[speed].append(mcs)
                    if speed not in speed_bler_tuple.keys():
                        speed_bler_tuple[speed] = [bler]
                    else:
                        speed_bler_tuple[speed].append(bler)
                    if speed not in speed_rsrp_tuple.keys():
                        speed_rsrp_tuple[speed] = [rsrp]
                    else:
                        speed_rsrp_tuple[speed].append(rsrp)
                
        else:
            for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list):
                if speed not in speed_tput_tuple.keys():
                        speed_tput_tuple[speed] = [tput]
                else:
                    speed_tput_tuple[speed].append(tput)

                if speed not in speed_ca_tuple.keys():
                    speed_ca_tuple[speed] = [ca]
                else:
                    speed_ca_tuple[speed].append(ca)

                if speed not in speed_fiveg_ca_tuple.keys():
                        speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                else:
                    speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                if speed not in speed_lte_ca_tuple.keys():
                        speed_lte_ca_tuple[speed] = [lte_ca]
                else:
                    speed_lte_ca_tuple[speed].append(lte_ca)

                if speed not in speed_tz_tuple.keys():
                    speed_tz_tuple[speed] = [tz_temp]
                else:
                    speed_tz_tuple[speed].append(tz_temp)

                if speed not in speed_dist_tuple.keys():
                    speed_dist_tuple[speed] = [dist]
                else:
                    speed_dist_tuple[speed].append(dist)
                
                if speed not in speed_mcs_tuple.keys():
                    speed_mcs_tuple[speed] = [mcs]
                else:
                    speed_mcs_tuple[speed].append(mcs)
                if speed not in speed_bler_tuple.keys():
                    speed_bler_tuple[speed] = [bler]
                else:
                    speed_bler_tuple[speed].append(bler)
                if speed not in speed_rsrp_tuple.keys():
                    speed_rsrp_tuple[speed] = [rsrp]
                else:
                    speed_rsrp_tuple[speed].append(rsrp)
    
    return [speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple]

def get_speed_dl_tput_ca_atnt(df_main, df_short_tput):
    speed_tput_tuple = {}
    speed_ca_tuple = {}
    speed_tz_tuple = {}
    speed_fiveg_ca_tuple = {}
    speed_lte_ca_tuple = {}
    speed_dist_tuple = {}
    speed_mcs_tuple = {}
    speed_rsrp_tuple = {}
    speed_bler_tuple = {}
    cols = ['Lat', 'Lon', "LTE KPI PCell DL MCS0", "5G KPI PCell Layer1 DL MCS (Avg)", "LTE KPI PDSCH BLER[%]", "5G KPI PCell Layer1 DL BLER [%]", 'LTE KPI PCell Serving RSRP[dBm]', '5G KPI PCell RF Serving SS-RSRP [dBm]']
    df_short_tput.loc[:,cols] = df_short_tput.loc[:,cols].ffill().bfill()
    speed_tput_tuple = {}
    if len(df_short_tput["Lat"].dropna()) == 0 or len(df_short_tput["Lon"].dropna()) == 0:
        return [speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple]
    short_index_list = list(df_short_tput["index"])
    lat_list = list(df_short_tput["Lat"])
    lon_list = list(df_short_tput["Lon"])
    ts_list = list(df_short_tput["TIME_STAMP"])
    lte_bler_list = list(df_short_tput["LTE KPI PDSCH BLER[%]"]) 
    fiveg_bler_list = list(df_short_tput["5G KPI PCell Layer1 DL BLER [%]"]) 
    lte_mcs_list = list(df_short_tput["LTE KPI PCell DL MCS0"])
    fiveg_mcs_list = list(df_short_tput["5G KPI PCell Layer1 DL MCS (Avg)"])
    lte_rsrp_list = list(df_short_tput['LTE KPI PCell Serving RSRP[dBm]'])
    fiveg_rsrp_list = list(df_short_tput['5G KPI PCell RF Serving SS-RSRP [dBm]'])
    tput_list = list(df_short_tput["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"])
    fiveg_cell_tput_list = df_short_tput[["5G KPI PCell Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC DL Throughput [Mbps]"]].values.tolist()
    lte_cell_tput_list = df_short_tput[["LTE KPI PCell MAC DL Throughput[Mbps]", "LTE KPI SCell[1] MAC DL Throughput[Mbps]", "LTE KPI SCell[2] MAC DL Throughput[Mbps]", "LTE KPI SCell[3] MAC DL Throughput[Mbps]", "LTE KPI SCell[4] MAC DL Throughput[Mbps]"]].values.tolist()
    prev_lat_lon = (lat_list[0], lon_list[0])
    prev_ts = ts_list[0]
    dist_list = []
    tz_list = []
    speed_list = []
    mcs_list = []
    rsrp_list = []
    ca_list = []
    fiveg_ca_list = []
    lte_ca_list = []
    tput_current_list = []
    bler_list = []
    dt_measurement = downtown_measurements_mod((lat_list[0], lon_list[0]), (lat_list[-1], lon_list[-1]))
    for short_index, lat, lon, ts, tput, fiveg_cells, lte_cells, lte_mcs, fiveg_mcs, lte_bler, fiveg_bler, lte_rsrp, fiveg_rsrp in zip(short_index_list[1:], lat_list[1:], lon_list[1:], ts_list[1:], tput_list[1:], fiveg_cell_tput_list[1:], lte_cell_tput_list[1:], lte_mcs_list[1:], fiveg_mcs_list[1:], lte_bler_list[1:], fiveg_bler_list[1:], lte_rsrp_list[1:], fiveg_rsrp_list[1:]):
        #check nans in lte/five g cells list
        fiveg_cell_count = 0
        lte_cell_count = 0
        nan_count = 0
        for cell in fiveg_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                fiveg_cell_count+=1
        if nan_count == len(fiveg_cells):
            fiveg_empty = True
        else:
            fiveg_empty = False

        nan_count = 0
        for cell in lte_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                lte_cell_count+=1
        if nan_count == len(lte_cells):
            lte_empty = True
        else:
            lte_empty = False
        if lte_empty == True and fiveg_empty == True:
            # let's backtrack 1 second
            main_index = short_index - 1
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_cell_list_main = df_main.iloc[main_index][["5G KPI PCell Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC DL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC DL Throughput [Mbps]"]]
                lte_cell_list_main = df_main.iloc[main_index][["LTE KPI PCell MAC DL Throughput[Mbps]", "LTE KPI SCell[1] MAC DL Throughput[Mbps]", "LTE KPI SCell[2] MAC DL Throughput[Mbps]", "LTE KPI SCell[3] MAC DL Throughput[Mbps]", "LTE KPI SCell[4] MAC DL Throughput[Mbps]"]]
                fiveg_cell_count = 0
                lte_cell_count = 0
                nan_count = 0
                for cell in fiveg_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        fiveg_cell_count+=1
                if nan_count == len(fiveg_cell_list_main):
                    fiveg_empty = True
                else:
                    fiveg_empty = False

                nan_count = 0
                for cell in lte_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        lte_cell_count+=1
                if nan_count == len(lte_cell_list_main):
                    lte_empty = True
                else:
                    lte_empty = False
                
                if lte_empty == True and fiveg_empty == True:
                    main_index-=1
                else:
                    # match found
                    break

                    
            # last check -> if still empty continue
            if lte_empty == True and fiveg_empty == True:
                continue
        total_cell_count = fiveg_cell_count + lte_cell_count
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
        
        # if speed > 0 and speed < 1:
        #     speed = 1

        if dt_measurement and speed > 20:
            import random
            # speed = 10
            speed = random.randint(0, 20)

        if pd.isnull(fiveg_mcs) and pd.isnull(lte_mcs):
            # let's backtrack 1 second - mcs
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_mcs_main = df_main.iloc[main_index][["5G KPI PCell Layer1 DL MCS (Avg)"]][0]
                lte_mcs_main = df_main.iloc[main_index][["LTE KPI PCell DL MCS0"]][0]
                fiveg_mcs_count = 0
                lte_mcs_count = 0

                if pd.isnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(lte_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                mcs_list.append(fiveg_mcs)
        elif pd.isnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(lte_mcs)
        elif pd.notnull(fiveg_mcs) and pd.isnull(lte_mcs):
            mcs_list.append(fiveg_mcs)
        elif pd.notnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(fiveg_mcs)


        if pd.isnull(fiveg_bler) and pd.isnull(lte_bler):
            # let's backtrack 1 second - bler
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_bler_main = df_main.iloc[main_index][["5G KPI PCell Layer1 DL BLER [%]"]][0]
                lte_bler_main = df_main.iloc[main_index][["LTE KPI PDSCH BLER[%]"]][0]
                fiveg_bler_count = 0
                lte_bler_count = 0

                if pd.isnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(lte_bler_count)
                elif pd.notnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                elif pd.notnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                bler_list.append(fiveg_bler)
        elif pd.isnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(lte_bler)
        elif pd.notnull(fiveg_bler) and pd.isnull(lte_bler):
            bler_list.append(fiveg_bler)
        elif pd.notnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(fiveg_bler)

        if pd.isnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            # let's backtrack 1 second - rsrp
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_rsrp_main = df_main.iloc[main_index][['5G KPI PCell RF Serving SS-RSRP [dBm]']][0]
                lte_rsrp_main = df_main.iloc[main_index][['LTE KPI PCell Serving RSRP[dBm]']][0]
                fiveg_rsrp_count = 0
                lte_rsrp_count = 0

                if pd.isnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(lte_rsrp_count)
                elif pd.notnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                elif pd.notnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                rsrp_list.append(fiveg_rsrp)
        elif pd.isnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(lte_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)

        #get timezone
        tz = get_tz_info(prev_lat_lon, current_lat_lon)
        tz_list.append(tz)
        dist_list.append(distance_current)
        speed_list.append(speed)
        tput_current_list.append(tput)
        ca_list.append(total_cell_count)
        fiveg_ca_list.append(fiveg_cell_count)
        lte_ca_list.append(lte_cell_count)
        prev_lat_lon = (lat, lon)
        prev_ts = ts
    uniques, counts = np.unique(speed_list, return_counts=True)
    percentages = dict(zip(uniques, counts * 100 / len(speed_list)))
    speed_list = modify_speed_list(speed_list)
    if len(percentages) != 0:
        if 0 in percentages.keys():
            if percentages[0] > 85:
                #static run
                # global_static_removed_dl_df.append(df_current)
                pass                            
            else:
                for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list):
                    if speed not in speed_tput_tuple.keys():
                            speed_tput_tuple[speed] = [tput]
                    else:
                        speed_tput_tuple[speed].append(tput)

                    if speed not in speed_ca_tuple.keys():
                            speed_ca_tuple[speed] = [ca]
                    else:
                        speed_ca_tuple[speed].append(ca)
                    
                    if speed not in speed_fiveg_ca_tuple.keys():
                            speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                    else:
                        speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                    if speed not in speed_lte_ca_tuple.keys():
                            speed_lte_ca_tuple[speed] = [lte_ca]
                    else:
                        speed_lte_ca_tuple[speed].append(lte_ca)
                    
                    if speed not in speed_tz_tuple.keys():
                        speed_tz_tuple[speed] = [tz_temp]
                    else:
                        speed_tz_tuple[speed].append(tz_temp)

                    if speed not in speed_dist_tuple.keys():
                        speed_dist_tuple[speed] = [dist]
                    else:
                        speed_dist_tuple[speed].append(dist)

                    if speed not in speed_mcs_tuple.keys():
                        speed_mcs_tuple[speed] = [mcs]
                    else:
                        speed_mcs_tuple[speed].append(mcs)
                    
                    if speed not in speed_bler_tuple.keys():
                        speed_bler_tuple[speed] = [bler]
                    else:
                        speed_bler_tuple[speed].append(bler)
                    
                    if speed not in speed_rsrp_tuple.keys():
                        speed_rsrp_tuple[speed] = [rsrp]
                    else:
                        speed_rsrp_tuple[speed].append(rsrp)
        else:
            for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list):
                if speed not in speed_tput_tuple.keys():
                        speed_tput_tuple[speed] = [tput]
                else:
                    speed_tput_tuple[speed].append(tput)

                if speed not in speed_ca_tuple.keys():
                    speed_ca_tuple[speed] = [ca]
                else:
                    speed_ca_tuple[speed].append(ca)

                if speed not in speed_fiveg_ca_tuple.keys():
                        speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                else:
                    speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                if speed not in speed_lte_ca_tuple.keys():
                        speed_lte_ca_tuple[speed] = [lte_ca]
                else:
                    speed_lte_ca_tuple[speed].append(lte_ca)
                
                if speed not in speed_tz_tuple.keys():
                    speed_tz_tuple[speed] = [tz_temp]
                else:
                    speed_tz_tuple[speed].append(tz_temp)

                if speed not in speed_dist_tuple.keys():
                    speed_dist_tuple[speed] = [dist]
                else:
                    speed_dist_tuple[speed].append(dist)

                if speed not in speed_mcs_tuple.keys():
                    speed_mcs_tuple[speed] = [mcs]
                else:
                    speed_mcs_tuple[speed].append(mcs)
                
                if speed not in speed_bler_tuple.keys():
                    speed_bler_tuple[speed] = [bler]
                else:
                    speed_bler_tuple[speed].append(bler)

                if speed not in speed_rsrp_tuple.keys():
                    speed_rsrp_tuple[speed] = [rsrp]
                else:
                    speed_rsrp_tuple[speed].append(rsrp)

    return [speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple]

def get_speed_ul_tput_ca_atnt(df_main, df_short_tput):
    speed_tput_tuple = {}
    speed_ca_tuple = {}
    speed_tz_tuple = {}
    speed_fiveg_ca_tuple = {}
    speed_lte_ca_tuple = {}
    speed_dist_tuple = {}
    speed_mcs_tuple = {}
    speed_rsrp_tuple = {}
    speed_bler_tuple = {}
    cols = ['Lat', 'Lon', "LTE KPI PCell UL MCS", "5G KPI PCell Layer1 UL MCS (Avg)", "LTE KPI PUSCH BLER[%]", "5G KPI PCell Layer1 UL BLER [%]", 'LTE KPI PCell Serving RSRP[dBm]', '5G KPI PCell RF Serving SS-RSRP [dBm]']
    df_short_tput.loc[:,cols] = df_short_tput.loc[:,cols].ffill().bfill()
    if len(df_short_tput["Lat"].dropna()) == 0 or len(df_short_tput["Lon"].dropna()) == 0:
        return [speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple]
    short_index_list = list(df_short_tput["index"])
    lat_list = list(df_short_tput["Lat"])
    lon_list = list(df_short_tput["Lon"])
    ts_list = list(df_short_tput["TIME_STAMP"])
    lte_bler_list = list(df_short_tput["LTE KPI PUSCH BLER[%]"]) 
    fiveg_bler_list = list(df_short_tput["5G KPI PCell Layer1 UL BLER [%]"]) 
    lte_mcs_list = list(df_short_tput["LTE KPI PCell UL MCS"])
    fiveg_mcs_list = list(df_short_tput["5G KPI PCell Layer1 UL MCS (Avg)"])
    lte_rsrp_list = list(df_short_tput['LTE KPI PCell Serving RSRP[dBm]'])
    fiveg_rsrp_list = list(df_short_tput['5G KPI PCell RF Serving SS-RSRP [dBm]'])
    tput_list = list(df_short_tput["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"])
    fiveg_cell_tput_list = df_short_tput[["5G KPI PCell Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC UL Throughput [Mbps]"]].values.tolist()
    lte_cell_tput_list = df_short_tput[["LTE KPI PCell MAC UL Throughput[Mbps]", "LTE KPI SCell[1] MAC UL Throughput[Mbps]", "LTE KPI SCell[2] MAC UL Throughput[Mbps]", "LTE KPI SCell[3] MAC UL Throughput[Mbps]", "LTE KPI SCell[4] MAC UL Throughput[Mbps]"]].values.tolist()
    prev_lat_lon = (lat_list[0], lon_list[0])
    prev_ts = ts_list[0]
    dist_list = []
    speed_list = []
    tz_list = []
    ca_list = []
    mcs_list = []
    rsrp_list = []
    fiveg_ca_list = []
    lte_ca_list = []
    tput_current_list = []
    bler_list = []
    dt_measurement = downtown_measurements_mod((lat_list[0], lon_list[0]), (lat_list[-1], lon_list[-1]))
    for short_index, lat, lon, ts, tput, fiveg_cells, lte_cells, lte_mcs, fiveg_mcs, lte_bler, fiveg_bler, lte_rsrp, fiveg_rsrp in zip(short_index_list[1:], lat_list[1:], lon_list[1:], ts_list[1:], tput_list[1:], fiveg_cell_tput_list[1:], lte_cell_tput_list[1:], lte_mcs_list[1:], fiveg_mcs_list[1:], lte_bler_list[1:], fiveg_bler_list[1:], lte_rsrp_list[1:], fiveg_rsrp_list[1:]):
        #check nans in lte/five g cells list
        fiveg_cell_count = 0
        lte_cell_count = 0
        nan_count = 0
        for cell in fiveg_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                fiveg_cell_count+=1
        if nan_count == len(fiveg_cells):
            fiveg_empty = True
        else:
            fiveg_empty = False

        nan_count = 0
        for cell in lte_cells:
            if pd.isnull(cell):
                nan_count+=1
            else:
                lte_cell_count+=1
        if nan_count == len(lte_cells):
            lte_empty = True
        else:
            lte_empty = False
        if lte_empty == True and fiveg_empty == True:
            # let's backtrack 1 second
            main_index = short_index - 1
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_cell_list_main = df_main.iloc[main_index][["5G KPI PCell Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[1] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[2] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[3] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[4] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[5] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[6] Layer2 MAC UL Throughput [Mbps]", "5G KPI SCell[7] Layer2 MAC UL Throughput [Mbps]"]]
                lte_cell_list_main = df_main.iloc[main_index][["LTE KPI PCell MAC UL Throughput[Mbps]", "LTE KPI SCell[1] MAC UL Throughput[Mbps]", "LTE KPI SCell[2] MAC UL Throughput[Mbps]", "LTE KPI SCell[3] MAC UL Throughput[Mbps]", "LTE KPI SCell[4] MAC UL Throughput[Mbps]"]]
                fiveg_cell_count = 0
                lte_cell_count = 0
                nan_count = 0
                for cell in fiveg_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        fiveg_cell_count+=1
                if nan_count == len(fiveg_cell_list_main):
                    fiveg_empty = True
                else:
                    fiveg_empty = False

                nan_count = 0
                for cell in lte_cell_list_main:
                    if pd.isnull(cell):
                        nan_count+=1
                    else:
                        lte_cell_count+=1
                if nan_count == len(lte_cell_list_main):
                    lte_empty = True
                else:
                    lte_empty = False
                
                if lte_empty == True and fiveg_empty == True:
                    main_index-=1
                else:
                    # match found
                    break

                    
            # last check -> if still empty continue
            if lte_empty == True and fiveg_empty == True:
                continue
        total_cell_count = fiveg_cell_count + lte_cell_count
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
        
        # if speed > 0 and speed < 1:
        #     speed = 1

        if dt_measurement and speed > 20:
            import random
            # speed = 10
            speed = random.randint(0, 20)

        if pd.isnull(fiveg_mcs) and pd.isnull(lte_mcs):
            # let's backtrack 1 second - mcs
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_mcs_main = df_main.iloc[main_index][["5G KPI PCell Layer1 UL MCS (Avg)"]][0]
                lte_mcs_main = df_main.iloc[main_index][["LTE KPI PCell UL MCS"]][0]
                fiveg_mcs_count = 0
                lte_mcs_count = 0

                if pd.isnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(lte_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.isnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                elif pd.notnull(fiveg_mcs_main) and pd.notnull(lte_mcs_main):
                    mcs_list.append(fiveg_mcs_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                mcs_list.append(fiveg_mcs)
        elif pd.isnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(lte_mcs)
        elif pd.notnull(fiveg_mcs) and pd.isnull(lte_mcs):
            mcs_list.append(fiveg_mcs)
        elif pd.notnull(fiveg_mcs) and pd.notnull(lte_mcs):
            mcs_list.append(fiveg_mcs)

        if pd.isnull(fiveg_bler) and pd.isnull(lte_bler):
            # let's backtrack 1 second - bler
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_bler_main = df_main.iloc[main_index][["5G KPI PCell Layer1 UL BLER [%]"]][0]
                lte_bler_main = df_main.iloc[main_index][["LTE KPI PUSCH BLER[%]"]][0]
                fiveg_bler_count = 0
                lte_bler_count = 0

                if pd.isnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(lte_bler_count)
                elif pd.notnull(fiveg_bler_main) and pd.isnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                elif pd.notnull(fiveg_bler_main) and pd.notnull(lte_bler_count):
                    bler_list.append(fiveg_bler_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                bler_list.append(fiveg_bler)
        elif pd.isnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(lte_bler)
        elif pd.notnull(fiveg_bler) and pd.isnull(lte_bler):
            bler_list.append(fiveg_bler)
        elif pd.notnull(fiveg_bler) and pd.notnull(lte_bler):
            bler_list.append(fiveg_bler)

        if pd.isnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            # let's backtrack 1 second - rsrp
            main_index = short_index - 1
            found = 0
            while ts - df_main.iloc[main_index]["TIME_STAMP"] <= 1.0:
                fiveg_rsrp_main = df_main.iloc[main_index][['5G KPI PCell RF Serving SS-RSRP [dBm]']][0]
                lte_rsrp_main = df_main.iloc[main_index][['LTE KPI PCell Serving RSRP[dBm]']][0]
                fiveg_rsrp_count = 0
                lte_rsrp_count = 0

                if pd.isnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    main_index-=1
                    continue
                elif pd.isnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(lte_rsrp_count)
                elif pd.notnull(fiveg_rsrp_main) and pd.isnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                elif pd.notnull(fiveg_rsrp_main) and pd.notnull(lte_rsrp_count):
                    rsrp_list.append(fiveg_rsrp_main)
                found = 1
                break

            # last check -> put null
            if found == 0:
                rsrp_list.append(fiveg_rsrp)
        elif pd.isnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(lte_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.isnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)
        elif pd.notnull(fiveg_rsrp) and pd.notnull(lte_rsrp):
            rsrp_list.append(fiveg_rsrp)

        #get timezone
        tz = get_tz_info(prev_lat_lon, current_lat_lon)
        tz_list.append(tz)
        dist_list.append(distance_current)
        speed_list.append(speed)
        tput_current_list.append(tput)
        ca_list.append(total_cell_count)
        fiveg_ca_list.append(fiveg_cell_count)
        lte_ca_list.append(lte_cell_count)
        prev_lat_lon = (lat, lon)
        prev_ts = ts
    uniques, counts = np.unique(speed_list, return_counts=True)
    percentages = dict(zip(uniques, counts * 100 / len(speed_list)))
    speed_list = modify_speed_list(speed_list)
    if len(percentages) != 0:
        if 0 in percentages.keys():
            if percentages[0] > 85:
                #static run
                pass                            
            else:
                for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list):
                    if speed not in speed_tput_tuple.keys():
                            speed_tput_tuple[speed] = [tput]
                    else:
                        speed_tput_tuple[speed].append(tput)

                    if speed not in speed_ca_tuple.keys():
                            speed_ca_tuple[speed] = [ca]
                    else:
                        speed_ca_tuple[speed].append(ca)
                    
                    if speed not in speed_fiveg_ca_tuple.keys():
                            speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                    else:
                        speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                    if speed not in speed_lte_ca_tuple.keys():
                            speed_lte_ca_tuple[speed] = [lte_ca]
                    else:
                        speed_lte_ca_tuple[speed].append(lte_ca)
                    
                    if speed not in speed_tz_tuple.keys():
                        speed_tz_tuple[speed] = [tz_temp]
                    else:
                        speed_tz_tuple[speed].append(tz_temp)

                    if speed not in speed_dist_tuple.keys():
                        speed_dist_tuple[speed] = [dist]
                    else:
                        speed_dist_tuple[speed].append(dist)

                    if speed not in speed_mcs_tuple.keys():
                        speed_mcs_tuple[speed] = [mcs]
                    else:
                        speed_mcs_tuple[speed].append(mcs)

                    if speed not in speed_bler_tuple.keys():
                        speed_bler_tuple[speed] = [bler]
                    else:
                        speed_bler_tuple[speed].append(bler)
                    
                    if speed not in speed_rsrp_tuple.keys():
                        speed_rsrp_tuple[speed] = [rsrp]
                    else:
                        speed_rsrp_tuple[speed].append(rsrp)
        else:
            for speed, dist, tput, ca, fiveg_ca, lte_ca, tz_temp, mcs, bler, rsrp in zip(speed_list, dist_list, tput_current_list, ca_list, fiveg_ca_list, lte_ca_list, tz_list, mcs_list, bler_list, rsrp_list):
                if speed not in speed_tput_tuple.keys():
                        speed_tput_tuple[speed] = [tput]
                else:
                    speed_tput_tuple[speed].append(tput)

                if speed not in speed_ca_tuple.keys():
                    speed_ca_tuple[speed] = [ca]
                else:
                    speed_ca_tuple[speed].append(ca)

                if speed not in speed_fiveg_ca_tuple.keys():
                        speed_fiveg_ca_tuple[speed] = [fiveg_ca]
                else:
                    speed_fiveg_ca_tuple[speed].append(fiveg_ca)

                if speed not in speed_lte_ca_tuple.keys():
                        speed_lte_ca_tuple[speed] = [lte_ca]
                else:
                    speed_lte_ca_tuple[speed].append(lte_ca)

                if speed not in speed_tz_tuple.keys():
                    speed_tz_tuple[speed] = [tz_temp]
                else:
                    speed_tz_tuple[speed].append(tz_temp)

                if speed not in speed_dist_tuple.keys():
                    speed_dist_tuple[speed] = [dist]
                else:
                    speed_dist_tuple[speed].append(dist)
                
                if speed not in speed_mcs_tuple.keys():
                    speed_mcs_tuple[speed] = [mcs]
                else:
                    speed_mcs_tuple[speed].append(mcs)
                if speed not in speed_bler_tuple.keys():
                    speed_bler_tuple[speed] = [bler]
                else:
                    speed_bler_tuple[speed].append(bler)
                if speed not in speed_rsrp_tuple.keys():
                    speed_rsrp_tuple[speed] = [rsrp]
                else:
                    speed_rsrp_tuple[speed].append(rsrp)
    return [speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple]


base = r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\tput\driving"
main_op_link_dict = {"verizon" : {"dl" : 0, "ul" : 0}, "tmobile" : {"dl" : 0, "ul" : 0}, "atnt" : {"dl" : 0, "ul" : 0}}
for op in ["verizon", "tmobile", "atnt"]:
    for link in ["dl", "ul"]:
        csv_directory_list = glob.glob(base + "\\" + op + "\\" + link + "\\*.csv")
        global_count_continue = 1
        ca_reject_count = 0
        tput_tz_tech_dict = {'America/Los_Angeles' : [], 'America/Denver' : [], 'America/Chicago' : [], 'America/New_York' : [], None : []}
        tput_tz_tech_dict_modified = {'America/Los_Angeles' : "PacificTime", 'America/Denver' : "MountainTime", 'America/Chicago' : "CentralTime", 'America/New_York' : "EasternTime" }
        tz_tech_dict = {'America/Los_Angeles' : {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}, 'America/Denver' : {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}, 'America/Chicago' : {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}, 'America/New_York' : {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}, None : {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}}
        tput_speed_tech_dict = {"LTE" : {}, "LTE-A" : {}, "5G-low" : {}, "5G-sub6" : {}, "5G-mmWave 28 GHz" : {}, "5G-mmWave 39 GHz" : {}}
        dist_speed_tech_dict = {"LTE" : [], "LTE-A" : [], "5G-low" : [], "5G-sub6" : [], "5G-mmWave 28 GHz" : [], "5G-mmWave 39 GHz" : []}
        time_tput_speed_tech_dict = {"LTE" : {}, "LTE-A" : {}, "5G-low" : {}, "5G-sub6" : {}, "5G-mmWave 28 GHz" : {}, "5G-mmWave 39 GHz" : {}}
        ca_speed_tech_dict = {"LTE" : {}, "LTE-A" : {}, "5G-low" : {}, "5G-sub6" : {}, "5G-mmWave 28 GHz" : {}, "5G-mmWave 39 GHz" : {}}
        lte_ca_speed_dict = {"LTE" : {}, "LTE-A" : {}, "5G-low" : {}, "5G-sub6" : {}, "5G-mmWave 28 GHz" : {}, "5G-mmWave 39 GHz" : {}}
        fiveg_ca_speed_dict = {"LTE" : {}, "LTE-A" : {}, "5G-low" : {}, "5G-sub6" : {}, "5G-mmWave 28 GHz" : {}, "5G-mmWave 39 GHz" : {}}
        mcs_speed_dict = {"LTE" : {}, "LTE-A" : {}, "5G-low" : {}, "5G-sub6" : {}, "5G-mmWave 28 GHz" : {}, "5G-mmWave 39 GHz" : {}}
        bler_speed_dict = {"LTE" : {}, "LTE-A" : {}, "5G-low" : {}, "5G-sub6" : {}, "5G-mmWave 28 GHz" : {}, "5G-mmWave 39 GHz" : {}}
        wl_speed_dict = {"LTE" : {}, "LTE-A" : {}, "5G-low" : {}, "5G-sub6" : {}, "5G-mmWave 28 GHz" : {}, "5G-mmWave 39 GHz" : {}}
        rsrp_speed_dict = {"LTE" : {}, "LTE-A" : {}, "5G-low" : {}, "5G-sub6" : {}, "5G-mmWave 28 GHz" : {}, "5G-mmWave 39 GHz" : {}}
        overall_mean_list = []
        overall_std_list = []
        overall_5g_high_percent = []
        color_dict = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
        for csv in csv_directory_list:
            df_short = pd.read_csv(csv)
            if link == "dl":
                df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"].notna()]
                df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"] > 0.1]
            else:
                df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].notna()]
                df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"] > 0.1]

            df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
            if len(df_short_ho) != 0 and op == 'verizon':
                df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].str.contains("Handover Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Success")]
            df_merged = pd.concat([df_short_tput, df_short_ho])
            df_merged = df_merged.sort_values(by=["TIME_STAMP"])
            df_merged.reset_index(inplace=True)
            if len(df_merged) == 0:
                continue

            break_list = []
            event = -99
            start_flag = 0
            tech_list_all = []
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
                break_list.append(df_merged[start_index_count:end_index_count+1])
            # now calculate technology - throughput
            issue_count = 0
            used_test_count = 0
            for tput_df in break_list:
                modified_tech = ""
                # check if 5G frequency or 5G PCI  is empty
                if len(list(tput_df["5G KPI PCell RF Frequency [MHz]"].dropna())) > 0 or len(list(tput_df["5G KPI PCell RF Serving PCI"].dropna())) > 0:
                    # it is a 5G run 
                    # get type of 5G 
                    freq_list = list(tput_df["5G KPI PCell RF Frequency [MHz]"].dropna())
                    ffreq = float(max(set(freq_list), key=freq_list.count))
                    if int(ffreq) < 1000:
                        modified_tech = "5G-low"
                    elif int(ffreq) > 1000 and int(ffreq) < 7000:
                        modified_tech = "5G-sub6"
                    elif int(ffreq) > 7000 and int(ffreq) < 35000:
                        modified_tech = "5G-mmWave 28 GHz"
                    elif int(ffreq) > 35000:
                        modified_tech = "5G-mmWave 39 GHz"
                    
                    if link == "dl":
                        if op == "verizon":
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple, speed_wl_tuple = get_speed_dl_tput_ca_verizon(df_short, tput_df)
                        elif op == "tmobile":
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple = get_speed_dl_tput_ca_tmobile(df_short, tput_df)
                        else:
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple = get_speed_dl_tput_ca_atnt(df_short, tput_df)
                    else:
                        if op == "verizon":
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple, speed_wl_tuple = get_speed_ul_tput_ca_verizon(df_short, tput_df)
                        elif op == "tmobile":
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple = get_speed_ul_tput_ca_tmobile(df_short, tput_df)
                        else:
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple = get_speed_ul_tput_ca_atnt(df_short, tput_df)

                    for speed in speed_tput_tuple.keys():
                        used_test_count+=1

                        if speed not in tput_speed_tech_dict[modified_tech].keys():
                            tput_speed_tech_dict[modified_tech][speed] = speed_tput_tuple[speed]
                        else:
                            tput_speed_tech_dict[modified_tech][speed].extend(speed_tput_tuple[speed])

                        # total ca
                        if speed not in ca_speed_tech_dict[modified_tech].keys():
                            ca_speed_tech_dict[modified_tech][speed] = speed_ca_tuple[speed]
                        else:
                            ca_speed_tech_dict[modified_tech][speed].extend(speed_ca_tuple[speed])
                        
                        #fiveg ca
                        if speed not in fiveg_ca_speed_dict[modified_tech].keys():
                            fiveg_ca_speed_dict[modified_tech][speed] = speed_fiveg_ca_tuple[speed]
                        else:
                            fiveg_ca_speed_dict[modified_tech][speed].extend(speed_fiveg_ca_tuple[speed])

                        if speed not in lte_ca_speed_dict[modified_tech].keys():
                            lte_ca_speed_dict[modified_tech][speed] = speed_lte_ca_tuple[speed]
                        else:
                            lte_ca_speed_dict[modified_tech][speed].extend(speed_lte_ca_tuple[speed])
                        # tput_tz_tech_dict
                        temp_tz_tput_idx = 0
                        for tz in speed_tz_tuple[speed]:
                            tput_tz_tech_dict[tz].append(speed_tput_tuple[speed][temp_tz_tput_idx])
                            tz_tech_dict[tz][modified_tech].append(speed_tput_tuple[speed][temp_tz_tput_idx])
                            temp_tz_tput_idx+=1

                        if speed not in mcs_speed_dict[modified_tech].keys():
                            mcs_speed_dict[modified_tech][speed] = speed_mcs_tuple[speed]
                        else:
                            mcs_speed_dict[modified_tech][speed].extend(speed_mcs_tuple[speed])
                        
                        if speed not in bler_speed_dict[modified_tech].keys():
                            bler_speed_dict[modified_tech][speed] = speed_bler_tuple[speed]
                        else:
                            bler_speed_dict[modified_tech][speed].extend(speed_bler_tuple[speed])

                        if speed not in rsrp_speed_dict[modified_tech].keys():
                            rsrp_speed_dict[modified_tech][speed] = speed_rsrp_tuple[speed]
                        else:
                            rsrp_speed_dict[modified_tech][speed].extend(speed_rsrp_tuple[speed])

                        if op == "verizon":
                            if speed not in wl_speed_dict[modified_tech].keys():
                                wl_speed_dict[modified_tech][speed] = speed_wl_tuple[speed]
                            else:
                                wl_speed_dict[modified_tech][speed].extend(speed_wl_tuple[speed])
                        if "LTE" in modified_tech or "low" in modified_tech:
                            tech_list_all.append("LTE")
                        else:
                            tech_list_all.append("5G")
                    

                    dist_list = []
                    for speed in speed_dist_tuple.keys():
                        dist_list.extend(speed_dist_tuple[speed])
                    
                    dist_speed_tech_dict[modified_tech].append(np.sum(dist_list))
                    modified_tech = ""
                else:
                    # it is LTE
                    # what frequency ? 
                    earfcn_list = list(tput_df["LTE KPI PCell Serving EARFCN(DL)"].dropna())
                    if len(earfcn_list) == 0:
                        continue
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
                    
                    if link == "dl":
                        if op == "verizon":
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple, speed_wl_tuple = get_speed_dl_tput_ca_verizon(df_short, tput_df)
                        elif op == "tmobile":
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple = get_speed_dl_tput_ca_tmobile(df_short, tput_df)
                        else:
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple = get_speed_dl_tput_ca_atnt(df_short, tput_df)
                    else:
                        if op == "verizon":
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple, speed_wl_tuple = get_speed_ul_tput_ca_verizon(df_short, tput_df)
                        elif op == "tmobile":
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple = get_speed_ul_tput_ca_tmobile(df_short, tput_df)
                        else:
                            speed_tput_tuple, speed_ca_tuple, speed_fiveg_ca_tuple, speed_lte_ca_tuple, speed_tz_tuple, speed_dist_tuple, speed_mcs_tuple, speed_bler_tuple, speed_rsrp_tuple = get_speed_ul_tput_ca_atnt(df_short, tput_df)

                    for speed in speed_tput_tuple.keys():
                        used_test_count+=1
                     
                        for fivegca in speed_fiveg_ca_tuple[speed]:
                            # LTE trace - no 5G CA should be here - outlier data - remove it
                            if fivegca in [1, 2, 3, 4, 5, 6, 7, 8] :
                                ca_reject_count+=len(speed_fiveg_ca_tuple[speed])
                                continue
                        
                        if modified_tech == "LTE-A":
                            # theoretically not possible to have LTE-A with tput > 1000 Mbps - these are outliers in all probability - remove it
                            speed_tput_tuple[speed] = remove_values(speed_tput_tuple[speed], 1000)

                        if speed not in tput_speed_tech_dict[modified_tech].keys():
                            tput_speed_tech_dict[modified_tech][speed] = speed_tput_tuple[speed]
                        else:
                            tput_speed_tech_dict[modified_tech][speed].extend(speed_tput_tuple[speed])

                        # total ca
                        if speed not in ca_speed_tech_dict[modified_tech].keys():
                            ca_speed_tech_dict[modified_tech][speed] = speed_ca_tuple[speed]
                        else:
                            ca_speed_tech_dict[modified_tech][speed].extend(speed_ca_tuple[speed])
                        
                        #fiveg ca
                        if speed not in fiveg_ca_speed_dict[modified_tech].keys():
                            fiveg_ca_speed_dict[modified_tech][speed] = speed_fiveg_ca_tuple[speed]
                        else:
                            fiveg_ca_speed_dict[modified_tech][speed].extend(speed_fiveg_ca_tuple[speed])

                        #lte ca
                        if speed not in lte_ca_speed_dict[modified_tech].keys():
                            lte_ca_speed_dict[modified_tech][speed] = speed_lte_ca_tuple[speed]
                        else:
                            lte_ca_speed_dict[modified_tech][speed].extend(speed_lte_ca_tuple[speed])
                        
                        # tput_tz_tech_dict
                        temp_tz_tput_idx = 0
                        for tz in speed_tz_tuple[speed]:
                            if len(speed_tput_tuple[speed]) != 0:
                                tput_tz_tech_dict[tz].append(speed_tput_tuple[speed][temp_tz_tput_idx])
                                tz_tech_dict[tz][modified_tech].append(speed_tput_tuple[speed][temp_tz_tput_idx])
                                temp_tz_tput_idx+=1

                        if speed not in mcs_speed_dict[modified_tech].keys():
                            mcs_speed_dict[modified_tech][speed] = speed_mcs_tuple[speed]
                        else:
                            mcs_speed_dict[modified_tech][speed].extend(speed_mcs_tuple[speed])
                        
                        if speed not in bler_speed_dict[modified_tech].keys():
                            bler_speed_dict[modified_tech][speed] = speed_bler_tuple[speed]
                        else:
                            bler_speed_dict[modified_tech][speed].extend(speed_bler_tuple[speed])

                        if speed not in rsrp_speed_dict[modified_tech].keys():
                            rsrp_speed_dict[modified_tech][speed] = speed_rsrp_tuple[speed]
                        else:
                            rsrp_speed_dict[modified_tech][speed].extend(speed_rsrp_tuple[speed])
                        if op == "verizon":
                            if speed not in wl_speed_dict[modified_tech].keys():
                                wl_speed_dict[modified_tech][speed] = speed_wl_tuple[speed]
                            else:
                                wl_speed_dict[modified_tech][speed].extend(speed_wl_tuple[speed])
                        if "LTE" in modified_tech or "low" in modified_tech:
                            tech_list_all.append("LTE")
                        else:
                            tech_list_all.append("5G")

                    dist_list = []
                    for speed in speed_dist_tuple.keys():
                        dist_list.extend(speed_dist_tuple[speed])
                    
                    dist_speed_tech_dict[modified_tech].append(np.sum(dist_list))
                    modified_tech = ""

            if used_test_count == 0:
                print("Static!")
            else:
                if link == "dl":
                    if len(df_merged["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"].dropna()) > 0:
                        overall_mean_list.append(np.mean(list(df_merged["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"].dropna())))
                        overall_std_list.append(np.std(list(df_merged["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"].dropna())))
                        percentage_5g = (tech_list_all.count('5G') / len(tech_list_all)) * 100
                        overall_5g_high_percent.append(percentage_5g)
                else:
                    if len(df_merged["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].dropna()) > 0:
                        overall_mean_list.append(np.mean(list(df_merged["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].dropna())))
                        overall_std_list.append(np.std(list(df_merged["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].dropna())))
                        percentage_5g = (tech_list_all.count('5G') / len(tech_list_all)) * 100
                        overall_5g_high_percent.append(percentage_5g)
            
        
        main_op_link_dict[op][link] = [tput_speed_tech_dict, ca_speed_tech_dict, fiveg_ca_speed_dict, lte_ca_speed_dict, tput_tz_tech_dict, dist_speed_tech_dict, mcs_speed_dict, bler_speed_dict, rsrp_speed_dict, wl_speed_dict, overall_mean_list, overall_std_list, overall_5g_high_percent]

filehandler = open(base + "\\processed\main_op_link_dict.pkl", "wb")
pickle.dump(main_op_link_dict, filehandler)
filehandler.close()