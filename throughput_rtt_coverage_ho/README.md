# Coverage - Throughput & RTT tests - Handovers

## Dataset Structure

This sub-dataset is divided into 4 sections:
    * Coverage ([`coverage`](./coverage))
    * Throughput Data ([`tput`](./tput))
    * RTT Data ([`rtt`](./rtt))
    * Handover Data ([`ho`](./ho))

The respective raw data (application + XCAL) are in the aforementioned directories. Additionally, there are processed data under each subdirectory with a subfolder named "processed".

[`scripts`](./scripts) folder contains scripts starting with "imc_dataset_*_process.py" to generate the processed data. Scripts starting with "plot_*.py" generates figures 1 to 13 in the IMC paper.  
Note: The dataset already contains processed data to generate the plots used in the IMC paper, and processing scripts are provided as a starting point for users to extract various KPIs (used in the paper) according to their specific requirements

## Steps to Reproduce IMC Paper Plots

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

  
