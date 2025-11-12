#!/usr/bin/env python3

# Blue File converter with HCB and Extended Header Parsing
# This script reads and parses the HCB (Header Control Block) and
# extended header keywords from a Blue file format.
# It supports different file types and extracts metadata accordingly.
# Converts the extracted metadata into SigMF format.

# Author: Don Marshall (with help from AI!)
# Date: November 12, 2025

import os
import json
import struct
import hashlib
import numpy as np
from astropy.time import Time
from sigmf import SigMFFile # Assuming sigmf library is installed
from datetime import datetime, timezone


# --- HCB Layout (fixed fields up to adjunct) ---
HCB_LAYOUT = [
    ("version",   0,   4,  "4s",   "Header version"),
    ("head_rep",  4,   4,  "4s",   "Header representation"),
    ("data_rep",  8,   4,  "4s",   "Data representation"),
    ("detached",  12,  4,  "i",    "Detached header"),
    ("protected", 16,  4,  "i",    "Protected from overwrite"),
    ("pipe",      20,  4,  "i",    "Pipe mode (N/A)"),
    ("ext_start", 24,  4,  "i",    "Extended header start (512-byte blocks)"),
    ("ext_size",  28,  4,  "i",    "Extended header size in bytes"),
    ("data_start",32,  8,  "d",    "Data start in bytes"),
    ("data_size", 40,  8,  "d",    "Data size in bytes"),
    ("type",      48,  4,  "i",    "File type code"),
    ("format",    52,  2,  "2s",   "Data format code"),
    ("flagmask",  54,  2,  "h",    "16-bit flagmask"),
    ("timecode",  56,  8,  "d",    "Time code field"),
    ("inlet",     64,  2,  "h",    "Inlet owner"),
    ("outlets",   66,  2,  "h",    "Number of outlets"),
    ("outmask",   68,  4,  "i",    "Outlet async mask"),
    ("pipeloc",   72,  4,  "i",    "Pipe location"),
    ("pipesize",  76,  4,  "i",    "Pipe size in bytes"),
    ("in_byte",   80,  8,  "d",    "Next input byte"),
    ("out_byte",  88,  8,  "d",    "Next out byte (cumulative)"),
    ("outbytes",  96,  64, "8d",   "Next out byte (each outlet)"),
    ("keylength", 160, 4,  "i",    "Length of keyword string"),
    ("keywords",  164, 92, "92s",  "User defined keyword string"),
    # Adjunct starts at 256
]

# --- Extended header type map ---
TYPE_MAP = {
    "B": (np.int8,    1),
    "I": (np.int16,   2),
    "L": (np.int32,   4),
    "X": (np.int64,   8),
    "F": (np.float32, 4),
    "D": (np.float64, 8),
    "A": (np.dtype("S1"), 1),
}

SUPPORTED_TYPES = {'CI', 'CL', 'CF', 'SB', 'SI', 'SL', 'SX', 'SF', 'SD'}

HEADER_SIZE = 512
BLOCK_SIZE = 512

#  TODO: Look at this code and see if can be improved and possibly simplified. 
def detect_endian(data, layout, probe_fields=("data_size", "version")):
    """
    Detect endianness of a Bluefile header.

    Parameters
    ----------
    data : bytes
        Raw header data.
    layout : list of tuples
        HCB layout definition (name, offset, size, fmt, desc).
    probe_fields : tuple of str, optional
        Field names to test for sanity checks.
    Returns
    -------
    str
        "<" for little-endian or ">" for big-endian.
    """
    
    # TODO: handle both types of endianess 'EEEI' or IEEE and data rep and signal rep
    endianness = data[8:12].decode('utf-8') 
    print('Endianness: ', endianness)
    if endianness not in ('EEEI', 'IEEE'):
       raise ValueError(f"Unexpected endianness: {endianness}")    
    
    for endian in ("<", ">"):
        ok = True
        for name, offset, size, fmt, desc in layout:
            if name not in probe_fields:
                continue
            raw = data[offset:offset+size]
            try:
                val = struct.unpack(endian + fmt, raw)[0]
                # sanity checks
                MAX_DATA_SIZE_FACTOR = 100

                if name == "data_size":
                    if val <= 0 or val > len(data) * MAX_DATA_SIZE_FACTOR:
                        ok = False
                        break
                elif name == "version":
                    if not (0 < val < 10):  # expect small version number
                        ok = False
                        break
            except Exception:
                ok = False
                break
        if ok:
            return endian
    # fallback
    return "<"


