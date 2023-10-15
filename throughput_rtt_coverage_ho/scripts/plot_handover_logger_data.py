import glob
import os
import sys
import pandas as pd
from datetime import datetime
import plotly.express as px

base = r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\coverage\handover_logger"
operator_log_dict = {"tmobile1" : "12*", "tmobile2" : "26*", "verizon" : "1C*", "atnt" : "R5*"}
log_dict =  {"tmobile1" : [], "tmobile2" : [], "verizon" : [], "atnt" : []}

folder_list = glob.glob(base + "\\" + "*")
for folder in folder_list:
    for op in operator_log_dict.keys():
        file_list = sorted(glob.glob(folder + "\\" + operator_log_dict[op]))
        log_dict[op].extend(file_list)

log_dict["tmobile"] = log_dict["tmobile1"] + log_dict["tmobile2"]
print()

if 1:
    #parse verizon
    vz_lat_long_dict = {}
    vz_lat_dict = {}
    vz_long_dict = {}
    vz_earfcn_dict = {}
    vz_arfcn_dict = {}
    last_lat = None
    last_long = None
    for vz_file in log_dict["verizon"]:
        fh = open(vz_file, "r")
        data = fh.readlines()
        for d in data:
            d = d.strip()
            if "Latitude is" in d:
                temp_lat = d.split()[-1]
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                vz_lat_dict[millisec] = float(temp_lat)
                last_lat = float(temp_lat)
                
            elif "Longitude is" in d:
                temp_long = d.split()[-1]
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                vz_long_dict[millisec] = float(temp_long)  
                last_long = float(temp_long)       

            elif "EARFCN" in d:
                temp_earfcn = d.split()[-1]
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                if last_lat != None:
                    vz_earfcn_dict[millisec] = [last_lat]
                else:
                    vz_earfcn_dict[millisec] = [None]
                if last_long != None:
                    vz_earfcn_dict[millisec].append(last_long)
                else:
                    vz_earfcn_dict[millisec].append(None)
                vz_earfcn_dict[millisec].append(temp_earfcn)
            elif " ARFCN" in d:
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                #find arfcn 
                arfcn_index = d.split().index("ARFCN:")
                temp_arfcn = d.split()[arfcn_index + 1]
                if last_lat != None:
                    vz_arfcn_dict[millisec] = [last_lat]
                else:
                    vz_arfcn_dict[millisec] = [None]
                if last_long != None:
                    vz_arfcn_dict[millisec].append(last_long)
                else:
                    vz_arfcn_dict[millisec].append(None)
                vz_arfcn_dict[millisec].append(temp_arfcn)        

   
    #extract unique earfcn
    unique_earfcn_vz = []
    for keys in vz_earfcn_dict.keys():
        earfcn = vz_earfcn_dict[keys][-1]
        if earfcn not in unique_earfcn_vz:
            unique_earfcn_vz.append(earfcn)

    #extract unique arfcn
    unique_arfcn_vz = []
    for keys in vz_arfcn_dict.keys():
        arfcn = vz_arfcn_dict[keys][-1]
        if arfcn not in unique_arfcn_vz:
            unique_arfcn_vz.append(arfcn)

    arfcn_freq_dict = {'177020' : 885.100, '2083329' : 28249.800, '2071667' : 27550.080, '648672' : 3730.080, '2078331' : 27949.920, '2073333' : 27650.040, '177000' : 885.000, '174800' : 874.000, '175000' : 875.000, '650004' : 3750.060, '2239999' : 37650.000}

    earfcn_freq_dict = {'1000' : 1970.00, '1025' :  1972.50, '1075' : 1977.50, '1125' : 1982.50 , '2100' : 2125.00, '2450' : 874.0, '2460' : 875.0, '2559' : 884.90, '2560' : 885.00, '2561' : 885.10, '2600' : 889.00, '5230' : 751.00, '5780' : 739.00, '66486' : 2115.00, '66536' : 2120.00, '66561' : 2122.50, '66586' : 2125.00, '66611' : 2127.50, '66636' : 2130.0, '66686' : 2135.00, '66711' : 2137.50, '66761' : 2142.50, '66786' : 2145.00, '66811' : 2147.50, '66836' : 2150.00, '66911' : 2157.50, '66936' : 2160.00, '66986' : 2165.00, '67011' : 2167.50, '67086' : 2175.00, '750' : 1945.00, '775' : 1947.50, '825' : 1952.50, '925' : 1962.50, '950' : 1965.00, '975' : 1967.50}
    print()

    #modify arfcn and earfcn dict
    mod_arfcn_dict = {}
    mod_earfcn_dict = {}

    vz_earfcn_lte_lat = []
    vz_earfcn_lte_long = []
    vz_earfcn_ltea_lat = []
    vz_earfcn_ltea_long = []


    for key in vz_earfcn_dict.keys():
        lat = vz_earfcn_dict[key][0]
        long = vz_earfcn_dict[key][1]
        earfcn = vz_earfcn_dict[key][2]
        freq = float(earfcn_freq_dict[earfcn])
        
        if int(earfcn) > 60000:
            tech = 'LTE-A'
            vz_earfcn_lte_lat.append(lat)
            vz_earfcn_lte_long.append(long)
        else:
            tech = 'LTE'
            vz_earfcn_ltea_lat.append(lat)
            vz_earfcn_ltea_long.append(long)
        mod_earfcn_dict[key] = [lat, long, tech]


    vz_arfcn_5glow_lat = []
    vz_arfcn_5glow_long = []
    vz_arfcn_5gmid_lat = []
    vz_arfcn_5gmid_long = []
    vz_arfcn_5ghigh28_lat = []
    vz_arfcn_5ghigh28_long = []
    vz_arfcn_5ghigh39_lat = []
    vz_arfcn_5ghigh39_long = []

    for key in vz_arfcn_dict.keys():
        lat = vz_arfcn_dict[key][0]
        long = vz_arfcn_dict[key][1]
        arfcn = vz_arfcn_dict[key][2]
        freq = float(arfcn_freq_dict[arfcn])
        if freq < 1000:
            #5g low
            tech = '5G-low'
            vz_arfcn_5glow_lat.append(lat)
            vz_arfcn_5glow_long.append(long)
        elif freq > 1000 and freq < 25000:
            #5g mid
            tech = '5G-mid'
            vz_arfcn_5gmid_lat.append(lat)
            vz_arfcn_5gmid_long.append(long)
        elif freq > 25000 and freq < 35000:
            #5g-high-28ghz
            tech = '5G-mmWave (28 GHz)'
            vz_arfcn_5ghigh28_lat.append(lat)
            vz_arfcn_5ghigh28_long.append(long)
        elif freq > 35000:
            #5g-high-39ghz
            tech = '5G-mmWave (39GHz)'
            vz_arfcn_5ghigh39_lat.append(lat)
            vz_arfcn_5ghigh39_long.append(long)

        mod_arfcn_dict[key] = [lat, long, tech]

    print()

