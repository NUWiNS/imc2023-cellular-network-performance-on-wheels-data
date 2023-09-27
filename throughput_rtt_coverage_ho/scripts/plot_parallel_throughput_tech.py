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
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

arfcn_freq_dict = {'177020' : 885.100, '2083329' : 28249.800, '2071667' : 27550.080, '648672' : 3730.080, '2078331' : 27949.920, '2073333' : 27650.040, '177000' : 885.000, '174800' : 874.000, '175000' : 875.000, '650004' : 3750.060, '2239999' : 37650.000, '125400' : 627.000, '125900' : 629.500, '126400' : 632.000, '126490' :632.450, '126510' : 632.550, '126530' : 632.650, '126900' : 634.500, '506280' : 2531.400, '508296' : 2541.480, '509202' : 2546.010, '514056' : 2570.280, '520020' : 2600.100, '525204' :2626.020, '526002' : 2630.010, '526404' : 2632.020, '527202' : 2636.010, '528000' : 2640.000, '528696' : 2643.480, '529998' : 2649.990, '530700' : 2653.500}

earfcn_freq_dict = {'1000' : 1970.00, '1025' :  1972.50, '1050' : 1975, '1075' : 1977.50, '1125' : 1982.50 , '2100' : 2125.00, '2450' : 874.0, '2460' : 875.0, '2559' : 884.90, '2560' : 885.00, '2561' : 885.10, '2600' : 889.00, '5230' : 751.00, '5780' : 739.00, '66486' : 2115.00, '66536' : 2120.00, '66561' : 2122.50, '66586' : 2125.00, '66611' : 2127.50, '66636' : 2130.0, '66686' : 2135.00, '66711' : 2137.50, '66761' : 2142.50, '66786' : 2145.00, '66811' : 2147.50, '66836' : 2150.00, '66911' : 2157.50, '66936' : 2160.00, '66986' : 2165.00, '67011' : 2167.50, '67086' : 2175.00, '750' : 1945.00, '775' : 1947.50, '825' : 1952.50, '925' : 1962.50, '950' : 1965.00, '975' : 1967.50, '800' : 1950, '1025' :  1972.50, '1075' : 1977.50, '1100' : 1980.00, '1125' : 1982.50, '1150' : 1985.00, '2175' : 2132.50, '41094' : 2640.40, '41490' : 2680.00, '5035' : 731.50, '5090' : 737.00, '5110' : 739.00, '5145' : 742.50, '5330' : 763.00, '625' : 1932.50, '650' : 1935.00, '66461' : 2112.50, '66486' : 2115.00, '66511' : 2117.50, '66611' : 2127.50, '66661' : 2132.50, '66686' : 2135.00, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66936' : 2160.00, '66985' : 2164.90, '66986' : 2165.00, '67086' : 2175.00, '675' : 1937.50, '700' : 1940.00, '800' : 1950.00, '850' : 1955.00, '875' : 1957.50, '900' : 1960.00, '925' : 1962.50, '950' : 1965, '9820' : 765.00, '1099' : 1979.90, '1100' : 1980.00, '1123' : 1982.30, '1125' : 1982.50, '1126' : 1982.60, '1148' : 1984.80, '1150' : 1985.00, '2000' : 2115.00, '2050' : 2120.00, '2125' : 2127.50, '2175' : 2132.50, '2200' : 2135.00, '2225' : 2137.50, '2300' : 2145.00, '2325' : 2147.50, '2460': 875.0,  '39750' : 2506.00, '39907' : 2521.70, '39948' : 2525.80, '40072' : 2538.20, '40384' : 2569.40, '40770' : 2608.00, '40810' : 2612.00, '41176' : 2648.60, '41238' : 2654.80, '41490' : 2680.00, '5035' : 731.50, '5090' : 737, '5095' : 737.50, '5110' : 739.00, '5330' : 763.00, '5780' : 739, '5815': 742.5, '66486': 2115.00, '66487' : 2115.10, '66536' : 2120.00, '66561' : 2122.5, '66586' : 2125, '66661' : 2132.50, '66686' : 2135, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66811': 2147.5, '66836': 2150, '66886': 2150, '66911': 2150, '66961': 2150, '66986' : 2165.00, '67011': 2167.5, '675' : 1937.50, '676': 1937.6, '677': 1937.7, '68611': 619.5, '68636': 622, '68661': 624.5, '68686': 627, '68786': 637, '68836': 637, '68861': 637, '68886': 637, '68911': 649.5, '700' : 1940.00, '725': 1942.5, '750': 1942.5, '775': 1942.5, '801': 1950.1, '8115': 1937.5, '825': 1952.5, '8264': 1952.4, '8290': 1952.4, '8315': 1952.4, '8465': 1972.5, '850' : 1955.00, '851': 1955.1, '852': 1955.1, '8539': 1979.9, '8562': 1982.2, '8640': 1982.2, '8665': 1992.5, '875' : 1957.50, '876': 1957.6, '8763': 866.3, '877': 1957.7, '8950': 885, '901': 1960.1, '925' : 1962.50, '41305' : 2661.50, '66761' : 2142.50, '132122' : 1747.5}



