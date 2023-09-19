"""
    Script to plot the AR & CAV figures.

    @Author kong102@purdue.edu
    @Date   2023-09-19
"""
from pathlib import Path

import geopy.distance
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


operator_pretty_arr = ['Verizon', 'T-Mobile', 'AT&T']
operator_color_arr = ['red', 'magenta', 'blue']


def get_app_xcal_df_pairs(operator, app, encoding):
    app_paths = sorted(Path(f'{app}-{encoding}-{operator}').glob('app-*.csv'))
    xcal_paths = sorted(Path(f'{app}-{encoding}-{operator}').glob('xcal-*.csv'))
    for app_path, xcal_path in zip(app_paths, xcal_paths):
        df_app = pd.read_csv(app_path)
        df_xcal = pd.read_csv(xcal_path, parse_dates=['TIME_STAMP'], infer_datetime_format=True)
        yield df_app, df_xcal


def get_mean_e2e(df, fps, num_frames_total):
    if len(df) == 0:
        return np.nan

    # # Remove the first 2 seconds
    # df = df[df.idx > 2 * fps]

    e2e_lat_arr = (df.recv - df.avail).tolist()

    # If the last outstanding frame (which is not logged) did not return in time (that is, return
    # with the same E2E last the frame) to last frame, assume network entered zombie state and
    # the frame returned at the end of the run
    if len(df) >= 2:
        # Infer the frame ID of the outstanding frame
        last_frame_id = df.idx.iloc[-1]
        second_last_frame_id = df.idx.iloc[-2]
        outstanding_frame_id = last_frame_id + (last_frame_id - second_last_frame_id)

        # Check if last frame did not return in time
        if outstanding_frame_id + (outstanding_frame_id - last_frame_id) < num_frames_total:
            outstanding_frame_e2e = (num_frames_total - outstanding_frame_id) * 1000 / fps
            e2e_lat_arr.append(outstanding_frame_e2e)

    return np.mean(e2e_lat_arr)


def get_num_ho(df_xcal):
    return len(split_by_ho(df_xcal)) - 1


def get_cdf_data(raw_data, scale=1.0):
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


def is_wavelength(df_xcal):
    """
    Given a run, return whether a run is with AWS Wavelength. Assume edge server is used
    when the run is near the cities.
    """
    coord_city_arr = [
        [34.058479, -118.237534],
        [39.74691, -105.004723],
        [39.74435, -105.00943],
        [39.76627, -104.999107],
        [40.061871, -104.654373],
        [34.058441, -118.237549],
        [34.068748, -118.22921],
        [41.893082, -87.623756],
        [36.113411, -115.173218],
    ]
    coord = [
        df_xcal.Lat.dropna().median(),
        df_xcal.Lon.dropna().median(),
    ]

    # Nothing we can do if no coordinate
    if np.isnan(coord[0]) or np.isnan(coord[1]):
        return False

    for coord_city in coord_city_arr:
        if geopy.distance.geodesic(coord, coord_city).miles < 10:
            return True
    return False


def split_by_ho(df_xcal):
    """
    Split the xcal dataframe using HO as the boundary.
    """
    # Remove everything other than columns containing frequency or handover events
    try:
        df_short = df_xcal[["TIME_STAMP", "Lat", "Lon", "Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]", 'Event 5G-NR/LTE Events',
                            "5G KPI PCell RF Frequency [MHz]", "LTE KPI PCell Serving EARFCN(DL)", 'LTE KPI PCell Serving PCI', '5G KPI PCell RF Serving PCI']]
    except Exception as ex:
        exception = str(ex)
        # some fields missing - let us take a look
        missing_field_list = []
        for field in missing_field_list:
            if field in exception:
                # create dummy column with nan
                df_xcal[field] = np.nan
        df_short = df_xcal[["TIME_STAMP", "Lat", "Lon", "Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]", 'Event 5G-NR/LTE Events',
                            "5G KPI PCell RF Frequency [MHz]", "LTE KPI PCell Serving EARFCN(DL)", 'LTE KPI PCell Serving PCI', '5G KPI PCell RF Serving PCI']]

    df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"].notna()]
    df_short_tput = df_short[df_short["Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]"] > 0.1]
    df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
    # extra line
    df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].astype(str).str.contains("Handover Success") | df_short['Event 5G-NR/LTE Events'].astype(str).str.contains(
        "NR SCG Addition Success") | df_short['Event 5G-NR/LTE Events'].astype(str).str.contains("NR SCG Modification Success")]
    df_merged = pd.concat([df_short_tput, df_short_ho])
    df_merged = df_merged.sort_values(by=["TIME_STAMP"])
    df_merged.reset_index(inplace=True)

    # Divide the df_merged using handover events as the boundary
    idx_of_ho = np.where(df_merged['Event 5G-NR/LTE Events'].notnull().tolist())[0]

    df_splitted_arr = []
    start_idx = 0
    for end_idx in idx_of_ho:
        if end_idx > start_idx:
            df_splitted_arr.append(df_merged[start_idx: end_idx])
        start_idx = end_idx + 1
    if start_idx < len(df_merged):
        df_splitted_arr.append(df_merged[start_idx:len(df_merged)])

    return df_splitted_arr


