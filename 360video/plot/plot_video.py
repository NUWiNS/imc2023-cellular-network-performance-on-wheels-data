import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
pio.renderers.default='iframe'
from matplotlib.pyplot import figure
from plotly.subplots import make_subplots
import sys
import matplotlib.patches as mpatches
from matplotlib.ticker import StrMethodFormatter
import plotly.express as px
pd.options.display.float_format = "{:,.2f}".format
from matplotlib.lines import Line2D
import glob
import matplotlib

df_verizon = pd.read_csv("/Users/khan.i/Desktop/driving_trip/Test/NEW/plot/merged_verizon.csv")
df_tmobile = pd.read_csv("/Users/khan.i/Desktop/driving_trip/Test/NEW/plot/merged_tmobile.csv")
df_atnt = pd.read_csv("/Users/khan.i/Desktop/driving_trip/Test/NEW/plot/merged_atnt.csv")

## PLOT FIG 15A

mosaic = """AABBCC"""
fig = plt.figure(figsize=(5, 3.5), constrained_layout=True)
ax_dict = fig.subplot_mosaic(mosaic)


plt.rc('font', size=14)
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

operator_pretty_arr = ['Verizon', 'T-Mobile', 'AT&T']

##QOE

list_verizon_qoe = df_verizon.avg_qoe.to_list()
list_verizon_qoe.sort()
p_verizon_qoe = 100. * np.arange(len(list_verizon_qoe)) / (len(list_verizon_qoe) - 1)


list_tmobile_qoe = df_tmobile.avg_qoe.to_list()
list_tmobile_qoe.sort()
p_tmobile_qoe = 100. * np.arange(len(list_tmobile_qoe)) / (len(list_tmobile_qoe) - 1)

list_atnt_qoe = df_atnt.avg_qoe.to_list()
list_atnt_qoe.sort()
p_atnt_qoe = 100. * np.arange(len(list_atnt_qoe)) / (len(list_atnt_qoe) - 1)


df_tmobile['Rebuf_per'] = df_tmobile.cumRebuffer.multiply(100)/df_tmobile.duration
df_verizon['Rebuf_per'] = df_verizon.cumRebuffer.multiply(100)/df_verizon.duration
df_atnt['Rebuf_per'] = df_atnt.cumRebuffer.multiply(100)/df_atnt.duration

list_verizon_rebuf = df_verizon.Rebuf_per.to_list()
list_verizon_rebuf.sort()
p_verizon_rebuf = 100. * np.arange(len(list_verizon_rebuf)) / (len(list_verizon_rebuf) - 1)

list_tmobile_rebuf = df_tmobile.Rebuf_per.to_list()
list_tmobile_rebuf.sort()
p_tmobile_rebuf = 100. * np.arange(len(list_tmobile_rebuf)) / (len(list_tmobile_rebuf) - 1)

list_atnt_rebuf = df_atnt.Rebuf_per.to_list()
list_atnt_rebuf.sort()
p_atnt_rebuf = 100. * np.arange(len(list_atnt_rebuf)) / (len(list_atnt_rebuf) - 1)

# ##Bitrate

list_verizon_bitrate = df_verizon.Bitrate.to_list()
list_verizon_bitrate.sort()
p_verizon_bitrate = 100. * np.arange(len(list_verizon_bitrate)) / (len(list_verizon_bitrate) - 1)


list_tmobile_bitrate = df_tmobile.Bitrate.to_list()
list_tmobile_bitrate.sort()
p_tmobile_bitrate = 100. * np.arange(len(list_tmobile_bitrate)) / (len(list_tmobile_bitrate) - 1)

list_atnt_bitrate = df_atnt.Bitrate.to_list()
list_atnt_bitrate.sort()
p_atnt_bitrate = 100. * np.arange(len(list_atnt_bitrate)) / (len(list_atnt_bitrate) - 1)