def get_technology_df(tput_df, lte_only=False):
    modified_tech = None
    if lte_only == False and (len(list(tput_df["5G KPI PCell RF Frequency [MHz]"].dropna())) > 0 or len(list(tput_df["5G KPI PCell RF Serving PCI"].dropna()))) > 0:
        # it is a 5G run 
        # get type of 5G 
        # max(set(freq_list), key=freq_list.count)
        freq_list = list(tput_df["5G KPI PCell RF Frequency [MHz]"].dropna())
        ffreq = float(max(set(freq_list), key=freq_list.count))
        # tput_tech_dict = {"LTE" : [], "LTE-A" : [], "low" : [], "high" : [], "high" : [], "high" : []}
        if int(ffreq) < 1000:
            modified_tech = "low"
        elif int(ffreq) > 1000 and int(ffreq) < 7000:
            modified_tech = "high"
        elif int(ffreq) > 7000 and int(ffreq) < 35000:
            modified_tech = "high"
        elif int(ffreq) > 35000:
            modified_tech = "high"
    else:
        try:
            earfcn_list = list(tput_df["LTE KPI PCell Serving EARFCN(DL)"].dropna())
        except:
            earfcn_list = list(tput_df["LTE KPI PCell Serving EARFCN(DL)"].dropna())
        if len(earfcn_list) == 0:
            pass
        else:
            lfreq = str(int(max(set(earfcn_list), key=earfcn_list.count)))
            if lfreq not in earfcn_freq_dict.keys():
                print("EARFCN not present in dict. Need to add." + str(lfreq))
                sys.exit(1)
            else:
                lfreq = earfcn_freq_dict[lfreq]
            if int(lfreq) < 1000:
                modified_tech = "low"
            elif int(lfreq) > 1000:
                modified_tech = "low"
    if modified_tech == None:
        print()
    return modified_tech