def get_perc_5g(df_xcal):
    """
    Given a xcal trace corresponding to a run, get the percentage of time in a run that
    is 5G mmWave or 5G midband.
    """
    df_splitted_arr = split_by_ho(df_xcal)

    # For each divided df, check if is 5G by checking if any row contains 5G frequency
    time_total = 0.0
    time_5g = 0.0
    for df_divided in df_splitted_arr:
        if len(df_divided['5G KPI PCell RF Frequency [MHz]'].dropna()) == 0:
            is_5g = False
        # elif df_divided['5G KPI PCell RF Frequency [MHz]'].dropna().iloc[0] < 1000:
        #     is_5g = False
        else:
            is_5g = True
        t = float((df_divided['TIME_STAMP'].iloc[-1] -
                  df_divided['TIME_STAMP'].iloc[0]).to_timedelta64())
        t /= 1e6    # ns to s
        time_total += t
        if is_5g:
            time_5g += t
    if time_total == 0:
        return 0.0
    else:
        return time_5g / time_total


def lookup_accuracy(df, use_encoding: bool):
    if len(df) == 0:
        return 0.0

    # acc[i] means accuracy if E2E is bewteen i to i+1 frame times
    if use_encoding:
        # RCNN Argoverse, H264, w/ tracking
        e2e_table = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                     22, 23, 24, 25, 26, 27, 28, 29, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]
        acc_table = [38.45, 36.14, 34.75, 33.12, 31.82, 30.50, 29.53, 26.99, 25.73, 25.21, 24.35,
                     22.44, 21.56, 21.64, 21.16, 20.35, 19.69, 18.95, 17.61, 17.85, 17.00, 16.55,
                     15.97, 15.16, 14.94, 15.37, 14.71, 13.77, 13.62, 13.70, 10.50, 8.95, 7.72,
                     5.66, 4.76, 4.20, 3.26, 1.20, 0.91]
    else:
        # RCNN Argoverse, RAW, w/ tracking
        e2e_table = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                     22, 23, 24, 25, 26, 27, 28, 29, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]
        acc_table = [38.45, 37.22, 36.04, 34.65, 33.36, 32.20, 31.08, 28.03, 27.01, 25.62, 25.77,
                     23.29, 22.75, 22.48, 21.59, 20.59, 20.11, 19.53, 18.40, 18.01, 17.52, 16.96,
                     16.59, 15.41, 15.78, 15.86, 14.81, 14.70, 14.44, 14.05, 10.64, 9.33, 7.89,
                     6.02, 5.31, 3.99, 3.12, 1.20, 0.91]

    e2e_arr = (df.recv - df.avail).to_numpy()
    frame_time_arr = e2e_arr / 33.333

    # Cap max frame time because quadratic interpolation is not always non-increasing
    frame_time = min(np.mean(frame_time_arr), e2e_table[-1])

    # Linear extrapolation
    map_val = max(np.interp(frame_time, e2e_table, acc_table), 0.0)

    return map_val


