import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from glob import glob
from datetime import timezone, timedelta, datetime
import geopy
import pickle
import re
import warnings
from collections import Counter
warnings.simplefilter(action='ignore', category=FutureWarning)

XCAL_LOG_DIR=  'xcal_log_files/'
APP_LOG_DIR=  'app_log_files/'
OPERATORS   =   ['verizon', 'tmobile', 'atnt']
PRETTY_LABEL   =   [r'Verizon', r'T-Mobile', r'AT&T']
LABEL_DICT =   dict(zip(OPERATORS,PRETTY_LABEL))
operator_color_arr = ['red', 'magenta', 'blue']

plt.rc('font', size=14)
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

#operator_pretty_arr = ['Verizon']
operator_pretty_arr = ['Verizon', 'T-Mobile', 'AT&T']

def get_xcal_file_name_per_operator(operator,
        log_dir=XCAL_LOG_DIR,
        do_print=True):
    """
    """
    file_pattern   =   log_dir + operator  + '/*.csv' 
    file_names  =   glob(file_pattern)
    file_names   =  [os.path.basename(name)
            for name in file_names]
    file_names.sort()
    return file_names

def get_log_file_name_per_operator(operator,
        log_dir=APP_LOG_DIR,
        do_print=True):
    """
    """
    file_pattern   =   log_dir + operator  + '/*.log' 
    file_names  =   glob(file_pattern)
    file_names   =  [os.path.basename(name)
            for name in file_names]
    file_names.sort()
    return file_names

def get_app_start_and_stop_time(log_file, do_print=True):
    """
    """
    with open(log_file) as f:
        lines = f.readlines()
    split   = lines[0].split()
    date    =   split[0][1:]
    time    =   split[1][0:-1] 
    start_time   =   date + ' ' + time
    start_time   =   pd.to_datetime(start_time, 
            format='%Y-%m-%d %H:%M:%S.%f')
    split   = lines[-1].split()
    date    =   split[0][1:]
    time    =   split[1][0:-1] 
    stop_time   =   date + ' ' + time
    stop_time   =   pd.to_datetime(stop_time, 
            format='%Y-%m-%d %H:%M:%S.%f')
    for line in lines:
        if "SessionStats" in line:
            date    =   line[1:11]
            time    =   line[12:20] 
            stop_time   =   date + ' ' + time
            stop_time   =   pd.to_datetime(stop_time, 
                    format='%Y-%m-%d %H:%M:%S.%f')
    if stop_time-start_time > pd.Timedelta(value=10, unit='minutes'):
        stop_time   = pd.to_datetime(0,format='%Y-%m-%d %H:%M:%S.%f')
        start_time  = pd.to_datetime(0,format='%Y-%m-%d %H:%M:%S.%f')
        print(f"Bug: time zone changed, return zero timestamps for {log_file}")
    result  =   [start_time, stop_time]
    return result

def bitrate_info_from_app(log_file, do_print, overwrite):
    """
    """
    [start_time, stop_time] =   get_app_start_and_stop_time(log_file, 
                                                        do_print=True)

    regex   =   r"(.*\/.*\/\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2})\.log"
    log_prefix  =   re.search(regex, log_file).group(1)

    with open(log_file) as f:
         lines  =   f.readlines()

    useful_info_dict   =   {'TIME_STAMP':[],
                            'state':[],
                            'minRTT':[],
                            'maxRTT':[],
                            'gain':[],
                            'bitrate':[]}
    for line in lines:
        if('Bitrate adapter' in line):
            split   =   line.split()
            
            date    =   split[0][1:]
            time    =   split[1][0:-1] 
            state   =   float(split[6][0:-1])
            minRTT  =   float(split[9][0:-1])
            maxRTT  =   float(split[12][0:-1])
            gain    =   float(split[15][0:-1])
            bitrate =   float(split[18])
            timestamp   =   date + ' ' + time
            timestamp   =   pd.to_datetime(timestamp, 
                    format='%Y-%m-%d %H:%M:%S.%f')
            useful_info_dict['TIME_STAMP'].append(timestamp)
            useful_info_dict['state'].append(state)
            useful_info_dict['minRTT'].append(minRTT)
            useful_info_dict['maxRTT'].append(maxRTT)
            useful_info_dict['gain'].append(gain)
            useful_info_dict['bitrate'].append(bitrate)
    f.close()

    useful_info_df  =   pd.DataFrame.from_dict(useful_info_dict).\
            drop_duplicates(subset="TIME_STAMP", ignore_index=True)

    total_app_time  =   min((stop_time - start_time).total_seconds(), 250.0)

    bitrate_info_df  =   pd.DataFrame(columns=   ['TIME_STAMP',
                                                'state',
                                                'minRTT',
                                                'maxRTT',
                                                'gain',
                                                'bitrate'])

    bitrate_info_df['TIME_STAMP']   =   pd.date_range(start_time, 
                                        periods=total_app_time, 
                                        freq='S').to_list()

    for i1, r1 in bitrate_info_df.iterrows():
        for i2, r2 in useful_info_df.iterrows():
            if r1['TIME_STAMP']  == r2['TIME_STAMP']:
                bitrate_info_df.iloc[i1] =   useful_info_df.iloc[i2]
    
   
    #auto fill the info from the most recent read
    bitrate_info_df  =   bitrate_info_df.ffill()
    #bitrate_info_df['bitrate'] =  bitrate_info_df['bitrate'].fillna(float(5.0))
    if overwrite:
        print(f"Writing bitrate csv file for {log_file}") 
        bitrate_info_df.to_csv(log_prefix+"_bitrate.csv")
    result  =   bitrate_info_df
    return result

