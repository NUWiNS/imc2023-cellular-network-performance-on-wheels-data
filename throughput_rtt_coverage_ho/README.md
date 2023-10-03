# Coverage - Throughput & RTT tests - Handovers

## Dataset Structure

This sub-dataset is divided into 4 sections:

* Coverage ([`coverage`](./coverage))
* Throughput Data ([`tput`](./tput))
* RTT Data ([`rtt`](./rtt))
* Handover Data ([`ho`](./ho))

The respective raw data (application + XCAL) are in the aforementioned directories. Additionally, there are processed data under each subdirectory with a subfolder named "processed".

[`scripts`](./scripts) folder contains scripts starting with "imc_dataset_`*`_process.py" to generate the processed data. Scripts starting with "plot_`*`_.py" generates figures 1 to 12 in the IMC paper.  

Note: The dataset already contains processed data to generate the plots used in the IMC paper, and processing scripts are provided as a starting point for users to extract various KPIs (used in the paper) according to their specific requirements

## Using the processed data

In each sub-folder (coverage/tput/rtt/ho) there is a folder called "processed". The following explains how to use those processed data:

* Coverage:
  ```bash
  # Filename: dist_tz_speed_operator.pkl
  import pickle
  filehandler = open("dist_tz_speed_operator.pkl", "rb")
  total_dist_operator, breakup_dist_operator, total_dist_tz_operator, breakup_dist_tz_operator, total_dist_speed_operator, breakup_dist_speed_operator = pickle.load(filehandler)
  filehandler.close()
  ```
  Variable information and structure:
  | Variable | Description | Structure |
  | :-- | :---- | :----- |
  | `total_dist_operator` | Operator-wise total distance travelled in miles | `{operator1 : x, operator2 : y, ...}` |
  | `breakup_dist_operator` | Operator-wise and technology-wise breakdown <br/>- of distance travelled in miles| `{operator1 : {tech1 : x1, tech2: x2, ..}, operator2 : {tech1 : y1, tech2: y2, ..},...}` |
  | `total_dist_tz_operator` | Operator-wise total distance travelled <br/>- per timezone in miles | `{operator1 : {tz1 : x1, tz2 : x2, ...}, operator2 : {tz1 : y1, tz2 : y2, ...}}` |
  | `breakup_dist_tz_operator` | Operator-wise and technology-wise breakdown <br/>- of distance travelled per timezone in miles | `{operator1 : {tech1: {tz1 : x11, tz2 : x12, ...}, tech2: {tz1 : x21, tz2 : x22, ...}}, <br/>- operator2 : {tech1 : {tz1 : y11, tz2 : y12, ...}, tech2 : {tz1 : y21, tz2 : y22, ...}}}` |
  | `total_dist_speed_operator` | Operator-wise total distance travelled <br/>- per speed range in miles | `{operator1 : {speed-range1 : x1, speed-range2 : x2, ...}, <br/>- operator2 : {speed-range1 : y1, speed-range2 : y2, ...}` |
  | `breakup_dist_speed_operator` | Operator-wise and technology-wise breakdown <br/>- of distance travelled per speed range in miles | `{operator1 : {tech1 : {speed-range1 : x11, speed-range2 : x12, ...}, tech2 : {speed-range1 : x21, speed-range2 : x22, ...}}, <br/>- operator2 : {tech1 : {speed-range1 : y11, speed-range2 : y12, ...}, tech2 : {speed-range1 : y21, speed-range2 : y22, ...}}` |

