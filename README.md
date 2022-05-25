# EAZIIS_Lab1# Converter
## About

The console application is designed to convert files from csv to parquet and from parquet to csv formats, get schema of the file. The script was written in third version of the Python language.


## Libraries

- pandas -- a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language
- fastparquet -- a python implementation of the parquet format, aiming integrate into python-based big data work-flows 
- argparse -- a complete argument processing library.
- os  -- lib, which provides functions for interacting with the operating system
- sys -- lib, that  provides various functions and variables that are used to manipulate different parts of the Python runtime environment


## Usage

If you don't have libraries mentioned above, use command below in console.This command just install all the necessary libraries for the script to work.

```
pip install -r requirments.txt
```

Syntax of script.

```
python converter.py [--csv2parquet | --parquet2csv <src-filename> <dst-filename>] | [--get-schema <filename>] | [--help]
```
#### Flags

- help -- shows how to use this script.
- csv2parquet -- rewrite data from csv file to parquet file.
- parquet2csv -- rewrite data from parquet file to csv file.
- get-schema  -- shows schema of the file.

#### Args
##### Arguments for flags: csv2parquet, parquet2csv.

- src-filename -- path of file which will be read.
- dst-filename -- path of file which will be written.

##### Arguments for flags: get-schema.

- filename --  name of file which we get a schema.

## Examples


**Input**:
```
python converter.py --csv2parquet  .\Data\bikes_rent.csv .Data\bikes_rent.parq
```
**Result**:
Parquet file with name bikes_rent.parq in dir Data.

**Input**:
```
python converter.py --get-schema .\Data\bikes_rent.csv
```
**Result**:
> season              int64 
> 
>yr                  int64
>
>mnth                int64
>
>holiday             int64
>
>weekday             int64
>
>workingday          int64
>
>weathersit          int64
>
>temp              float64
>
>atemp             float64
>
>hum               float64
>
>windspeed(mph)    float64
>
>windspeed(ms)     float64
>
>cnt                 int64
>



## License

MIT

**Free Software, Hell Yeah!**
