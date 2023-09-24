#360 degree Video Streaming

## Dataset Structure

For the video streaming experiments, we configure each apps to stream videos hosted at the remote cloud/edge server, for each of the three operators. For each operator
we have a pair of files from the application side and xcal side. For ease of use for the reader these files are aggregated, matched and put into one single files for each operator in
[plot](./plot) folder.

## App Log Format

Each application data file have the following
columns of interest:

| Column Name | Meaning | Unit |
| :--- | :--- | :--- |
| `unixtimestamp` | The application recorded timestamp that we use to match with xcal files | - | 
| `qoe` | Quality of exprience calculated for the current chunk | - |
| `cumRebuffer` | The cumulative rebuffering time till the last chunk | Epoch time (seconds) |
| `New_Bitrate` | Bitrate of the current chunk fetched from the server | Mbps |
| `byteLength` | Amount of bytes downloaded from the server since last chunk | bytes |
| `format_vid` | Current Video Resolution | - |

## Steps to Reproduce

1. Install dependencies with pip:
    ```bash
    pip3 install numpy, pandas, geopy, matplotlib

2. Run the plotting script

    ```bash
    python plot_video.py
    ```
3. Examine figure 15A, 15B, 21A, 21B 
    