def collect_plotting_data():
    """
    """
    df = []
    for app in ['ar', 'cav']:
        for encoding in ['raw', 'h264']:
            fps = 30 if app == 'ar' else 10
            num_frames_total = (600 if app == 'ar' else 200)

            for operator in ['verizon', 'tmobile', 'atnt']:

                for df_app, df_xcal in get_app_xcal_df_pairs(operator, app, encoding):
                    is_driving = True

                    # Remove static runs by checking the diff between first and last GPS coord
                    lon_arr_this_run = df_xcal.Lon.dropna().to_numpy()
                    lat_arr_this_run = df_xcal.Lat.dropna().to_numpy()
                    if len(lon_arr_this_run) < 2:
                        print('Not sure whether static or driving, skip')
                        is_driving = False
                    else:
                        coord_arr = [[lat_arr_this_run[i], lon_arr_this_run[i]]
                                     for i in range(len(lat_arr_this_run))
                                     if not np.isnan(lat_arr_this_run[i])
                                     and not np.isnan(lon_arr_this_run[i])]
                    if is_driving and len(coord_arr) < 2:
                        print('skipped static due to nan')
                        is_driving = False
                    elif is_driving:
                        meter_per_second_arr = []
                        for i in range(len(coord_arr) - 1):
                            sampling_period = 0.5
                            meter_per_second_arr .append((geopy.distance.geodesic(
                                coord_arr[i], coord_arr[i + 1])).m / sampling_period)
                        meter_per_second = np.mean(meter_per_second_arr)
                        if meter_per_second < 5.0:
                            is_driving = False
                            print('skipped static due to low speed')

                    motion = 'driving' if is_driving else 'static'
                    offload_fps = fps * len(df_app) / num_frames_total
                    app_acc = lookup_accuracy(df_app, encoding == 'h264')
                    e2e = get_mean_e2e(df_app, fps, num_frames_total)
                    perc_5g = get_perc_5g(df_xcal)
                    num_ho = get_num_ho(df_xcal)
                    if operator == 'verizon' and is_wavelength(df_xcal):
                        server = 'edge'
                    else:
                        server = 'cloud'
                    xcal_tsp = df_xcal.TIME_STAMP.iloc[0]
                    df.append([app, encoding, operator, motion, e2e, offload_fps,
                              app_acc, server, perc_5g, num_ho, xcal_tsp])

    df = pd.DataFrame(df, columns=['app', 'encoding', 'operator', 'motion', 'e2e', 'offload_fps',
                                   'app_acc', 'server', 'perc_5g', 'num_ho', 'xcal_tsp'])
    return df


def plot_cdf_v4(df):
    """
    Plot app metric CDF of verizon. Put raw and h264 into same fig. 
    """
    operator = 'verizon'
    color = 'red'

    for app in ['ar', 'cav']:
        if app == 'ar':
            mosaic = """AABBCC"""
            fig = plt.figure(figsize=(7.5, 3), constrained_layout=True)
        else:
            mosaic = """AA"""
            fig = plt.figure(figsize=(3, 3), constrained_layout=True)
        ax_dict = fig.subplot_mosaic(mosaic)
        plt.subplots_adjust(wspace=0.04)

        for encoding in ['raw', 'h264']:
            if encoding == 'raw':
                label = 'w/o comp.'
                linestyle = 'solid'
            else:
                label = 'w/ comp.'
                linestyle = 'dotted'

            df_part = df[(df.app == app) & (df.encoding == encoding)
                         & (df.operator == operator) & (df.motion == 'driving')]

            # E2E CDF
            ax = ax_dict['A']
            x, y = get_cdf_data(df_part.e2e)
            ax.plot(x, y, label=label, c=color, linestyle=linestyle)
            ax.set_ylabel('CDF')

            if app == 'ar':
                # FPS CDF
                ax = ax_dict['B']
                x, y = get_cdf_data(df_part.offload_fps.to_numpy())
                ax.plot(x, y, c=color, linestyle=linestyle)

                # App acc CDF
                ax = ax_dict['C']
                x, y = get_cdf_data(df_part.app_acc.to_numpy())
                ax.plot(x, y, c=color, linestyle=linestyle)
                ax.set_xlim(0, 40)

            # Plot the best run
            df_part = df[(df.app == app) & (df.operator == operator)]
            if encoding == 'raw':
                ax_dict['A'].axvline(df_part.e2e.min(), color='k', linestyle='--')
            else:
                ax_dict['A'].axvline(df_part.e2e.min(), color='k', linestyle='--', label='Best Run')
            if app == 'ar':
                ax_dict['B'].axvline(df_part.offload_fps.max(), color='k', linestyle='--')
                ax_dict['C'].axvline(df_part.app_acc.max(), color='k', linestyle='--')

        ax_dict['A'].set_xlabel('E2E latency (ms)', fontsize=14)
        ax_dict['A'].legend(fontsize=12, loc='lower right')
        if app == 'ar':
            ax_dict['A'].set_xlim(0, 1999)
            ax_dict['B'].set_xlabel('Offloading FPS', fontsize=14)
            ax_dict['B'].set_xlim(0, 14)
            ax_dict['B'].set_yticklabels([])
            ax_dict['C'].set_xlabel('Accuracy (mAP)', fontsize=14)
            ax_dict['C'].set_xlim(0, 40)
            ax_dict['C'].set_yticklabels([])
        else:
            ax_dict['A'].set_xlim(0, 3999)

        save_path = f'v4_{app}.pdf'
        plt.savefig(save_path)