linwwidth_ik = 3
for idx_operator, operator in enumerate(['verizon', 'tmobile', 'atnt']):
            
            #QOE
            ax = ax_dict['A']
            if (operator == 'verizon'):
                ax.plot(list_verizon_qoe, p_verizon_qoe, label ='Verizon', linewidth= linwwidth_ik, color = "red")
            ax.set_xlabel('Avg.\nQoE')
            ax.set_xlim(-1300,120)


            # REBUFF

            ax = ax_dict['B']
            if (operator == 'verizon'):
                ax.plot(list_verizon_rebuf, p_verizon_rebuf, linewidth=linwwidth_ik, color = "red")
            ax.set_xlabel('Rebuffer\nTime %')
            ax.set_xlim(0,90)
            ax.set_yticklabels([])

            #Bitrate
            ax = ax_dict['C']
            if (operator == 'verizon'):
                ax.plot(list_verizon_bitrate, p_verizon_rebuf, linewidth=linwwidth_ik, color = "red")
            ax.set_xlabel('Avg.\nBitrate')
            ax.set_xlim(0,100)
            ax.set_yticklabels([])
            
ik_tick = 18
    
legend_elements = [
        Line2D([0], [0], color='black', linestyle='--', lw=2, label='Best\nrun'),
    ]
ax_dict['A'].legend(handles=legend_elements, loc='upper left', prop={'size': 12})
ax_dict['A'].axvline(96.29, color='k', linestyle='--',lw=linwwidth_ik)
ax_dict['B'].axvline(0.4, color='k', linestyle='--', lw=linwwidth_ik)
ax_dict['C'].axvline(97.92, color='k', linestyle='--', lw=linwwidth_ik)

plt.savefig("360_CDF_Summary_driving_verizon.pdf", dpi = 100)

## PLOT Scatter

#Figure 15B

mosaic = """AABB"""
fig = plt.figure(figsize=(3.5, 3.5), constrained_layout=True)
ax_dict = fig.subplot_mosaic(mosaic)
plt.rc('font', size=14)
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

operator_pretty_arr = ['Verizon']
operator_color_arr = ['red']

linwwidth_ik = 2

ik_tick = 18
df_verizon_wlen_true = df_verizon[df_verizon['Wlength']== True]
df_verizon_wlen_false = df_verizon[df_verizon['Wlength']== False]

for idx_operator, operator in enumerate(['verizon']):
    perc_5g_arr = []
    app_acc_arr = []
    ho_arr =[]
    if (operator == "verizon"):
        #print("Gere")
        axs = ax_dict["A"]
        perc_5g_arr_2 = df_verizon_wlen_false['5G_Time'].to_list()
        app_acc_arr_2 = df_verizon_wlen_false['avg_qoe'].to_list()
        axs.scatter(perc_5g_arr_2, app_acc_arr_2, s=15,  c=operator_color_arr[idx_operator], label= 'cloud')
        
        perc_5g_arr = df_verizon_wlen_true['5G_Time'].to_list()
        app_acc_arr = df_verizon_wlen_true['avg_qoe'].to_list()
        
        axs.scatter(perc_5g_arr, app_acc_arr, s=60, marker='x', c=f'C5', label= 'edge')
        
        axs2 = ax_dict["B"]
        perc_5g_arr_2 = df_verizon_wlen_false['ho'].to_list()
        app_acc_arr_2 = df_verizon_wlen_false['avg_qoe'].to_list()
        axs2.scatter(perc_5g_arr_2, app_acc_arr_2, s=15,  c=operator_color_arr[idx_operator], label= 'cloud')
        
        perc_5g_arr = df_verizon_wlen_true['ho'].to_list()
        app_acc_arr = df_verizon_wlen_true['avg_qoe'].to_list()
        
        axs2.scatter(perc_5g_arr, app_acc_arr, s=60, marker='x', c=f'C5', label= 'edge')
        axs2.set_ylim(-1300, 200)
        axs2.set_xlim(-1, 50)
        if idx_operator == 0:
            print("") 
        if idx_operator == 0:
            axs2.set_xlabel('No. \nof HOs')
            axs2.set_yticklabels([])
        if idx_operator > 0:
            axs2.set_yticklabels([])
      
    axs.set_ylim(-1300, 200)
    axs.set_xlim(-0.1, 1.1)
    if idx_operator == 0:
        axs.set_ylabel('Avg. QoE')
        #axs.legend(fontsize='6')
    if idx_operator == 0:
        axs.set_xlabel('% 5G mmWave\n/midband')
    if idx_operator > 0:
        axs.set_yticklabels([])
           
ax_dict['A'].legend(fontsize='10')
plt.savefig("360_Scatter_Summary_driving_updated_combined.pdf", bbox_inches="tight", dpi = 100)

## APPENDIX FIG 21A

mosaic = """AABBCC"""
fig = plt.figure(figsize=(8, 3.5), constrained_layout=True)
ax_dict = fig.subplot_mosaic(mosaic)

