Listing of missing sensor files or issues with specific files. Go to the 
<a href="https://github.com/amazon-riverbgc/trocas-herokuapp1/tree/master/docs/MissingDataInventory.md" target="_blank">`MissingDataInventory.md` markdown document on GitHub</a>
to update it directly. Last update: 2020-4-20

### TR 1
- 2019-8-29: **Licor** `transect01_11_2014_7.txt` has 241,474 observations, more than twice the number as the file with the next highest number. If that means it actually goes over > 24 hours, my assumption for handling the midnight roll over breaks down
- 2019-8-29: **Picarro** files are missing

### TR 2
- 2020-4-18: **Licor** data are less comprehensive, geographically, than EXO Sonde and Picarro. Prior to 2020-4-18 these data files were not being read (the directory was not set correctly).
- **EXO Sonde:**
    - 2020-4-18: Data are less comprehensive than Picarro, and area coverage varies with parameter. Downstream half is largely missing. The files under `T2 Underway data/Sonde Transects/Upstream`, with names that reference downstream areas (Santarem, Xingu, Macapa), have dates in early November prior to the first GPS date.
    - 2019-8-29: File `Sonde Transects/Upstream/All Upstream.xlsx` is big; I suspect it may aggregate other Sonde files also found in that directory. In that case, it adds a duplication. I've renamed it temporarily, to prevent it being read.
- 2019-8-29: Two **Picarro** files have corrupted TIME values; they're in the form of 48:49.7, with a single colon, the first part not being a proper hour. Will try to read date-time information instead from one of the other time columns, like EPOCH_TIME. The files are: `CFIDS2061-20141107-071220Z-DataLog_User.dat` and `CFIDS2061-20141108-093330Z-DataLog_User.dat`

### TR 3
- **Licor:**
    - 2020-1-18: There's barely any data, relative to the other sensors.
    - 2019-8-29: For file `Santarem 7_8_15a.txt`, I corrected the first header row from """2015-07" -08 at "08:39""" to "2015-07-08 at 08:39"; and in second header row, Time(H:M        :S)  CO2    (ppm) to Time(H:M:S)  CO2(ppm). But in the end I've excluded this file b/c the data rows are corrupted (have two extra columns) starting in row 2075.
- 2019-8-29: **EXO Sonde** files are missing (2020-1-18: or largely missing? I think I found some files under TR 4 that obviously were part of TR 3, and moved them to TR 3)

### TR 4
- 2020-1-18: **EXO Sonde** coverage is much more sparse than all other sensors. Data from the upstream half of the transect are missing.

### TR 5
- **Licor**:
    - 2019-8-29: `Tidal/Surface` directory has no .txt files, just .xlsx files. So, I can't ingest it as the other files.
    - 2019-8-29: `diel/diel_ 11_8_16 Sika.txt` and `Tidal/50 percent depth/50Depth_NMCP_11_8_16.txt` are non-standard. They nare very different from conventional files, having no header rows and 3 columns like this: <incremental int counter>  Time(H:M:S)   CO2(ppm). I can't ingest them.

### TR 7
- 2019-12-17: **Picarro:** Regarding files Nick sent us, data from the last day are missing: "doesn't include the very last day since I left a day early (ADCP In north macapa)? Either M/Vania downloaded the last day or it's still sitting on the Picarro hard drive and someone can retrieve it next time she's fired up."

### TR 8
- **Picarro** data was not collected


### General issues, by sensor type
#### EXO Sonde
- Conductivity needs to be added to the binned-merged file.
- Dates are reversed (YYYY-DD-MM vs YYYY-MM-DD) in some files. In TROCAS 6, see "2017-05-01" vs "2017-01-05"
- Files don't always have the same set of columns. I've added a mechanism to exclude manually added "extra" columns. But this doesn't necessarily fix all issues related to modified columns
- A variety of datetime columns occur, apparently added manually and sometimes including duplicate column names. Columns sometimes include one actually called `datetime` (and `Datetime`), which collides with the `datetime` name I was using for the final, processed column name. I renamed that column to `date_time`.
- There are still a number of "bad" extra columns, most of them probably added manually. See the notes in the data processing Jupyter notebook. These issues are resulting in good data probably not being read appropriately, including data being generated with modified column names (eg, `ODO % sat.1`, `ODO mg/L.1`) that are then not retained in the data binning and merging workflow

#### Picarro
- Are times in UTC or Brasilia TZ?
- For now, to handle the large-file (and memory) issue, I'm dropping many of the columns not being used directly.