def get_timing_info_from_app(log_file, do_print, overwrite):
    """
    """
    [start_time, stop_time] =   get_app_start_and_stop_time(log_file, 
                                                        do_print=True)
    #Get the first timing info message we don't know the timing info up until
    #this point
    regex   =   r"(.*\/.*\/\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2})\.log"
    log_prefix  =   re.search(regex, log_file).group(1)
    
    with open(log_file) as f:
        lines = f.readlines()
    for line in lines:
        if('Slow framerate' in line 
                or 'Setting target framerate' in line):
            split   =   line.split()
            date    =   split[0][1:]
            time    =   split[1][0:-1] 
            first_timing_info  =  date + ' ' + time 
            first_timing_info   =   pd.to_datetime(first_timing_info, 
                    format='%Y-%m-%d %H:%M:%S.%f')
            break
    f.close()
    total_app_time  =   min((stop_time - start_time).total_seconds(), 250.0)
    
    with open(log_file) as f:
        lines = f.readlines()

    useful_info_dict   =   {'TIME_STAMP':[],
                            'game':[],
                            'capture':[],
                            'convert':[],
                            'encode':[],
                            'network':[],
                            'decode':[],
                            'display':[]}

    for line in lines:
        if('Slow framerate' in line):
            split   =   line.split()
            date    =   split[0][1:]
            time    =   split[1][0:-1] 
            timestamp   =   date + ' ' + time
            timestamp   =   pd.to_datetime(timestamp, 
                    format='%Y-%m-%d %H:%M:%S.%f')
            game    =   float(split[5][0:-1])
            capture =   float(split[7][0:-1])
            convert =   float(split[9][0:-1])
            encode  =   float(split[11][0:-1])
            network =   float(split[13][0:-1])
            decode  =   float(split[15][0:-1])
            display =   float(split[17][0:-1])
            useful_info_dict['TIME_STAMP'].append(timestamp)
            useful_info_dict['game'].append(game)
            useful_info_dict['capture'].append(capture)
            useful_info_dict['convert'].append(convert)
            useful_info_dict['encode'].append(encode)
            useful_info_dict['network'].append(network)
            useful_info_dict['decode'].append(decode)
            useful_info_dict['display'].append(network)
        elif ('Setting target framerate' in line):
            split   =   line.split()
            date    =   split[0][1:]
            time    =   split[1][0:-1] 
            timestamp   =   date + ' ' + time
            timestamp   =   pd.to_datetime(timestamp, 
                    format='%Y-%m-%d %H:%M:%S.%f')
            game    =   float(split[8][0:-1])
            capture =   float(split[10][0:-1])
            convert =   float(split[12][0:-1])
            encode  =   float(split[14][0:-1])
            network =   float(split[16][0:-1])
            decode  =   float(split[18][0:-1])
            display =   float(split[20][0:-1])
            useful_info_dict['TIME_STAMP'].append(timestamp)
            useful_info_dict['game'].append(game)
            useful_info_dict['capture'].append(capture)
            useful_info_dict['convert'].append(convert)
            useful_info_dict['encode'].append(encode)
            useful_info_dict['network'].append(network)
            useful_info_dict['decode'].append(decode)
            useful_info_dict['display'].append(display)
    f.close()

    try:
        #Upper bounded since sometimes the server logs garbage after
        #experiments stop
        total_app_time  =   min(
                        (stop_time - start_time).total_seconds(),
                        250.0)
        #print(f"first_timing_info: {first_timing_info}")
        temp    =   first_timing_info
    except UnboundLocalError:
        print(f"No timing info in file {log_file}, assining zero total time")
        total_app_time =  0
        first_timing_info =  0
    
    #Now create the timing info dataframe
    timing_info_df  =   pd.DataFrame(columns=   ['TIME_STAMP',
                                                'game',
                                                'capture',
                                                'convert',
                                                'encode',
                                                'network',
                                                'decode',
                                                'display'])

    #this should be empty when total_app_time=0 (no timing) info
    timing_info_df['TIME_STAMP']   =   pd.date_range(start_time, 
                                        periods=total_app_time, 
                                        freq='S').to_list()

    useful_info_df  =   pd.DataFrame.from_dict(useful_info_dict)
    #Drop duplcates time stamp
    useful_info_df  =   useful_info_df.drop_duplicates(subset="TIME_STAMP",
                                                        ignore_index=True)
    #Recover timing info
    for i1, r1 in timing_info_df.iterrows():
        for i2, r2 in useful_info_df.iterrows():
            if r1['TIME_STAMP']  == r2['TIME_STAMP']:
                timing_info_df.iloc[i1] =   useful_info_df.iloc[i2]
    #auto fill value of the previous rows
    timing_info_df  =   timing_info_df.ffill()
    #drop the NaN at the beginning since we don't know the timing info then
    if overwrite:
        print(f"Writing timing csv file for {log_file}") 
        timing_info_df.to_csv(log_prefix+"_timing.csv")
    result  =   timing_info_df.dropna()

    if  do_print:
        print()
        print(f"Getting timing info: {log_file}")
        print(f"start_time: {start_time}")
        print(f"stop_time: {stop_time}")
        print(f"total_app_time: {total_app_time}")
    return result