* Throughput data:
  
  The `main_op_link_dict.pkl` has a dict which contains data in the following format:
  ```bash
  ├── operator
      ├── downlink or uplink
          ├── tput_speed_tech_dict
          ├── ca_speed_tech_dict
          ├── fiveg_ca_speed_dict
          ├── lte_ca_speed_dict
          ├── tput_tz_tech_dict
          ├── dist_speed_tech_dict
          ├── mcs_speed_dict
          ├── bler_speed_dict
          ├── rsrp_speed_dict
          ├── wl_speed_dict
          ├── overall_mean_list
          ├── overall_std_list
          ├── overall_5g_high_percent
  ```
  ```bash
  # Filename: main_op_link_dict.pkl
  import pickle
  filehandler = open("main_op_link_dict.pkl", "rb")
  main_op_link_tput_dict = pickle.load(filehandler)
  for op in main_op_link_tput_dict.keys():
     for link in ['dl', 'ul']: 
        tput_speed_tech_dict, ca_speed_tech_dict, fiveg_ca_speed_dict, lte_ca_speed_dict, tput_tz_tech_dict, dist_speed_tech_dict, mcs_speed_dict, bler_speed_dict, rsrp_speed_dict, wl_speed_dict, overall_mean_list, overall_std_list, overall_5g_high_percent = main_op_link_tput_dict[op][link]
  filehandler.close()
  ```
  Variable information and structure:
  | Variable | Structure |
  | :-- | :----- |
  | `tput_speed_tech_dict` | `{tech1 : {speed1 : [throughput values], speed2 : [throughput values]}, tech2 : {speed1 : [throughput values], speed2 : [throughput values]}}, ...}` |
  | `ca_speed_tech_dict` | `{tech1 : {speed1 : [total ca values], speed2 : [total ca values]}, tech2 : {speed1 : [total ca values], speed2 : [total ca values]}}, ...}` |
  | `fiveg_ca_speed_dict` | `{tech1 : {speed1 : [5g ca values], speed2 : [5g ca values]}, tech2 : {speed1 : [5g ca values], speed2 : [5g ca values]}}, ...}`  |
  | `lte_ca_speed_dict` | `{tech1 : {speed1 : [lte ca values], speed2 : [lte ca values]}, tech2 : {speed1 : [lte ca values], speed2 : [lte ca values]}}, ...}` |
  | `tput_tz_tech_dict` | `{tz1 : [throughput values], tz2 : [throughput values], ...}` |
  | `dist_speed_tech_dict` | `x` |
  | `mcs_speed_dict` | `{tech1 : {speed1 : [mcs values], speed2 : [mcs values]}, tech2 : {speed1 : [mcs values], speed2 : [mcs values]}}, ...}` |
  | `bler_speed_dict` | `{tech1 : {speed1 : [bler values], speed2 : [bler values]}, tech2 : {speed1 : [bler values], speed2 : [bler values]}}, ...}` |
  | `rsrp_speed_dict` | `{tech1 : {speed1 : [rsrp values], speed2 : [rsrp values]}, tech2 : {speed1 : [rsrp values], speed2 : [rsrp values]}}, ...}` |
  | `wl_speed_dict` | `{tech1 : {speed1 : [edge used or not values], speed2 : [edge used or not values]}, tech2 : {speed1 : [edge used or not values], speed2 : [edge used or not values]}}, ...}` |
  | `overall_mean_list` | `[average of each 30-35 seconds throughput test]` |
  | `overall_std_list` | `[standard deviation of each 30-35 seconds throughput test]` |
  | `overall_5g_high_percent` | `[% of 5G mid/mmWave in each 30-35 seconds throughput test]` |
  ```

* Handovers:
  
  There are 3 pickle files which contains data in the following format:
  ```bash
  ├── main_op_link_ho_per_mile_dict
      ├── operator
          ├── downlink/uplink
              ├── data structure
  ├── main_op_link_ho_duration_dict
      ├── operator
          ├── downlink/uplink
              ├── data structure
  ├── main_op_link_ho_tput_dict
      ├── operator
          ├── downlink/uplink
              ├── data structure
  ```
  ```bash
  # Filenames: main_op_link_ho_per_mile_dict.pkl, main_op_link_ho_duration_dict.pkl, main_op_link_ho_tput_dict.pkl
  import pickle
  filehandler = open("main_op_link_ho_per_mile_dict.pkl", "rb")
  main_op_link_ho_per_mile_dict = pickle.load(filehandler)
  filehandler.close()
  filehandler = open("main_op_link_ho_duration_dict.pkl", "rb")
  main_op_link_ho_duration_dict = pickle.load(filehandler)
  filehandler.close()
  filehandler = open("main_op_link_ho_tput_dict.pkl", "rb")
  main_op_link_ho_tput_dict = pickle.load(filehandler)
  filehandler.close()
  ```
  Variable information and structure:
  | Variable | Structure |
  | :-- | :----- |
  | `main_op_link_ho_per_mile_dict` | `{operator1 : {linkype1 : [[list of latitude longitude pairs], [handover count list], [distance travelled list], [handovers per mile list]], ...}, ...}` |
  | `main_op_link_ho_duration_dict` | `{operator1 : {linktype1 : [list of handover duration], ...}, ...}` |
  | `main_op_link_ho_tput_dict` | `{operator1 : {linktype1: [{dictionary of different handovers with pre-handover throughput list}, {dictionary of different handovers with post-ho throughput list}, {list of post - pre handover throughput values}, [list of t1, t2, t3, t4, t5 from the paper]], ...}, ...}`  |
  ```

