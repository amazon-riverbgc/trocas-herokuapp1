from collections import OrderedDict as odict
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd

import holoviews as hv
import geoviews as gv


TROCAS_BASEPATH = Path('./')

def get_mbdata(Points, holoviewsmapping=False):
    """Load and pre-process Binned-Merged data
    """
    mb_all_df = pd.read_parquet(TROCAS_BASEPATH / 'data' / 'merged_1minbinned_df.parq', 
                                engine='fastparquet')

    mb_df = mb_all_df[mb_all_df.latitude.notnull()].copy()

    # Store into new variables b/c the original ones will be overwritten into web mercator
    mb_df['londeg'] = mb_df['longitude']
    mb_df['latdeg'] = mb_df['latitude']

    if holoviewsmapping:
        import datashader.geo

        mb_df['longitude'], mb_df['latitude'] = datashader.geo.lnglat_to_meters(mb_df.londeg, mb_df.latdeg)
        mb_points = Points(mb_df, kdims=['longitude', 'latitude']) #, vdims=['date_time'])
        mb_points = hv.Dataset(mb_points)
    else:
        mb_points = Points(mb_df, kdims=['longitude', 'latitude']) #, vdims=['date_time'])
        mb_points = gv.Dataset(gv.operation.project_points(mb_points))
    
    return mb_all_df, mb_df, mb_points


def create_dielcollections(Points, mb_df, save_to_excel=False):
    """Generate diel station collections from merged-binned data and flags
    """
    ## Extract diel file flags (collectiontype) and create points, by individual files via groupby

    mbdata_dielcoll_df = mb_df[
        (mb_df.collectiontype_lico == 'diel') | (mb_df.collectiontype_sond == 'diel')
    ]

    # 'date_time':'mean',
    agg_dct = odict(
        TROCAS_nbr=('TROCAS_nbr', 'first'), 
        collectiontype_lico=('collectiontype_lico', 'first'), 
        collectiontype_sond=('collectiontype_sond', 'first'), 
        longitude=('longitude', 'mean'),  # ('longitude', 'median'),
        latitude=('latitude', 'mean'),  # ('latitude', 'median'),
        bin_count=('date_time', 'count'),
        londeg=('londeg', 'mean'),
        latdeg=('latdeg', 'mean'),
        londeg_min=('londeg', 'min'),
        londeg_max=('londeg', 'max'),
        latdeg_min=('latdeg', 'min'),
        latdeg_max=('latdeg', 'max'),
        date_time_min=('date_time', 'min'),
        date_time_max=('date_time', 'max')
    )

    mbdata_dielcoll_pts_df = mbdata_dielcoll_df.groupby(['filename_lico', 'filename_sond']).agg(**agg_dct)
    mbdata_dielcoll_pts_df.reset_index(inplace=True)

    # **NOTE: Save to Excel file for examination as needed. BUT THIS SHOULDN'T BE HAPPENING EVERY TIME THIS APP IS RUN!! 
    # CHANGE THIS, COMMENT IT OUT, ETC**
    if save_to_excel:
        mbdata_dielcoll_pts_df.to_excel(TROCAS_BASEPATH / 'mbdata_dielcoll_pts_df.xlsx')

    mbdata_dielcoll_points = Points(mbdata_dielcoll_pts_df, kdims=['longitude', 'latitude'],
                                    label='stations - diel files')  #, vdims=['date_time'])
    
    return mbdata_dielcoll_pts_df, mbdata_dielcoll_points


def get_jeffstations(Points, holoviewsmapping=False):
    """ "Jeff's" stations points
    """
    stations_gdf = gpd.read_file(TROCAS_BASEPATH / 'data' / 'stations.geojson', 
                                 crs='epsg:4326')

    # Store into new variables b/c the original ones will be overwritten into web mercator
    stations_gdf['londeg'] = stations_gdf['lon']
    stations_gdf['latdeg'] = stations_gdf['lat']

    if holoviewsmapping:
        import datashader.geo

        stations_gdf['lon'], stations_gdf['lat'] = datashader.geo.lnglat_to_meters(stations_gdf.londeg, stations_gdf.latdeg)
        stations_gv_vdims = Points(pd.DataFrame(stations_gdf), kdims=['lon', 'lat'],
                                vdims=['name'], label="stations - jeff's set")
    else:
        stations_gv_vdims = Points(stations_gdf, vdims=['name'], label="stations - jeff's set")

    return stations_gdf, stations_gv_vdims



def create_tr_sensorinventory():
    """Sensor inventory
    This could be extracted from mbdata_points, too.
    """
    sensorinventory_df = pd.read_parquet(TROCAS_BASEPATH / 'data' / 'sensorinventory_df.parq', 
                                         engine='fastparquet')
    
    sensorinv_agg_dct = odict(
        TROCAS_nbr=('TROCAS_nbr', 'first'), 
        date_time_min=('date_time_min', 'min'), 
        date_time_max=('date_time_max', 'max')
    )
    trocasinventory_df = sensorinventory_df.groupby(['TROCAS_nbr']).agg(**sensorinv_agg_dct)
    trocasinventory_df.reset_index(inplace=True, drop=True)

    sensorinv_agg_dct = odict(
        TROCAS_nbr=('TROCAS_nbr', 'first'), 
        sensorname=('sensorname', 'first'),
        date_time_min=('date_time_min', 'min'), 
        date_time_max=('date_time_max', 'max'),
        date_time_count=('date_time_count', 'sum')
    )
    inv_bysensor_df = sensorinventory_df.groupby(['TROCAS_nbr', 'sensorname']).agg(**sensorinv_agg_dct)
    inv_bysensor_df.reset_index(inplace=True, drop=True)

    # Pivot the sensorname column to create a wide table with columns TROCAS_nbr 
    # and each of the 4 sensor names
    inv_bysensor_wide_df = inv_bysensor_df.pivot(
        index='TROCAS_nbr', columns='sensorname', values='sensorname'
    )
    # reset index? .reset_index()
    for sensorname in inv_bysensor_df.sensorname.unique():
        inv_bysensor_wide_df[sensorname] = np.where(inv_bysensor_wide_df[sensorname].isna(), '', 'X')

    # Merge the sensor name indicators into `trocasinventory_df`
    trocasinventory_df = trocasinventory_df.merge(inv_bysensor_wide_df, on='TROCAS_nbr')
    
    return trocasinventory_df, sensorinventory_df