def get_dropped_frame_info_from_app(log_file, do_print, overwrite):
    """
    """
    [start_time, stop_time] =   get_app_start_and_stop_time(log_file, 
                                                        do_print=True)
    regex   =   r"(.*\/.*\/\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2})\.log"
    log_prefix  =   re.search(regex, log_file).group(1)

    #Get set frame rate
    with open(log_file) as f:
        lines = f.readlines()
    droppedframe_id_dict   =   {'TIME_STAMP':[],
                                'Dropped frame ID': []}
    for line in lines:
        if('k_EStreamFrameResultDroppedReset' in line
                or 'k_EStreamFrameResultDroppedNetworkLost' in line):
            split   =   line.split()
            date    =   split[0][1:]
            time    =   split[1][0:-1] 
            timestamp   =   date + ' ' + time
            timestamp   =   pd.to_datetime(timestamp, 
                    format='%Y-%m-%d %H:%M:%S.%f')
            droppedframe_id_dict['TIME_STAMP'].append(timestamp)
            droppedframe_id_dict['Dropped frame ID'].append(int(split[5]))
    f.close()
    timestamps  =   [*Counter(droppedframe_id_dict['TIME_STAMP'])
                            .keys()]
    no_dropped_frames  =   [*Counter(droppedframe_id_dict['TIME_STAMP'])\
                                .values()]
    no_dropped_frame_dict   =   {'TIME_STAMP': timestamps,
                                'Number of frames dropped': no_dropped_frames}
    no_dropped_frame_df  =   pd.DataFrame.from_dict(no_dropped_frame_dict)

    with open(log_file) as f:
        lines = f.readlines()
    fps_dict    =   {'TIME_STAMP':[],
                    'FPS':  []}
    for line in lines:
        if('Setting target framerate' in line):
            split   =   line.split()
            date    =   split[0][1:]
            time    =   split[1][0:-1] 
            timestamp   =   date + ' ' + time
            timestamp   =   pd.to_datetime(timestamp, 
                    format='%Y-%m-%d %H:%M:%S.%f')
            fps_dict['TIME_STAMP'].append(timestamp)
            fps_dict['FPS'].append(float(split[5]))
    f.close()
    fps_df  =   pd.DataFrame.from_dict(fps_dict)
    total_app_time  =   min((stop_time - start_time).total_seconds(), 250.0)
    #
    dropped_frame_info_df =   pd.DataFrame(columns=['TIME_STAMP',
                                                    'Number of frames dropped',
                                                    'FPS',
                                                    ])
    dropped_frame_info_df['TIME_STAMP']   =   pd.date_range(start_time, 
                                                    periods=total_app_time, 
                                                    freq='S').to_list()

    #Fill no frames dropped information
    for i1, r1 in dropped_frame_info_df.iterrows():
        for i2, r2 in no_dropped_frame_df.iterrows():
            if r1['TIME_STAMP']  == r2['TIME_STAMP']:
                dropped_frame_info_df.at[i1,'Number of frames dropped']=\
                    no_dropped_frame_df.iloc[i2]['Number of frames dropped']

    dropped_frame_info_df[['Number of frames dropped']]   =   \
            dropped_frame_info_df[['Number of frames dropped']].fillna(value=0)
    #Fill FPS information
    for i1, r1 in dropped_frame_info_df.iterrows():
        for i2, r2 in fps_df.iterrows():
            if r1['TIME_STAMP']  == r2['TIME_STAMP']:
                dropped_frame_info_df.at[i1,'FPS']=\
                    fps_df.iloc[i2]['FPS']

    dropped_frame_info_df.loc[:,['FPS']]  = \
                dropped_frame_info_df.loc[:,['FPS']].ffill()

    #Assuming FPS = 60 for the first few seconds (no info)
    dropped_frame_info_df[['FPS']]   =   \
            dropped_frame_info_df[['FPS']].fillna(value=float(60))
    dropped_frame_info_df['Frame drop percentage']  =   \
        dropped_frame_info_df['Number of frames dropped']/ \
            dropped_frame_info_df['FPS']*100

    if overwrite:
        print(f"Writing frame drop csv file for {log_file}") 
        dropped_frame_info_df.to_csv(log_prefix+"_framedrop.csv")
    result  =   dropped_frame_info_df
    return result

def get_average_df(df):
    """
    """
    result  =   pd.DataFrame(pd.DataFrame(np.mean(df)).T)
    return result  
def get_bitrate_info_all(log_files, do_print=True, overwrite=False):
    """
    """
    regex   =   r"(.*\/.*\/\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2})\.log"
    result  =   pd.DataFrame()
    log_dict    =  {'Application logs':[]} 
    for f in log_files:
        log_prefix  =   re.search(regex, f).group(1)
        log_dict['Application logs'].append(f)
        csv_file    =  log_prefix+ "_bitrate.csv" 
        if os.path.isfile(csv_file) and not overwrite:
            df  =   pd.read_csv(csv_file, index_col=None)
        else:
            df =   bitrate_info_from_app(f, do_print, overwrite)
        average_df  =   get_average_df(df)
        result  =   pd.concat([result, average_df], axis    =   0,
                ignore_index    =   False)
    log_df  =   pd.DataFrame.from_dict(log_dict)
    result  =   result.reset_index()
    result   =   pd.concat([result, log_df], axis=1)
    return result

def get_timing_info_all(log_files, do_print=False, overwrite=False):
    """
    """
    regex   =   r"(.*\/.*\/\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2})\.log"
    result  =   pd.DataFrame()
    
    for f in log_files:
        log_prefix  =   re.search(regex, f).group(1)
        csv_file    =  log_prefix+ "_timing.csv" 
        if os.path.isfile(csv_file) and not overwrite:
            df  =   pd.read_csv(csv_file, index_col=None)
        else:
            df =   get_timing_info_from_app(f, do_print, overwrite)
        average_df  =   get_average_df(df)
        if(average_df['network'].values[0]    > 500 and do_print):
            print(f"high latency: {f}")
        result  =   pd.concat([result, average_df], axis    =   0, 
                ignore_index    =   False)
    return result

def get_dropped_frame_info_all(log_files, do_print=False, overwrite=False):
    """
    """
    regex   =   r"(.*\/.*\/\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2})\.log"
    result  =   pd.DataFrame()
    
    for f in log_files:
        log_prefix  =   re.search(regex, f).group(1)
        csv_file    =  log_prefix+ "_framedrop.csv" 
        if os.path.isfile(csv_file) and not overwrite:
            df  =   pd.read_csv(csv_file, index_col=None)
        else:
            df =   get_dropped_frame_info_from_app(f, do_print, overwrite)
        average_df  =   get_average_df(df)
        result  =   pd.concat([result, average_df], axis    =   0, 
                ignore_index    =   False)
    return result

def get_app_info_per_operator(operator):
    """
    """
    log_files   =   sorted(glob(APP_LOG_DIR+ operator + '/*.log'))
    df1 =   get_bitrate_info_all(log_files).reset_index(drop=True)
    df2  =   get_timing_info_all(log_files).reset_index(drop=True)
    df3 =   get_dropped_frame_info_all(log_files).reset_index(drop=True)
    result  =   pd.concat([df1, df2, df3], axis = 1).drop(columns='TIME_STAMP') 
    xcal_log_dict   =   {'XCAL logs': []}
    run_type_dict   =   {'Run type':[]}
    percentage_dict   =   {'5G percentage':[]}
    no_handover_dict    =   {'Number of handovers': []}
    app_to_xcal_log_map =   get_app_to_xcal_log_map_per_operator(operator)    
    driving_runs    =   filter_static_runs(operator, do_print=False)
    perc_5g_dict =   get_5G_percentage_per_operator(operator)
    operator_handover_dict    =   get_no_handovers_per_operator(operator)
    handover_dict   =   get_no_handovers_per_operator(operator)
    for log in result['Application logs']:
        xcal_log    =   app_to_xcal_log_map[log]
        xcal_log_dict['XCAL logs'].append(xcal_log)
        if(app_to_xcal_log_map[log] in driving_runs):
            run_type_dict['Run type'].append('Driving')
        else:
            run_type_dict['Run type'].append('Static')
        if(app_to_xcal_log_map[log] in perc_5g_dict.keys()):
            percentage_dict['5G percentage'].append(
                    perc_5g_dict[app_to_xcal_log_map[log]])
            no_handovers =   float(handover_dict[xcal_log])
            no_handover_dict['Number of handovers'].append(no_handovers)
        else:
            percentage_dict['5G percentage'].append(float(100))
            no_handover_dict['Number of handovers'].append(float(0))

    xcal_log_df =   pd.DataFrame.from_dict(xcal_log_dict)
    run_type_df =   pd.DataFrame.from_dict(run_type_dict)
    percentage_df =   pd.DataFrame.from_dict(percentage_dict)
    no_handover_df    =   pd.DataFrame.from_dict(no_handover_dict)
    result  =   pd.concat([result, xcal_log_df, 
                        run_type_df, percentage_df, 
                        no_handover_df], axis = 1)
    #Remove the percentages for the logs when we cannot obtains the info (due to 
    #time zone switch
    for index, row in result.iterrows():
        if pd.isna(row['bitrate']):
            result.at[index,'5G percentage']=np.nan
            try:
                result.at[index,'Number of handovers']=np.nan
            except ValueError as err:
                print(f"err: {err}")
                
    result.to_csv(f"{operator}_all.csv")
    return result