* RTT:
  
  The `main_op_link_dict.pkl` has a dict which contains data in the following format:
  ```bash
  ├── main_op_rtt_dict
      ├── operator
          ├── data structure
  ├── main_rtt_5g_dict
      ├── operator
        ├── data structure
  ├── main_rtt_tech_dict
      ├── operator
            ├── data structure
  ├── main_rtt_edge_tech_dict
      ├── operator
        ├── data structure
  ├── op_speed_dict
      ├── operator
        ├── data structure
  ├── op_rtt_dict
      ├── operator
        ├── data structure
  ├── op_tech_dict
      ├── operator
        ├── data structure
  ```
  ```bash
  # Filename: main_op_link_dict.pkl
  import pickle
  filehandler = open("main_op_link_dict.pkl", "rb")
  main_op_link_rtt_dict = pickle.load(filehandler)
  main_op_rtt_dict, main_rtt_5g_dict, main_rtt_tech_dict, main_rtt_edge_tech_dict, op_speed_dict, op_rtt_dict, op_tech_dict = main_op_link_rtt_dict
  filehandler.close()
  ```
  Variable information and structure:
  | Variable | Structure |
  | :-- | :----- |
  | `main_op_rtt_dict` | `{operator1 : [[latitude, longitude, [list of rtt values], path_to_rtt_file]], ...}` |
  | `main_rtt_5g_dict` | `{operator1 : {percent-high-5g : [list of rtt values]}}, ...}` |
  | `main_rtt_tech_dict` | `{operator1 : {tech1 : [list of rtt values], ...}, ...}`  |
  | `main_rtt_edge_tech_dict` | `{operator1 : {tech1 : [list indicating whether an rtt values was from a edge/cloud server test], ...}, ...}` |
  | `op_rtt_dict` | `{operator1: [list of each 200 ms rtt samples], ...}`  |
  | `op_speed_dict` | `{operator1: [list of speed in miles for each rtt sample], ...}` |
  | `op_tech_dict` | `{operator1: [list of cellular technology for each rtt sample], ...}`  |
  ```

## Steps to Reproduce IMC Paper Plots (Use a Windows system to generate the plots)

1. Install dependencies with pip:
    ```bash
    python3 -m pip install -r requirements.txt
    ```

2. Run the plotting script

    ```bash
    python3 scripts\plot_coverage.py
    python3 scripts\plot_tput_rtt.py
    python3 scripts\plot_parallel_throughput_tech.py
    python3 scripts\plot_ho.py
    ```

3. Examine the resulting figures. You are supposed to see the following figures
   being plotted, with filenames matching the figure IDs in the paper:

    ```bash
    plots/
    ├── fig_1
        ├── fig_1*.pdf
    ├── fig_2
        ├── fig_2*.pdf
    ├── fig_3a.pdf
    ├── fig_3b.pdf
    ├── fig_4.pdf
    ├── fig_5.pdf
    ├── fig_6a.pdf
    ├── fig_6b.pdf
    ├── fig_6c.pdf
    ├── fig_6d.pdf
    ├── fig_7
        ├── *.pdf
    ├── fig_8.pdf
    ├── fig_9.pdf
    ├── fig_10dl.pdf
    ├── fig_10ul.pdf
    ├── fig_10c.pdf
    ├── fig_11a.pdf
    ├── fig_11b.pdf
    └── fig_12
        ├── *.pdf
    ```

  
