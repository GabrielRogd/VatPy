# VatPy - A Python-based VATSIM Tool

This **VatPy** project aims to provide various functionalities to interact with VATSIM online data using Python.

No API key is required to use any script.

## Scripts

The project currently consists of the following Python scripts:

- `servers.py`: A script to fetch server data from VATSIM's API, ping each server (excluding 'SweatBox' servers), and
  find the best suitable server based on the ping time.

- `metar.py`: A script to fetch raw METAR data from VATSIM's METAR source (metar.vatsim.net/{ICAO}) and has the ability
  to decode it in a more understandable manner (it still needs some work).

## Installation

Please ensure to have Python installed (tested on 3.12). Besides, the following Python libraries are required:

- requests
- ping3
- operator

You can install these using pip. Or by loading the `dependencies.txt` file by typing `pip install -r dependencies.txt`
in terminal.