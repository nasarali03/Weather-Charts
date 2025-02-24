import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import scipy as sp
import json,os,random
import re
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI Agg backend


def idw_interpolation(x, y, z, xi, yi, power=3, chunk_size=10000):
    tree = cKDTree(np.c_[x, y])
    zi = np.zeros(len(xi))
    for i in range(0, len(xi), chunk_size):
        xi_chunk = xi[i:i + chunk_size]
        yi_chunk = yi[i:i + chunk_size]
        distances, indices = tree.query(np.c_[xi_chunk, yi_chunk], k=min(10, len(x)), p=2, workers=-1)
        weights = 1 / (distances + 1e-12) ** power
        weights /= weights.sum(axis=1)[:, np.newaxis]
        zi[i:i + chunk_size] = np.sum(weights * z[indices], axis=1)
    return zi

def contours_to_geojson(contour_set):
    features = []
    for level, segs in zip(contour_set.levels, contour_set.allsegs):
        for seg in segs:
            coords = [[pt[0], pt[1]] for pt in seg if pt[0] is not None and pt[1] is not None]
            if len(coords) > 0:
                # Determine label position
                label_position = random.choice(['start', 'middle', 'end'])
                if label_position == 'start':
                    label_coords = coords[0]
                elif label_position == 'middle':
                    mid_index = len(coords) // 2
                    label_coords = coords[mid_index]
                else:  # 'end'
                    label_coords = coords[-1]
                
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coords
                    },
                    "properties": {
                        "level": int(level),
                        "label": int(level),
                        "label_coords": label_coords,
                        "path": coords
                    }
                })
    return {"type": "FeatureCollection", "features": features}

def get_base_dir():
    """Determine the correct base directory based on the environment."""
    if "RAILWAY_ENVIRONMENT" in os.environ:
        return "/app/data/"  # Railway persistent storage
    return os.path.join(os.getcwd(), "data")  # Local storage

def read_data(timestamp):
    """Read CSV file and return data."""
    try:
        base_dir = get_base_dir()
        data_file = os.path.join(base_dir, "Decoded_Data", f"{timestamp}.csv")

        data = pd.read_csv(data_file)
        filtered_data = data[data["Elevation"] < 700]
        return filtered_data
    except FileNotFoundError:
        print(f"File not found: {data_file}")
        return pd.DataFrame()  # Return an empty DataFrame instead of None
    except Exception as e:
        print("An error occurred:", str(e))
        return pd.DataFrame()  # Return an empty DataFrame in case of other errors

def generate_geojson(timestamp):
    """Generate a GeoJSON file from the interpolated data."""
    data = read_data(timestamp)

    if data.empty:
        print(f"No data available for timestamp: {timestamp}")
        return

    data = data.drop_duplicates(subset='station_id')
    lats = data['Latitude'].values
    lons = data['Longitude'].values  
    pressure = data['pressure_sea_level'].values

    valid_indices = ~np.isnan(pressure)
    valid_lats = lats[valid_indices]
    valid_lons = lons[valid_indices]
    valid_pressure = pressure[valid_indices].astype(float)

    lat_arr = np.linspace(valid_lats.min(), valid_lats.max(), 1000)
    lon_arr = np.linspace(valid_lons.min(), valid_lons.max(), 1000)
    lat_grid, lon_grid = np.meshgrid(lat_arr, lon_arr)
    lat_grid_flat, lon_grid_flat = lat_grid.flatten(), lon_grid.flatten()

    pressure_grid_flat = idw_interpolation(valid_lons, valid_lats, valid_pressure, lon_grid_flat, lat_grid_flat)
    pressure_grid = pressure_grid_flat.reshape(lat_grid.shape)
    
    pressure_grid = sp.ndimage.gaussian_filter(pressure_grid, sigma=5)
    min_pressure = np.nanmin(pressure_grid)
    max_pressure = np.nanmax(pressure_grid)
    levels = np.arange(np.floor(min_pressure / 2) * 2, np.ceil(max_pressure / 2) * 2 + 2, 2)
    
    # Create contours
    contours = plt.contour(lon_grid, lat_grid, pressure_grid, levels=levels)

    base_dir = get_base_dir()
    output_dir = os.path.join(base_dir, "contours_data")
    
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
    
    contour_geojson = contours_to_geojson(contours)
    output_file = os.path.join(output_dir, f"{timestamp}.geojson")

    with open(output_file, 'w') as f:
        json.dump(contour_geojson, f)

    print(f"GeoJSON saved to {output_file}")

def generate_geojson_diff_four(timestamp):
    data=read_data(timestamp)
    data = data.drop_duplicates(subset='station_id')
    lats = data['Latitude'].values
    lons = data['Longitude'].values  
    pressure = data['pressure_sea_level'].values

    valid_indices1 = ~np.isnan(pressure)
    valid_lats = lats[valid_indices1]
    valid_lons = lons[valid_indices1]
    valid_pressure = pressure[valid_indices1].astype(float)

    lat_arr = np.linspace(valid_lats.min(), valid_lats.max(), 1000)
    lon_arr = np.linspace(valid_lons.min(), valid_lons.max(), 1000)
    lat_grid, lon_grid = np.meshgrid(lat_arr, lon_arr)
    lat_grid_flat, lon_grid_flat = lat_grid.flatten(), lon_grid.flatten()

    pressure_grid_flat = idw_interpolation(valid_lons, valid_lats, valid_pressure, lon_grid_flat, lat_grid_flat)
    pressure_grid = pressure_grid_flat.reshape(lat_grid.shape)
    
    pressure_grid = sp.ndimage.gaussian_filter(pressure_grid, sigma=5)
    min_pressure = np.nanmin(pressure_grid)
    max_pressure = np.nanmax(pressure_grid)
    levels = np.arange(np.floor(min_pressure / 4) * 4, np.ceil(max_pressure / 4) * 4 + 4, 4)
    
    # Create contours
    contours = plt.contour(lon_grid, lat_grid, pressure_grid, levels=levels)
    output_dir = 'contours_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    contour_geojson = contours_to_geojson(contours)
    output_file = os.path.join(output_dir, f'{timestamp}l4.geojson')
    with open(output_file, 'w') as f:
        json.dump(contour_geojson, f)
    print(f'GeoJSON saved to {output_file}')

# geojson_dir = "Decoded_Data"
# geojson_files = [os.path.splitext(f)[0] for f in os.listdir(geojson_dir) if f.endswith('.csv')]

# for timestamp in geojson_files:
#     generate_geojson(timestamp)
# for x in a:
#     generate_geojson_diff_four(f"20241219{x}")

# a=["00","03","06","09","12","15","18","21"]
# b=['07','08','09','10','11','12','13','14','15','16','17']
# for x in b:
#     for y in a:
#         generate_geojson(f"202502{x}{y}")

generate_geojson(f"2025022400")