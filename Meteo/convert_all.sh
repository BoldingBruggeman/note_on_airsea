#!/bin/bash

python nc2ascii.py ssr_2020_2021.nc ssr >ssr.dat
python nc2ascii.py ssr_2022_2023.nc ssr >>ssr.dat

python nc2ascii.py str_2020_2021.nc str >str.dat
python nc2ascii.py str_2022_2023.nc str >>str.dat

python nc2ascii.py strd_2020.nc strd >strd.dat
python nc2ascii.py strd_2021_2022.nc strd >>strd.dat
python nc2ascii.py strd_2023.nc strd >>strd.dat
