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


base = r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\ho\processed"
filehandler = open(base + "\\main_op_link_ho_per_mile_dict.pkl", "rb")
main_op_link_ho_per_mile_dict = pickle.load(filehandler)
filehandler.close()
op_dict = {"verizon" : "Verizon", "tmobile" : "T-Mobile", "atnt" : "AT&T"}
color_dict = {"verizon" : "red", "tmobile" : "magenta", "atnt" : "blue"}
fig, ax = plt.subplots(1, 2, figsize=(4, 3), sharey=True, sharex=True)
i = 0
dl_values = {"verizon" : [], "tmobile" : [], "atnt" : []}
ul_values = {"verizon" : [], "tmobile" : [], "atnt" : []}
for link in ["dl", "ul"]:
    for op in ["verizon", "tmobile", "atnt"]:
        lat_lon_list, ho_count_list, dist_list, ho_per_mile_list = main_op_link_ho_per_mile_dict[op][link]
        sorted_data = np.sort(ho_per_mile_list)
        ax[i].plot(sorted_data, np.linspace(0, 1, sorted_data.size), label=op_dict[op], color=color_dict[op])
    i+=1
ax[0].set_ylabel("CDF", fontsize=20)
fig.text(0.55,0, "HO(s) per mile", ha="center", va="center", fontsize=19)
ax[0].set_title("DL", fontsize=17, fontweight="bold")
ax[1].set_title("UL", fontsize=17, fontweight="bold")
ax[0].set_ylim(0, 1)
ax[0].set_xlim(xmin=0, xmax=20)
ax[1].set_xlim(xmin=0, xmax=20)
ax[1].legend(loc="lower right", fontsize=9)
ax[0].tick_params(axis='both', which='major', labelsize=13)
ax[0].tick_params(axis='both', which='minor', labelsize=13)
ax[1].tick_params(axis='both', which='major', labelsize=13)
ax[1].tick_params(axis='both', which='minor', labelsize=13)
plt.tight_layout()
plt.savefig(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_11a.pdf")
plt.close()


base = r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\ho\processed"
filehandler = open(base + "\\main_op_link_ho_duration_dict.pkl", "rb")
main_op_link_ho_duration_dict = pickle.load(filehandler)
filehandler.close()
op_dict = {"verizon" : "Verizon", "tmobile" : "T-Mobile", "atnt" : "AT&T"}
color_dict = {"verizon" : "red", "tmobile" : "magenta", "atnt" : "blue"}
fig, ax = plt.subplots(1, 2, figsize=(4, 3), sharey=True, sharex=True)
i = 0
dl_values = {"verizon" : [], "tmobile" : [], "atnt" : []}
ul_values = {"verizon" : [], "tmobile" : [], "atnt" : []}
for link in ["dl", "ul"]:
    for op in ["verizon", "tmobile", "atnt"]:
        if 0:
        # if op == "atnt" and link == "ul":
            base = r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\xcal_names_folder_wise\csvs\combined\ho_duration_operator"
            filehandler = open(base + "\\" + op + "_" + link + ".pkl", "rb")
            ho_duration = pickle.load(filehandler)
            filehandler.close()
        else:
            ho_duration = main_op_link_ho_duration_dict[op][link]
        sorted_data = np.sort(ho_duration)
        ax[i].plot(sorted_data, np.linspace(0, 1, sorted_data.size), label=op_dict[op], color=color_dict[op])
    i+=1
ax[0].set_ylabel("CDF", fontsize=20)
fig.text(0.55,0, "HO Duration (s)", ha="center", va="center", fontsize=19)
ax[0].set_title("DL", fontsize=17, fontweight="bold")
ax[1].set_title("UL", fontsize=17, fontweight="bold")
ax[0].set_ylim(0, 1)
ax[0].set_xlim(xmin=0, xmax=0.2)
ax[1].set_xlim(xmin=0, xmax=0.2)
ax[0].set_xticks([0,0.1, 0.2])
ax[1].set_xticks([0,0.1, 0.2])
ax[0].tick_params(axis='both', which='major', labelsize=13)
ax[0].tick_params(axis='both', which='minor', labelsize=13)
ax[1].tick_params(axis='both', which='major', labelsize=13)
ax[1].tick_params(axis='both', which='minor', labelsize=13)
plt.tight_layout()
plt.savefig(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_11b.pdf")
plt.close()                     



op_list = ["verizon", "tmobile", "atnt"]
op_dict = {"verizon" : "Verizon", "tmobile" : "T-Mobile", "atnt" : "AT&T"}
link_list = ["dl", "ul"]
color_dict = {'4G->5G' : "red", '5G->4G' : "orange", '4G->4G' : "green", '5G->5G' : "royalblue"}
base = r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\ho\processed"
filehandler = open(base + "\\main_op_link_ho_tput_dict.pkl", "rb")
main_op_link_ho_tput_dict = pickle.load(filehandler)
filehandler.close()
for link in link_list:
    i = 0
    for op in op_list:
        pre_ho_dict, post_ho_dict, pre_post_diff_dict, all_ho_t_list = main_op_link_ho_tput_dict[op][link]
        t1_list = []
        t2_list = []
        t3_list = []
        t4_list = []
        t5_list = []
        diff_t3_avg_t2_t4 = []
        diff_avg_t4_5_t1_2 = []
        for each_segment in all_ho_t_list:
            t1, t2, t3, t4, t5 = each_segment
            t1_list.append(t1)
            t2_list.append(t2)
            t3_list.append(t3)
            t4_list.append(t4)
            t5_list.append(t5)
            diff_t3_avg_t2_t4.append(t3 - np.mean([t4, t2]))
            diff_avg_t4_5_t1_2.append(np.mean([t4, t5]) - np.mean([t1, t2]))
        pre_post_diff_dict["5G->5G"].extend(pre_post_diff_dict['5G->4G->5G'])
        del pre_post_diff_dict['5G->4G->5G']
        t2_sorted = np.sort(t2_list)
        t3_sorted = np.sort(t3_list)
        t4_sorted = np.sort(t4_list)
        diff_t3_avg_t2_t4_sorted = np.sort(diff_t3_avg_t2_t4)
        diff_avg_t4_5_t1_2_sorted = np.sort(diff_avg_t4_5_t1_2)
        fig, ax = plt.subplots(figsize=(5, 4), sharey=True)
        ax.plot(diff_t3_avg_t2_t4_sorted, np.linspace(0, 1, diff_t3_avg_t2_t4_sorted.size), color="red", linewidth=4)
        from statistics import quantiles
        ax.axvline(x=0, linewidth=1.5, linestyle='--', color="gray")
        ax.set_ylim(ymin=0, ymax=1)
        if op == "verizon":
            ax.set_ylabel("CDF", fontsize=20)
        if link == "ul":
            ax.set_xlabel("Throughput (Mbps)", fontsize=20)
            ax.set_xlim(-25, 25)
        else:
            ax.set_title("$(T_{3} - (T_{2} + T_{4})/2)$", fontsize=20, fontweight="bold")
            ax.set_xlim(-50, 50)
        plt.tight_layout()
        plt.savefig(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_13" + "\\" + op + "_" + link + "_diff_t3.pdf")
        plt.close()
        fig, ax = plt.subplots(figsize=(5, 4), sharey=True)
        for ho_type in pre_post_diff_dict.keys():
            sorted_data = np.sort(pre_post_diff_dict[ho_type])
            ax.plot(sorted_data, np.linspace(0, 1, sorted_data.size), label=ho_type, color=color_dict[ho_type], linewidth=4)
        ax.plot(diff_avg_t4_5_t1_2_sorted, np.linspace(0, 1, diff_avg_t4_5_t1_2_sorted.size), label="All HOs", color="black", linewidth=4)
        ax.axvline(x=0, linewidth=1.5, linestyle='--', color="gray")
        if link == "ul":
            ax.set_xlabel("Throughput (Mbps)", fontsize=22)
            ax.set_xlim(-25, 25)

        else:
            ax.set_title("$(((T_{4} + T_{5}) /2) - ((T_{1} + T_{2})/2))$", fontsize=20, fontweight="bold")
            ax.set_xlim(-100, 100)
            if op == "atnt":
                ax.legend(loc="best", fontsize=17)
        if op == "verizon":
            ax.set_ylabel("CDF", fontsize=20)
        ax.set_ylim(ymin=0, ymax=1)
        i+=1
        plt.tight_layout()
        plt.savefig(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_13" + "\\" + op + "_" + link + "_diff_tput.pdf")
        plt.close()
        print()