# Notes from `trocas_panelapp_1.ipynb`
- 9/15-12/2020
- Bugs, long-term to-dos, update history, etc
- Complements - See https://github.com/amazon-riverbgc/TROCAS/blob/master/AppTODOs.md


## Recently completed tasks
- 3/14. Tested with env `holoviztrocas_panelapp_latest` created today from `data/notebooks/environment.yml`.
- 3/11. Reverted to using JupyterLab 1.x, via a new conda env, `jupyterlab1`. Everything is working again, with both conda envs (`holoviztrocas_panelapp` and `holoviztrocas_panelapp_latest2`). The histogram axis-range-update fix still works.
- 3/10. 
    - Implemented the fix to the histogram axis-range-udpate problem, using `.opts(framewise=True)`
    - The app is having problems since I upgraded JupyterLab to 2.0. First (yesterday), before the `jupyterlab_pyviz` extension was updated today, the drop downs were not working properly. Now, the app is started in completely screwed up and unworkable form, with a *tiny* piece of real estate. When I launch the app from the notebook via `panel serve`, the same problem with the drop-down menus is present.
- 2/22/2020. T8 EXO Sonde data is now visible as expected
- 2/2, 1/30,18/2020. 
- 12/26-23/2019. Ran with updated (T7 & T8) data files. Updated `trocas_nbr` widget to auto span to all TROCAS present in `sensorinventory_df.parq` 
- 11/19-17/2019. 
  - Testing running with new conda env, with the latest versions of holoviz packages
  - Changed basemap tiles usage to rely on holoviews instead of geoviews, and changed the actual tile set used b/c holoviews apparenlty only supports pre-defined tile sets.
  - Added tabs, including a Start/documentation tab and a TROCAS inventory tab
- (11/13-11. Tweaked. Rerun on 11/11/2019). Testing with new conda env on 11/17
- 10/26/2019 

### Also:
- Overhaul histogram so it truly responds dynamically to all selections.
  - The histogram is responding dynamically to changes in TROCAS number (but with hiccups!), but not to changes in variables that lead to a completely different value range -- both x axis and y axis ranges. The xlabel does update, but the axis range doesn't. For now, updating the histogram requires rerunning the cell. See https://holoviz.org/tutorial/Interlinked_Plots.html for good examples of a linked histogram plots, but using a more complex scheme (streams, `from holoviews.streams import Selection1D`, etc). See also http://earthml.pyviz.org/topics/Carbon_Flux.html
  - This scheme didn't work. It still required rerunning the code to get the xaxis range to update
    ```python
       obs_param_dynmap_ser = geopoints.dframe()[geopoints.dimensions(selection='value')[0].name]
       bin_range=(obs_param_dynmap_ser.min(), obs_param_dynmap_ser.max()) # using this bin_range in hist()
     ```

## Notes, bug comments, etc

### Code samples for replacing geoviews use with holoviews and datashader functionality

`hv.Tiles` (same as `hv.element.tiles.Tiles`)

Init signature: hv.Tiles(data, kdims=None, vdims=None, **params)
Docstring:     
params(extents=Tuple, cdims=Dict, kdims=List, vdims=List, group=String, label=String, name=String)

    The Tiles element represents tile sources, specified as URL
    containing different template variables.

See https://holoviews.org/reference/elements/bokeh/Tiles.html for a listing and thumbnails of tiles available in `tiles.tile_sources`.

From http://holoviz.org/tutorial/Interlinked_Plots.html (and see also https://datashader.org/user_guide/Geography.html):
```python
import datashader.geo
x, y = datashader.geo.lnglat_to_meters(most_severe.longitude, most_severe.latitude)
```


### colormap and color range limit customizations

#### Setting color range limits
Use `clim` option (or hvplot) parameter, eg: `clim=(5000, 8000)`

#### Setting colormap min, max and NaN colors
Use the `clipping_colors` option, like this:
```python
clipping = {'min': 'red', 'max': 'green', 'NaN': 'transparent'}
myplot.opts(clipping_colors=clipping)
```

