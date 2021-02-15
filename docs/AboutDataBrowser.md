The TROCAS Data Browser is intended to provide convenient overviews and exploration of TROCAS data. It aggregates sensor data from the TROCAS project across all TROCAS transects conducted so far and collected from a boat in continuous "underway" mode while transiting or remaining stationary at a location. Sensor types currently included are EXO Sonde, Licor CO2, Picarro and GPS. It does not yet include ADCP dataq or data from experiments or from laboratory analyses of samples.

See the annotated screenshot below for usage instructions. The main component of the application is in the **Data Browser tab**. The **Inventory tab** presents an inventory table for each TROCAS transect and a list of currently known data gaps or issues that need to be addressed.

This is a work in progress. Some of the enhancements currently identified for near-term implementation are <a href="https://github.com/emiliom/TROCAS/blob/master/AppTODOs.md" target="_blank">listed in this TO-DOs page</a>.

### TROCAS data processing

- Data presented in this Data Browser are based on raw sensor output files (including GPS) averaged into 1-minute bins. The binned data from each sensor are then joined on matching time-interval bins. Sensor data that don't have a corresponding GPS 1-minute bin are not presented on this application; such data will require further investigation to attach geospatial coordinates.
- Source sensor data files in parent folders indicating their sampling "type" as *underway* (moving) or *diel* (stationary) are flagged as such in data processing workflow. All others are labelled with a default *mixed* (unknown or a combination of the two) flag. The **"stations - diel files" points (small blue squares)** represent aggregations of diel-flagged files, identified for further investigation and identification.

### Files available for download

Data and inventory files will be made available for download in the near future. 
The following Excel files are some of the core files that will be available from Google Drive for download (*but currently only to users with UW accounts*):

- [merged_1minbinned.xlsx](https://drive.google.com/open?id=1j3DU1ealqm-y1saOiZBvJFkGGHcVDYyA): 1-min median binned, merged file. 14 MB.
- [sensorinventory.xlsx](https://drive.google.com/open?id=10lrflq_yQgX--ZnoP4ovhDKaAoi-wDrK): Sensor inventory, by individual, raw sensor file.
- Sensor statistics: [GPS](https://drive.google.com/open?id=18hKJVenXlMchqmeC7EJiDe8wj8UMyWyI), [EXO Sonde](https://drive.google.com/open?id=14ZTD2Qk6CcT-kQMpodOIdbUzYGde4gM1), [Licor](https://drive.google.com/open?id=1KVJ3qwhaSgsUyPdKv5gBUAvTM8BqbtXN), [Picarro](https://drive.google.com/open?id=1m6ykuS1gF_wM_nfdg3W1WAh8hnaimrC5).

### Annotated screenshot of Data Browser tab
