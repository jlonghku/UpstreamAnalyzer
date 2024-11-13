import numpy as np
from pysheds.grid import Grid
import matplotlib.pyplot as plt
from pyproj import Transformer

def analyze_upstream_basin(asc_file_path, col, row, threshold, xytype='index', target_crs=None, source_crs=None, clip_to=False):
    # Initialize Grid and add DEM data
    grid = Grid.from_ascii(asc_file_path)
    dem = grid.read_ascii(asc_file_path)

    # Fill depressions in DEM
    flooded_dem = grid.fill_depressions(dem)

    # Resolve flat areas in DEM
    inflated_dem = grid.resolve_flats(flooded_dem)

    # Compute flow direction
    fdir = grid.flowdir(inflated_dem)

    # Extract upstream basin (catchment area)
    if xytype == 'coordinate':
        # Snap pour point to high accumulation cell
        acc = grid.accumulation(fdir)
        if target_crs is not None:
            # Define the coordinate transformer to convert to the target CRS
            transformer = Transformer.from_crs("EPSG:4326", target_crs, always_xy=True)
            if source_crs is not None:
                transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)
            # Transform the coordinates
            col, row = transformer.transform(col, row)
        
        # Snap the pour point to the nearest cell with high accumulation
        col, row = grid.snap_to_mask(acc > threshold, (col, row))
        
        # Get nearest cell index
        x, y = grid.nearest_cell(col, row)
        print(f"Nearest cell index for the snapped pour point: X={x}, Y={y}")
        
        # Extract catchment area based on pour point
        catch = grid.catchment(x=col, y=row, fdir=fdir, xytype=xytype)
    else:
        # Extract catchment area when using grid index coordinates
        catch = grid.catchment(x=col, y=row, fdir=fdir, xytype=xytype)
        x, y = col, row
        acc = grid.accumulation(fdir)
    
    # Optionally clip the catchment area
    if clip_to:
        grid.clip_to(catch)
      
    # View catchment data
    catchment_data = grid.view(catch)
    
    # Visualize results
    plt.figure(figsize=(10, 8))
    plt.imshow(catchment_data, cmap='Blues', interpolation='nearest')
    plt.imshow(np.where(acc > threshold, threshold, acc), cmap='binary', interpolation='nearest', alpha=0.7)
    plt.colorbar(label='Catchment Area')
    plt.title(f'Upstream Basin from Specified Outlet: X={x}, Y={y}')
    plt.show()

# Example usage
threshold = 500
asc_file_path = 'WA_Samish/Data_Inputs90m/m_1_DEM/Samish_DredgeMask_EEX.asc'

# Example usage 1: Using grid index coordinates
col, row = 108, 207
analyze_upstream_basin(asc_file_path, col, row, threshold, xytype='index')

# Example usage 2: Using geographic coordinates with transformation
lat, long = 48.54594127, -122.3382169 
analyze_upstream_basin(asc_file_path, long, lat, threshold, xytype='coordinate', target_crs="EPSG:32610")