def get_cdf_data(raw_data, scale=1.0):
    """
    """
    index = 1
    x_data = []
    y_data = []

    raw_data = np.array(raw_data)
    raw_data = raw_data[~np.isnan(raw_data)]

    sorted_data = sorted(raw_data)
    for row in sorted_data:
        x_data.append(1.0 * row / scale)
        y_data.append(index * 1.0 / len(sorted_data) * 100)
        index += 1
    return [x_data, y_data]

def get_app_to_xcal_log_map_per_operator(operator):
    """
    """
    xcal_log_files      =  sorted(glob(XCAL_LOG_DIR+ operator + '/*.csv'))
    app_log_files      =  sorted(glob(APP_LOG_DIR+ operator + '/*.log'))
    
    xcal_time_regex      =   r".*\/(\d{8}_\d{6})_*"
    app_time_regex      =   r".*\/(\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}).log"
    #read xcal_first_timestamp
    xcal_time_dict  =   {}
    for log_file in xcal_log_files:
        time_str  =   re.search(xcal_time_regex, log_file).group(1)
        yyyy    =   time_str[0:4]
        mm      =   time_str[4:6]
        dd      =   time_str[6:8]
        hh      =   time_str[9:11]
        MM      =   time_str[11:13]
        ss      =   time_str[13:15]
        timestamp =  yyyy + mm + dd + ' ' + hh + MM + ss
        timestamp   =   pd.to_datetime(timestamp, 
                format='%Y-%m-%d %H:%M:%S.%f')
        xcal_time_dict[log_file]    =   timestamp

    app_time_dict  =   {}
    for log_file in app_log_files:
        time_str  =   re.search(app_time_regex, log_file).group(1)
        yyyy    =   time_str[0:4]
        mm      =   time_str[5:7]
        dd      =   time_str[8:10]
        HH      =   time_str[11:13]
        MM      =   time_str[14:16]
        SS      =   time_str[17:19]
        timestamp =  yyyy + mm + dd + ' ' + HH + MM + SS
        timestamp   =   pd.to_datetime(timestamp, 
                format='%Y-%m-%d %H:%M:%S.%f')
        app_time_dict[log_file]    =   timestamp

    #Check time mismatch
    app_to_xcal_log_map =   {}
    mismatch_tolerance  =   pd.Timedelta(value=60, unit='second')
    timezone_difference  =   pd.Timedelta(value=1, unit='hour')
    for k1, k2 in zip(xcal_time_dict.keys(), app_time_dict.keys()):
        mismatch    =   app_time_dict[k2] - xcal_time_dict[k1] 
        if (mismatch < mismatch_tolerance):
            app_to_xcal_log_map[k2] =   k1
        elif(mismatch > timezone_difference and
                mismatch < timezone_difference+mismatch_tolerance): 
            app_to_xcal_log_map[k2] =   k1
        else:
            print(f"Bug: weird mismatch between {k1} and {k2}, " +
                    f"{mismatch} seconds")

    result  =   app_to_xcal_log_map
    return result

def filter_static_runs(operator, do_print):
    """
    """
    xcal_log_files      =  sorted(glob(XCAL_LOG_DIR+ operator + '/*.csv'))
    driving_runs    =   []
    count = 0
    for log_file in xcal_log_files:
        df  =   pd.read_csv(log_file, low_memory=False)
        #get summary
        summary=   df.tail(8)
        min_max_lon =   (summary['Lon'].iloc[1],summary['Lon'].iloc[2])
        lon_diff    =   min_max_lon[1]-min_max_lon[0]
        min_max_lat =   (summary['Lat'].iloc[1],summary['Lat'].iloc[2])
        lat_diff    =   min_max_lat[1]-min_max_lat[0]
        if(lon_diff < 0.001 and lat_diff < 0.001):
            if do_print: print(f"Static: {log_file} (based on GPS)")
        elif(np.isnan(lat_diff) and np.isnan(lon_diff)):
            if do_print:
                print(f"no GPS data for {log_file}, looking into event info")
            try:
                if('Handover Attempt' in df['Event LTE Events'].unique()):
                    if do_print: print(f"Driving: {log_file} (found Handover)")
                    driving_runs.append(log_file)
                    count +=1
            except KeyError as err:
                    if do_print:
                        print(f"Static: {log_file} "+  
                        f"(no GPS data and cannot find event info)")
        else:
            if do_print:
                print(f"Driving: {log_file} (based on GPS)")

            driving_runs.append(log_file)
            count +=1
    if do_print: print(f"Total driving run: {count}")
    result  =   driving_runs
    return  result

