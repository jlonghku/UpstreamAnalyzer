# User Guide for Analyzing Upstream Basin

This guide provides instructions for using the tool to delineate upstream catchment areas from Digital Elevation Model (DEM) data. The tool processes DEM data, visualizes catchment areas, and optionally resamples the DEM for improved analysis.

## Requirements

To use this tool, ensure you have the following Python packages installed:

- **numpy**: `pip install numpy`
- **pysheds**: `pip install pysheds`
- **matplotlib**: `pip install matplotlib`
- **scipy**: `pip install scipy`
- **pyproj**: `pip install pyproj`

## Installation

To install this tool, run the following command:

- **upstream\_analyzer**: `pip install upstream_analyzer`

## Function Overview

### Analyze Upstream Basin

```python
from upstream_analyzer.analyze_basin import analyze_upstream_basin

analyze_upstream_basin(asc_file_path, col, row, threshold, xytype='index', crs='EPSG:4326', clip_to=False, new_asc_file_path=None)
```

#### Parameters

- **asc\_file\_path** (str): Path to the DEM ASCII file.
- **col** (int/float): Column coordinate or longitude value.
- **row** (int/float): Row coordinate or latitude value.
- **threshold** (int): Minimum flow accumulation threshold for identifying high-accumulation cells.
- **xytype** (str, optional): Type of coordinates used. Set to 'index' for grid cell indices or 'coordinate' for geographic coordinates. Default is 'index'.
- **crs** (str, optional): EPSG code of the coordinate reference system (e.g., "EPSG:32610"). Default is "EPSG:4326".
- **clip\_to** (bool, optional): If set to True, the catchment area will be clipped for visualization.
- **new\_asc\_file\_path** (str, optional): Path to save the processed DEM file in ASCII format. If specified, the filled and resolved DEM will be saved to this path.

#### Output

The function displays a plot of the upstream catchment area. The plot includes a color-coded representation of the catchment with flow accumulation. If **new\_asc\_file\_path** is provided, the processed DEM will be saved to the specified file.

### Resample DEM

```python
from upstream_analyzer.analyze_basin import resample_dem

resample_dem(input_asc, resample_asc, crs="EPSG:4326", scale_factor=0.5, interpolation_order=1)
```

#### Parameters

- **input\_asc** (str): Path to the input DEM ASCII file.
- **resample\_asc** (str): Path to save the resampled DEM ASCII file.
- **crs** (str, optional): EPSG code of the coordinate reference system (e.g., "EPSG:32610"). Default is "EPSG:4326".
- **scale\_factor** (float, optional): Scaling factor for resampling. Default is 0.5 (reduces resolution by half).
- **interpolation\_order** (int, optional): Interpolation method to use (0 - nearest, 1 - bilinear, etc.). Default is 1.

#### Output

The function saves the resampled DEM to the specified output file.

## Instructions

### 1. Analyze Upstream Basin

The function requires a DEM ASCII file path and coordinates for the outlet point. You have two options for specifying the coordinates:

#### Option 1: Using Grid Index Coordinates

Specify the outlet point using grid index coordinates (**col** and **row**).

```python
# Define the input parameters
asc_file_path = 'WA_Samish/Data_Inputs90m/m_1_DEM/Samish_DredgeMask_EEX.asc'
col, row = 108, 207
threshold = 500

# Call the function
analyze_upstream_basin(asc_file_path, col, row, threshold, xytype='index')
```

#### Option 2: Using Geographic Coordinates

Specify the outlet point using geographic coordinates (latitude and longitude) and transform them to grid index coordinates.

```python
# Define the input parameters
asc_file_path = 'WA_Samish/Data_Inputs90m/m_1_DEM/Samish_DredgeMask_EEX.asc'
lat, long = 48.54594127, -122.3382169
threshold = 500

# Call the function with coordinate transformation and save processed DEM to a new file
crs = "EPSG:32610"
new_asc_file_path = 'New_Samish.asc'
analyze_upstream_basin(asc_file_path, long, lat, threshold, xytype='coordinate', crs=crs, new_asc_file_path=new_asc_file_path)
```

### 2. Resample DEM

The `resample_dem` function allows you to resample the resolution of a DEM file to a new ASCII file.

```python
# Define the input parameters
input_asc = 'WA_Samish/Data_Inputs90m/m_1_DEM/Samish_DredgeMask_EEX.asc'
resample_asc = 'Resample_dem.asc'

# Resample the DEM to half the original resolution
resample_dem(input_asc, resample_asc, crs="EPSG:32610", scale_factor=0.5)
```

### 3. Explanation of Processing Steps

1. **Initialize Grid and Read DEM**: The DEM data is read using PySheds.
2. **Fill Pits in DEM**: Pits (local depressions) in the DEM are filled to ensure proper flow direction calculations.
3. **Fill Depressions and Resolve Flats**: Depressions are filled, and flat areas are resolved for accurate flow calculations.
4. **Compute Flow Direction**: Flow direction is calculated based on the processed DEM.
5. **Extract Upstream Basin**:
   - For **xytype = 'coordinate'**, the specified outlet point is snapped to the nearest high-accumulation cell, with optional CRS transformation.
   - For **xytype = 'index'**, the outlet point is treated as a grid cell index.
6. **Visualize Catchment Area**: The catchment area and flow accumulation data are visualized.

### 4. Visualization

The function will produce a plot displaying the upstream basin and flow accumulation values.

- **Blues Color Map**: Indicates the extent of the catchment area.
- **Binary Color Map**: Represents flow accumulation values greater than the specified threshold.

The visualization provides a clear indication of the upstream area that contributes to the specified outlet point.

## Example Outputs

The following images represent typical outputs from the function:

![Upstream Basin from Specified Outlet](https://raw.githubusercontent.com/jlonghku/UpstreamAnalyzer/main/img/Figure_1.png)
*Figure: Upstream Basin from Specified Outlet*

## Notes

- Ensure that the DEM ASCII file is accessible and correctly formatted.
- The **threshold** value affects the snapping process for geographic coordinates; a higher value will snap the outlet point to cells with greater flow accumulation.
- The coordinate transformation is performed using the PyProj library.
- If **new\_asc\_file\_path** is provided, the processed DEM file will be saved for further use.

## Troubleshooting

- **FileNotFoundError**: Verify that the provided DEM file path is correct.
- **IndexError**: Ensure the provided coordinates are within the grid bounds.
- **Coordinate Transformation Issues**: Ensure that the **crs** value is a valid EPSG code.

## Additional Resources

- [PySheds Documentation](https://pysheds.readthedocs.io/)
- [PyProj Documentation](https://pyproj4.github.io/pyproj/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

Feel free to customize the parameters as needed to explore different areas of interest within your DEM data!