def read_hcb(file_path):
    """Read HCB fields and adjunct block from a Blue file.

    Parameters
    ----------
    file_path : str
        Path to the Blue file.

    Returns
    -------
    dict
        Parsed HCB fields and adjunct metadata.
    """
    
    hcb = {}
    with open(file_path, "rb") as f:
        data = f.read(HEADER_SIZE)
        endian = detect_endian(data, HCB_LAYOUT)

        # Fixed fields
        for name, offset, size, fmt, desc in HCB_LAYOUT:
            raw = data[offset:offset+size]
            try:
                val = struct.unpack(endian + fmt, raw)[0]
            except struct.error:
                raise ValueError(f"Failed to unpack field {name} with endian {endian}")
            # Unpack based on format
            val = struct.unpack(endian+fmt, raw)[0]
            if isinstance(val, bytes):
                val = val.decode("ascii", errors="replace").strip("\x00 ")
            hcb[name] = val

        # Adjunct parsing
        ADJUNCT_OFFSET = 256
        f.seek(ADJUNCT_OFFSET)
        if hcb["type"] in (1000, 1001):
            hcb["adjunct"] = {
                "xstart": struct.unpack(f"{endian}d", f.read(8))[0],
                "xdelta": struct.unpack(f"{endian}d", f.read(8))[0],
                "xunits": struct.unpack(f"{endian}i", f.read(4))[0],
            }
        elif hcb["type"] == 2000:
            hcb["adjunct"] = {
                "xstart": struct.unpack(f"{endian}d", f.read(8))[0],
                "xdelta": struct.unpack(f"{endian}d", f.read(8))[0],
                "xunits": struct.unpack(f"{endian}i", f.read(4))[0],
                "subsize": struct.unpack(f"{endian}i", f.read(4))[0],
                "ystart": struct.unpack(f"{endian}d", f.read(8))[0],
                "ydelta": struct.unpack(f"{endian}d", f.read(8))[0],
                "yunits": struct.unpack(f"{endian}i", f.read(4))[0],
            }
        else:
            hcb["adjunct_raw"] = f.read(ADJUNCT_OFFSET)

    return hcb 


def parse_extended_header(file_path, hcb, endian="<"):
    """Parse extended header keyword records.

    Parameters
    ----------
    file_path : str
        Path to the Bluefile.
    hcb : dict
        Header Control Block containing 'ext_size' and 'ext_start'.
    endian : str, optional
        Endianness ('<' for little-endian, '>' for big-endian).

    Returns
    -------
    list of dict
        List of dictionaries containing parsed records.
    """
    if hcb["ext_size"] <= 0:
        return []
    entries = []
    with open(file_path, "rb") as f:
        f.seek(int(hcb["ext_start"]) * BLOCK_SIZE)
        bytes_remaining = int(hcb["ext_size"])
        while bytes_remaining > 0:
            lkey = struct.unpack(f"{endian}i", f.read(4))[0]
            lext = struct.unpack(f"{endian}h", f.read(2))[0]
            ltag = struct.unpack(f"{endian}b", f.read(1))[0]
            type_char = f.read(1).decode("ascii", errors="replace")

            dtype, bytes_per_element = TYPE_MAP.get(type_char, (np.dtype("S1"), 1))
            val_len = lkey - lext
            val_count = val_len // bytes_per_element if bytes_per_element else 0

            if type_char == "A":
                raw = f.read(val_len)
                if len(raw) < val_len:
                    raise ValueError("Unexpected end of extended header")
                value = raw.rstrip(b"\x00").decode("ascii", errors="replace")
            else:
                value = np.frombuffer(f.read(val_len), dtype=dtype, count=val_count)
                if value.size == 1:
                    value = value[0]
                else:
                    value = value.tolist()

            tag = f.read(ltag).decode("ascii", errors="replace") if ltag > 0 else ""

            total = 4+2+1+1+val_len+ltag
            pad = (8 - (total % 8)) % 8
            if pad: f.read(pad)

            entries.append({
                "tag": tag, "type": type_char, "value": value,
                "lkey": lkey, "lext": lext, "ltag": ltag
            })
            bytes_remaining -= lkey

    return entries