def get_perc_5g(log_file):
    """
    Given a xcal trace corresponding to a run, 
    get the percentage of time in a run that
    is 5G mmWave or 5G midband.
    """
    # Remove everything other rows containing frequency or handover events
    
    df_xcal = pd.read_csv(log_file, low_memory=False)
    df_xcal.drop(df_xcal.tail(8).index, inplace=True)
    try:
        df_short = df_xcal[["TIME_STAMP", "Lat", "Lon", 
            "Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]", 
            'Event 5G-NR/LTE Events',
            "5G KPI PCell RF Frequency [MHz]", 
            "LTE KPI PCell Serving EARFCN(DL)", 
            'LTE KPI PCell Serving PCI', 
            '5G KPI PCell RF Serving PCI']]
    except Exception as ex:
        exception = str(ex)
        # some fields missing - let us take a look
        missing_field_list = ['5G KPI PCell RF Frequency [MHz]', 
                                '5G KPI PCell RF Serving PCI',
                                'Event 5G-NR/LTE Events']
        for field in missing_field_list:
            if field in exception:
                # create dummy column with nan
                df_xcal[field] = np.nan
        df_short = df_xcal[["TIME_STAMP", "Lat", "Lon", 
            "Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]",
            'Event 5G-NR/LTE Events',
            "5G KPI PCell RF Frequency [MHz]", 
            "LTE KPI PCell Serving EARFCN(DL)", 
            'LTE KPI PCell Serving PCI', 
            '5G KPI PCell RF Serving PCI']]

    df_short_tput = df_short[
    df_short[
        "Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"
        ].notna()]
    df_short_tput = df_short[
    df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"]
            > 0.1]
    df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
    # extra line
    df_short_ho = df_short[
            (df_short['Event 5G-NR/LTE Events']=="Handover Success") |
            (df_short['Event 5G-NR/LTE Events']=="NR SCG Addition Success") | 
        (df_short['Event 5G-NR/LTE Events'] == "NR SCG Modification Success")]

    df_merged = pd.concat([df_short_tput, df_short_ho])
    df_merged = df_merged.sort_values(by=["TIME_STAMP"])
    df_merged.reset_index(inplace=True)
    
    # Divide the df_merged using handover events as the boundary
    idx_of_ho = np.where(df_merged['Event 5G-NR/LTE Events'].\
            notnull().tolist())[0]
    
    df_divided_arr = []
    start_idx = 0
    for end_idx in idx_of_ho:
        if end_idx > start_idx:
            df_divided_arr.append(df_merged[start_idx: end_idx])
        start_idx = end_idx + 1
    if start_idx < len(df_merged):
        df_divided_arr.append(df_merged[start_idx:len(df_merged)])
    
    # For each divided df, check if is 5G by checking if any row contains 5G frequency
    time_total = 0.0
    time_5g = 0.0
    for df_divided in df_divided_arr:
        if len(df_divided['5G KPI PCell RF Frequency [MHz]'].dropna()) == 0:
            is_5g = False
        elif df_divided['5G KPI PCell RF Frequency [MHz]']\
                .dropna().iloc[0] < 1000:
            is_5g = False
        else:
            is_5g = True
        try:
            t1      =   pd.to_datetime(df_divided['TIME_STAMP'].iloc[0],
                            format='%Y-%m-%d %H:%M:%S.%f')
            t2      =   pd.to_datetime(df_divided['TIME_STAMP'].iloc[-1],
                            format='%Y-%m-%d %H:%M:%S.%f')
            t = float((t2-t1).to_timedelta64())
        except ValueError:
            print(f"Wrong time format: {log_file}")
        t /= 1e6    # ns to s
        time_total += t
        if is_5g:
            time_5g += t
    result  =   0 if time_total==0 else time_5g / time_total*100
    return result
    
def get_no_handovers(log_file):
    """
    Given a xcal trace corresponding to a run, 
    get the number of handover in a run that
    is 5G mmWave or 5G midband.
    """
    # Remove everything other rows containing frequency or handover events
    
    df_xcal = pd.read_csv(log_file, low_memory=False)
    df_xcal.drop(df_xcal.tail(8).index, inplace=True)
    try:
        df_short = df_xcal[["TIME_STAMP", "Lat", "Lon", 
            "Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]", 
            'Event 5G-NR/LTE Events']]
    except KeyError:
       return np.nan 
    df_short_tput = df_short[
    df_short[
        "Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"
        ].notna()]
    df_short_tput = df_short[
    df_short["Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]"]
            > 0.1]
    df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
    # extra line
    df_short_ho = df_short[
            (df_short['Event 5G-NR/LTE Events']=="Handover Success") |
            (df_short['Event 5G-NR/LTE Events']=="NR SCG Addition Success") | 
        (df_short['Event 5G-NR/LTE Events'] == "NR SCG Modification Success")]

    df_merged = pd.concat([df_short_tput, df_short_ho])
    df_merged = df_merged.sort_values(by=["TIME_STAMP"])
    df_merged.reset_index(inplace=True)
    result   =   df_merged['Event 5G-NR/LTE Events'].count()
    
    return result

def get_5G_percentage_per_operator(operator):
    """
    """
    xcal_log_files  =   filter_static_runs(operator, do_print=False)
    percentage_dict =   {}
    for log_file in xcal_log_files:
        percentage  =   get_perc_5g(log_file)
        percentage_dict[log_file]   =   percentage
    result =    percentage_dict
    return result

def get_no_handovers_per_operator(operator):
    """
    """
    xcal_log_files  =   filter_static_runs(operator, do_print=False)
    no_handover_dict =   {}
    for log_file in xcal_log_files:
        no_handovers  =   get_no_handovers(log_file)
        no_handover_dict[log_file]   =   no_handovers
    result =    no_handover_dict
    
    return result

def plot_bitrate_performance_scatter():
    """
    """
    fig, axs =   plt.subplots(ncols=3)
    for operator_idx, operator in enumerate(OPERATORS):
        df  =   pd.read_csv(f"{operator}_all.csv", low_memory=False)
        df_driving  =   df[df['Run type']== 'Driving']
        perc_5g_arr =   df_driving['5G percentage']

        perc_5g_arr =   df_driving['5G percentage']
        bitrate =   df_driving['bitrate']
        network_latency =   df_driving['network'].dropna()
        frame_drop_percentage   =   df_driving['Frame drop percentage']
        #Scatter plots
        ax  =   axs[(operator_idx)]
        ax.set_title(LABEL_DICT[OPERATORS[operator_idx]])
        bitrate_mbps    =   [i/1000 for i in bitrate]
        ax.scatter(perc_5g_arr, bitrate_mbps, s=8, c=f'C{operator_idx}')
        ax.set_ylim(0, 100)
        ax.set_xlim(-15,110)
        #ax.set_xlim(-0.1, 1.1)
        if operator_idx == 1:
            ax.set_xlabel('% times 5G mmWave/C-band', fontsize=16)
        if operator_idx > 0:
            ax.set_yticklabels([])
        if operator_idx == 0:
            ax.set_ylabel('Avg. Bitrate', fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=18)

    plt.savefig('Scatter_Bitrate.pdf')

