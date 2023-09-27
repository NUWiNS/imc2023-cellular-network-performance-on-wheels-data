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
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.patches as patches

def parse_ping(filename):
    fh = open(filename, "r")
    data = fh.readlines()
    fh.close()
    ping_list = []
    for d in data:
        if "46 bytes from" in d:
            d = d.strip()
            d = d.split()
            ms_idx = d.index("ms")
            ping_list.append(float(d[ms_idx - 1].split("=")[-1]))
    return ping_list[5:]

def parse_tput(filename):
    fh = open(filename, "r")
    data = fh.readlines()
    fh.close()
    tput_list = []
    if "nuttcp-t" in data[0]:
        run_type = "ul"
    elif "nuttcp-r" in data[0]:
        run_type = "dl"
    else:
        # try next line because timestamp may be there
        if "nuttcp-t" in data[1]:
            run_type = "ul"
        elif "nuttcp-r" in data[1]:
            run_type = "dl"
        else:
            run_type = None
    for d in data:
        if "sec" in d and "retrans" in d and "nuttcp" not in d:
            d = d.strip()
            d = d.split()
            equal_to_idx = d.index("=")
            tput_list.append(float(d[equal_to_idx + 1]))
    
    if run_type == None:
        print("weird! this should not happen!")
        sys.exit(1)
    if run_type not in filename:
        print("!")
    tput_list = np.array(tput_list[20:])
    arr_len = int((len(tput_list) // 10) * 10)
    tput_list = tput_list[:arr_len]
    tput_list = np.mean(tput_list.reshape(-1, 5), axis=1)
    return [tput_list, run_type]

def return_speed_latency(df):
    speed = list(df['Speed'])
    latency = list(df['RTT'])

    # Initialize lists for unique speeds and corresponding latencies
    unique_speeds = []
    speed_latencies = []

    # Create a dictionary to store latencies for each unique speed
    speed_latency_dict = {}

    # Iterate through the lists
    for i in range(len(speed)):
        current_speed = speed[i]
        current_latency = latency[i]

        # Check if the speed value is already in the unique_speeds list
        if current_speed not in unique_speeds:
            # If it's a new unique speed, add it to the list
            unique_speeds.append(current_speed)
            # Initialize the list of latencies for this speed
            speed_latency_dict[current_speed] = []

        # Add the latency value to the corresponding speed's list
        speed_latency_dict[current_speed].append(current_latency)

    # Convert the dictionary to a list of tuples
    for speed_value in unique_speeds:
        speed_latencies.append(tuple(speed_latency_dict[speed_value]))

    return [unique_speeds, speed_latencies]

def plot_static_cdf_3a(base, plot_path):

    operator_list = ["verizon", "tmobile", "atnt"]
    operator_dict = {"verizon" : "Verizon", "tmobile" : "T-Mobile", "atnt" : "AT&T"}
    color_dict = {"verizon" : "red", "tmobile" : "magenta", "atnt" : "blue"}
    city_list = ["chic", "clev", "de", "indy", "la", "lv", "omaha", "slc"]
    city_names_dict = {"la" : "LA", "lv" : "LV", "slc" : "SLC", "de" : "DE", "omaha" : "OM", "chic" : "CHIC", "indy" : "INDY", "clev" : "CLEV"}

    operator_main_dict = {}
    
    fig, ax = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    for op in operator_list:
        static_ping_list = []
        static_dl_list =   []
        static_ul_list =   []
        for city in city_list:
            if ("lv" in city):
                # in LV due to extreme heat we never got 5G, it was always switching to LTE
                continue

            out_files = glob.glob(base + "\\" + op + "\\" + "*%s*.out" %city)
            for out_file in out_files:
                if "ping" in out_file:
                    # ping parse
                    static_ping_list.extend(parse_ping(out_file))
                else:
                    # tput parse
                    tput, run_type = parse_tput(out_file)
                    if run_type == "ul":
                        static_ul_list.extend(tput)
                    elif run_type == "dl":
                        static_dl_list.extend(tput)
            
        sorted_ping_data = np.sort(static_ping_list)
        ping_linspace = np.linspace(0, 1, sorted_ping_data.size)
        sorted_dl_data = np.sort(static_dl_list)
        dl_linspace = np.linspace(0, 1, sorted_dl_data.size)
        sorted_ul_data = np.sort(static_ul_list)
        ul_linspace = np.linspace(0, 1, sorted_ul_data.size)
        # print("********************")
        # print("Op is " + op)
        # print("Min dl tput = " + str(np.quantile(sorted_dl_data, 0)))
        # print("Median dl tput = " + str(np.median(sorted_dl_data)))
        # print("75 percentile dl tput = " + str(np.quantile(sorted_dl_data, 0.75)))
        # print("Max dl tput = " + str(np.quantile(sorted_dl_data, 1)))
        # print("100 percentile dl tput = " + str(np.quantile(sorted_dl_data, 1)))
        # print("Min ul tput = " + str(np.quantile(sorted_ul_data, 0)))
        # print("Median ul tput = " + str(np.median(sorted_ul_data)))
        # print("75 percentile ul tput = " + str(np.quantile(sorted_ul_data, 0.75)))
        # print("Max ul tput = " + str(np.quantile(sorted_ul_data, 1)))
        # print("100 percentile ul tput = " + str(np.quantile(sorted_ul_data, 1)))
        # print("Min ping = " + str(np.quantile(sorted_ping_data, 0)))
        # print("Median ping tput = " + str(np.median(sorted_ping_data)))
        # print("75 percentile ping = " + str(np.quantile(sorted_ping_data, 0.75)))
        # print("Max ping = " + str(np.quantile(sorted_ping_data, 1)))
        # print("100 percentile ping = " + str(np.quantile(sorted_ping_data, 1)))
        ax[0].plot(sorted_dl_data, dl_linspace, label=operator_dict[op], color=color_dict[op], linewidth=4)
        ax[0].set_xlabel("DL Throughput (Mbps)", fontsize=25)
        ax[1].plot(sorted_ul_data, ul_linspace, label=operator_dict[op], color=color_dict[op], linewidth=4)
        ax[1].set_xlabel("UL Throughput (Mbps)", fontsize=25)
        ax[2].plot(sorted_ping_data, ping_linspace, label=operator_dict[op], color=color_dict[op] , linewidth=4)
        ax[2].set_xlabel("RTT (ms)", fontsize=25)
    ax[0].set_ylabel("CDF", fontsize=25)
    ax[0].set_ylim(ymin=0)
    ax[0].set_xlim(xmin=0)
    ax[1].set_xlim(xmin=0)
    ax[2].set_xlim(xmin=0)
    ax[0].legend(loc="best", fontsize=18)
    ax[0].tick_params(axis='both', labelsize=15)
    ax[1].tick_params(axis='both', labelsize=15)
    ax[2].tick_params(axis='both', labelsize=15)
    plt.tight_layout()
    plt.savefig(plot_path + r"\fig_3a.pdf")
    plt.close()

def plot_driving_cdf_3b(main_op_link_tput_dict, main_rtt_tech_dict, plot_path):
    op_list =  ["verizon", "tmobile", "atnt"]
    color_dict = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
    fig, ax = plt.subplots(3, 3, figsize=(27, 14))
    i = 0
    xput_data = {"verizon" : {"dl" : [], "ul" : [], "ping" : []}, "tmobile" : {"dl" : [], "ul" : [], "ping" : []} , "atnt" : {"dl" : [], "ul" : [], "ping" : []}}
    for op in ["verizon", "tmobile", "atnt"]:
        j = 0
        for link in ["dl", "ul", "ping"]:
            if link == "ping":
                tput_tech_dict = main_rtt_tech_dict[2][op]
            else:
                tput_speed_tech_dict = main_op_link_tput_dict[op][link][0]
                tput_tech_dict = {}
                for tech in tput_speed_tech_dict.keys():
                    tmp = []
                    speed_dict = tput_speed_tech_dict[tech]
                    for speed, lst in zip(speed_dict.keys(), speed_dict.values()):
                        tmp.extend(lst)
                    tput_tech_dict[tech] = tmp
               
            for key in tput_tech_dict.keys():
                # if "39" in key and op == "verizon" and link == "ping":
                #     tput_tech_dict[key] = []
                sorted_data = np.sort(tput_tech_dict[key])
                xput_data[op][link].extend(sorted_data)

    op_dict = {"verizon" : "Verizon", "tmobile" : "T-Mobile", "atnt" : "AT&T"}
    color_dict = {"verizon" : "red", "tmobile" : "magenta", "atnt" : "blue"}
    fig, ax = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    axins_dl = inset_axes(ax[0], width='40%', height='75%', loc='center right')
    axins_ul = inset_axes(ax[1], width='40%', height='75%', loc='center right')
    axins_dl.set_xlim(0, 220)
    axins_dl.set_ylim(0, 1)
    axins_ul.set_xlim(0, 50)
    axins_ul.set_ylim(0, 1)
    for op in op_list:
        print("********************************")
        print("OP is " + op)
        i = 0
        for link in ["dl", "ul", "ping"]:
            sorted_data = np.sort(xput_data[op][link])
            lt_5 = sum(i < 5 for i in sorted_data)
            ax[i].plot(sorted_data, np.linspace(0, 1, sorted_data.size), color = color_dict[op], label=op_dict[op], linewidth=4)
            if link == "dl":
                axins_dl.plot(sorted_data, np.linspace(0, 1, sorted_data.size), color = color_dict[op], label=op_dict[op], linewidth=4)
            elif link == "ul":
                axins_ul.plot(sorted_data, np.linspace(0, 1, sorted_data.size), color = color_dict[op], label=op_dict[op], linewidth=4)
            i+=1

    rect_dl = patches.Rectangle((0, 0), 220, 1, linewidth=1, edgecolor='black', facecolor='none')
    rect_ul = patches.Rectangle((0, 0), 50, 1, linewidth=1, edgecolor='black', facecolor='none')
    ax[0].add_patch(rect_dl)
    ax[1].add_patch(rect_ul)
    ax[0].indicate_inset_zoom(axins_dl, edgecolor="black")
    ax[1].indicate_inset_zoom(axins_ul, edgecolor="black")
    ax[0].set_ylabel("CDF", fontsize=25)
    ax[0].set_ylim(ymin=0)
    ax[0].set_xlim(0, 3500)
    ax[0].set_xticks([0, 1000, 2000, 3000])
    ax[1].set_xlim(0, 350)
    ax[1].set_xticks([0, 100, 200, 300])
    ax[2].set_xlim(0, 165)
    ax[0].set_xlabel("DL Throughput (Mbps)", fontsize=25)
    ax[1].set_xlabel("UL Throughput (Mbps)", fontsize=25)
    ax[2].set_xlabel("RTT (ms)", fontsize=25)
    ax[0].tick_params(axis='both', labelsize=15)
    ax[1].tick_params(axis='both', labelsize=15)
    ax[2].tick_params(axis='both', labelsize=15)

    plt.tight_layout()
    plt.savefig(plot_path + r"\fig_3b.pdf")
    plt.close()

def plot_fig_4(main_op_link_tput_dict, main_op_link_rtt_dict, plot_path):
    op_dict = {"verizon" : "Verizon", "tmobile" : "T-Mobile", "atnt" : "AT&T"}
    color_dict = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
    op_list =  ["verizon", "tmobile", "atnt"]
    label_dict = {'LTE' : 'LTE', 'LTE-A' : 'LTE-A', '5G-low' : '5G-low', '5G-sub6' : '5G-mid', '5G-mmWave 28 GHz' : '5G-mmWave (28 GHz)', '5G-mmWave 39 GHz' : '5G-mmWave (39 GHz)'}
    fig, ax = plt.subplots(3, 3, figsize=(21, 11))
    i = 0
    xput_data = {"verizon" : {"dl" : [], "ul" : [], "ping" : []}, "tmobile" : {"dl" : [], "ul" : [], "ping" : []} , "atnt" : {"dl" : [], "ul" : [], "ping" : []}}
    for op in ["verizon", "tmobile", "atnt"]:
        j = 0
        for link in ["dl", "ul", "ping"]:
            if op == "verizon":
                if link == "ping":
                    main_op_dict, main_rtt_5g_dict, main_rtt_tech_dict, main_edge_tech_dict, op_speed_dict, op_rtt_dict, op_tech_dict  = main_op_link_rtt_dict            
                    rtt_tech_dict = main_rtt_tech_dict[op]
                    edge_tech_dict = main_edge_tech_dict[op]
                    for tech in rtt_tech_dict.keys():
                        if "39" in tech:
                            rtt_tech_dict[tech] = []
                            edge_tech_dict[tech] = []
                        wl_list = []
                        cloud_list = []
                        rtt_list = rtt_tech_dict[tech]
                        edge_list = edge_tech_dict[tech]
                        for edge, rtt in zip(edge_list, rtt_list):
                            if edge == 1:
                                wl_list.append(rtt)
                            else:
                                cloud_list.append(rtt)
                        sorted_wl_data = np.sort(wl_list)
                        sorted_cloud_data = np.sort(cloud_list)
                        if "39" in tech:
                            ax[j][i].plot(sorted_wl_data, np.linspace(0, 1, sorted_wl_data.size), color=color_dict[tech], linestyle="--", linewidth=4)
                        else:
                            if "mmWave" in tech:
                                ax[j][i].plot(sorted_wl_data, np.linspace(0, 1, sorted_wl_data.size), color=color_dict[tech], linestyle="--", label="5G-mmWave\n (28 GHz) (Edge)", linewidth=4)
                            else:
                                ax[j][i].plot(sorted_wl_data, np.linspace(0, 1, sorted_wl_data.size), color=color_dict[tech], linestyle="--", label=label_dict[tech] + " (Edge)", linewidth=4)
                        if '28' not in tech:
                            ax[j][i].plot(sorted_cloud_data, np.linspace(0, 1, sorted_cloud_data.size), color=color_dict[tech], linestyle="-", linewidth=4)
                        ax[j][i].legend(loc="lower right", fontsize=14)
                else:
                    tput_speed_tech_dict = main_op_link_tput_dict[op][link][0]
                    wl_speed_dict =  main_op_link_tput_dict[op][link][9]
                    for tech in tput_speed_tech_dict.keys():
                        wl_list = []
                        cloud_list = []
                        for speed in tput_speed_tech_dict[tech].keys():
                            temp_tput_list = tput_speed_tech_dict[tech][speed]
                            temp_wl_list = wl_speed_dict[tech][speed]
                            for wl, tput in zip(temp_wl_list, temp_tput_list):
                                if wl == 1:
                                    wl_list.append(tput)
                                else:
                                    cloud_list.append(tput)
                        sorted_wl_data = np.sort(wl_list)
                        sorted_cloud_data = np.sort(cloud_list)
                        if "mmWave" in tech:
                            ax[j][i].plot(sorted_wl_data, np.linspace(0, 1, sorted_wl_data.size), color=color_dict[tech], linestyle="--", label=label_dict[tech] + "\n(Edge)", linewidth=4)
                        else:
                            ax[j][i].plot(sorted_wl_data, np.linspace(0, 1, sorted_wl_data.size), color=color_dict[tech], linestyle="--", label=label_dict[tech] + " (Edge)", linewidth=4)

                        ax[j][i].plot(sorted_cloud_data, np.linspace(0, 1, sorted_cloud_data.size), color=color_dict[tech], linestyle="-", linewidth=4)
                filehandler.close()
              
            else:
                if link == "ping":
                    tput_tech_dict = main_op_link_rtt_dict[2][op]
                else:
                    tput_speed_tech_dict = main_op_link_tput_dict[op][link][0]
                    tput_tech_dict = {}
                    for tech in tput_speed_tech_dict.keys():
                        tmp = []
                        speed_dict = tput_speed_tech_dict[tech]
                        for speed, lst in zip(speed_dict.keys(), speed_dict.values()):
                            tmp.extend(lst)
                        tput_tech_dict[tech] = tmp

                for key in tput_tech_dict.keys():
                    if "39" in key and op == "verizon" and link == "ping":
                        tput_tech_dict[key] = []
                    
                    sorted_data = np.sort(tput_tech_dict[key])
                    xput_data[op][link].extend(sorted_data)
                    ax[j][i].plot(sorted_data, np.linspace(0, 1, sorted_data.size), color=color_dict[key], label=label_dict[key], linewidth=4)
            
            if i == 0:
                ax[j][i].set_ylabel("CDF", fontsize=22.5)
            if j == 2:
                ax[j][i].set_xlabel("RTT (ms)", fontsize=22.5)
            else:
                ax[j][i].set_xlabel("Throughput (Mbps)", fontsize=22.5)
            if j == 1 and i == 2:
                ax[j][i].legend(loc="lower right", fontsize=14)
            ax[j][i].set_ylim(ymin=0)
            if j == 0:
                ax[j][i].set_xlim(xmin=0, xmax=1200)
            elif j == 1:
                ax[j][i].set_xlim(xmin=0, xmax=80)
            else:
                ax[j][i].set_xlim(xmin=0, xmax=170)
            if link == "ping":
                link_mod = "RTT"
            else:
                link_mod = link
            ax[j][i].set_title(op_dict[op] + ": " + link_mod.upper(), fontsize=22, fontweight="bold")
            j+=1
        i+=1
    plt.tight_layout()
    plt.tick_params(axis='both', labelsize=15)
    plt.savefig(plot_path + r"\fig_4.pdf")
    plt.close()

def plot_fig_5(main_op_link_tput_dict, plot_path):
    op_dict = {"verizon" : "Verizon", "tmobile" : "T-Mobile", "atnt" : "AT&T"}
    tech_dict = {"verizon" : [], "tmobile" : [], "atnt" : []}
    color_dict = {'America/Los_Angeles' : "black", 'America/Denver' : "red", 'America/Chicago' : "green", 'America/New_York' : "orange" }
    labels_dict = {'America/Los_Angeles' : "Pacific Time", 'America/Denver' : "Mountain Time", 'America/Chicago' : "Central Time", 'America/New_York' : "Eastern Time" }
    fig, ax = plt.subplots(2, 3, figsize=(15, 10))
    i = 0
    for op in ["verizon", "tmobile", "atnt"]:
        j = 0
        for link in ["dl", "ul"]:
            tput_tz_tech_dict = main_op_link_tput_dict[op][link][4]
            for key in tput_tz_tech_dict.keys():
                if key == None:
                    continue
                sorted_data = np.sort(tput_tz_tech_dict[key])

                ax[j][i].plot(sorted_data, np.linspace(0, 1, sorted_data.size), color=color_dict[key], label=labels_dict[key], linewidth=4)
            
            if j == 1:
                ax[j][i].set_xlabel("Throughput (Mbps)", fontsize=25)
            if i == 0:
                ax[j][i].set_ylabel("CDF", fontsize=25)
            if j == 1 and i == 2:
                ax[j][i].legend(loc="lower right", fontsize=17)
            ax[j][i].set_ylim(ymin=0)
            if j == 0:
                ax[j][i].set_xlim(xmin=0, xmax=1000)
            elif j == 1:
                ax[j][i].set_xlim(xmin=0, xmax=80)
            else:
                ax[j][i].set_xlim(xmin=0, xmax=150)
            ax[j][i].set_title(op_dict[op] + ": " + link.upper(), fontsize=25, fontweight="bold")
            j+=1
        i+=1
    plt.tick_params(axis='both', labelsize=15)
    plt.tight_layout()
    plt.savefig(plot_path + r"\fig_5.pdf")
    plt.close()

def plot_fig_7(main_op_link_tput_dict, plot_path):
    label_dict = {'LTE' : 'LTE', 'LTE-A' : 'LTE-A', '5G-low' : '5G-low', '5G-sub6' : '5G-mid', '5G-mmWave 28 GHz' : '5G-mmWave (28 GHz)', '5G-mmWave 39 GHz' : '5G-mmWave (39 GHz)'}
    color_dict = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
    for op in ["verizon", "tmobile", "atnt"]:
        # print("****************************************************")
        # print("Operator is == " + op)
        for link in ["dl", "ul"]:
            # print("Link is == " + link)
            # print("****************************************************")
            tput_speed_tech_dict = main_op_link_tput_dict[op][link][0]
            if 1:
                fig, ax = plt.subplots(figsize=(20, 5))
                for tech_key in tput_speed_tech_dict.keys():
                    if len(tput_speed_tech_dict[tech_key]) == 0:
                        ax.scatter([], [], color=color_dict[tech_key], marker=".", label=label_dict[tech_key])
                        continue
                    sorted_speed_tput_dict = tput_speed_tech_dict[tech_key]
                    #plot speed vs throughput
                    x_val = []
                    y_val = []
                    for key in sorted_speed_tput_dict.keys():
                        sorted_speed_tput_dict[key] = [x for x in sorted_speed_tput_dict[key] if not pd.isnull(x)]
                        x_val.append(key)
                        y_val.append(tuple(sorted_speed_tput_dict[key]))

                    x_val, y_val = zip(*sorted(zip(x_val, y_val)))
                    #plot the scatter plot now
                    # x axis = speed
                    # y axis = throughput mbps
                    count = 0
                    for xe, ye in zip(x_val, y_val):
                        if count == 0:
                            ax.scatter([xe] * len(ye), ye, color= color_dict[tech_key], marker=".", label=label_dict[tech_key])
                        else:
                            ax.scatter([xe] * len(ye), ye, color= color_dict[tech_key], marker=".")
                        count+=1
                if link == "dl":
                    ax.set_ylabel("Throughput\n(Mbps)", fontsize=30)
                if link == "ul" and op == "atnt":
                    ax.legend(loc="upper center", fontsize=20, markerscale=2)
                if op == "atnt":
                    ax.set_xlabel("Speed (miles/hr)", fontsize=30)
                ax.set_xlim(xmin=0, xmax=95)
                # We change the fontsize of minor ticks label 
                ax.tick_params(axis='both', which='major', labelsize=16)
                ax.tick_params(axis='both', which='minor', labelsize=16)
                ax.axvline(20, linewidth=2.5, linestyle='--', color="black")
                ax.axvline(60, linewidth=2.5, linestyle='--', color="black")
                if link == "dl":
                    ax.set_ylim(0, 1000)
                else:
                    ax.set_ylim(0, 140)
                plt.tight_layout()
                plt.savefig(plot_path + r"\fig_7\\" + op + "_" + link + "_speed_tput_tech_scatter.pdf")
                plt.close()

def plot_fig_8(main_op_link_rtt_dict, plot_path):
    label_dict = {'LTE' : 'LTE', 'LTE-A' : 'LTE-A', '5G-low' : '5G-low', '5G-sub6' : '5G-mid', '5G-mmWave 28 GHz' : '5G-mmWave (28 GHz)', '5G-mmWave 39 GHz' : '5G-mmWave (39 GHz)'}
    color_dict = {"LTE" : "#08710C", "LTE-A" : "#70CA32", "5G-low" : "#F3FF33", "5G-sub6" : "#FFB233", "5G-mmWave 28 GHz" : "#FF4629", "5G-mmWave 39 GHz" : "#CB0404" }
    op_dict = {"verizon" : "Verizon", "tmobile" : "T-Mobile", "atnt" : "AT&T"}

    fig, ax = plt.subplots(1, 3, figsize=(40, 6), sharey=True)
    count = 0
    for op in ["verizon", "tmobile", "atnt"]:
        op_speed_dict = main_op_link_rtt_dict[-3][op]
        op_rtt_dict = main_op_link_rtt_dict[-2][op]
        op_tech_dict = main_op_link_rtt_dict[-1][op]
        list_of_lists = [op_speed_dict, op_rtt_dict, op_tech_dict]
        transposed_data = list(map(list, zip(*list_of_lists)))
        df = pd.DataFrame(transposed_data, columns=['Speed', 'RTT', 'Tech'])
        df_grouped = df.groupby(['Tech'])
        grouped_dataframes = [group for name, group in df_grouped]
        # group in order
        temp_grouped_dataframes = []
        for tech_order in label_dict.keys():
            for df_temp in grouped_dataframes:
                if df_temp["Tech"].iloc[0] == tech_order:
                    temp_grouped_dataframes.append(df_temp)
                    break
        grouped_dataframes = temp_grouped_dataframes.copy()
        for grouped_dataframe in grouped_dataframes:
            tech_key = grouped_dataframe['Tech'].iloc[0]
            if "mmWave" in tech_key and "39" in tech_key and op == "verizon":
                continue
            unique_speeds, speed_latencies = return_speed_latency(grouped_dataframe)
            x_val, y_val = zip(*sorted(zip(unique_speeds, speed_latencies)))
            for xe, ye in zip(x_val, y_val):
                ax[count].scatter([xe] * len(ye), ye, color= color_dict[tech_key], marker=".")
            if count == 0:
                ax[count].set_ylabel("RTT (ms)", fontsize=30)
            ax[count].set_xlabel("Speed (miles/hr)", fontsize=30)
            ax[count].set_xlim(xmin=0, xmax=95)
            ax[count].axvline(20, linewidth=2.5, linestyle='--', color="black")
            ax[count].axvline(60, linewidth=2.5, linestyle='--', color="black")
            ax[count].set_ylim(0, 250)
        ax[count].set_title(op_dict[op], fontsize=30, fontweight="bold")
        count+=1
    plt.tight_layout()
    plt.savefig(plot_path + r"\fig_8.pdf")
    plt.close()

def plot_fig_10(main_op_link_tput_dict, main_op_link_rtt_dict, plot_path):
    op_dict = {"verizon" : "Verizon", "tmobile" : "T-Mobile", "atnt" : "AT&T"}
    color_dict = {"verizon" : "red", "tmobile" : "magenta", "atnt" : "blue"}
    
    for link in ["dl", "ul"]:
        fig, ax = plt.subplots(1, 3, figsize=(4.5, 3), sharex=True)
        i = 0
        for op in color_dict.keys():
            overall_mean_list = main_op_link_tput_dict[op][link][-3]
            overall_std_list = main_op_link_tput_dict[op][link][-2]
            overall_5g_high_percent = main_op_link_tput_dict[op][link][-1]

            if op == "tmobile" and link == "dl":
                overall_mean_list = overall_mean_list[:-1]
                overall_std_list = overall_std_list[:-1]
                overall_5g_high_percent = overall_5g_high_percent[:-1]
            ax[i].scatter(overall_5g_high_percent, overall_mean_list, color=color_dict[op], label=op_dict[op], marker='o', s=20)
            
            if link == "dl":
                ax[i].set_ylim(0, 1500)
                ax[i].set_yticks([0, 250, 500, 750, 1000, 1250, 1500])
                if i == 0:
                    ax[i].set_ylabel("DL Throughput (Mbps)", fontsize=16)
                else:
                    ax[i].set_yticks([])
                    ax[i].set_yticklabels([])
            else:
                ax[i].set_ylim(0, 80)
                if i == 0:
                    ax[i].set_ylabel("UL Throughput (Mbps)", fontsize=16)
                else:
                    ax[i].set_yticks([])
                    ax[i].set_yticklabels([])
            ax[i].set_xticks([0, 100])
            ax[i].set_xticklabels(["0", "1"])
            ax[i].set_title(op_dict[op], fontweight='bold', fontsize=12)
            i+=1
        
        fig.text(0.55, -0.02, "\n% 5G mmWave/midband", ha='center', fontsize=14)
        plt.tight_layout()
        plt.savefig(plot_path + r"\fig_10" + link + ".pdf")
        plt.close()

    ping_avg_data = main_op_link_rtt_dict[1]
    fig, ax = plt.subplots(1, 3, figsize=(4.5, 3), sharex=True)
    i = 0
    for op in ping_avg_data.keys():
        fiveg_percent = []
        mean_rtt = []
        for key in ping_avg_data[op].keys():
            for mean in ping_avg_data[op][key]:
                fiveg_percent.append(key)
                mean_rtt.append(mean)

        ax[i].scatter(fiveg_percent, mean_rtt, color=color_dict[op], label=op_dict[op], marker='o', s=20)
        ax[i].set_xticks([0, 1])
        ax[i].set_xticklabels(["0", "1"])
        ax[i].set_ylim(0,500)
        if i == 0:
            ax[i].set_ylabel("RTT (ms)", fontsize=16)
        else:
            ax[i].set_yticks([])
            ax[i].set_yticklabels([])
        ax[i].set_title(op_dict[op], fontweight='bold', fontsize=12)
        i+=1
    fig.text(0.55, -0.02, "\n% 5G mmWave/midband", ha='center', fontsize=14)
    plt.tight_layout()
    plt.savefig(plot_path + r"\fig_10c.pdf")
    plt.close()

def plot_fig_9(main_op_link_tput_dict, main_op_link_rtt_dict, plot_path):
    fig, ax = plt.subplots(2, 3, figsize=(12, 7), sharey=True)
    op_dict = {"verizon" : "Verizon", "tmobile" : "T-Mobile", "atnt" : "AT&T"}
    color_dict = {"verizon" : "red", "tmobile" : "magenta", "atnt" : "blue"}
    i = 0
    for op in color_dict.keys():
        j = 0
        for link in ["dl", "ul"]:
            overall_mean_list = main_op_link_tput_dict[op][link][-3]
            overall_std_list = main_op_link_tput_dict[op][link][-2]
            if op == "tmobile" and link == "dl":
                overall_mean_list = overall_mean_list[:-1]
                overall_std_list = overall_std_list[:-1]
            percentage_std_list = [round(((std * 100)/mean), 2) for std, mean in zip(overall_std_list, overall_mean_list)]
            sorted_mean = np.sort(overall_mean_list)
            sorted_std = np.sort(percentage_std_list)
            ax[0][j].plot(sorted_mean, np.linspace(0, 1, sorted_mean.size), color=color_dict[op], label=op_dict[op], linewidth=4)
            ax[0][j].set_xlabel("Average (Mbps)", fontsize=22)
            ax[1][j].plot(sorted_std, np.linspace(0, 1, sorted_std.size), color=color_dict[op], label=op_dict[op], linewidth=4)
            ax[1][j].set_xlabel("Deviation (%)", fontsize=22)
            ax[0][j].set_title(link.upper() + " Throughput", fontweight="bold", fontsize=20)

            if j == 0:
                ax[0][j].set_xlim(0, 700)
                ax[1][j].set_xlim(0, 200)
            elif j == 1:
                ax[0][j].set_xlim(0, 80)
                ax[1][j].set_xlim(0, 200)
            j+=1

    main_rtt_dict = main_op_link_rtt_dict[0]
    for op in color_dict.keys():
        op_rtt = main_rtt_dict[op]
        sorted_mean = []
        sorted_std = []
        sorted_std_percent = []
        for each_run in op_rtt:
            sorted_mean.append(np.mean(each_run[2][5:]))
            sorted_std.append(np.std(each_run[2][5:]))
            sorted_std_percent.append(round((sorted_std[-1] * 100)/sorted_mean[-1],2))
        sorted_mean = np.sort(sorted_mean)
        if "tmobile" in op:
            sorted_mean = sorted_mean[:-1]
            sorted_std = sorted_std[:-1]
            sorted_std_percent = sorted_std_percent[:-1]
            #37 is nan - remove
            sorted_mean = np.delete(sorted_mean, 37)
            sorted_std = np.delete(sorted_std, 37)
            sorted_std_percent = np.delete(sorted_std_percent, 37)

        sorted_std = np.sort(sorted_std)
        sorted_std_percent = np.sort(sorted_std_percent)
        ax[0][2].plot(sorted_mean, np.linspace(0, 1, sorted_mean.size), color=color_dict[op], label=op_dict[op], linewidth=4)
        ax[0][2].set_xlabel("Average (ms)", fontsize=22)
        ax[1][2].plot(sorted_std_percent, np.linspace(0, 1, sorted_std_percent.size), color=color_dict[op], label=op_dict[op], linewidth=4)
        ax[1][2].set_xlabel("Deviation (%)", fontsize=22)
        ax[0][2].set_title("RTT", fontweight="bold", fontsize=20)

    ax[0][2].set_xlim(0, 300)
    ax[1][2].set_xlim(0, 200)
    ax[1][2].set_ylim(0, 1)
    ax[0][0].set_ylabel("CDF", fontsize=25)
    ax[1][0].set_ylabel("CDF", fontsize=25)
    ax[0][0].legend(loc="lower right", fontsize=18)
    plt.tick_params(axis='both', labelsize=16)
    plt.tight_layout()
    plt.savefig(plot_path + r"\fig_9.pdf")
    plt.close()

# load tput processed data
base_tput = r'C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\tput'
filehandler = open(base_tput + r'\driving\processed\main_op_link_dict.pkl', "rb")
# main_op_link_tput_dict format == [tput_speed_tech_dict, ca_speed_tech_dict, fiveg_ca_speed_dict, lte_ca_speed_dict, tput_tz_tech_dict, dist_speed_tech_dict, mcs_speed_dict, bler_speed_dict, rsrp_speed_dict, wl_speed_dict, overall_mean_list, overall_std_list, overall_5g_high_percent]
main_op_link_tput_dict = pickle.load(filehandler)
filehandler.close()

# load rtt processed data
base_rtt = r'C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\rtt'
filehandler = open(base_rtt + "\\" + r'processed\main_op_link_dict.pkl', "rb")
# main_op_link_rtt_dict format == [main_op_rtt_dict, main_rtt_5g_dict, main_rtt_tech_dict, main_rtt_edge_tech_dict, op_speed_dict, op_rtt_dict, op_tech_dict] 
main_op_link_rtt_dict = pickle.load(filehandler)
filehandler.close()

# static CDF 3-a
base = r'C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\tput\static'
plot_path = r"C:\Users\ubwin\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots"
plot_static_cdf_3a(base, plot_path)
# static CDF 3-b
plot_driving_cdf_3b(main_op_link_tput_dict, main_op_link_rtt_dict, plot_path)
# figure 4
plot_fig_4(main_op_link_tput_dict, main_op_link_rtt_dict, plot_path)
# figure 5
plot_fig_5(main_op_link_tput_dict, plot_path)
# figure 7
plot_fig_7(main_op_link_tput_dict, plot_path)
# figure 8
plot_fig_8(main_op_link_rtt_dict, plot_path)
# figure 9
plot_fig_9(main_op_link_tput_dict, main_op_link_rtt_dict, plot_path)
# figure 10
plot_fig_10(main_op_link_tput_dict, main_op_link_rtt_dict, plot_path)