if 1:
    #parse atnt
    atnt_lat_long_dict = {}
    atnt_lat_dict = {}
    atnt_long_dict = {}
    atnt_earfcn_dict = {}
    atnt_arfcn_dict = {}
    last_lat = None
    last_long = None
    for atnt_file in log_dict["atnt"]:
        fh = open(atnt_file, "r")
        data = fh.readlines()
        for d in data:
            d = d.strip()
            if "Latitude is" in d:
                temp_lat = d.split()[-1]
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                atnt_lat_dict[millisec] = float(temp_lat)
                last_lat = float(temp_lat)
                # if millisec not in atnt_lat_long_dict.keys():
                #     atnt_lat_long_dict[millisec] = [float(temp_lat)]
                # else:
                #     print("Some error with latitude!")
                #     sys.exit(1)
            elif "Longitude is" in d:
                temp_long = d.split()[-1]
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                atnt_long_dict[millisec] = float(temp_long)  
                last_long = float(temp_long)  
             

            elif "EARFCN" in d:
                temp_earfcn = d.split()[-1]
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                if last_lat != None:
                    atnt_earfcn_dict[millisec] = [last_lat]
                else:
                    atnt_earfcn_dict[millisec] = [None]
                if last_long != None:
                    atnt_earfcn_dict[millisec].append(last_long)
                else:
                    atnt_earfcn_dict[millisec].append(None)
                atnt_earfcn_dict[millisec].append(temp_earfcn)
            elif " ARFCN" in d:
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                #find arfcn 
                arfcn_index = d.split().index("ARFCN:")
                temp_arfcn = d.split()[arfcn_index + 1]
                if last_lat != None:
                    atnt_arfcn_dict[millisec] = [last_lat]
                else:
                    atnt_arfcn_dict[millisec] = [None]
                if last_long != None:
                    atnt_arfcn_dict[millisec].append(last_long)
                else:
                    atnt_arfcn_dict[millisec].append(None)
                atnt_arfcn_dict[millisec].append(temp_arfcn)        

    #extract unique earfcn
    unique_earfcn_atnt = []
    for keys in atnt_earfcn_dict.keys():
        earfcn = atnt_earfcn_dict[keys][-1]
        if earfcn not in unique_earfcn_atnt:
            unique_earfcn_atnt.append(earfcn)

    #extract unique arfcn
    unique_arfcn_atnt = []
    for keys in atnt_arfcn_dict.keys():
        arfcn = atnt_arfcn_dict[keys][-1]
        if arfcn not in unique_arfcn_atnt:
            unique_arfcn_atnt.append(arfcn)

    print()
    earfcn_freq_dict = {'1025' :  1972.50, '1075' : 1977.50, '1100' : 1980.00, '1125' : 1982.50, '1150' : 1985.00, '2175' : 2132.50, '41094' : 2640.40, '41490' : 2680.00, '5035' : 731.50, '5090' : 737.00, '5110' : 739.00, '5145' : 742.50, '5330' : 763.00, '625' : 1932.50, '650' : 1935.00, '66461' : 2112.50, '66486' : 2115.00, '66511' : 2117.50, '66611' : 2127.50, '66661' : 2132.50, '66686' : 2135.00, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66936' : 2160.00, '66985' : 2164.90, '66986' : 2165.00, '67086' : 2175.00, '675' : 1937.50, '700' : 1940.00, '800' : 1950.00, '850' : 1955.00, '875' : 1957.50, '900' : 1960.00, '925' : 1962.50, '950' : 1965, '9820' : 765.00}
    
    #modify arfcn and earfcn dict
    mod_arfcn_dict = {}
    mod_earfcn_dict = {}

    atnt_earfcn_lte_lat = []
    atnt_earfcn_lte_long = []
    atnt_earfcn_ltea_lat = []
    atnt_earfcn_ltea_long = []


    for key in atnt_earfcn_dict.keys():
        lat = atnt_earfcn_dict[key][0]
        long = atnt_earfcn_dict[key][1]
        earfcn = atnt_earfcn_dict[key][2]
        freq = float(earfcn_freq_dict[earfcn])
        if int(earfcn) > 60000:
            tech = 'LTE-A'
            atnt_earfcn_lte_lat.append(lat)
            atnt_earfcn_lte_long.append(long)
        else:
            tech = 'LTE'
            atnt_earfcn_ltea_lat.append(lat)
            atnt_earfcn_ltea_long.append(long)
        mod_earfcn_dict[key] = [lat, long, tech]

if 1:
    #parse tmobile
    tmobile_lat_long_dict = {}
    tmobile_lat_dict = {}
    tmobile_long_dict = {}
    tmobile_earfcn_dict = {}
    tmobile_arfcn_dict = {}
    last_lat = None
    last_long = None
    for tmobile_file in log_dict["tmobile"]:
        fh = open(tmobile_file, "r")
        data = fh.readlines()
        for d in data:
            d = d.strip()
            if "Latitude is" in d:
                temp_lat = d.split()[-1]
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                tmobile_lat_dict[millisec] = float(temp_lat)
                last_lat = float(temp_lat)

            elif "Longitude is" in d:
                temp_long = d.split()[-1]
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                tmobile_long_dict[millisec] = float(temp_long)  
                last_long = float(temp_long)  
                     

            elif "EARFCN" in d:
                temp_earfcn = d.split()[-1]
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                if last_lat != None:
                    tmobile_earfcn_dict[millisec] = [last_lat]
                else:
                    tmobile_earfcn_dict[millisec] = [None]
                if last_long != None:
                    tmobile_earfcn_dict[millisec].append(last_long)
                else:
                    tmobile_earfcn_dict[millisec].append(None)
                tmobile_earfcn_dict[millisec].append(temp_earfcn)
            elif " ARFCN" in d:
                temp_month = d.split()[0].split("-")[0]
                temp_date = d.split()[0].split("-")[1]
                temp_year = "2022"
                time_all = d.split()[1]
                datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
                dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                #find arfcn 
                arfcn_index = d.split().index("ARFCN:")
                temp_arfcn = d.split()[arfcn_index + 1]
                if last_lat != None:
                    tmobile_arfcn_dict[millisec] = [last_lat]
                else:
                    tmobile_arfcn_dict[millisec] = [None]
                if last_long != None:
                    tmobile_arfcn_dict[millisec].append(last_long)
                else:
                    tmobile_arfcn_dict[millisec].append(None)
                tmobile_arfcn_dict[millisec].append(temp_arfcn)        

    #extract unique earfcn
    unique_earfcn_tmobile = []
    for keys in tmobile_earfcn_dict.keys():
        earfcn = tmobile_earfcn_dict[keys][-1]
        if earfcn not in unique_earfcn_tmobile:
            unique_earfcn_tmobile.append(earfcn)

    #extract unique arfcn
    unique_arfcn_tmobile = []
    for keys in tmobile_arfcn_dict.keys():
        arfcn = tmobile_arfcn_dict[keys][-1]
        if arfcn not in unique_arfcn_tmobile:
            unique_arfcn_tmobile.append(arfcn)
    
    print()
    earfcn_freq_dict = {'1099' : 1979.90, '1100' : 1980.00, '1123' : 1982.30, '1125' : 1982.50, '1126' : 1982.60, '1148' : 1984.80, '1150' : 1985.00, '2000' : 2115.00, '2050' : 2120.00, '2125' : 2127.50, '2175' : 2132.50, '2200' : 2135.00, '2225' : 2137.50, '2300' : 2145.00, '2325' : 2147.50, '2460': 875.0,  '39750' : 2506.00, '39907' : 2521.70, '39948' : 2525.80, '40072' : 2538.20, '40384' : 2569.40, '40770' : 2608.00, '40810' : 2612.00, '41176' : 2648.60, '41238' : 2654.80, '41490' : 2680.00, '5035' : 731.50, '5090' : 737, '5095' : 737.50, '5110' : 739.00, '5330' : 763.00, '5780' : None, '5815': None, '66486': 2115.00, '66487' : 2115.10, '66536' : 2120.00, '66561' : None, '66586' : None, '66661' : 2132.50, '66686' : 2135, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66811': None, '66836': None, '66886': None, '66911': None, '66961': None, '66986' : 2165.00, '67011': None, '675' : 1937.50, '676': None, '677': None, '68611': None, '68636': None, '68661': None, '68686': None, '68786': None, '68836': None, '68861': None, '68886': None, '68911': None, '700' : 1940.00, '725': None, '750': None, '775': None, '801': None, '8115': None, '825': None, '8264': None, '8290': None, '8315': None, '8465': None, '850' : 1955.00, '851': None, '852': None, '8539': None, '8562': None, '8640': None, '8665': None, '875' : 1957.50, '876': None, '8763': None, '877': None, '8950': None, '901': None, '925' : 1962.50}

    arfcn_freq_dict = {'125400' : 627.000, '125900' : 629.500, '126400' : 632.000, '126490' :632.450, '126510' : 632.550, '126530' : 632.650, '126900' : 634.500, '506280' : 2531.400, '508296' : 2541.480, '509202' : 2546.010, '514056' : 2570.280, '520020' : 2600.100, '525204' :2626.020, '526002' : 2630.010, '526404' : 2632.020, '527202' : 2636.010, '528000' : 2640.000, '528696' : 2643.480, '529998' : 2649.990, '530700' : 2653.500}

        #modify arfcn and earfcn dict
    mod_arfcn_dict = {}
    mod_earfcn_dict = {}

    tmobile_earfcn_lte_lat = []
    tmobile_earfcn_lte_long = []
    tmobile_earfcn_ltea_lat = []
    tmobile_earfcn_ltea_long = []


    for key in tmobile_earfcn_dict.keys():
        lat = tmobile_earfcn_dict[key][0]
        long = tmobile_earfcn_dict[key][1]
        earfcn = tmobile_earfcn_dict[key][2]
        # freq = float(earfcn_freq_dict[earfcn])
        if int(earfcn) > 60000:
            tech = 'LTE-A'
            tmobile_earfcn_lte_lat.append(lat)
            tmobile_earfcn_lte_long.append(long)
        else:
            tech = 'LTE'
            tmobile_earfcn_ltea_lat.append(lat)
            tmobile_earfcn_ltea_long.append(long)
        mod_earfcn_dict[key] = [lat, long, tech]


    tmobile_arfcn_5glow_lat = []
    tmobile_arfcn_5glow_long = []
    tmobile_arfcn_5gmid_lat = []
    tmobile_arfcn_5gmid_long = []
    tmobile_arfcn_5ghigh28_lat = []
    tmobile_arfcn_5ghigh28_long = []
    tmobile_arfcn_5ghigh39_lat = []
    tmobile_arfcn_5ghigh39_long = []

    for key in tmobile_arfcn_dict.keys():
        lat = tmobile_arfcn_dict[key][0]
        long = tmobile_arfcn_dict[key][1]
        arfcn = tmobile_arfcn_dict[key][2]
        freq = float(arfcn_freq_dict[arfcn])
        if freq < 1000:
            #5g low
            tech = '5G-low'
            tmobile_arfcn_5glow_lat.append(lat)
            tmobile_arfcn_5glow_long.append(long)
        elif freq > 1000 and freq < 25000:
            #5g mid
            tech = '5G-mid'
            tmobile_arfcn_5gmid_lat.append(lat)
            tmobile_arfcn_5gmid_long.append(long)
        elif freq > 25000 and freq < 35000:
            #5g-high-28ghz
            tech = '5G-high-28GHz'
            tmobile_arfcn_5ghigh28_lat.append(lat)
            tmobile_arfcn_5ghigh28_long.append(long)
        elif freq > 35000:
            #5g-high-39ghz
            tech = '5G-high-39GHz'
            tmobile_arfcn_5ghigh39_lat.append(lat)
            tmobile_arfcn_5ghigh39_long.append(long)

        mod_arfcn_dict[key] = [lat, long, tech]

    print()

print()
#convert lists to df
vz_lte_df = pd.DataFrame(list(zip(vz_earfcn_lte_lat,vz_earfcn_lte_long, ["LTE"] * len(vz_earfcn_lte_lat))), columns = ["Latitude", "Longitude", "Color"])
vz_ltea_df = pd.DataFrame(list(zip(vz_earfcn_ltea_lat,vz_earfcn_ltea_long, ["LTE-A"] * len(vz_earfcn_ltea_lat))), columns = ["Latitude", "Longitude", "Color"])
vz_5glow_df = pd.DataFrame(list(zip(vz_arfcn_5glow_lat,vz_arfcn_5glow_long, ["5G-low"] * len(vz_arfcn_5glow_lat))), columns = ["Latitude", "Longitude", "Color"])
vz_5gmid_df = pd.DataFrame(list(zip(vz_arfcn_5gmid_lat,vz_arfcn_5gmid_long, ["5G-mid"] * len(vz_arfcn_5gmid_lat))), columns = ["Latitude", "Longitude", "Color"])
vz_5ghigh28_df = pd.DataFrame(list(zip(vz_arfcn_5ghigh28_lat,vz_arfcn_5ghigh28_long, ["5G-mmWave (28 GHz)"] * len(vz_arfcn_5ghigh28_lat))), columns = ["Latitude", "Longitude", "Color"])
vz_5ghigh39_df = pd.DataFrame(list(zip(vz_arfcn_5ghigh39_lat,vz_arfcn_5ghigh39_long, ["5G-mmWave (39 GHz)"] * len(vz_arfcn_5ghigh28_lat))), columns = ["Latitude", "Longitude", "Color"])


atnt_lte_df = pd.DataFrame(list(zip(atnt_earfcn_lte_lat,atnt_earfcn_lte_long, ["LTE"] * len(atnt_earfcn_lte_lat))), columns = ["Latitude", "Longitude", "Color"])
atnt_ltea_df = pd.DataFrame(list(zip(atnt_earfcn_ltea_lat,atnt_earfcn_ltea_long, ["LTE-A"] * len(atnt_earfcn_ltea_lat))), columns = ["Latitude", "Longitude", "Color"])


tmobile_lte_df = pd.DataFrame(list(zip(tmobile_earfcn_lte_lat,tmobile_earfcn_lte_long, ["LTE"] * len(tmobile_earfcn_lte_lat))), columns = ["Latitude", "Longitude", "Color"])
tmobile_ltea_df = pd.DataFrame(list(zip(tmobile_earfcn_ltea_lat,tmobile_earfcn_ltea_long, ["LTE-A"] * len(tmobile_earfcn_ltea_lat))), columns = ["Latitude", "Longitude", "Color"])
tmobile_5glow_df = pd.DataFrame(list(zip(tmobile_arfcn_5glow_lat,tmobile_arfcn_5glow_long, ["5G - low band"] * len(tmobile_arfcn_5glow_lat))), columns = ["Latitude", "Longitude", "Color"])
tmobile_5gmid_df = pd.DataFrame(list(zip(tmobile_arfcn_5gmid_lat,tmobile_arfcn_5gmid_long, ["5G - mid band"] * len(tmobile_arfcn_5gmid_lat))), columns = ["Latitude", "Longitude", "Color"])

#plot verizon data
fig1 = px.scatter_geo(vz_lte_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig2 = px.scatter_geo(vz_ltea_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig3 = px.scatter_geo(vz_5glow_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig4 = px.scatter_geo(vz_5gmid_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig5 = px.scatter_geo(vz_5ghigh28_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig6 = px.scatter_geo(vz_5ghigh39_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig=px.scatter_geo()
fig.add_traces(fig1._data)
fig.add_traces(fig2._data)
fig.add_traces(fig3._data)
fig.add_traces(fig4._data)
fig.add_traces(fig5._data)
fig.add_traces(fig6._data)


fig.data[1].marker.color = '#08710C'
fig.data[2].marker.color = '#70CA32'
fig.data[3].marker.color = '#F3FF33'
fig.data[4].marker.color = '#FFB233'
fig.data[5].marker.color = '#FF4629'
fig.data[6].marker.color = '#CB0404'

fig.data[1].marker.size = 3
fig.data[2].marker.size = 3
fig.data[3].marker.size = 3
fig.data[4].marker.size = 3
fig.data[5].marker.size = 3
fig.data[6].marker.size = 3

# f = fig.full_figure_for_development(warn=False)
fig.update_layout(geo_scope='usa', showlegend=True, margin=dict(l=25, r=25, t=25, b=15),)
fig.write_image(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_1\fig_1b.pdf")

#plot atnt data
fig1 = px.scatter_geo(atnt_lte_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig2 = px.scatter_geo(atnt_ltea_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig=px.scatter_geo()
fig.add_traces(fig1._data)
fig.add_traces(fig2._data)

fig.data[1].marker.color = '#08710C'
fig.data[2].marker.color = '#70CA32'

fig.data[1].marker.size = 3
fig.data[2].marker.size = 3

# f = fig.full_figure_for_development(warn=False)
fig.update_layout(geo_scope='usa', showlegend=False, margin=dict(l=25, r=25, t=25, b=15),)
fig.write_image(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_1\fig_1d.pdf")


#plot tmobile data
fig1 = px.scatter_geo(tmobile_lte_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig2 = px.scatter_geo(tmobile_ltea_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig3 = px.scatter_geo(tmobile_5glow_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig4 = px.scatter_geo(tmobile_5gmid_df, lat='Latitude', lon='Longitude', color='Color', width=300, height=100)
fig=px.scatter_geo()
fig.add_traces(fig1._data)
fig.add_traces(fig2._data)
fig.add_traces(fig3._data)
fig.add_traces(fig4._data)

fig.data[1].marker.color = '#08710C'
fig.data[2].marker.color = '#70CA32'
fig.data[3].marker.color = '#F3FF33'
fig.data[4].marker.color = '#FFB233'

fig.data[1].marker.size = 3
fig.data[2].marker.size = 3
fig.data[3].marker.size = 3
fig.data[4].marker.size = 3

# f = fig.full_figure_for_development(warn=False)
fig.update_layout(geo_scope='usa', showlegend=False, margin=dict(l=25, r=25, t=25, b=15),)
fig.write_image(r"C:\Users\nuwinslab\Desktop\segregated_drive_trip_data\imc2023-cellular-network-performance-on-wheels-data\throughput_rtt_coverage_ho\plots\fig_1\fig_1c.pdf")