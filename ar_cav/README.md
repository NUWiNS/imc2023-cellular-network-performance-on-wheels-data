# Augmented Reality (AR) & Connected Autonomous Vehicle (CAV)

## Dataset Structure

For the AR and CAV experiments, we configure each apps to send un-compressed or
h264-compressed frames respectively, for each of the three operators. This
resulted in 12 configuration combinations, each placed in a sub-folder named:
`<APP>-<ENCODING>-<OPERATOR>`.

* For example, [`ar-h264-atnt`](./ar-h264-atnt) contains the logs for the AR
  app offloading compressed frames over the AT\&T network.

Under each folder, each experiment is 0-index-numbered and corresponds to a
pair of csv files: 

* `app-<idx>.csv`: the application log
* `xcal-<idx>.csv`: the xcal-log

The events in two files above can be associated by the timestamp. All
timestamps are logged in UTC.


## App Log Format

The AR & CAV apps log each frame that have being offloaded. Each offloaded
frame corresponds to a row in the application log csv, having the following
columns:

| Column Name | Meaning | Unit |
| :--- | :--- | :--- |
| `idx` | The 0-indexed frame index that was being offloaded <br/>- May be non-continuous as only a subset of frames are offloaded | - | 
| `size` | The size of the offloaded frame | Bytes |
| `avail` | The time when the frame was captured on the phone | Epoch time (milliseconds) |
| `enc_fin` | The time when the app finishes compressing the frame <br/>- Equals to `avail` if compression is disabled | Epoch time (milliseconds) |
| `offload` | The time when the app starts to transfer the frame to the server | Epoch time (milliseconds) |
| `inf` | The inference duration on the edge server | Milliseconds |
| `recv` | The time when the app receives the result of the offloaded frame | Epoch time (milliseconds) |

## Steps to Reproduce

1. Install dependencies with pip:
    ```bash
    pip3 install numpy, pandas, geopy, matplotlib
    ```

    or with anaconda / miniconda:
    ```bash
    conda create -n ar_cav numpy pandas geopy matplotlib -c conda-forge -y
    conda activate ar_cav
    ```

2. Run the plotting script

    ```bash
    python plot.py
    ```

3. Examine the resulting figures. You are supposed to see the following figures
   being plotted, with filenames matching the figure IDs in the paper:

    ```bash
    ar_cav/
    ├── fig-12a.pdf
    ├── fig-12b.pdf
    ├── fig-12c.pdf
    ├── fig-13a.pdf
    ├── fig-13b.pdf
    ├── fig-13c.pdf
    ├── fig-17a.pdf
    ├── fig-17b.pdf
    ├── fig-18a.pdf
    ├── fig-18b.pdf
    ├── fig-18d.pdf
    ├── fig-19a.pdf
    ├── fig-19b.pdf
    └── fig-19c.pdf
    ```