## Rasterize and spread all-TROCAS points as gray-scale background

- http://holoviews.org/releases.html
- **4/20/2020: Currently all this code is commented out because of error I ran into starting in mid November 2019.**
    ```python
    # SPREAD background points
    rasterized_postds2 = rasterize(mbdata_points, aggregator=ds.count())
    ```
- See also `holoviz_rasterize_issues_versions.odt`

### Old conda env, `holoviztrocas_panelapp` ("older" holoviz versions)
- `rasterized_postds2` generates a bokeh/holoviews image, and `print(rasterized_postds2)` results in:
```
:DynamicMap   []
   :Image   [longitude,latitude]   (Count)
```
- `type(mbdata_points), type(rasterized_postds2)`: `(geoviews.element.geo.Dataset, holoviews.core.spaces.DynamicMap)`
- `rasterized_postds2.type` = `geoviews.element.geo.Image`

### New conda env, `holoviztrocas_panelapp` (latest holoviz versions)
- `rasterized_postds2` does not produce a plot and instead gives this message:
    ```
    No plotting class for Dataset found

    :DynamicMap   []
       :Dataset   [longitude,latitude]   (date_time,TROCAS_nbr,TROCAS_nbr_lico,TROCAS_nbr_gps,collectiontype_lico,filename_lico,reldirpath_lico,CO2(ppm),TROCAS_nbr_sond,collectiontype_sond,filename_sond,reldirpath_sond,ODO mg/L,pH,Temp °C,Turbidity FNU,Chlorophyll µg/L,TROCAS_nbr_pica,12CO2,Delta_Raw_iCO2,12CH4,Delta_iCH4_Raw,latdeg,londeg)
    ```
- `print(rasterized_postds2)` results in:
```
:DynamicMap   []
```
- `type(mbdata_points), type(rasterized_postds2)`: `(geoviews.element.geo.Dataset, holoviews.core.spaces.DynamicMap)`
- `rasterized_postds2.type` = None

### Other commented out code

```python
vars(rasterized_postds2)

# Below I show only the object elements that are different.

# OLD CONDA ENV:
'_type': geoviews.element.geo.Image,
 'data': OrderedDict([((), :Image   [longitude,latitude]   (Count))]),

# NEW CONDA ENV:
'_type': None,
 'data': OrderedDict(),
 
# These options are not making any obvious difference: .opts(logz=True, cmap=list(reversed(colorcet.gray)))
# hv.DynamicMap(points) instead of selected?

shaded_postds2 = shade(rasterized_postds2, cmap=list(reversed(cc.b_linear_grey_10_95_c0)))
spreaded_postds = spread(shaded_postds2, px=1)    
```

## 4.1. Extract diel file flags (collectiontype) and create points, by individual files via groupby

```python
mbdata_dielcoll_pts_df['longitude'], mbdata_dielcoll_pts_df['latitude'] = \
    datashader.geo.lnglat_to_meters(mbdata_dielcoll_pts_df.longitude, mbdata_dielcoll_pts_df.latitude)
mbdata_dielcoll_points = hv.Points(mbdata_dielcoll_pts_df, kdims=['longitude', 'latitude'],
                                   label='stations - diel files')
```

## 6.3. Map and Histogram plots

### 6.3.1. Map

```python
selected = mbdata_points.select(TROCAS_nbr=trocas_nbr.value)
geopoints = selected.to(gv.Points, ['longitude', 'latitude'], [obs_parameter.value], []
                        ).opts(**geo_opts)

geopoints.opts(clim=obs_variable_clim)
colorbar_opts={'title': 'my parameter (units)'},
       title works but its position at the top is of limited use; label is not accepted
clabel works as a stand-alone opts parameter, but has the same effect as title
```

Then this block:

