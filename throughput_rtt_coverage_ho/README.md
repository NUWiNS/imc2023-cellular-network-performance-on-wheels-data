# Coverage - Throughput & RTT tests - Handovers

## Dataset Structure

This sub-dataset is divided into 4 sections:

* Coverage ([`coverage`](./coverage))
* Throughput Data ([`tput`](./tput))
* RTT Data ([`rtt`](./rtt))
* Handover Data ([`ho`](./ho))

The respective raw data (application + XCAL) are in the aforementioned directories. Additionally, there are processed data under each subdirectory with a subfolder named "processed".

The [`scripts`](./scripts) folder contains scripts starting with `imc_dataset_*_process.py` to generate the processed data. Scripts starting with `plot_*_.py` generates figures 1 to 12 in the IMC paper.  

> Note: The dataset already contains processed data to generate the plots used in the IMC paper, and processing scripts are provided as a starting point for users to extract various KPIs (used in the paper) according to their specific requirements

## Using the processed data

In each sub-folder (coverage/tput/rtt/ho) there is a folder called `processed`. The following explains how to use those processed data:

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
  | `total_dist_operator` | Operator-wise total distance travelled in miles | <pre>{<br />   "operator1":"x",<br />   "operator2":"y",<br />   ...<br />}<br /></pre> |
  | `breakup_dist_operator` | Operator-wise and technology-wise breakdown <br/>- of distance travelled in miles| <pre>{<br />  "operator1":{<br />    "tech1":x1,<br />    "tech2":x2,<br />    "…"<br />  },<br />  "…"<br />}<br /></pre> |
  | `total_dist_tz_operator` | Operator-wise total distance travelled <br/>- per timezone in miles | <pre>{<br />  "operator1":{<br />    "tz1":x1,<br />    "tz2":x2,<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `breakup_dist_tz_operator` | Operator-wise and technology-wise breakdown <br/>- of distance travelled per timezone in miles | <pre>{<br />  "operator1":{<br />    "tech1":{<br />      "tz1":x11,<br />      "tz2":x12,<br />      ...<br />    },<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `total_dist_speed_operator` | Operator-wise total distance travelled <br/>- per speed range in miles | <pre>{<br />  "operator1":{<br />    "speed-range1":x1,<br />    "speed-range2":x2,<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `breakup_dist_speed_operator` | Operator-wise and technology-wise breakdown <br/>- of distance travelled per speed range in miles | <pre>{<br />  "operator1":{<br />    "tech1":{<br />      "speed-range1":x11,<br />      "speed-range2":x12,<br />      ...<br />    },<br />    ...<br />  },<br />  ...<br />}<br /></pre> |

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
  | `tput_speed_tech_dict` | <pre>{<br />  "tech1":{<br />    "speed1":[<br />      "throughput values"<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `ca_speed_tech_dict` | <pre>{<br />  "tech1":{<br />    "speed1":[<br />      "total ca values"<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `fiveg_ca_speed_dict` | <pre>{<br />  "tech1":{<br />    "speed1":[<br />      5g ca values<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre>  |
  | `lte_ca_speed_dict` | <pre>{<br />  "tech1":{<br />    "speed1":[<br />      "lte ca values"<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `tput_tz_tech_dict` | <pre>{<br />  "tz1":[<br />    "throughput values"<br />  ],<br />  "tz2":[<br />    "throughput values"<br />  ],<br />  ...<br />}<br /></pre> |
  | `dist_speed_tech_dict` | `x` |
  | `mcs_speed_dict` | <pre>{<br />  "tech1":{<br />    "speed1":[<br />      "mcs values"<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `bler_speed_dict` | <pre>{<br />  "tech1":{<br />    "speed1":[<br />      "bler values"<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `rsrp_speed_dict` | <pre>{<br />  "tech1":{<br />    "speed1":[<br />      "rsrp values"<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `wl_speed_dict` | <pre>{<br />  "tech1":{<br />    "speed1":[<br />      "edge used or not values"<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
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
  | `main_op_link_ho_per_mile_dict` | <pre>{<br />  "operator1":{<br />    "linkype1":[<br />      [<br />        "list of latitude longitude pairs"<br />      ],<br />      [<br />        "handover count list"<br />      ],<br />      [<br />        "distance travelled list"<br />      ],<br />      [<br />        "handovers per mile list"<br />      ]<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `main_op_link_ho_duration_dict` | <pre>{<br />  "operator1":{<br />    "linktype1":[<br />      "list of handover duration"<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `main_op_link_ho_tput_dict` | <pre>{<br />  "operator1":{<br />    "linktype1":[<br />      {<br />        "dictionary of different handovers with pre-handover throughput list"<br />      },<br />      {<br />        "dictionary of different handovers with post-ho throughput list"<br />      },<br />      {<br />        "list of post - pre handover throughput values"<br />      },<br />      [<br />        list of t1,<br />        t2,<br />        t3,<br />        t4,<br />        t5 from the paper<br />      ]<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre>  |
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
  | `main_op_rtt_dict` | <pre>{<br />  "operator1":[<br />    [<br />      "latitude",<br />      "longitude",<br />      [<br />        "list of rtt values"<br />      ],<br />      "path_to_rtt_file"<br />    ]<br />  ],<br />  ...<br />}<br /></pre> |
  | `main_rtt_5g_dict` | <pre>{<br />  "operator1":{<br />    "percent-high-5g":[<br />      "list of rtt values"<br />    ]<br />  }<br />}<br /></pre> |
  | `main_rtt_tech_dict` | <pre>{<br />  "operator1":{<br />    "tech1":[<br />      "list of rtt values"<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre>  |
  | `main_rtt_edge_tech_dict` | <pre>{<br />  "operator1":{<br />    "tech1":[<br />      "list indicating whether an rtt values was from a edge/cloud server test"<br />    ],<br />    ...<br />  },<br />  ...<br />}<br /></pre> |
  | `op_rtt_dict` | <pre>{<br />  "operator1":[<br />    list of each 200 ms rtt samples<br />  ],<br />  ...<br />}:<br /></pre>  |
  | `op_speed_dict` | <pre>{<br />  "operator1":[<br />    "list of speed in miles for each rtt sample"<br />  ],<br />  ...<br />}<br /></pre> |
  | `op_tech_dict` | <pre>{<br />  "operator1":[<br />    "list of cellular technology for each rtt sample"<br />  ],<br />  ...<br />}<br /></pre>  |
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

  