plt.rc('font', size=14)
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

operator_pretty_arr = ['Verizon', 'T-Mobile', 'AT&T']

#QOE

list_verizon_qoe = df_verizon.avg_qoe.to_list()
list_verizon_qoe.sort()
p_verizon_qoe = 100. * np.arange(len(list_verizon_qoe)) / (len(list_verizon_qoe) - 1)


list_tmobile_qoe = df_tmobile.avg_qoe.to_list()
list_tmobile_qoe.sort()
p_tmobile_qoe = 100. * np.arange(len(list_tmobile_qoe)) / (len(list_tmobile_qoe) - 1)

list_atnt_qoe = df_atnt.avg_qoe.to_list()
list_atnt_qoe.sort()
p_atnt_qoe = 100. * np.arange(len(list_atnt_qoe)) / (len(list_atnt_qoe) - 1)

#Rebuffer
df_tmobile['Rebuf_per'] = df_tmobile.cumRebuffer.multiply(100)/df_tmobile.duration
df_verizon['Rebuf_per'] = df_verizon.cumRebuffer.multiply(100)/df_verizon.duration
df_atnt['Rebuf_per'] = df_atnt.cumRebuffer.multiply(100)/df_atnt.duration

list_verizon_rebuf = df_verizon.Rebuf_per.to_list()
list_verizon_rebuf.sort()
p_verizon_rebuf = 100. * np.arange(len(list_verizon_rebuf)) / (len(list_verizon_rebuf) - 1)

list_tmobile_rebuf = df_tmobile.Rebuf_per.to_list()
list_tmobile_rebuf.sort()
p_tmobile_rebuf = 100. * np.arange(len(list_tmobile_rebuf)) / (len(list_tmobile_rebuf) - 1)

list_atnt_rebuf = df_atnt.Rebuf_per.to_list()
list_atnt_rebuf.sort()
p_atnt_rebuf = 100. * np.arange(len(list_atnt_rebuf)) / (len(list_atnt_rebuf) - 1)

#Bitrate

list_verizon_bitrate = df_verizon.Bitrate.to_list()
list_verizon_bitrate.sort()
p_verizon_bitrate = 100. * np.arange(len(list_verizon_bitrate)) / (len(list_verizon_bitrate) - 1)


list_tmobile_bitrate = df_tmobile.Bitrate.to_list()
list_tmobile_bitrate.sort()
p_tmobile_bitrate = 100. * np.arange(len(list_tmobile_bitrate)) / (len(list_tmobile_bitrate) - 1)

list_atnt_bitrate = df_atnt.Bitrate.to_list()
list_atnt_bitrate.sort()
p_atnt_bitrate = 100. * np.arange(len(list_atnt_bitrate)) / (len(list_atnt_bitrate) - 1)

linwwidth_ik = 2.5
for idx_operator, operator in enumerate(['verizon', 'tmobile', 'atnt']):
    
            ax = ax_dict['A']
            if (operator == 'verizon'):
                ax.plot(list_verizon_qoe, p_verizon_qoe, label ='Verizon', linewidth= linwwidth_ik, color = "red")
            if (operator == 'tmobile'):    
                ax.plot(list_tmobile_qoe, p_tmobile_qoe, label = 'T-Mobile',linewidth=linwwidth_ik, color = "magenta")
            if (operator == 'atnt'):    
                ax.plot(list_atnt_qoe, p_atnt_qoe, label = 'AT&T', linewidth=linwwidth_ik, color = "blue")
            ax.set_xlabel('Avg. QOE')
            ax.set_ylabel('CDF')
            ax.set_xlim(-1300,120)

            # ##REBUFF

            ax = ax_dict['B']
            if (operator == 'verizon'):
                ax.plot(list_verizon_rebuf, p_verizon_rebuf, linewidth=linwwidth_ik, color = "red")
            if (operator == 'tmobile'):    
                ax.plot(list_tmobile_rebuf, p_tmobile_rebuf, linewidth=linwwidth_ik, color = "magenta")
            if (operator == 'atnt'):     
                ax.plot(list_atnt_rebuf, p_atnt_rebuf, linewidth=linwwidth_ik, color = "blue")
            ax.set_xlabel('Rebuffer Time %')
            ax.set_xlim(0,100)
            ax.set_yticklabels([])


            ax = ax_dict['C']
            if (operator == 'verizon'):
                ax.plot(list_verizon_bitrate, p_verizon_bitrate, linewidth=linwwidth_ik, color = "red")
            if (operator == 'tmobile'):    
                ax.plot(list_tmobile_bitrate, p_tmobile_bitrate, linewidth=linwwidth_ik, color = "magenta")
            if (operator == 'atnt'):     
                ax.plot(list_atnt_bitrate, p_atnt_bitrate, linewidth=linwwidth_ik, color = "blue")
            ax.set_xlabel('Avg. Bitrate')
            ax.set_xlim(0,100, 20)
            ax.set_yticklabels([])

