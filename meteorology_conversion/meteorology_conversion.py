from typing import Union
import numpy as np
import rasters as rt
from rasters import Raster

# gas constant for dry air in joules per kilogram per kelvin
RD = 286.9

# gas constant for moist air in joules per kilogram per kelvin
RW = 461.5

# specific heat of water vapor in joules per kilogram per kelvin
CPW = 1846.0

# specific heat of dry air in joules per kilogram per kelvin
CPD = 1005.0

def kelvin_to_celsius(T_K: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Convert temperature from Kelvin (K) to Celsius (°C).

    Scientific basis:
        The Kelvin and Celsius scales are linearly related, with 0°C defined as 273.15 K. This conversion is fundamental in thermodynamics and meteorology.

    Args:
        T_K (Union[Raster, np.ndarray]): Temperature in Kelvin.

    Returns:
        Union[Raster, np.ndarray]: Temperature in Celsius.

    References:
        Wallace, J. M., & Hobbs, P. V. (2006). Atmospheric Science: An Introductory Survey (2nd ed.). Academic Press.
    """
    # Kelvin to Celsius conversion: T_C = T_K - 273.15
    return T_K - 273.15

def celcius_to_kelvin(T_C: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Convert temperature from Celsius (°C) to Kelvin (K).

    Scientific basis:
        The Kelvin scale is the SI base unit for thermodynamic temperature, and this conversion is universally used in atmospheric sciences.

    Args:
        T_C (Union[Raster, np.ndarray]): Temperature in Celsius.

    Returns:
        Union[Raster, np.ndarray]: Temperature in Kelvin.

    References:
        Wallace, J. M., & Hobbs, P. V. (2006). Atmospheric Science: An Introductory Survey (2nd ed.). Academic Press.
    """
    # Celsius to Kelvin conversion: T_K = T_C + 273.15
    return T_C + 273.15

def calculate_specific_humidity(
        Ea_Pa: Union[Raster, np.ndarray], 
        Ps_Pa: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Calculate the specific humidity (q) of air as a ratio of kilograms of water vapor to kilograms of moist air.

    Scientific basis:
        The constant 0.622 is the ratio of the molecular weight of water vapor to dry air. The formula is derived from the definition of specific humidity and the ideal gas law. This is a standard approach in meteorology.

    Args:
        Ea_Pa (Union[Raster, np.ndarray]): Actual water vapor pressure in Pascal.
        Ps_Pa (Union[Raster, np.ndarray]): Surface pressure in Pascal.

    Returns:
        Union[Raster, np.ndarray]: Specific humidity (kg water / kg moist air).

    References:
        Rogers, R. R., & Yau, M. K. (1989). A Short Course in Cloud Physics (3rd ed.). Pergamon Press.
        Stull, R. B. (2017). Practical Meteorology: An Algebra-based Survey of Atmospheric Science.
    """
    # q = 0.622 * Ea / (Ps - 0.387 * Ea)
    # 0.622 = Mw/Md (molecular weight ratio)
    return ((0.622 * Ea_Pa) / (Ps_Pa - (0.387 * Ea_Pa)))

def calculate_specific_heat(specific_humidity: Union[Raster, np.ndarray]):
    """
    Calculate the specific heat capacity at constant pressure (Cp) for moist air.

    Scientific basis:
        The specific heat of moist air depends on its composition. This function computes Cp as a weighted sum of the specific heats of dry air (CPD) and water vapor (CPW), based on the specific humidity.

    Args:
        specific_humidity (Union[Raster, np.ndarray]): Specific humidity (kg water / kg moist air).

    Returns:
        Cp_Jkg (Union[Raster, np.ndarray]): Specific heat capacity (J/kg/K).

    References:
        Wallace, J. M., & Hobbs, P. V. (2006). Atmospheric Science: An Introductory Survey (2nd ed.). Academic Press.
        Stull, R. B. (2017). Practical Meteorology.
    """
    # Cp = q * CPW + (1 - q) * CPD
    Cp_Jkg = specific_humidity * CPW + (1 - specific_humidity) * CPD
    return Cp_Jkg

def calculate_air_density(
        surface_pressure_Pa: Union[Raster, np.ndarray], 
        Ta_K: Union[Raster, np.ndarray], 
        specific_humidity: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Calculate the density of moist air (ρ) using the ideal gas law, accounting for water vapor.

    Scientific basis:
        The density of air decreases with increasing water vapor content because water vapor is less dense than dry air. This formula is derived from Dalton’s law and the ideal gas law, and is standard in meteorology.

    Args:
        surface_pressure_Pa (Union[Raster, np.ndarray]): Surface pressure in Pascal.
        Ta_K (Union[Raster, np.ndarray]): Air temperature in Kelvin.
        specific_humidity (Union[Raster, np.ndarray]): Specific humidity (kg water / kg moist air).

    Returns:
        Union[Raster, np.ndarray]: Air density (kg/m^3).

    References:
        Wallace, J. M., & Hobbs, P. V. (2006). Atmospheric Science: An Introductory Survey (2nd ed.). Academic Press.
        Stull, R. B. (2017). Practical Meteorology.
    """
    # Dry air density: rhoD = Ps / (RD * T)
    rhoD = surface_pressure_Pa / (RD * Ta_K)
    # Adjust for water vapor: rho = rhoD * ((1 + q) / (1 + q * (RW / RD)))
    rho = rhoD * ((1.0 + specific_humidity) / (1.0 + specific_humidity * (RW / RD)))
    return rho

def SVP_kPa_from_Ta_C(Ta_C: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Calculate the saturation vapor pressure (SVP) in kiloPascal (kPa) from air temperature in Celsius using the Magnus-Tetens approximation.

    Scientific basis:
        This is the Magnus-Tetens approximation, widely used for its accuracy in the range of typical atmospheric temperatures. It is a practical form of the Clausius-Clapeyron equation.

    Args:
        Ta_C (Union[Raster, np.ndarray]): Air temperature in Celsius.

    Returns:
        Union[Raster, np.ndarray]: Saturation vapor pressure in kPa.

    References:
        Alduchov, O. A., & Eskridge, R. E. (1996). Improved Magnus Form Approximation of Saturation Vapor Pressure. Journal of Applied Meteorology, 35(4), 601–609.
        Bolton, D. (1980). The computation of equivalent potential temperature. Monthly Weather Review, 108(7), 1046–1053.
    """
    # Magnus-Tetens formula for SVP (kPa):
    SVP_kPa = np.clip(0.611 * np.exp((Ta_C * 17.27) / (Ta_C + 237.7)), 1, None)
    return SVP_kPa

def SVP_Pa_from_Ta_C(Ta_C: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Calculate the saturation vapor pressure in Pascal (Pa) from air temperature in Celsius.

    Scientific basis:
        This function converts the result from the Magnus-Tetens approximation (in kPa) to Pascals (Pa) by multiplying by 1000.

    Args:
        Ta_C (Union[Raster, np.ndarray]): Air temperature in Celsius.

    Returns:
        Union[Raster, np.ndarray]: Saturation vapor pressure in Pascal (Pa).

    References:
        Alduchov, O. A., & Eskridge, R. E. (1996). Improved Magnus Form Approximation of Saturation Vapor Pressure. Journal of Applied Meteorology, 35(4), 601–609.
    """
    # Convert SVP from kPa to Pa
    return SVP_kPa_from_Ta_C(Ta_C) * 1000

def calculate_surface_pressure(elevation_m: Union[Raster, np.ndarray], Ta_C: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Estimate surface pressure (Ps) at a given elevation and temperature using the barometric formula.

    Scientific basis:
        This is a standard approximation for the decrease of pressure with altitude, assuming a constant lapse rate and ideal gas behavior. The formula is widely used in meteorology and atmospheric science.

    Args:
        elevation_m (Union[Raster, np.ndarray]): Elevation in meters.
        Ta_C (Union[Raster, np.ndarray]): Air temperature in Celsius.

    Returns:
        Union[Raster, np.ndarray]: Surface pressure in Pascal (Pa).

    References:
        Wallace, J. M., & Hobbs, P. V. (2006). Atmospheric Science: An Introductory Survey (2nd ed.). Academic Press.
        Stull, R. B. (2017). Practical Meteorology.
    """
    # Convert Celsius to Kelvin for the barometric formula
    Ta_K = kelvin_to_celsius(Ta_C)
    # Barometric formula for surface pressure at elevation
    Ps_Pa = 101325.0 * (1.0 - 0.0065 * elevation_m / Ta_K) ** (9.807 / (0.0065 * 287.0))  # [Pa]
    return Ps_Pa

