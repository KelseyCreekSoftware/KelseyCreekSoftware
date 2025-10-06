# MIDIS Blue File Project Notes

## Goal

Create a pyton script similar to this file to covert Blue 1.1 files to SigMF

https://github.com/IQEngine/IQEngine/blob/main/api/converters/vita49_to_sigmf/vita49.py

## ToDo

### REDHAWK

REDHAWK is a software-defined radio (SDR) framework designed to support the development, deployment, and management of real-time software radio applications.

It includes libaries such as blueFileLib.

https://github.com/RedhawkSDR/blueFileLib/blob/develop-2.0/cpp/src/HeaderControlBlock.cc

It is possible to intergrate REDHAWK with GNURadio. A GNURadio Convention 2017 (GRCon 2017) talk provided information on this integration.

https://github.com/geontech/gnuradio-redhawk

### XMidasBlueReader

This MATLAB class is a utility to progressively read through BLUE format files.

https://github.com/Geontech/XMidasBlueReader/

### Blue file version information 

- Gold (original, deprecated)
- BLUE 1.0
- BLUE 1.1 (current community standard)
- BLUE 2.0 / Platinum (a stricter variant / branch of BLUE)

(Within BLUE / Platinum, internal subtypes (TYPE = 1999, 2000, 3000, 4000, 5000, 6000))


### Blue file field information 

Blue file field information from https://lgsinnovations.github.io/sigfile/bluefile.js.html

ToDo - Determine version

 | Offset  |  Name      | Size |  Type      | Description                                |
 |:--------|:-----------|:-----|:-----------|:-------------------------------------------|
 |  0      |  version   | 4    |  char[4]   | Header version                             |
 |  4      |  head_rep  | 4    |  char[4]   | Header representation                      |
 |  8      |  data_rep  | 4    |  char[4]   | Data representation                        |
 | 12      |  detached  | 4    |  int_4     | Detached header                            |
 | 16      |  protected | 4    |  int_4     | Protected from overwrite                   |
 | 20      |  pipe      | 4    |  int_4     | Pipe mode (N/A)                            |
 | 24      |  ext_start | 4    |  int_4     | Extended header start, in 512-byte blocks  |
 | 28      |  ext_size  | 4    |  int_4     | Extended header size in bytes              |
 | 32      |  data_start| 8    |  real_8    | Data start in bytes                        |
 | 40      |  data_size | 8    |  real_8    | Data size in bytes                         |
 | 48      |  type      | 4    |  int_4     | File type code                             |
 | 52      |  format    | 2    |  char[2]   | Data format code                           |
 | 54      |  flagmask  | 2    |  int_2     | 16-bit flagmask (1=flagbit)                |
 | 56      |  timecode  | 8    |  real_8    | Time code field                            |
 | 64      |  inlet     | 2    |  int_2     | Inlet owner                                |
 | 66      |  outlets   | 2    |  int_2     | Number of outlets                          |
 | 68      |  outmask   | 4    |  int_4     | Outlet async mask                          |
 | 72      |  pipeloc   | 4    |  int_4     | Pipe location                              |
 | 76      |  pipesize  | 4    |  int_4     | Pipe size in bytes                         |
 | 80      |  in_byte   | 8    |  real_8    | Next input byte                            |
 | 88      |  out_byte  | 8    |  real_8    | Next out byte (cumulative)                 |
 | 96      |  outbytes  | 64   |  real_8[8] | Next out byte (each outlet)                |
 | 160     |  keylength | 4    |  int_4     | Length of keyword string                   |
 | 164     |  keywords  | 92   |  char[92]  | User defined keyword string                |
 | 256     |  Adjunct   | 256  |  char[256] | Type-specific adjunct union (See below for 1000 and 2000 type bluefiles)|
 
 Type-1000 Adjunct
 
 | Offset | Name | Size | Type | Description                      |
 :--------|:-----|:-----|:-----|:---------------------------------|
 |  0     |xstart| 8    |real_8| Abscissa value for first sample  |
 |  8     |xdelta| 8    |real_8| Abscissa interval between samples|
 | 16     |xunits| 4    | int_4| Units for abscissa values        |
 
 Type-2000 Adjunct

 | Offset | Name  | Size | Type | Description                          |
 |:-------|:------|:-----|:-----|:-------------------------------------|
 |  0     |xstart |  8   |real_8| Frame (column) starting value        |
 |  8     |xdelta |  8   |real_8| Increment between samples in frame   |
 | 16     |xunits |  4   |int_4 | Frame (column) units                 |
 | 20     |subsize|  4   |int_4 | Number of data points per frame (row)|
 | 24     |ystart |  8   |real_8| Abscissa (row) start                 |
 | 32     |ydelta |  8   |real_8| Increment between frames             |
 | 36     |yunits |  4   |int_4 | Abscissa (row) unit code             |



