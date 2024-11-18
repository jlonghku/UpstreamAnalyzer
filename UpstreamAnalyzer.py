import numpy as np
from pysheds.grid import Grid
from pysheds.sview import Raster, ViewFinder
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
from pyproj import Transformer, Proj

def analyze_upstream_basin(asc_file_path, col, row, threshold, xytype='index', crs='EPSG:4326', clip_to=False, new_asc_file_path=None):
    # Initialize the Grid object and add DEM data
    grid = Grid.from_ascii(asc_file_path, crs=Proj(crs))
    dem = grid.read_ascii(asc_file_path, crs=Proj(crs))
    
    # Fill pits in the DEM
    pit_filled_dem = grid.fill_pits(dem)
    
    # Fill depressions in the DEM
    flooded_dem = grid.fill_depressions(pit_filled_dem)
    
    # Resolve flat areas in the DEM
    inflated_dem = grid.resolve_flats(flooded_dem)
    
    # Optionally save the processed DEM to a new ASC file
    if new_asc_file_path is not None:
        grid.to_ascii(inflated_dem, new_asc_file_path)

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
        
        # Get the nearest cell index
        x, y = grid.nearest_cell(col, row)
        print(f"Nearest cell index for the snapped pour point: X={x}, Y={y}")
        
        # Extract the catchment area based on the pour point
        catch = grid.catchment(x=col, y=row, fdir=fdir, xytype=xytype)
    else:
        # Extract the catchment area when using grid index coordinates
        catch = grid.catchment(x=col, y=row, fdir=fdir, xytype=xytype)
        x, y = col, row
        acc = grid.accumulation(fdir)
    
    # Optionally clip the catchment area
    if clip_to:
        grid.clip_to(catch)
        acc = grid.accumulation(fdir)
      
    # View the catchment data
    catchment_data = grid.view(catch)
    
    # Visualize the results
    plt.figure(figsize=(10, 8))
    plt.imshow(catchment_data, cmap='Blues', interpolation='nearest')
    plt.imshow(np.where(acc > threshold, threshold, acc), cmap='binary', interpolation='nearest', alpha=0.7)
    plt.colorbar(label='Catchment Area')
    plt.title(f'Upstream Basin from Specified Outlet: X={x}, Y={y}')
    plt.show()


def resample_dem(input_asc, resample_asc, crs="EPSG:4326", scale_factor=0.5, interpolation_order=1):
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
   
# Example usage
threshold = 500
crs = "EPSG:32610"
asc_file_path = 'WA_Samish/Data_Inputs90m/m_1_DEM/Samish_DredgeMask_EEX.asc'
new_asc_file_path = 'New_Samish.asc'

# Example usage 1: Using grid index coordinates
col, row = 108, 207
analyze_upstream_basin(asc_file_path, col, row, threshold, xytype='index')

# Example usage 2: Using geographic coordinates with transformation and saving the processed ASC file to a new file
lat, long = 48.54594127, -122.3382169 
new_asc_file_path = 'New_Samish.asc'
analyze_upstream_basin(asc_file_path, long, lat, threshold, xytype='coordinate', crs=crs, new_asc_file_path=new_asc_file_path)

# Example usage 3: Resampling DEM and analyzing the upstream basin
resample_asc = "Resample_dem.asc" 
resample_dem(asc_file_path, resample_asc, crs=crs, scale_factor=0.5)
lat, long = 48.54594127, -122.3382169 
analyze_upstream_basin(resample_asc, long, lat, threshold, xytype='coordinate', crs=crs, new_asc_file_path=new_asc_file_path)
