# analyze_basin.py

import numpy as np
from pysheds.grid import Grid
from pysheds.sview import Raster, ViewFinder
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
from pyproj import Transformer, Proj

def analyze_upstream_basin(asc_file_path, col, row, threshold, xytype='index', crs='EPSG:4326', clip_to=False, new_asc_file_path=None):
    """
    Analyze upstream basin from the specified outlet point.
    
    Parameters:
    - asc_file_path (str): Path to the input ASC file.
    - col, row (int or float): Coordinates of the outlet point.
    - threshold (float): Threshold for flow accumulation.
    - xytype (str): 'index' or 'coordinate'.
    - crs (str): Coordinate Reference System (CRS) for coordinate conversion.
    - clip_to (bool): Whether to clip the catchment.
    - new_asc_file_path (str): Path to save the new ASC file (optional).
    """
    # Initialize the Grid object and add DEM data
    grid = Grid.from_ascii(asc_file_path, crs=Proj(crs))
    dem = grid.read_ascii(asc_file_path, crs=Proj(crs))
    
    # Fill pits in the DEM
    pit_filled_dem = grid.fill_pits(dem)
    
    # Fill depressions in the DEM
    flooded_dem = grid.fill_depressions(pit_filled_dem)
    
    # Resolve flat areas in the DEM
    inflated_dem = grid.resolve_flats(flooded_dem)

    # Compute flow direction
    fdir = grid.flowdir(inflated_dem)

    # Extract the upstream basin (catchment area)
    if xytype == 'coordinate':        
        # Calculate flow accumulation
        acc = grid.accumulation(fdir)
        
        # Transform the coordinates to the target CRS
        transformer = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
        col, row = transformer.transform(col, row)
        
        # Snap the pour point to the nearest cell with high accumulation
        col, row = grid.snap_to_mask(acc > threshold, (col, row))
        
        # Extract the catchment area based on the pour point
        catch = grid.catchment(x=col, y=row, fdir=fdir, xytype=xytype)
        
        # Get the nearest cell index
        col, row = grid.nearest_cell(col, row)
        print(f"Nearest cell index for the snapped pour point: X={col}, Y={row}")
        
    else:
        # Extract the catchment area when using grid index coordinates
        catch = grid.catchment(x=col, y=row, fdir=fdir, xytype=xytype)
        acc = grid.accumulation(fdir)
    
    # Optionally clip the catchment area
    if clip_to:
        grid.clip_to(catch)
        acc = grid.accumulation(fdir)
    
    # Optionally save the processed DEM to a new ASC file
    if new_asc_file_path is not None:
        grid.to_ascii(inflated_dem, new_asc_file_path)
        
    # View the catchment data
    catchment_data = grid.view(catch)
    
    # Visualize the results
    plt.figure(figsize=(10, 8))
    plt.imshow(catchment_data, cmap='Blues', interpolation='nearest')
    plt.imshow(np.where(acc > threshold, threshold, acc), cmap='binary', interpolation='nearest', alpha=0.7)
    plt.colorbar(label='Catchment Area')
    plt.title(f'Upstream Basin from Specified Outlet: X={col}, Y={row}')
    plt.show()


def resample_dem(input_asc, resample_asc, crs="EPSG:4326", scale_factor=0.5, interpolation_order=1):
    """
    Resample a DEM to a different resolution.
    
    Parameters:
    - input_asc (str): Path to the input ASC file.
    - resample_asc (str): Path to save the resampled ASC file.
    - crs (str): Coordinate Reference System (CRS).
    - scale_factor (float): Scaling factor for resampling.
    - interpolation_order (int): Order of interpolation for resampling.
    """
    # Read the ASC file
    grid = Grid.from_ascii(input_asc, crs=Proj(crs))
    dem = grid.read_ascii(input_asc, crs=Proj(crs))
    
    # Perform resampling on the array data
    resample_dem = zoom(dem, (scale_factor, scale_factor), order=interpolation_order)

    # Create a new ViewFinder
    new_viewfinder = ViewFinder(
        affine=dem.affine * dem.affine.scale(1 / scale_factor, 1 / scale_factor),  # Update affine transform
        shape=resample_dem.shape,  # Use the new shape after resampling
        crs=dem.crs,  # Retain the original CRS
        nodata=dem.nodata  # Retain the original no-data value
    )

    # Create a new Raster object
    resampled_raster = Raster(resample_dem, viewfinder=new_viewfinder)
    newgrid = Grid.from_raster(resampled_raster)
    
    # Save the resampled data to a new ASC file
    newgrid.to_ascii(resampled_raster, resample_asc)
    
    print(f"Resampled DEM has been saved to: {resample_asc}")