```python
def get_dfcol_param_value(sensor_val, obs_param_label):
    if not OP_IDX:
        obs_param = obs_param_label
    else:
        # obs_param must be initialized
        obs_param = 'pH'
        for param_tup in _obs_parameters[sensor_val]:
            if param_tup[OP_IDX] == obs_param_label:
                obs_param = param_tup[not OP_IDX] 
                break
    return obs_param

def mbdata_points_tr_map(ds, sensor_val, obs_param_label):
    if not OP_IDX:
        obs_param = obs_param_label
    else:
        # obs_param must be initialized
        obs_param = 'pH'
        for param_tup in _obs_parameters[sensor_val]:
            if param_tup[OP_IDX] == obs_param_label:
                obs_param = param_tup[not OP_IDX] 
                break

    # return ds.opts(color=obs_param)
    return ds.opts(color=obs_param)
```

### logz (log-scale colormap)
- I'm not getting this to work with `logz=use_logscale.param.value` or `logz=use_logscale.value`:
    ```python
    use_logscale = pn.widgets.Checkbox(name='Use Log scale', value=False)
    ```
- Using `.opts(logz=True`) on an early iteration of the mapped point data (likely shaded/rasterized) did not work
- Note from a [2019-11 comment online](http://bebi103.caltech.edu.s3-website-us-east-1.amazonaws.com/2019a/content/recitations/recitation_05/overplotting.html#Datashader): "HoloViews currently cannot display datashaded plots with a log axis, so we have to manually compute the logarithms for the data set."


#### BUG, 3/15/2020

After the change in `obs_parameter` away from dataframe column names proper, and the corresponding change in `mbdata_points_tr`, `mainmap` is broken. The holoviews map of geopoints no longer works:
```python
# This previous element:
geopoints.apply.opts(color=obs_parameter.param.value, size=3, clipping_colors={'NaN':'transparent'})
# Needs to be changed to something like this:
(geopoints.apply(mbdata_points_tr_map, sensor.param.value, obs_parameter.param.value)
 .opts(size=3, clipping_colors={'NaN':'transparent'}))

# But it's not working. It leads the holoviews/param error:
ValueError: Boolean 'link_inputs' only takes a Boolean value.
```

I had to revert to using dataframe column names in the drop downs, as before. Will have to resolve this later.

```python
# (basemap
# * geopoints.apply(mbdata_points_tr_map, sensor_val=sensor.param.value, obs_param_label=obs_parameter.param.value).opts(size=3)
# ).opts(**size_opts)

# geopoints.apply(mbdata_points_tr_map, sensor.param.value, obs_parameter.param.value)

# (basemap
# * geopoints.apply.opts(color=get_dfcol_param_value(sensor_val=sensor.param.value, obs_param_label=obs_parameter.param.value)).opts(size=3)
# ).opts(**size_opts)

# (basemap
# * (geopoints.apply.opts(color=obs_parameter.param.value)).opts(size=3)
# ).opts(**size_opts)
```

## 6.5. Documentation and supplementary App Tabs

Column width options
- https://docs.bokeh.org/en/latest/docs/reference/models/widgets.tables.html#bokeh.models.widgets.tables.DataTable
- https://github.com/holoviz/holoviews/issues/3613
- http://holoviews.org/user_guide/Customizing_Plots.html
- http://holoviews.org/user_guide/Tabular_Datasets.html


## Serve the Panel App

**11/16/2019 NOTE:** The error in running the panel with the "latest" conda env is with `mainmap`, specifically with `spreaded_postds` and apparently more specifically the `shade` statement `shaded_postds2 = shade(rasterized_postds2, cmap=list(reversed(cc.b_linear_grey_10_95_c0)))`. All the other elements check out.
```python
~/miniconda/envs/holoviztrocas_panelapp_latest/lib/python3.7/site-packages/holoviews/operation/datashader.py in _process(self, element, key)
   1063             return element.map(self._process, [Element])
   1064         else:
-> 1065             xdensity = element.xdensity
   1066             ydensity = element.ydensity
   1067             bounds = element.bounds

AttributeError: 'Dataset' object has no attribute 'xdensity'
```