def parse_data_values(file_path,hcb,endianess):
    """
    Parse key HCB values used for further processing.

    Parameters
    ----------
    file_path : str
        Path to the Blue file.
    hcb : dict
        Header Control Block dictionary.
    endianess : str
        Endianness ('<' for little-endian, '>' for big-endian).

    Returns
    -------
    numpy.ndarray
        Parsed samples.
    """

    
    print("===== Parsing blue file data values =====")
    with open(file_path, "rb") as f:
        data = f.read(HEADER_SIZE)
        if len(data) < HEADER_SIZE:
            raise ValueError("Incomplete header")
        dtype = data[52:54].decode('utf-8') # eg 'CI', 'CF', 'SD'
        print('Data type: ', dtype)
        if dtype not in SUPPORTED_TYPES:
            raise ValueError(f"Unsupported data type: {dtype}")

        time_interval = np.frombuffer(data[264:272], dtype=np.float64)[0]
        if time_interval <= 0:
            raise ValueError(f"Invalid time interval: {time_interval}")
        sample_rate = 1/time_interval
        print('Sample rate: ', sample_rate/1e6, 'MHz')
        extended_header_data_size = int.from_bytes(data[28:32], byteorder='little')
        filesize = os.path.getsize(file_path)
        print('File size: ', filesize)

    # Determine destination path for SigMF data file
    dest_path = file_path.rsplit(".",1)[0]
  
    # Complex data parsing

    # complex 16-bit integer  IQ data > ci16_le in SigMF
    if dtype == 'CI':
      elem_size = np.dtype(np.int16).itemsize
      elem_count = (filesize - extended_header_data_size) // elem_size
      raw_samples = np.fromfile(file_path, dtype=np.int16, offset=HEADER_SIZE, count=elem_count)
    # Reassemble interleaved IQ samples
      samples = raw_samples[::2] + 1j*raw_samples[1::2] # convert to IQIQIQ...
    # Normalize samples to -1.0 to +1.0 range
      samples = samples.astype(np.float32)  / 32767.0
    # Save out as SigMF IQ data file
      samples.tofile(f"{dest_path}.sigmf-data")
    
    # complex 32-bit integer  IQ data > ci32_le in SigMF
    if dtype == 'CL':
      elem_size = np.dtype(np.int32).itemsize
      elem_count = (filesize - extended_header_data_size) // elem_size
      raw_samples = np.fromfile(file_path, dtype=np.int32, offset=HEADER_SIZE, count=elem_count)
    # Reassemble interleaved IQ samples
      samples = raw_samples[::2] + 1j*raw_samples[1::2] # convert to IQIQIQ...
    # Normalize samples to -1.0 to +1.0 range
      samples = samples.astype(np.float32) / 2147483647.0
    # Save out as SigMF IQ data file
      samples.tofile(f"{dest_path}.sigmf-data")

    # complex 32-bit float  IQ data > cf32_le in SigMF
    if dtype == 'CF':
      # Each complex sample is 8 bytes total (2 × float32), so np.complex64 is appropriate
      # No need to reassemble IQ — already complex
      elem_size=np.dtype(np.complex64).itemsize  # Will be 8 bytes
      elem_count = (filesize - extended_header_data_size) // elem_size
      samples = np.fromfile(file_path, dtype=np.complex64, offset=HEADER_SIZE, count=elem_count)
    # Save out as SigMF IQ data file
      samples.tofile(f"{dest_path}.sigmf-data")
     
    # Scalar data parsing

    # Scalar data parsing > ri8_le in SigMF
    if dtype == 'SB': 
      elem_size=np.dtype(np.int8).itemsize 
      elem_count = (filesize - extended_header_data_size) // elem_size
      samples = np.fromfile(file_path, dtype=np.int8, offset=HEADER_SIZE, count=elem_count)
    # Normalize samples to -1.0 to +1.0 range
      samples = samples.astype(np.float32)  / 127.0
    # Save out as SigMF IQ data file
      samples.tofile(f"{dest_path}.sigmf-data")

    # Scalar data parsing > ri16_le in SigMF
    if dtype == 'SI': 
      elem_size = np.dtype(np.int16).itemsize
      elem_count = (filesize - extended_header_data_size) // elem_size
      samples = np.fromfile(file_path, dtype=np.int16, offset=HEADER_SIZE, count=elem_count)
    # Normalize samples to -1.0 to +1.0 range
      samples = samples / 32767.0
    # Save out as SigMF IQ data file
      samples.tofile(f"{dest_path}.sigmf-data")

    # Scalar data parsing > ri32_le in SigMF
    if dtype == 'SL':
      elem_size=np.dtype(np.int32).itemsize 
      elem_count = (filesize - extended_header_data_size) // elem_size
      samples = np.fromfile(file_path, dtype=np.int32, offset=HEADER_SIZE, count=elem_count)
    # Normalize samples to -1.0 to +1.0 range
      samples = samples / 2147483647.0
    # Save out as SigMF IQ data file
      samples.tofile(f"{dest_path}.sigmf-data")

    # Scalar data parsing > ri64_le in SigMF
    if dtype == 'SX':
      elem_size=np.dtype(np.int64).itemsize 
      elem_count = (filesize - extended_header_data_size) // elem_size
      samples = np.fromfile(file_path, dtype=np.int64, offset=HEADER_SIZE, count=elem_count)
    # Save out as SigMF IQ data file
      samples.tofile(f"{dest_path}.sigmf-data")

    # Scalar data parsing > rf32_le in SigMF
    if dtype == 'SF':
      elem_size=np.dtype(np.float32).itemsize 
      elem_count = (filesize - extended_header_data_size) // elem_size
      samples = np.fromfile(file_path, dtype=np.float32, offset=HEADER_SIZE, count=elem_count)
    # Save out as SigMF IQ data file
    samples.tofile(f"{dest_path}.sigmf-data")

    # Scalar data parsing > rf64_le in SigMF
    if dtype == 'SD':
      elem_size=np.dtype(np.float64).itemsize 
      elem_count = (filesize - extended_header_data_size) // elem_size
      samples = np.fromfile(file_path, dtype=np.float64, offset=HEADER_SIZE, count=elem_count)
    # Save out as SigMF IQ data file
    samples.astype(np.complex64).tofile(f"{dest_path}.sigmf-data")

