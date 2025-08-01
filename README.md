# meteorology-conversion

[![CI](https://github.com/JPL-Evapotranspiration-Algorithms/meteorology-conversion/actions/workflows/ci.yml/badge.svg)](https://github.com/JPL-Evapotranspiration-Algorithms/meteorology-conversion/actions/workflows/ci.yml)

The `meteorology-conversion` Python package provides robust utilities for meteorological and atmospheric science calculations, including temperature conversions, humidity, air density, and pressure estimations.

[Gregory H. Halverson](https://github.com/gregory-halverson-jpl) (they/them)<br>
[gregory.h.halverson@jpl.nasa.gov](mailto:gregory.h.halverson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329G

## Installation

This package is available on PyPI as `meteorology-conversion`.

```bash
pip install meteorology-conversion
```

## Usage

Import this package as `meteorology_conversion`:

```python
import meteorology_conversion
```

### 1. `kelvin_to_celsius(T_K)`
- **Description:** Converts temperature from Kelvin (K) to Celsius (°C).
- **Parameters:** `T_K` (numpy array or Raster): Temperature in Kelvin.
- **Returns:** Temperature in Celsius.
- **Reference:** Wallace, J. M., & Hobbs, P. V. (2006). Atmospheric Science: An Introductory Survey (2nd ed.). Academic Press.

### 2. `celcius_to_kelvin(T_C)`
- **Description:** Converts temperature from Celsius (°C) to Kelvin (K).
- **Parameters:** `T_C` (numpy array or Raster): Temperature in Celsius.
- **Returns:** Temperature in Kelvin.
- **Reference:** Wallace, J. M., & Hobbs, P. V. (2006).

### 3. `calculate_specific_humidity(Ea_Pa, Ps_Pa)`
- **Description:** Calculates the specific humidity (kg water vapor / kg moist air) from actual vapor pressure and surface pressure.
- **Parameters:**
	- `Ea_Pa` (numpy array or Raster): Actual water vapor pressure in Pascal.
	- `Ps_Pa` (numpy array or Raster): Surface pressure in Pascal.
- **Returns:** Specific humidity (kg/kg).
- **References:**
	- Rogers, R. R., & Yau, M. K. (1989). A Short Course in Cloud Physics (3rd ed.). Pergamon Press.
	- Stull, R. B. (2017). Practical Meteorology.

### 4. `calculate_specific_heat(specific_humidity)`
- **Description:** Calculates the specific heat capacity at constant pressure (Cp) for moist air.
- **Parameters:** `specific_humidity` (numpy array or Raster): Specific humidity (kg/kg).
- **Returns:** Specific heat capacity (J/kg/K).
- **References:**
	- Wallace, J. M., & Hobbs, P. V. (2006).
	- Stull, R. B. (2017).

### 5. `calculate_air_density(surface_pressure_Pa, Ta_K, specific_humidity)`
- **Description:** Calculates the density of moist air (kg/m³) using the ideal gas law, accounting for water vapor.
- **Parameters:**
	- `surface_pressure_Pa` (numpy array or Raster): Surface pressure in Pascal.
	- `Ta_K` (numpy array or Raster): Air temperature in Kelvin.
	- `specific_humidity` (numpy array or Raster): Specific humidity (kg/kg).
- **Returns:** Air density (kg/m³).
- **References:**
	- Wallace, J. M., & Hobbs, P. V. (2006).
	- Stull, R. B. (2017).

### 6. `SVP_kPa_from_Ta_C(Ta_C)`
- **Description:** Calculates the saturation vapor pressure (SVP) in kPa from air temperature in Celsius using the Magnus-Tetens approximation.
- **Parameters:** `Ta_C` (numpy array or Raster): Air temperature in Celsius.
- **Returns:** Saturation vapor pressure in kPa.
- **References:**
	- Alduchov, O. A., & Eskridge, R. E. (1996). Improved Magnus Form Approximation of Saturation Vapor Pressure. Journal of Applied Meteorology, 35(4), 601–609.
	- Bolton, D. (1980). The computation of equivalent potential temperature. Monthly Weather Review, 108(7), 1046–1053.

### 7. `SVP_Pa_from_Ta_C(Ta_C)`
- **Description:** Calculates the saturation vapor pressure in Pascal (Pa) from air temperature in Celsius.
- **Parameters:** `Ta_C` (numpy array or Raster): Air temperature in Celsius.
- **Returns:** Saturation vapor pressure in Pascal (Pa).
- **Reference:** Alduchov & Eskridge (1996).

### 8. `calculate_surface_pressure(elevation_m, Ta_C)`
- **Description:** Estimates surface pressure (Pa) at a given elevation and temperature using the barometric formula.
- **Parameters:**
	- `elevation_m` (numpy array or Raster): Elevation in meters.
	- `Ta_C` (numpy array or Raster): Air temperature in Celsius.
- **Returns:** Surface pressure in Pascal (Pa).
- **References:**
	- Wallace, J. M., & Hobbs, P. V. (2006).
	- Stull, R. B. (2017).

## References

- Alduchov, O. A., & Eskridge, R. E. (1996). Improved Magnus Form Approximation of Saturation Vapor Pressure. Journal of Applied Meteorology, 35(4), 601–609.
- Bolton, D. (1980). The computation of equivalent potential temperature. Monthly Weather Review, 108(7), 1046–1053.
- Rogers, R. R., & Yau, M. K. (1989). A Short Course in Cloud Physics (3rd ed.). Pergamon Press.
- Stull, R. B. (2017). Practical Meteorology: An Algebra-based Survey of Atmospheric Science. University of British Columbia.
- Wallace, J. M., & Hobbs, P. V. (2006). Atmospheric Science: An Introductory Survey (2nd ed.). Academic Press.