def plot_droppercentage_performance_scatter():
    """
    """
    fig, axs =   plt.subplots(ncols=3)
    for operator_idx, operator in enumerate(OPERATORS):
        df  =   pd.read_csv(f"{operator}_all.csv", low_memory=False)
        df_driving  =   df[df['Run type']== 'Driving']
        perc_5g_arr =   df_driving['5G percentage']

        perc_5g_arr =   df_driving['5G percentage']
        bitrate =   df_driving['bitrate']
        network_latency =   df_driving['network'].dropna()
        frame_drop_percentage   =   df_driving['Frame drop percentage']
        #Scatter plots
        ax  =   axs[(operator_idx)]
        ax.set_title(LABEL_DICT[OPERATORS[operator_idx]])
        ax.scatter(perc_5g_arr, frame_drop_percentage, s=8, c=f'C{operator_idx}')
        ax.set_ylim(0, 15)
        ax.set_xlim(-15,110)
        #ax.set_xlim(-0.1, 1.1)
        if operator_idx == 1:
            ax.set_xlabel('% times 5G mmWave/C-band', fontsize=16)
        if operator_idx > 0:
            ax.set_yticklabels([])
        if operator_idx == 0:
            ax.set_ylabel('Dropped Frame (%)', fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=18)

    plt.savefig('Scatter_DroppedFrame.pdf')

def plot_app_performance_all():
    """
    """
    mosaic = """AABBCC012"""
    fig = plt.figure(figsize=(14, 4), constrained_layout=True)
    ax_dict = fig.subplot_mosaic(mosaic)
    #plt.subplots_adjust(wspace=0.1)
    best_bitrate=0
    best_network_latency=float("inf")
    best_frame_drop_percentage=float(100)
    for operator_idx, operator in enumerate(OPERATORS):
        df  =   pd.read_csv(f"{operator}_all.csv", low_memory=False)
        df_driving  =   df[df['Run type']== 'Driving']
        

        
        perc_5g_arr =   df_driving['5G percentage'].dropna()
        network_latency =   df_driving['network'].dropna()
        bitrate         =   df_driving['bitrate'].dropna()
        frame_drop_percentage   =   df_driving['Frame drop percentage']
        

        best_bitrate    =   max(max(df['bitrate']),best_bitrate)
        best_network_latency    = min(min(df['network']),
                                        best_network_latency)
        best_frame_drop_percentage  =   min(min(df['Frame drop percentage']), 
                                            best_frame_drop_percentage)
        #Bit rate cdf
        ax  =   ax_dict['A']
        x,y =   get_cdf_data(bitrate)
        x   =   [i/1000 for i in x]
        ax.plot(x, y, label=LABEL_DICT[OPERATORS[operator_idx]])
        ax.tick_params(axis='both', which='major', labelsize=18)
        if operator_idx ==  0:
            ax.set_xlabel('Bit rate (Mbps)', fontsize=18)
            ax.set_xlim(0,100)
        ax.set_ylabel('CDF')
        #Network latency cdf
        ax  =   ax_dict['B']
        x,y =   get_cdf_data(network_latency)
        ax.plot(x, y, label=LABEL_DICT[OPERATORS[operator_idx]])
        if operator_idx ==  0:
            ax.set_xlabel('Network latency (ms)', fontsize=16)
            ax.set_yticklabels([])
            #ax.set_xlim(0,1999)
        ax.tick_params(axis='both', which='major', labelsize=18)

        #Frame drop cdf
        ax  =   ax_dict['C']
        x,y =   get_cdf_data(frame_drop_percentage)
        ax.plot(x, y, label=LABEL_DICT[OPERATORS[operator_idx]])
        if operator_idx ==  0:
            ax.set_xlabel('Frame drop (%)', fontsize=16)
            ax.set_xlim(-1,15)
            ax.set_xticks(np.arange(0,20,5))
            ax.set_yticklabels([])
            #ax.set_xlim(0,1999)
        ax.tick_params(axis='both', which='major', labelsize=18)

        #Scatter plots
        ax  =   ax_dict[str(operator_idx)]
        ax.set_title(LABEL_DICT[OPERATORS[operator_idx]])
        bitrate_mbps    =   [i/1000 for i in bitrate]
        ax.scatter(perc_5g_arr, bitrate_mbps, s=8, c=f'C{operator_idx}')
        ax.set_ylim(0, 100)
        ax.set_xlim(-15,110)
        #ax.set_xlim(-0.1, 1.1)
        if operator_idx == 1:
            ax.set_xlabel('% times 5G mmWave/C-band', fontsize=16)
        if operator_idx > 0:
            ax.set_yticklabels([])
        if operator_idx == 0:
            ax.set_ylabel('Bit rate (Mbps)', fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=18)

    ax_dict['B'].legend(fontsize=10)
    ax_dict['A'].axvline(best_bitrate/1000, color='k', linestyle='--')
    ax_dict['B'].axvline(best_network_latency, color='k', linestyle='--')
    ax_dict['C'].axvline(best_frame_drop_percentage, color='k', linestyle='--')
    plt.savefig('Gaming_Performance.pdf')

def plot_performance_scatter():
    """
    """
    plt.rc('font', size=14)
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, axs    =  plt.subplots(1, 3, figsize=(4.5, 3.5),
                                constrained_layout=False)
    plt.subplots_adjust(wspace=0.1)

    for operator_idx, operator in enumerate(OPERATORS):
        df  =   pd.read_csv(f"{operator}_all.csv", low_memory=False)
        df_driving  =   df[df['Run type']== 'Driving']
        ax  =   axs[operator_idx]
        ax.set_title(LABEL_DICT[operator], fontsize=10, fontweight='bold')
        ax.scatter(df_driving['5G percentage']/100,
                    df_driving['Frame drop percentage'],
                    s=15,
                    c=operator_color_arr[operator_idx])
        ax.set_xticks([0,1])
        ax.set_xlim(-0.1,1.1)
        ax.set_ylim(0,30)
        if operator_idx==1:
            ax.set_xlabel('% times 5G mmWave/C-band')
        if operator_idx == 0:
            ax.set_ylabel("Drop frame (%)", fontsize=14)
        if operator_idx > 0:
            ax.set_yticklabels([])
        plt.savefig("Gaming_Scatter.pdf", bbox_inches="tight")