def plot_scatter_v2(df):
    operator = 'verizon'
    color = 'red'

    for app in ['ar', 'cav']:
        metric = 'app_acc' if app == 'ar' else 'e2e'

        for factor in ['perc_5g', 'num_ho']:

            fig, axs = plt.subplots(1, 2, figsize=(3.5, 3.5), constrained_layout=True)
            plt.subplots_adjust(wspace=0.02)

            for i, encoding in enumerate(['raw', 'h264']):
                ax = axs[i]

                df_part = df[(df.app == app) & (df.encoding == encoding)
                             & (df.operator == operator) & (df.motion == 'driving')]

                df_part.e2e /= 1000.0    # ms to s

                df_cloud = df_part[df_part.server == 'cloud']

                x = df_cloud[factor]
                if factor == 'perc_5g':
                    x *= 100    # Make 1.0 to 100 percent
                ax.scatter(x, df_cloud[metric], s=6, c=color, label='cloud')

                df_edge = df_part[df_part.server == 'edge']
                x = df_edge[factor]
                if factor == 'perc_5g':
                    x *= 100
                ax.scatter(x, df_edge[metric], marker='x', s=80, c=f'C5', label='edge')

                if encoding == 'raw':
                    ax.set_title('w/o comp.')
                    if app == 'ar':
                        ax.set_ylabel('mAP')
                    else:
                        ax.set_ylabel('E2E latency (s)')
                else:
                    ax.set_title('w/ comp.')
                    ax.set_yticklabels([])
                    if factor == 'num_ho':
                        ax.legend(fontsize='12')

                if factor == 'perc_5g':
                    ax.set_xlim(-18, 118)
                    # Pad spaces to push to the middle visually
                    fig.supxlabel('        % 5G mmWave/midband',
                                  fontname='Verdana', fontweight='bold', fontsize=14)
                else:
                    ax.set_xlim(-0.5, 5.5)
                    fig.supxlabel('        Number of HOs',
                                  fontname='Verdana', fontweight='bold', fontsize=14)

                if app == 'ar':
                    ax.set_ylim(0, 38)
                else:
                    ax.set_ylim(0, 18)

            save_path = f'scatter_v2_{app}_{factor}.pdf'
            plt.savefig(save_path)


def plot_cdf_v3(df):
    """
    Plot a row CDFs (3 for AR, 1 for CAV), one for each app metric that contains all operators.
    """
    for app in ['ar', 'cav']:
        for encoding in ['raw', 'h264']:

            if app == 'ar':
                mosaic = """AABBCC"""
                fig = plt.figure(figsize=(8.5, 3.5), constrained_layout=True)
            else:
                mosaic = """AA"""
                fig = plt.figure(figsize=(3.5, 3.5), constrained_layout=True)
            ax_dict = fig.subplot_mosaic(mosaic)
            plt.subplots_adjust(wspace=0.04)

            for idx_operator, operator in enumerate(['verizon', 'tmobile', 'atnt']):
                df_part = df[(df.app == app) & (df.encoding == encoding)
                             & (df.operator == operator) & (df.motion == 'driving')]
                # E2E CDF
                ax = ax_dict['A']
                x, y = get_cdf_data(df_part.e2e)
                ax.plot(x, y, label=operator_pretty_arr[idx_operator],
                        c=operator_color_arr[idx_operator])
                if idx_operator == 0:
                    ax.set_xlabel('E2E latency (ms)', fontsize=14)
                    if app == 'ar':
                        ax.set_xlim(0, 1999)
                    else:
                        ax.set_xlim(0, 3999)
                    ax.set_ylabel('CDF')

                if app == 'ar':
                    # FPS CDF
                    ax = ax_dict['B']
                    x, y = get_cdf_data(df_part.offload_fps.to_numpy())
                    ax.plot(x, y, c=operator_color_arr[idx_operator])
                    if idx_operator == 0:
                        ax.set_xlabel('Offloading FPS', fontsize=14)
                        ax.set_xlim(0, (14 if app == 'ar' else 5.5))
                        ax.set_yticklabels([])

                    # App acc CDF
                    ax = ax_dict['C']
                    x, y = get_cdf_data(df_part.app_acc.to_numpy())
                    ax.plot(x, y, c=operator_color_arr[idx_operator])
                    ax.set_xlim(0, 40)
                    if idx_operator == 0:
                        ax.set_xlabel('Accuracy (mAP)', fontsize=14)
                        ax.set_yticklabels([])

            # Plot best run
            df_part = df[(df.app == app) & (df.encoding == encoding)]
            ax_dict['A'].axvline(df_part.e2e.min(), color='k', linestyle='--', label='Best Run')
            if app == 'ar':
                ax_dict['B'].axvline(df_part.offload_fps.max(), color='k', linestyle='--')
                ax_dict['C'].axvline(df_part.app_acc.max(), color='k', linestyle='--')

            ax_dict['A'].legend(fontsize='12')

            save_path = f'v3_{app}_{encoding}.pdf'
            plt.savefig(save_path)


