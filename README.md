# Using Tinybird to see Soil Moisture from Space

by Alison Davey

## Hackathon

This project is for the ["To Infinity and beyond"](https://www.tinybird.co/events/tinybird-hackathon) Tinybird's first hackathon.

The theme is **space**. We use satellite data measuring soil moisture across the globe.

## The App

The satellite data in Tinybird powers the [HEX](https://app.hex.tech/138d7e08-1b21-474f-a78c-baee6d4bfc2a/app/8b9f85a8-3841-4162-9471-ede3ae685576/latest) app showing soil moisture.

![Data Flow](images/global_5_days.png)

## The Data

NASA's Soil Moisture Active Passive (SMAP) satellite uses two microwave instruments to monitor the top 2 inches (5 centimeters) of soil on Earth's surface. Together, the instruments create soil moisture estimates with a resolution of about 6 miles (9 kilometers), mapping the entire globe every two or three days.

NASA's [SMAP viewer](https://smap.jpl.nasa.gov/map/) is not currently working, so let's build our own.

The Level-3 (L3) soil moisture data is a composite of daily estimates of global land surface conditions. SMAP L-band soil moisture data are resampled to a global, cylindrical 36 km Equal-Area Scalable Earth Grid (406 rows x 964 columns). 

#### Citation

O'Neill, P. E., S. Chan, E. G. Njoku, T. Jackson, R. Bindlish, and J. Chaubell. (2021). SMAP L3 Radiometer Global Daily 36 km EASE-Grid Soil Moisture, Version 8 [Data Set]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. https://doi.org/10.5067/OMHVSRGFX38O. Date Accessed 10-23-2022.

The NASA National Snow and Ice Data Center Distributed Active Archive Center (NSIDC DAAC) distributes cryosphere and related geophysical data from NASA Earth-observing satellite missions, airborne campaigns, and field observations. 

## Create a Tinybird account

Go to [Tinybird](https://www.tinybird.co/) and create a free account, if don't already have one already. You can create a new workspace or use an existing one.

## Project setup

* `workspace` directory:

This is the Tinybird's project. It contains the Pipe and Data Source needed to build the project.

* `scripts` directory:

- python script to download the data and send it to Tinybird. You will need to set up an [Earthdata login](https://urs.earthdata.nasa.gov/oauth/authorize) to have your {uid} and {password}. Use the Tinybird {token} from your workspace.
- python script showing the plot commands used in the HEX app

## Initialize project

1. Create a virtual environment

```sh
virtualenv -p python3.8 .e
```

2. Authenticate using the Tinybird's CLI

```sh
pip install tinybird-cli
```

```sh
cd workspace
```

```sh
tb auth --token $TOKEN
```

3. Push project to workspace

```sh
tb push
```

![Data Flow](images/dataflow.png)

## Push soil moisture data

Download, preprocess and push the data to Tinybird using the script `script/soil_moisture_data_to_tinybird.py`

## Sources

* [Elena Torro's entry](https://github.com/elenatorro/asteroids-k-means-clustering) for the readme and project structure
* [NASA's SMAP Documentation](https://nsidc.org/data/spl3smp/versions/8)