import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import json
import csv
import zipfile



def transit_from_gtfs(city):

    out_geojson_shapes = {
        'type': 'FeatureCollection',
        'features': [
        ]
    }

    zf = zipfile.ZipFile(city + "/transit_data/gtfs.zip") 

    df = pd.read_csv(zf.open('shapes.txt'))

    df = df.sort_values(by=['shape_id', 'shape_pt_sequence'])

    coord_list = []
    c_shape_id = "0"
    c = 0
    for row in df.itertuples():
        
        if c_shape_id != row.shape_id:

            feature = {
                "type": "Feature",
                "properties": {
                    "shape_id": c_shape_id
                },
                "geometry": {
                    'type': 'LineString',
                    'coordinates': coord_list
                }
            }

            out_geojson_shapes["features"].append(feature)

            c_shape_id = row.shape_id
            coord_list = []
            coord_list.append([float(row.shape_pt_lon),float(row.shape_pt_lat)])
            c += 1

        else:
            coord_list.append([float(row.shape_pt_lon),float(row.shape_pt_lat)])


    with open(city + '/transit_data/gtfs_routes.geojson', 'w') as file:
        file.write(json.dumps(out_geojson_shapes))


    dft = gpd.read_file(city + '/transit_data/gtfs_routes.geojson')

    del dft["shape_id"]

    gdf = gpd.read_file(city + "/transit_data/boundary.topojson")

    dft = gpd.clip(dft,gdf)

    dft.to_file(city + '/transit_data/gtfs_routes.geojson', driver='GeoJSON')


transit_from_gtfs("Victoria")  