def plot_bitrate_performance_scatter():
    """
    """
    fig, axs =   plt.subplots(ncols=3)
    for operator_idx, operator in enumerate(OPERATORS):
        df  =   pd.read_csv(f"{operator}_all.csv", low_memory=False)
        df_driving  =   df[df['Run type']== 'Driving']
        perc_5g_arr =   df_driving['5G percentage']
        bitrate =   df_driving['bitrate']
        network_latency =   df_driving['network'].dropna()
        frame_drop_percentage   =   df_driving['Frame drop percentage']
        #Scatter plots
        ax  =   axs[(operator_idx)]
        ax.set_title(LABEL_DICT[OPERATORS[operator_idx]])
        bitrate_mbps    =   [i/1000 for i in bitrate]
        ax.scatter(perc_5g_arr, bitrate_mbps, s=8, c=f'C{operator_idx}')
        ax.set_ylim(0, 100)
        ax.set_xlim(-15,110)
        #ax.set_xlim(-0.1, 1.1)
        if operator_idx == 1:
            ax.set_xlabel('% times 5G mmWave/C-band', fontsize=16)
        if operator_idx > 0:
            ax.set_yticklabels([])
        if operator_idx == 0:
            ax.set_ylabel('Avg. Bitrate', fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=18)

    plt.savefig('Scatter_Bitrate.pdf')

def plot_performance_cdf():
    """
    """
    mosaic =   "AABBCC"
    fig =   plt.figure(figsize=(8,3), constrained_layout=False)
    ax_dict = fig.subplot_mosaic(mosaic)
    plt.subplots_adjust(wspace=0.1)
    best_bitrate=0
    best_network_latency=float("inf")
    best_frame_drop_percentage=float(100)
    for operator_idx, operator in enumerate(OPERATORS):
        df  =   pd.read_csv(f"{operator}_all.csv", low_memory=False)
        df_driving  =   df[df['Run type']== 'Driving']

        perc_5g_arr =   df_driving['5G percentage'].dropna()
        network_latency =   df_driving['network'].dropna()
        bitrate         =   df_driving['bitrate'].dropna()
        frame_drop_percentage   =   \
                df_driving['Frame drop percentage'].dropna()

        best_bitrate    =   max(max(df['bitrate']),best_bitrate)
        best_network_latency    = min(min(df['network']),
                                        best_network_latency)
        best_frame_drop_percentage  =   min(min(df['Frame drop percentage']), 
                                            best_frame_drop_percentage)
    
        #Bit rate cdf
        ax  =   ax_dict['A']
        x,y =   get_cdf_data(bitrate)
        x   =   [i/1000 for i in x]
        ax.plot(x, y, label=LABEL_DICT[operator],
                c   =   operator_color_arr[operator_idx],
                linewidth = 2)
        ax.tick_params(axis='both', which='major', labelsize=14)
        if operator_idx ==  0:
            ax.set_xlabel('Avg. Bitrate', fontsize=14, fontweight='bold')
            ax.set_xlim(0,100)
            ax.set_xticks(np.arange(0,110,20))
            ax.set_xticks(ax.get_xticks()[:-1])
        ax.set_ylabel('CDF')
        #Network latency cdf
        ax  =   ax_dict['B']
        x,y =   get_cdf_data(network_latency)
        ax.plot(x, y, label=LABEL_DICT[operator], 
                c   =   operator_color_arr[operator_idx],
                linewidth = 2)
        if operator_idx ==  0:
            ax.set_xlabel('Network latency (ms)', fontsize=14, fontweight='bold')
            ax.set_yticklabels([])
            ax.set_xlim(-1,800)
            ax.set_xticks(np.arange(0,900,200))
            ax.set_xticks(ax.get_xticks()[:-1])
            #ax.set_xlim(0,1999)
        ax.tick_params(axis='both', which='major', labelsize=14)

        #Frame drop cdf
        ax  =   ax_dict['C']
        x,y =   get_cdf_data(frame_drop_percentage)
        ax.plot(x, y, label=LABEL_DICT[operator], 
                c   =   operator_color_arr[operator_idx],
                linewidth = 2)
        if operator_idx ==  0:
            ax.set_xlabel('Frame drop %', fontsize=14, fontweight='bold')
            ax.set_xlim(-1,30)
            ax.set_xticks(np.arange(0,40,10))
            ax.set_yticklabels([])
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax_dict['A'].legend(fontsize=12)
        ax_dict['A'].axvline(best_bitrate/1000, color='k', linestyle='--',
                            linewidth=2)
        ax_dict['B'].axvline(best_network_latency, color='k', linestyle='--',
                            linewidth=2)
        ax_dict['C'].axvline(best_frame_drop_percentage, color='k', 
                            linestyle='--', linewidth=2)
        plt.savefig('Gaming_CDF.pdf', bbox_inches='tight')

def plot_scatter_verizon():
    """
    Plot 2 scatter plots
    1. Between performance (frame drop) and 5G percentage
    2. Between performance (frame drop) and no of handovers
    """


    fig,ax = plt.subplots(ncols=2, constrained_layout=True)
    fig.set_size_inches(2.5,3.5)
    df  =   pd.read_csv("verizon_all.csv", low_memory=False)
    df_driving  =   df[df['Run type']=='Driving']
    perc_5g_arr =   df_driving['5G percentage']
    frame_drop_percentage   =   df_driving['Frame drop percentage']
    no_handovers   =   df_driving['Number of handovers']
    
    ax[0].scatter(perc_5g_arr, frame_drop_percentage,
                s=20, c= 'red')
    ax[0].set_ylabel("Frame drop (%)", size=15)
    ax[0].set_xlabel("% 5G mmWave/midband")
    ax[0].set_xticks([0,1])

    ax[1].scatter(no_handovers, frame_drop_percentage,
                s=20, c= 'red')
    ax[1].set_xlim(0,50)
    ax[1].set_xticks([0,50])
    ax[1].set_xlabel("Number of HOs")
    ax[1].set_ylabel("Frame drop (%)")
    print("Saving fig")
    plt.savefig("Gaming_Verizon_Scatter_Percentage.pdf", bbox_inches="tight")


