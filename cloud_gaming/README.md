# Cloud gaming 

## Dataset structure For the cloud gaming experiments, we used Steam Remote
Play, the game is hosted on an AWS Windows cloud server. The game client is
installed on Android devices.  The dataset includes two directories,
[`xcal_log_files`](./xcal_log_files) and [`app_log_files`](.\app_log_files).
With each of these [directories](directories), there are three subdirectories,
named according to the operator and containing the game logs/xcal logs. For each
of the game logs in [`app_log_files`](.\app_log_files) in , there is a
corresponding xcal logs [`xcal_log_files`](./xcal_log_files). You can use the
function get_app_info_per_operator(<operator>) to generate the information about
that operator in a file named '<operator>_all.csv', including the pairing of the
files and the plotted metrics. For instance,
get_app_info_per_operator('tmobile') will generate tmobile_all.csv with the
necessary metrics for T-mobile operators. Then, you can run all the necessary
function as commented in the scripts.

## App Log Format
The application event logs for cloud gaming do not come automatically in csv
format to be imports as pandas dataframe. Therefore, a preprocessing step was
performed to generate three corresponding csv files for each *.log file. This
step can reproduced using the three following functions in the [`main
script`](./parse_and_plot.py)
```python
# Obtain all bit rate related statistics from event logs
get_bitrate_info_all(log_files, do_print=False, overwrite=False)
# Obtain all bit rate related statistics from event logs
get_timing_info_all(log_files, do_print=False, overwrite=False)
# Obtain all dropped frame related statistics from event logs
get_dropped_frame_info_all(log_files, do_print=False, overwrite=False)
```
After preprocessing steps, the following metrics of interest are used in the
paper:
| Column Name             | Meaning                            | Unit         |
|-------------------------|------------------------------------|--------------|
| `bitrate`               | Application average bit rate       | Kbps         |
| `network`               | Network average end-to-end latency | milliseconds |
| `Frame drop percentage` | Average frame drop percentage      | percent      |