base = r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\tput\driving"
plot_path = r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots"
lte_only = False
dl = 1
if dl:         
    original_val_len = {"verizon" : [], "tmobile" : [], "atnt" : []}
    op_time_stamp = {"verizon" : [], "tmobile" : [], "atnt" : []}
    op_tput = {"verizon" : [], "tmobile" : [], "atnt" : []}
    color_dict = {"Verizon" : "red", "T-Mobile" : "magenta", "AT&T" : "blue"}
    vz_df = pd.DataFrame()
    csv_directory_list = glob.glob(base + "\\" + 'verizon' + "\\" + 'dl' + "\\*.csv")
    for csv in csv_directory_list:
        df_short = pd.read_csv(csv)
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"].notna()]
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"] > 0.1]
        df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
        if len(df_short_ho) != 0:
            df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].str.contains("Handover Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Success")]
        
        df_merged = pd.concat([df_short_tput, df_short_ho])
        df_merged = df_merged.sort_values(by=["TIME_STAMP"])
        df_merged.reset_index(inplace=True)
        if len(df_merged) <= 1:
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

        mod_df_break_list = []
        for tput_df in break_list:
            tech = get_technology_df(tput_df, lte_only)
            tech_list = [tech] * len(tput_df)
            tput_df['modified_tech'] = tech_list
            mod_df_break_list.append(tput_df)
        if len(mod_df_break_list) == 0:
            continue
        vz_df = pd.concat([vz_df, pd.concat(mod_df_break_list)])

    vz_df = vz_df.sort_values(by=["TIME_STAMP"])
    vz_df = vz_df.rename(columns={"Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]": 'Verizon DL Throughput'})
    vz_df = vz_df.rename(columns={"modified_tech": 'Verizon modified_tech'})
    op_time_stamp["verizon"].extend(list(vz_df["TIME_STAMP"]))
    op_tput["verizon"].extend(list(vz_df['Verizon DL Throughput']))
    original_val_len["verizon"] = len(vz_df)


    tmobile_df = pd.DataFrame()
    csv_directory_list = glob.glob(base + "\\" + 'tmobile' + "\\" + 'dl' + "\\*.csv")
    for csv in csv_directory_list:
        df_short = pd.read_csv(csv)
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"].notna()]
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"] > 0.1]
        df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
        if len(df_short_ho) != 0:
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

        mod_df_break_list = []
        for tput_df in break_list:
            tech = get_technology_df(tput_df, lte_only)
            if tech == None:
                print()
            tech_list = [tech] * len(tput_df)
            tput_df['modified_tech'] = tech_list
            mod_df_break_list.append(tput_df)
        if len(mod_df_break_list) == 0:
            continue
        tmobile_df = pd.concat([tmobile_df, pd.concat(mod_df_break_list)])
    tmobile_df = tmobile_df.sort_values(by=["TIME_STAMP"])
    tmobile_df = tmobile_df.rename(columns={"Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]": 'T-Mobile DL Throughput'})
    tmobile_df = tmobile_df.rename(columns={"modified_tech": 'T-Mobile modified_tech'})
    op_time_stamp["tmobile"].extend(list(tmobile_df["TIME_STAMP"]))
    op_tput["tmobile"].extend(list(tmobile_df['T-Mobile DL Throughput']))
    original_val_len["tmobile"] = len(vz_df)


    atnt_df = pd.DataFrame()
    csv_directory_list = glob.glob(base + "\\" + 'atnt' + "\\" + 'dl' + "\\*.csv")
    for csv in csv_directory_list:
        df_short = pd.read_csv(csv)
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"].notna()]
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"] > 0.1]
        df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
        if len(df_short_ho) != 0:
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

        mod_df_break_list = []
        for tput_df in break_list:
            tech = get_technology_df(tput_df, lte_only)
            if tech == None:
                print()
            tech_list = [tech] * len(tput_df)
            tput_df['modified_tech'] = tech_list
            mod_df_break_list.append(tput_df)

        if len(mod_df_break_list) == 0:
            continue
        atnt_df = pd.concat([atnt_df, pd.concat(mod_df_break_list)])
    atnt_df = atnt_df.sort_values(by=["TIME_STAMP"])
    atnt_df = atnt_df.rename(columns={"Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]": 'AT&T DL Throughput'})
    atnt_df = atnt_df.rename(columns={"modified_tech": 'AT&T modified_tech'})
    op_time_stamp["atnt"].extend(list(atnt_df["TIME_STAMP"]))
    op_tput["atnt"].extend(list(atnt_df['AT&T DL Throughput']))

    fig, ax = plt.subplots(1, 3, figsize=(11, 4.5), sharey=True)
    count = 0
    linestyle_dict = {"high-high" : 'solid', "high-low" : 'dotted', "low-low" : 'dashed', "low-high" : "dashdot"}
    color_dict = {"high-high" : "green", "high-low" : "orange", "low-high" : "red", "low-low" : "darkred"}
    label_dict = {"high-high" : 'HT - HT', "high-low" : 'HT - LT', "low-low" : 'LT - LT', "low-high" : "LT - HT"}
    dl_diff_list = []
    for pair in [(vz_df, tmobile_df), (tmobile_df, atnt_df), (atnt_df, vz_df)]:
        print("***************************************")
        op1, op2 = pair
        df_merged = pd.merge_asof(op1, op2, on="TIME_STAMP", direction="nearest", tolerance=2)
        if count == 0:
            df_merged = df_merged[['Verizon DL Throughput', 'T-Mobile DL Throughput', 'Verizon modified_tech', 'T-Mobile modified_tech']].dropna()
            dl_diff_list.append(list(df_merged['Verizon DL Throughput'] - df_merged['T-Mobile DL Throughput']))
            grouped = df_merged.groupby(['Verizon modified_tech', 'T-Mobile modified_tech'])
            title = "Verizon - T-Mobile"
        elif count == 1:
            df_merged = df_merged[['T-Mobile DL Throughput', 'AT&T DL Throughput', 'T-Mobile modified_tech', 'AT&T modified_tech']].dropna()
            dl_diff_list.append(list(df_merged['T-Mobile DL Throughput'] - df_merged['AT&T DL Throughput']))
            grouped = df_merged.groupby(['T-Mobile modified_tech', 'AT&T modified_tech'])
            title = "T-Mobile - AT&T"
        else:
            df_merged = df_merged[['AT&T DL Throughput', 'Verizon DL Throughput', 'AT&T modified_tech', 'Verizon modified_tech']].dropna()
            dl_diff_list.append(list(df_merged['AT&T DL Throughput'] - df_merged['Verizon DL Throughput']))
            grouped = df_merged.groupby(['AT&T modified_tech', 'Verizon modified_tech'])
            title = "AT&T - Verizon"
        
        grouped_dataframes = [group for name, group in grouped]
        print("Comparison == " + title)
        for grouped_dataframe in grouped_dataframes:
            group_filtered_columns = [col for col in grouped_dataframe.columns if "modified_tech" in col]
            group_filtered_df = grouped_dataframe[group_filtered_columns]
            group_type = group_filtered_df.iloc[:, 0].iloc[0] + "-" + group_filtered_df.iloc[:, 1].iloc[0]
            filtered_columns = [col for col in grouped_dataframe.columns if "Throughput" in col]
            # Create a new DataFrame with the filtered columns
            filtered_df = grouped_dataframe[filtered_columns]
            diff_list = []
            for first_val, second_val in zip(list(filtered_df.iloc[:, 0]), list(filtered_df.iloc[:, 1])):
                diff_list.append(first_val - second_val)
            diff_list_sorted = np.sort(diff_list)
            if len(diff_list_sorted) > 20:
                ax[count].plot(diff_list_sorted, np.linspace(0, 1, diff_list_sorted.size), linewidth=4,  label=label_dict[group_type], color=color_dict[group_type])
                print(label_dict[group_type] + " == " + str(len(diff_list_sorted)))
        if count == 0:
            ax[count].set_ylabel("CDF", fontsize=25)
        if count == 2:
            ax[count].legend(loc='upper left', fontsize=14.5)


        fig.text(0.5, -0.04, 'Throughput Difference (Mbps)', ha='center', fontsize=25, fontweight='bold')
        ax[count].axvline(0, linewidth=2, linestyle='--', color="gray")
        ax[count].axvline(0, linewidth=2, linestyle='--', color="gray")
        ax[count].axhline(0.5, linewidth=2, linestyle='--', color="gray")
        ax[count].axhline(0.5, linewidth=2, linestyle='--', color="gray")
        ax[count].set_ylim(ymin=0, ymax= 1)
        ax[count].set_xlim(-200, 200)
        ax[count].set_title(title, fontweight='bold', fontsize=20)
        count+=1
    plt.tick_params(axis='both', labelsize=15)
    plt.tight_layout()
    plt.savefig(plot_path + r"\\fig_6c.pdf")