def plot_scatter(df):
    """
    Three scatter plots, one for each operator.
    """
    for app in ['ar', 'cav']:
        for encoding in ['raw', 'h264']:

            fig, axs = plt.subplots(1, 3, figsize=(4.5, 3.5), constrained_layout=True)
            plt.subplots_adjust(wspace=0.02)

            for idx_operator, operator in enumerate(['verizon', 'tmobile', 'atnt']):
                df_part = df[(df.app == app) & (df.encoding == encoding)
                             & (df.operator == operator) & (df.motion == 'driving')]

                # Scatter of app accuracy vs perc of 5G
                ax = axs[idx_operator]
                ax.set_title(operator_pretty_arr[idx_operator])

                if app == 'ar':
                    df_cloud = df_part[df_part.server == 'cloud']
                    ax.scatter(df_cloud.perc_5g, df_cloud.app_acc, s=6,
                               c=operator_color_arr[idx_operator], label='cloud')
                    if operator == 'verizon':
                        df_edge = df_part[df_part.server == 'edge']
                        ax.scatter(df_edge.perc_5g, df_edge.app_acc,
                                   marker='x', s=80, c=f'C5', label='edge')
                    ax.set_ylim(0, 40)
                    ax.set_xlim(-0.1, 1.1)
                    if idx_operator == 0:
                        ax.set_ylabel('Accuracy')
                else:
                    df_cloud = df_part[df_part.server == 'cloud']
                    ax.scatter(df_cloud.perc_5g, df_cloud.e2e / 1000.0, s=6,
                               c=operator_color_arr[idx_operator], label='cloud')
                    if operator == 'verizon':
                        df_edge = df_part[df_part.server == 'edge']
                        ax.scatter(df_edge.perc_5g, df_edge.e2e / 1000.0,
                                   marker='x', s=80, c=f'C5', label='edge')
                    ax.set_xlim(-0.1, 1.1)
                    if idx_operator == 0:
                        ax.set_ylabel('E2E latency (s)')
                    if encoding == 'raw':
                        ax.set_ylim(0, 18)
                    else:
                        ax.set_ylim(0, 2)
                if idx_operator == 0:
                    ax.legend(fontsize='12')
                if idx_operator == 1:
                    ax.set_xlabel('% times 5G mmWave / midband ', fontsize=14)
                if idx_operator > 0:
                    ax.set_yticklabels([])

            save_path = f'scatter_{app}_{encoding}.pdf'
            plt.savefig(save_path)


if __name__ == '__main__':
    # Cache preprocessed data
    if not Path('preprocessed-data-cache.csv').exists():
        df = collect_plotting_data()
        df.to_csv('preprocessed-data-cache.csv', index=False)
    else:
        df = pd.read_csv('preprocessed-data-cache.csv')

    plot_cdf_v4(df)
    Path('v4_ar.pdf').rename('fig-12a.pdf')
    Path('v4_cav.pdf').rename('fig-13a.pdf')

    plot_scatter_v2(df)
    Path('scatter_v2_ar_perc_5g.pdf').rename('fig-12b.pdf')
    Path('scatter_v2_ar_num_ho.pdf').rename('fig-12c.pdf')
    Path('scatter_v2_cav_perc_5g.pdf').rename('fig-13b.pdf')
    Path('scatter_v2_cav_num_ho.pdf').rename('fig-13c.pdf')

    plot_cdf_v3(df)
    Path('v3_ar_raw.pdf').rename('fig-17a.pdf')
    Path('v3_ar_h264.pdf').rename('fig-18a.pdf')
    Path('v3_cav_raw.pdf').rename('fig-19a.pdf')
    Path('v3_cav_h264.pdf').rename('fig-19c.pdf')

    plot_scatter(df)
    Path('scatter_ar_raw.pdf').rename('fig-17b.pdf')
    Path('scatter_ar_h264.pdf').rename('fig-18b.pdf')
    Path('scatter_cav_raw.pdf').rename('fig-19b.pdf')
    Path('scatter_cav_h264.pdf').rename('fig-18d.pdf')