ik_tick = 18
list_verizon_5g = df_verizon['5G_Time'].to_list()

legend_elements = [

        Line2D([0], [0], color='black', linestyle='--', lw=2, label='Best Run'),
    ]

ax_dict['A'].legend()
ax_dict['B'].legend(handles=legend_elements, loc='lower right', prop={'size': 14})
ax_dict['A'].axvline(96.29, color='k', linestyle='--',lw=3)
ax_dict['B'].axvline(0.2, color='k', linestyle='--', lw=3)
ax_dict['C'].axvline(96.29, color='k', linestyle='--', lw=3)


plt.savefig("360_CDF_Summary_driving.pdf", dpi = 100)


## APPENDIX FIG 21B

mosaic = """AABBCC"""
fig = plt.figure(figsize=(5, 3.5), constrained_layout=True)
ax_dict = fig.subplot_mosaic(mosaic)

plt.rc('font', size=14)
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

operator_pretty_arr = ['Verizon', 'T-Mobile', 'AT&T']
operator_color_arr = ['red', 'magenta', 'blue']
##QOE

linwwidth_ik = 2

### 5G DATA
ik_tick = 18
# list_verizon_5g = df_verizon['5G_Time'].to_list()

for idx_operator, operator in enumerate(['verizon','tmobile', 'atnt' ]):
    perc_5g_arr = []
    app_acc_arr = []
    
    ho_arr =[]

    # ax = axs[idx_operator]
    # ax.set_title(operator_pretty_arr[idx_operator])
    if (operator == "verizon"):
        #print("Gere")
        ax = ax_dict['A']
        perc_5g_arr_2 = df_verizon_wlen_false['5G_Time'].to_list()
        app_acc_arr_2 = df_verizon_wlen_false['avg_qoe'].to_list()
        ax.scatter(perc_5g_arr_2, app_acc_arr_2, s=20,  c=operator_color_arr[idx_operator], label= 'cloud')
        
        perc_5g_arr = df_verizon_wlen_true['5G_Time'].to_list()
        app_acc_arr = df_verizon_wlen_true['avg_qoe'].to_list()
        
        ax.scatter(perc_5g_arr, app_acc_arr, s=80, marker='x', c=f'C5', label= 'edge')
        ax.set_title(operator_pretty_arr[idx_operator], fontweight="bold")
        
    if (operator == "tmobile"):
        ax = ax_dict['B']
        perc_5g_arr = df_tmobile['5G_Time'].to_list()
        app_acc_arr = df_tmobile['avg_qoe'].to_list()
        ax.scatter(perc_5g_arr, app_acc_arr, s=10, c=operator_color_arr[idx_operator])
        ax.set_title(operator_pretty_arr[idx_operator], fontweight="bold")
    
    if (operator == "atnt"):
        ax = ax_dict['C']
        perc_5g_arr = df_atnt['5G_Time'].to_list()
        app_acc_arr = df_atnt['avg_qoe'].to_list()
        ax.scatter(perc_5g_arr, app_acc_arr, s=10, c=operator_color_arr[idx_operator])
        ax.set_title(operator_pretty_arr[idx_operator], fontweight="bold")
        
    
    ax.set_ylim(-1300, 200)
    ax.set_xlim(-0.1, 1.1)
    if idx_operator == 0:
        ax.set_ylabel('Avg. QoE')
        #axs.legend(fontsize='6')
    if idx_operator == 1:
        ax.set_xlabel('% of times 5G mmWave /C-band')
    if idx_operator > 0:
        ax.set_yticklabels([])
           
ax_dict['A'].legend(loc='lower left', prop={'size': 12})

plt.savefig("360_Scatter_Summary_driving.pdf", bbox_inches="tight", dpi = 100)