# MIDIS Blue File Project Notes

## Overview

For an overview of the Midas Blue file format, refer to this topic in PySDR.

https://pysdr.org/content/iq_files.html#midas-blue-file-format

The 1.1 spec is available here.

https://web.archive.org/web/20150413061156/http://nextmidas.techma.com/nm/nxm/sys/docs/MidasBlueFileFormat.pdf

## Goal

Create a pyton script similar to this file to covert Blue 1.1 files to SigMF

https://github.com/IQEngine/IQEngine/blob/main/api/converters/vita49_to_sigmf/vita49.py

## ToDo

- Create python code
- Create unit tests

## Blue file version information 

- Gold (original, deprecated)
- BLUE 1.0
- BLUE 1.1 (current community standard)
- BLUE 2.0 / Platinum (a stricter variant / branch of BLUE)

(Within BLUE / Platinum, internal subtypes (TYPE = 1999, 2000, 3000, 4000, 5000, 6000))

## Tools and input streams

### XMidasBlueReader

This MATLAB class is a utility to progressively read through BLUE format files.

https://github.com/Geontech/XMidasBlueReader/

### RUST BlueJay reader

https://docs.rs/crate/bluefile/latest/source/src/bluejay.rs

#### 1.1 Blue test resource files

https://docs.rs/crate/bluefile/latest/source/resources/test/

```
Format-Hex sin.tmp
Path:
C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\bluefile-main\bluefile-main\resources\test\sin.tmp

           00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

00000000   42 4C 55 45 45 45 45 49 45 45 45 49 00 00 00 00  BLUEEEEIEEEI....
00000010   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000020   00 00 00 00 00 00 80 40 00 00 00 00 00 00 E0 40  ......@......à@
00000030   E8 03 00 00 53 44 00 00 00 00 00 00 00 00 00 00  è...SD..........
00000040   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000050   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000060   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000070   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000080   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000090   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
000000A0   13 00 00 00 56 45 52 3D 31 2E 31 00 49 4F 3D 58  ....VER=1.1.IO=X
000000B0   2D 4D 69 64 61 73 00 20 20 20 20 20 20 20 20 20  -Midas.
```

### Spectere

3db labs provides signal processing and analysis software such as Sceptre that saves IQ signals.

https://3db-labs.com/support/#customer-support

### REDHAWK

REDHAWK is a software-defined radio (SDR) framework designed to support the development, deployment, and management of real-time software radio applications.

It includes libaries such as blueFileLib.

https://github.com/RedhawkSDR/blueFileLib/blob/develop-2.0/cpp/src/HeaderControlBlock.cc

It is possible to intergrate REDHAWK with GNURadio. A GNURadio Convention 2017 (GRCon 2017) talk provided information on this integration.

https://github.com/geontech/gnuradio-redhawk

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


