from upstream_analyzer.analyze_basin import analyze_upstream_basin, resample_dem

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