# TODO: validate handling of scalar types - Reshape per mathlab port shown here?

    """

        # Save out as SigMF IQ data file
    if dtype in ("CI", "CL", "CF"):
        # Complex IQ data → save as cf32_le
        samples.astype(np.complex64).tofile(f"{dest_path}.sigmf-data")
    else:
        # Scalar data → save in native dtype
        samples.tofile(f"{dest_path}.sigmf-data")
    """

# TODO: validate handling of scalar types - Reshape per mathlab port shown here?

    """
            fmt_size_char = self.hcb["format"][0]
            fmt_type_char = self.hcb["format"][1]

            elementsPerSample = self.FormatSize(fmt_size_char)
            print('Elements Per Sample', elementsPerSample/1e6)
            elem_count_per_sample = (
                np.prod(elementsPerSample) if isinstance(elementsPerSample, (tuple, list)) else elementsPerSample
            )

            dtype_str, elem_bytes = self.FormatType(fmt_type_char)
            bytesPerSample = int(elem_bytes) * int(elem_count_per_sample)

            bytesRead = int(self.dataOffset - self.hcb["data_start"])
            bytes_remaining = int(self.hcb["data_size"] - bytesRead)

    """

   # Return the IQ data if needed for further processing if needed 
    return samples


def blue_to_sigmf(hcb, ext_entries, file_path):
    """
    Build a SigMF metadata dict from parsed Bluefile HCB and extended header.

    Parameters
    ----------
    hcb : dict
        Header Control Block from read_hcb().
    ext_entries : list of dict
        Parsed extended header entries from parse_extended_header().
    data_path : str
        Path to the .sigmf-data file.
    Returns
    -------
    dict
        SigMF metadata structure.

    Raises
    ------
    ValueError
        If required fields are missing or invalid.
    """

    # Helper to look up extended header values by tag
    def get_tag(tag):
        for e in ext_entries:
            if e["tag"] == tag:
                return e["value"]
        return None