def plot_cdf_verizon():
    """
    Plot 3 cdfs:
    1. bit rate (Mbps)
    2. network latency (ms)
    3. frame drop (%)
    """
    mosaic =   "AABBCC"
    fig =   plt.figure(figsize=(5,3.5), constrained_layout=False)
    ax_dict = fig.subplot_mosaic(mosaic)
    plt.rc('font', size=14)
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    plt.subplots_adjust(wspace=0.1)
    df  =   pd.read_csv("verizon_all.csv", low_memory=False)
    best_bitrate    =   max(df["bitrate"])/1000
    best_network_latency    =   min(df["network"])
    best_frame_drop    =   min(df["Frame drop percentage"])
    df_driving  =   df[df["Run type"] =="Driving"]
    bit_rate    =   df_driving["bitrate"]/1000
    network_latency =   df_driving["network"]
    frame_drop  =   df_driving["Frame drop percentage"]
    ax  =   ax_dict['A']
    x, y    =   get_cdf_data(bit_rate)
    ax.plot(x, y, label='Verizon', c='red', linewidth=3)
    ax.set_xlim(0,100)
    ax.set_xticks([0, 50])
    ax.set_xlabel("Avg. Bitrate")
    ax.set_ylabel("CDF", fontsize=16)
    ax  =   ax_dict['B']
    x, y    =   get_cdf_data(network_latency)
    ax.plot(x, y, label='Verizon', c='red', linewidth=3)
    ax.set_xlim(0,1000)
    ax.set_xticks([0, 500])
    ax.set_xlabel("Network latency (ms)")
    ax.set_yticklabels([])
    ax  =   ax_dict['C']
    x, y    =   get_cdf_data(frame_drop)
    ax.set_xlim(-1,15)
    ax.set_xlabel("Frame drop (%)")
    ax.plot(x, y, label='Verizon', c='red', linewidth=3)
    ax.set_yticklabels([])
    ax_dict['A'].axvline(best_bitrate, color='k', linestyle='--', 
                            linewidth=3, label='Best run')
    ax_dict['B'].axvline(best_network_latency, color='k', linestyle='--',
                            linewidth=3, label='Best run')
    ax_dict['C'].axvline(best_frame_drop, color='k', linestyle='--',
                            linewidth=3, label='Best run')
    ax_dict['A'].legend(fontsize='small')
    plt.savefig('Gaming_Verizon_CDF.pdf', bbox_inches="tight")

def plot_cdf_verizon_only():
    """
    Plot 3 cdfs:
    1. bit rate (Mbps)
    2. network latency (ms)
    3. frame drop (%)
    """
    mosaic =   "AABBCC"
    fig =   plt.figure(figsize=(5,3.5), constrained_layout=True)
    ax_dict = fig.subplot_mosaic(mosaic)
    plt.rc('font', size=14)
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    df  =   pd.read_csv("verizon_all.csv", low_memory=False)
    best_bitrate    =   max(df["bitrate"])/1000
    best_network_latency    =   min(df["network"])
    best_frame_drop    =   min(df["Frame drop percentage"])
    df_driving  =   df[df["Run type"] =="Driving"]
    bit_rate    =   df_driving["bitrate"]/1000
    network_latency =   df_driving["network"]
    frame_drop  =   df_driving["Frame drop percentage"]
    ax  =   ax_dict['A']
    x, y    =   get_cdf_data(bit_rate)
    ax.plot(x, y, c='red', linewidth=3)
    ax.set_xlim(0,100)
    ax.set_xticks([0, 50])
    ax.set_xlabel("Avg.\nBitrate", fontsize=16,fontweight='bold')
    ax  =   ax_dict['B']
    ax.tick_params(axis='both', which='minor', labelsize=14)
    x, y    =   get_cdf_data(network_latency)
    ax.plot(x, y, c='red', linewidth=3)
    ax.set_xlim(0,1000)
    ax.set_xticks([0, 500])
    ax.set_xlabel("Network \n latency(ms)", fontsize=16,fontweight='bold')
    ax.set_yticklabels([])
    ax  =   ax_dict['C']
    x, y    =   get_cdf_data(frame_drop)
    ax.set_xlim(-1,15)
    ax.set_xlabel("Frame \n drop %", fontsize=16, fontweight='bold')
    ax.plot(x, y, label='Verizon', c='red', linewidth=3)
    ax.set_yticklabels([])
    ax_dict['A'].axvline(best_bitrate, color='k', linestyle='--',
                            linewidth=3, label='Best\nrun')
    ax_dict['B'].axvline(best_network_latency, color='k', linestyle='--',
                            linewidth=3, label='Best run')
    ax_dict['C'].axvline(best_frame_drop, color='k', linestyle='--',
                            linewidth=3, label='Best run')
    ax_dict['A'].legend(fontsize='small')
    plt.savefig('Gaming_Verizon_CDF.pdf', bbox_inches="tight")

def plot_scatter_verizon_only():
    mosaic = """AABB"""
    fig = plt.figure(figsize=(3.5, 3.5), constrained_layout=True)
    ax_dict = fig.subplot_mosaic(mosaic)
    plt.rc('font', size=14)
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    for idx_operator, operator in enumerate(OPERATORS):
        if (operator == "verizon"):
            df  =   pd.read_csv(f"{operator}_all.csv", low_memory=False)
            df_driving  =   df[df['Run type']=='Driving']
            perc_5g_arr =   df_driving['5G percentage']/100
            frame_drop_percentage   =   df_driving['Frame drop percentage']
            no_handovers   =   df_driving['Number of handovers']

            ax = ax_dict["A"]
            ax.scatter(perc_5g_arr, frame_drop_percentage,
                            s=20, c= 'red')
            ax.set_xlabel("% 5G mmWave\n/midband")
            ax.set_xticks([0,1])
            ax.set_ylabel("Frame drop (%)")

            ax = ax_dict["B"]
            ax.scatter(no_handovers, frame_drop_percentage,
                        s=20, c= 'red')
            ax.set_xlim(0,50)
            ax.set_xticks([0,50])
            ax.set_xlabel("No. \nof HOs'")
            ax.set_yticklabels([])
            plt.savefig("Gaming_Verizon_Scatter_Percentage.pdf", bbox_inches="tight")

if __name__ == '__main__':

    # Run the following functions first  to parse the XCAL and game logs to
    # generate the <operator>_all.csv files first

    get_app_info_per_operator('verizon')
    get_app_info_per_operator('tmobile')
    get_app_info_per_operator('atnt')

    # After you have the  <operator>_all.csv files, run the following functions
    # to plot

    plot_cdf_verizon_only() # Figure 16 a
    plot_scatter_verizon_only() # Figure 16 b
    plot_performance_scatter() # Figure 22 a
    plot_performance_cdf() # Figure 22 b
