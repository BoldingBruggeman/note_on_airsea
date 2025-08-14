import netCDF4
import numpy as np
import sys

nc_file = sys.argv[1]
nc = netCDF4.Dataset(nc_file, "r")

# Load variables
time_var = nc.variables["valid_time"]
var = nc.variables[sys.argv[2][:]]  # Replace with your variable name

# Convert time to datetime objects
time_units = time_var.units
time_calendar = getattr(time_var, "calendar", "standard")
times = netCDF4.num2date(time_var[:], units=time_units, calendar=time_calendar)

for t_idx, t in enumerate(times):
    value = var[t_idx, 0, 0]
    sys.stdout.write(f"{t}   {value / 3600.0:7.1f}\n")

nc.close()