# S - Scalar
# C-  Complex
# V - Vector
# Q-  Quad - TODO: Pri 2 - Add support for other types if they are commonly used.

# B: 8-bit integer
# I: 16-bit integer
# L: 32-bit integer
# X: 64-bit integer
# F: 32-bit float
# D: 64-bit float

    # --- Global datatype object - little endian---
    datatype_map_le = {
        "SB": "ri8_le",
        "SI": "ri16_le",
        "SL": "ri32_le",
        "SX": "ri64_le",
        "SF": "rf32_le",
        "SD": "rf64_le",
        "CB": "ci8_le",
        "CI": "ci16_le",
        "CL": "ci32_le",
        "CX": "ci64_le",
        "CF": "cf32_le",
        "CD": "cf32_le",
    }

    # --- Global datatype object - big endian---
    datatype_map_be = {
        "SB": "ri8_be",
        "SI": "ri16_be",
        "SL": "ri32_be",
        "SX": "ri64_be",
        "SF": "rf32_be",
        "SD": "rf64_be",
        "CB": "ci8_be",
        "CI": "ci16_be",
        "CL": "ci32_be",
        "CX": "ci64_be",
        "CF": "cf32_be",
        "CD": "cf32_be",
    }


    # header data representation  : 'EEEI' or 'IEEE' # Little or big data endianess representation
    header_rep = hcb.get("head_rep")

    # data_rep  : 'EEEI' or 'IEEE' # Little or big data endianess representation
    data_rep = hcb.get("data_rep")

    # data_format : For example 'CI'  or 'SD'  Data format code - real or complex, int or float
    data_format = hcb.get("format")
            
    if data_rep == "EEEI": # Little Endian
        data_map = datatype_map_le.get(data_format)
    
    elif data_rep == "IEEE": # Big Endian
        data_map = datatype_map_be.get(data_format)
    
    datatype = data_map if data_map is not None else "unknown"

    print(f"Determined SigMF datatype: {datatype} and data representation: {data_rep}")

    # Sample rate: prefer adjunct.xdelta, else extended header SAMPLE_RATE
    if "adjunct" in hcb and "xdelta" in hcb["adjunct"]:
        sample_rate = 1.0 / hcb["adjunct"]["xdelta"]
    else:
        sr = get_tag("SAMPLE_RATE")
        sample_rate = float(sr) if sr is not None else None

    # For now define static values. Perhaps take as JSON input 
    hardware_description = "Blue File Conversion - Unknown Hardware"
    blue_author = "Blue File Conversion - Unknown Author"
    blue_licence = "Blue File Conversion - Unknown License"

    if "outlets"in hcb and hcb["outlets"] > 0:
        channelNumber = int(hcb["outlets"])
    else:    
       channelNumber = 1
    
    # --- Base Global Metadata ---
    global_md = {
        "core:author": blue_author,
        "core:datatype": datatype,
        "core:description": hcb.get("keywords", ""),
        "core:hw": hardware_description,
        "core:license": blue_licence,
        "core:num_channels":channelNumber,
        "core:sample_rate": sample_rate,
        "core:version": "1.0.0",
    }

    for name, _, _, _, desc in HCB_LAYOUT:
        # hcb_annotation[f"blue:hcb_{name}"] = hcb[name]
        value = hcb.get(name)             # safe access
        if value is None:
            continue                      # or set a default
        global_md[f"core:blue_hcb_{name}"] = value

    # --- Merge adjunct fields ---
    adjunct = hcb.get("adjunct", {})    
    for key, value in adjunct.items():
        global_md[f"core:blue_adjunct_header_{key}"] = value   

    # --- Merge extended header fields ---
    for e in ext_entries:
        name = e.get("tag")
        if name is None:
           continue
        key = f"core:blue_extended_header_{name}"
        value = e.get("value")
        if hasattr(value, "item"):
            value = value.item()
        global_md[key] = value
  
    # Convert the datetime object to an ISO 8601 formatted string
    epoch_time_raw = int(hcb.get("timecode", 0))

    # Adjust for Bluefile POSIX epoch (1950 vs 1970)
    bluefile_epoch_offset = 631152000  # seconds between 1950 and 1970
    epoch_time = epoch_time_raw - bluefile_epoch_offset

    dt_object_utc = datetime.fromtimestamp(epoch_time, tz=timezone.utc)
    # Format with milliseconds and Zulu suffix
    iso_8601_string = dt_object_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    print(f"Epoch time: {epoch_time}")
    print(f"ISO 8601 time: {iso_8601_string}")

    # --- Captures array ---
    captures = [{
        "core:datetime": iso_8601_string,
        "core:frequency": float(get_tag("RF_FREQ") or 0.0),
        "core:sample_start": 0,
    }]

    # compute SHA‑512 hash of data file
    def compute_sha512(path, bufsize=1024*1024):
        """Compute SHA-512 hash of a file in chunks."""
        
        h = hashlib.sha512()
        with open(path, "rb") as f:
            while chunk := f.read(bufsize):
                h.update(chunk)
        return h.hexdigest()

    # Strip the extension from the original file path
    base_file_name = os.path.splitext(file_path)[0]

    # Build the .sigmf-data path
    data_file_path = base_file_name + ".sigmf-data"

    # Compute SHA-512 of the data file
    data_sha512 = compute_sha512(data_file_path)   # path to the .sigmf-data file
    global_md["core:sha512"] = data_sha512

    # --- Annotations array ---
    datatype_sizes = {
        "ri8_le": 1,
        "ri16_le": 2,
        "ri32_le": 4,
        "ci16_le": 4,
        "ci32_le": 8,
        "cf32_le": 8,
        "rf32_le": 4,
        "rf64_le": 8,
        "ri64_le": 8,
        "ri8_be": 1,
        "ri16_be": 2,
        "ri32_be": 4,
        "ci16_be": 4,
        "ci32_be": 8,
        "cf32_be": 8,
        "rf32_be": 4,
        "rf64_be": 8,
        "ri64_be": 8,
    }

    # Calculate sample count
    data_size = int(hcb.get("data_size", 0))
    if datatype not in datatype_sizes:
        raise ValueError(f"Unsupported datatype {datatype}")
    bytes_per_sample = datatype_sizes[datatype]
    sample_count = int(data_size // bytes_per_sample)

    annotations = [{
        "core:sample_start": 0,
        "core:sample_count": sample_count,
        "core:freq_upper_edge": float(get_tag("RF_FREQ") or 0.0) + float(get_tag("SBT_BANDWIDTH") or 0.0),
        "core:freq_lower_edge": float(get_tag("RF_FREQ") or 0.0),
        "core:label": "Sceptere"
    }]

    # --- Final SigMF object ---
    sigmf = {
        "global": global_md,
        "captures": captures,
        "annotations": annotations,
    }

    # Write .sigmf-meta file
    base_file_name = os.path.splitext(file_path)[0]
    meta_path = base_file_name + ".sigmf-meta"
    
    with open(meta_path, "w") as f:
        json.dump(sigmf, f, indent=2)
    print(f"==== Wrote SigMF metadata to {meta_path} ====")

    return sigmf


def blue_file_to_sigmf(file_path):
    """
    Convert a MIDIS Bluefile to SigMF metadata and data.

    Parameters
    ----------
    file_path : str
        file_path to the Blue file.

    Returns
    -------
    samples : numpy.ndarray
        IQ Data.
    """

    print("==========================================")
    print("===== Starting blue file processing =====")
    print("==========================================")

    # Read Header control block (HCB) from blue file to determine how to process the rest of the file
    hcb = read_hcb(file_path) 

    print("=== Header Control Block (HCB) Fields ===")
    for name, _, _, _, desc in HCB_LAYOUT:
        print(f"{name:10s}: {hcb[name]!r}  # {desc}")

    print("\n=== Adjunct Header ===")
    print(hcb.get("adjunct", hcb.get("adjunct_raw")))

    # data_rep  : 'EEEI' or 'IEEE' # Little or big extended header endianess representation
    extended_header_endianess = hcb.get("head_rep")
    
    if extended_header_endianess == "EEEI":
        ext_endianess = "<"   # little-endian
    elif extended_header_endianess == "IEEE":
        ext_endianess = ">"   # big-endian
    else:
        raise ValueError(f"Unknown head_rep value: {extended_header_endianess}")

    # Parse extended header entries
    ext = parse_extended_header(file_path, hcb, ext_endianess)
    print("\n=== Extended Header Keywords ===")
    for e in ext:
        print(f"{e['tag']:20s}:{e['value']}")
    print(f"Total extended header entries: {len(ext)}")

   # data_rep  : 'EEEI' or 'IEEE' # Little or big data endianess representation
    data_rep_endianess = hcb.get("data_rep")
    data_endianess = "<" if data_rep_endianess == "EEEI" else ">"
 
    # Parse key data values    
    # iq_data will be available if needed for further processing.
    try:
        iq_data = parse_data_values(file_path, hcb, data_endianess)
    except Exception as e:
        raise RuntimeError(f"Failed to parse data values: {e}")

    # Call the SigMF conversion for metadata generation 
    blue_to_sigmf(hcb, ext, file_path)

    # Return the IQ data if needed for further processing if needed 
    return iq_data

if __name__ == "__main__":
    # Main calls blue_file_to_sigmf to convert dump blue file contents to SigMF.
    # TODO: Add input args for file name - cdif or .tmp files
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("blue_file")
    # TODO: Uncomment for passing input args for file name - cdif or .tmp files
    # args = parser.parse_args()
    # TODO: Add input args for file name - cdif or .tmp files
    file_path = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\SceptreTestFile1.cdif'
    # file_path = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\RustBlueTestFiles\pulse_cx.tmp'
    # file_path = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\RustBlueTestFiles\sin.tmp' 
    # file_path = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\RustBlueTestFiles\penny.prm' 
    # file_path = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\RustBlueTestFiles\keyword_test_file.tmp' 
    # file_path = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\RustBlueTestFiles\lots_of_keywords.tmp'
    try:
        blue_file_to_sigmf(file_path)
        print("DONE")
    except Exception as e:
        print(f"Processing failed: {e}")