ul = 1
if ul:         
    original_val_len = {"verizon" : [], "tmobile" : [], "atnt" : []}
    op_time_stamp = {"verizon" : [], "tmobile" : [], "atnt" : []}
    op_tput = {"verizon" : [], "tmobile" : [], "atnt" : []}
    color_dict = {"Verizon" : "red", "T-Mobile" : "magenta", "AT&T" : "blue"}
    vz_df = pd.DataFrame()
    csv_directory_list = glob.glob(base + "\\" + 'verizon' + "\\" + 'ul' + "\\*.csv")
    for csv in csv_directory_list:
        df_short = pd.read_csv(csv)
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].notna()]
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"] > 0.1]
        df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
        if len(df_short_ho) != 0:
            df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].str.contains("Handover Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Success")]
        
        df_merged = pd.concat([df_short_tput, df_short_ho])
        df_merged = df_merged.sort_values(by=["TIME_STAMP"])
        df_merged.reset_index(inplace=True)
        if len(df_merged) <= 1:
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

        mod_df_break_list = []
        for tput_df in break_list:
            tech_list = [get_technology_df(tput_df, lte_only)] * len(tput_df)
            tput_df['modified_tech'] = tech_list
            mod_df_break_list.append(tput_df)
        if len(mod_df_break_list) == 0:
            continue
        vz_df = pd.concat([vz_df, pd.concat(mod_df_break_list)])

    vz_df = vz_df.sort_values(by=["TIME_STAMP"])
    vz_df = vz_df.rename(columns={"Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]": 'Verizon UL Throughput'})
    vz_df = vz_df.rename(columns={"modified_tech": 'Verizon modified_tech'})
    op_time_stamp["verizon"].extend(list(vz_df["TIME_STAMP"]))
    op_tput["verizon"].extend(list(vz_df['Verizon UL Throughput']))
    original_val_len["verizon"] = len(vz_df)

    tmobile_df = pd.DataFrame()
    csv_directory_list = glob.glob(base + "\\" + 'tmobile' + "\\" + 'ul' + "\\*.csv")
    for csv in csv_directory_list:
        df_short = pd.read_csv(csv)
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].notna()]
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"] > 0.1]
        df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
        if len(df_short_ho) != 0:
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

        mod_df_break_list = []
        for tput_df in break_list:
            tech_list = [get_technology_df(tput_df, lte_only)] * len(tput_df)
            tput_df['modified_tech'] = tech_list
            mod_df_break_list.append(tput_df)
        if len(mod_df_break_list) == 0:
            continue
        tmobile_df = pd.concat([tmobile_df, pd.concat(mod_df_break_list)])
        
    tmobile_df = tmobile_df.sort_values(by=["TIME_STAMP"])
    tmobile_df = tmobile_df.rename(columns={"Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]": 'T-Mobile UL Throughput'})
    tmobile_df = tmobile_df.rename(columns={"modified_tech": 'T-Mobile modified_tech'})
    op_time_stamp["tmobile"].extend(list(tmobile_df["TIME_STAMP"]))
    op_tput["tmobile"].extend(list(tmobile_df['T-Mobile UL Throughput']))
    original_val_len["tmobile"] = len(vz_df)

    atnt_df = pd.DataFrame()
    csv_directory_list = glob.glob(base + "\\" + 'atnt' + "\\" + 'ul' + "\\*.csv")
    for csv in csv_directory_list:
        df_short = pd.read_csv(csv)
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].notna()]
        df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"] > 0.1]
        df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
        if len(df_short_ho) != 0:
            df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].str.contains("Handover Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Success") | df_short['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Success")]
        
        df_merged = pd.concat([df_short_tput, df_short_ho])
        df_merged = df_merged.sort_values(by=["TIME_STAMP"])
        df_merged.reset_index(inplace=True)

        if len(df_merged) <= 1:
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
            # if df_merged[start_index_count:end_index_count+1] != break_list[-1]:
            break_list.append(df_merged[start_index_count:end_index_count+1])

        mod_df_break_list = []
        for tput_df in break_list:
            tech_list = [get_technology_df(tput_df, lte_only)] * len(tput_df)
            tput_df['modified_tech'] = tech_list
            mod_df_break_list.append(tput_df)
        if len(mod_df_break_list) == 0:
            continue


        atnt_df = pd.concat([atnt_df, pd.concat(mod_df_break_list)])
    atnt_df = atnt_df.sort_values(by=["TIME_STAMP"])
    atnt_df = atnt_df.rename(columns={"Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]": 'AT&T UL Throughput'})
    atnt_df = atnt_df.rename(columns={"modified_tech": 'AT&T modified_tech'})
    op_time_stamp["atnt"].extend(list(atnt_df["TIME_STAMP"]))
    op_tput["atnt"].extend(list(atnt_df['AT&T UL Throughput']))

    fig, ax = plt.subplots(1, 3, figsize=(11, 4.5), sharey=True)
    count = 0
    linestyle_dict = {"high-high" : 'solid', "high-low" : 'dotted', "low-low" : 'dashed', "low-high" : "dashdot"}
    color_dict = {"high-high" : "green", "high-low" : "orange", "low-high" : "red", "low-low" : "darkred"}
    label_dict = {"high-high" : 'HT - HT', "high-low" : 'HT - LT', "low-low" : 'LT - LT', "low-high" : "LT - HT"}
    ul_diff_list = []
    ul_sum_list = []
    ul_max_list = []
    for pair in [(vz_df, tmobile_df), (tmobile_df, atnt_df), (atnt_df, vz_df)]:
        print("***************************************")
        op1, op2 = pair
        df_merged = pd.merge_asof(op1, op2, on="TIME_STAMP", direction="nearest", tolerance=2)

        if count == 0:
            df_merged = df_merged[['Verizon UL Throughput', 'T-Mobile UL Throughput', 'Verizon modified_tech', 'T-Mobile modified_tech']].dropna()
            ul_diff_list.append(list(df_merged['Verizon UL Throughput'] - df_merged['T-Mobile UL Throughput']))
            grouped = df_merged.groupby(['Verizon modified_tech', 'T-Mobile modified_tech'])
            title = "Verizon - T-Mobile"
        elif count == 1:
            df_merged = df_merged[['T-Mobile UL Throughput', 'AT&T UL Throughput', 'T-Mobile modified_tech', 'AT&T modified_tech']].dropna()
            ul_diff_list.append(list(df_merged['T-Mobile UL Throughput'] - df_merged['AT&T UL Throughput']))
            grouped = df_merged.groupby(['T-Mobile modified_tech', 'AT&T modified_tech'])
            title = "T-Mobile - AT&T"
        else:
            df_merged = df_merged[['AT&T UL Throughput', 'Verizon UL Throughput', 'AT&T modified_tech', 'Verizon modified_tech']].dropna()
            ul_diff_list.append(list(df_merged['AT&T UL Throughput'] - df_merged['Verizon UL Throughput']))
            grouped = df_merged.groupby(['AT&T modified_tech', 'Verizon modified_tech'])
            title = "AT&T - Verizon"

        grouped_dataframes = [group for name, group in grouped]
        print("Comparison == " + title)
        group_count = 0
        for grouped_dataframe in grouped_dataframes:
            group_filtered_columns = [col for col in grouped_dataframe.columns if "modified_tech" in col]
            group_filtered_df = grouped_dataframe[group_filtered_columns]
            group_type = group_filtered_df.iloc[:, 0].iloc[0] + "-" + group_filtered_df.iloc[:, 1].iloc[0]
            filtered_columns = [col for col in grouped_dataframe.columns if "Throughput" in col]
            # Create a new DataFrame with the filtered columns
            filtered_df = grouped_dataframe[filtered_columns]
            diff_list = []
            for first_val, second_val in zip(list(filtered_df.iloc[:, 0]), list(filtered_df.iloc[:, 1])):
                diff_list.append(first_val - second_val)
            diff_list_sorted = np.sort(diff_list)
            if len(diff_list_sorted) > 20:
                ax[count].plot(diff_list_sorted, np.linspace(0, 1, diff_list_sorted.size), linewidth=4,  label=label_dict[group_type], color=color_dict[group_type])
                print(label_dict[group_type] + " == " + str(len(diff_list_sorted)))
            group_count+=1
        if count == 0:
            ax[count].set_ylabel("CDF", fontsize=25)
        if count == 0:
            ax[count].legend(loc='lower right', fontsize=14.5)


        fig.text(0.5, -0.04, 'Throughput Difference (Mbps)', ha='center', fontsize=25, fontweight='bold')
        ax[count].axvline(0, linewidth=2, linestyle='--', color="gray")
        ax[count].axvline(0, linewidth=2, linestyle='--', color="gray")
        ax[count].axhline(0.5, linewidth=2, linestyle='--', color="gray")
        ax[count].axhline(0.5, linewidth=2, linestyle='--', color="gray")
        ax[count].set_ylim(ymin=0, ymax= 1)
        ax[count].set_xlim(-50, 50)
        ax[count].set_title(title, fontweight='bold', fontsize=20)
        count+=1
    plt.tick_params(axis='both', labelsize=15)
    plt.tight_layout()
    plt.savefig(plot_path + r"\\fig_6d.pdf")

# combined cdf
fig, ax = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
count = 0
new_color_dict = {0 : 'red', 1 : 'magenta', 2 : 'blue'}
label_dict = {0 : "(Verizon - T-Mobile)", 1 : "(T-Mobile - AT&T)", 2 : "(AT&T - Verizon)"}
while count < 3:
    ax[0].plot(np.sort(dl_diff_list[count]), np.linspace(0, 1, len(np.sort(dl_diff_list[count]))), linewidth=4, label=label_dict[count], color=new_color_dict[count])
    count+=1
while count < 6:
    ax[1].plot(np.sort(ul_diff_list[count%3]), np.linspace(0, 1, len(np.sort(ul_diff_list[count%3]))), linewidth=4, label=label_dict[count%3], color=new_color_dict[count%3])
    count+=1
ax[0].set_ylabel("CDF")
ax[0].set_xlabel("Downlink\nThroughput Difference (Mbps)", fontsize=18)
ax[1].set_xlabel("Uplink\nThroughput Difference (Mbps)", fontsize=18)
ax[1].legend(loc='best', fontsize=13)
ax[0].axvline(0, linewidth=2.5, linestyle='--', color="black")
ax[1].axvline(0, linewidth=2.5, linestyle='--', color="black")
ax[0].axhline(0.5, linewidth=2.5, linestyle='--', color="black")
ax[1].axhline(0.5, linewidth=2.5, linestyle='--', color="black")
ax[0].set_ylim(ymin=0)
ax[0].set_xlim(-200, 200)
ax[1].set_xlim(-50, 50)
ax[0].set_xticks([-200, -100, 0, 100, 200])
ax[1].set_ylim(ymin=0)
plt.tick_params(axis='both', labelsize=15)
plt.tight_layout()
plt.savefig(plot_path + r"\\fig_6a.pdf")
plt.close()



# pi chart 
dl_comparison_dict = {"Verizon - T-Mobile" : [192, 134, 513, 1012], "T-Mobile - AT&T" : [93, 619, 6, 592], "AT&T - Verizon" : [127, 46, 355, 2382]}
ul_comparison_dict = {"Verizon - T-Mobile" : [46, 43, 457, 1033], "T-Mobile - AT&T" : [78, 357, 3, 692], "AT&T - Verizon" : [9, 0, 269, 2405]}
labels = ["HT - HT", "HT - LT", "LT - HT", "LT - LT"]
colors = color_dict.values()
fig, ax = plt.subplots(2, 3, figsize=(8, 4.5))
count = 0
for key in dl_comparison_dict.keys():
    ax[0][count].pie(dl_comparison_dict[key], colors=colors)
    ax[0][count].set_title(key, fontsize=14, fontweight='bold')
    count+=1
ax[0][0].set_ylabel("DL", rotation=0)
count = 0
for key in ul_comparison_dict.keys():
    ax[1][count].pie(ul_comparison_dict[key], colors=colors)
    count+=1
ax[1][0].set_ylabel("UL", rotation=0)
plt.legend(labels=labels, bbox_to_anchor = (1.1, 1.1), loc='center right', ncols=4, fontsize=13)
plt.tight_layout()
plt.savefig(plot_path + r"\\fig_6b.pdf")
plt.close()