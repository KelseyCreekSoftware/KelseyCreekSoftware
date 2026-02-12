# Signal Hound Spike IQ Project Notes

*Updated 2-12-2026*

## Code status

- Have moved stand alone code into local copy of sigmf code tree to integrate into convert command line __main__.py.
- Have reviewed all 1408 lines of sigmffile.py to better understand intergration when coding a converter.
- Converter docs are at: https://sigmf.readthedocs.io/en/latest/converters.html
- Need to locate multi channel IQ file to see how it is structured and determine how to convert to SigMF archive format.

## Resources

Spike-User-Manual.pdf - https://signalhound.com/sigdownloads/Spike/Spike-User-Manual.pdf

A GNU Radio OOT module for Signal Hound Devices - gr-signal-hound 

https://github.com/SignalHound/gr-signal-hound

## XML Signal Attributes

Validate:

* DataType – Should be Complex Short indicating the binary format of the binary IQ file. 

Convert and Store:

* CenterFrequency of data capture, for example 100000000.000
* SampleCount – Number of IQ values stored in the IQ binary file.
* EpochNanos – Nanoseconds elapsed since January 1, 1970 to the first sample in the IQ waveform 
acquisition.  Unix epoch timestamp. 
* DeviceType – Signa Hound device type, for example BB60C
* SampleRate – Sample rate in Hz, of the IQ waveform acquisition. 

Annotations:
* IFBandwidth – Cutoff frequency of the IQ bandpass filter. 
* ScaleFactor – Used to scale the IQ data from full scale to mW. 
* Decimation – Power of two integer value representing the decimation rate of the IQ waveform 
from the full sample rate of the receiver. For example, 40MS/s for the BB60C 
* ReferenceLevel – The reference level, in dBm, set in the Spike software for the acquisition. 

* SerialNumber – Serial number of the device used in acquisition. 
* IQFileName – Full file path of the IQ binary file saved by the Spike software on the originating system. 

Notes on data conversion from the Spike User Manual

The binary file contains SampleCount signed 16-bit IQ values. The binary file has little-endian byte 
ordering. Samples are stored in sequential order as: 

`I1, Q1, I2, Q2 … In, Qn` 

The values are stored as full scale, ranging from -32768 to +32767 representing floating point values 
between -1.0 and 1.0. To recover the original values, perform the following steps.

1) Read in the binary file to signed 16-bit complex values. 
2) Convert the full scale 16-bit I and Q integer values into floating point values in the range of -1.0 to 
+1.0. 
3) Multiply each I and Q value by the inverse of the scale factor in the XML file. 
4) The IQ samples should now be scaled to mW, where I2 + Q2 = mW.
 
## Experimental Code

*Note: Many ToDo's and basic issues to work on*

### Updates to convert  `__main__.py`

One idea for convert integration is to add a --signalhound option as shown below.

A better aproach may be update MagicBytes to parse the Signal Hound XML for the string `<SignalHoundIQFile Version="1.0">`. 

```python
# Copyright: Multiple Authors
#
# This file is part of sigmf-python. https://github.com/sigmf/sigmf-python
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unified converter for non-SigMF file formats"""

import argparse
import logging
import textwrap
from pathlib import Path

from .. import __version__ as toolversion
from ..error import SigMFConversionError
from ..utils import get_magic_bytes
from .blue import blue_to_sigmf
from .wav import wav_to_sigmf
from .signalhound import signalhound_to_sigmf



def main() -> None:
    """
    Unified entry-point for SigMF conversion of non-SigMF recordings.

    This command-line interface converts various non-SigMF file formats into SigMF-compliant datasets.
    It currently supports WAV and BLUE/Platinum file formats.
    The converter detects the file type based on magic bytes and invokes the appropriate conversion function.

    By default it will output a SigMF pair (.sigmf-meta and .sigmf-data).

    Converter Processing Pattern
    ----------------------------
    if out_path is None:
        create_ncd = True
    <create global_info and capture_info>
    if create_ncd:
        <create Non-Conforming Dataset (NCD) with .sigmf-meta only>
        if out_path:
            <write out_path.sigmf-meta>
        return SigMFFile
    if create_archive:
        with TemporaryDirectory() as temp_dir:
            <write .sigmf-data>
        <write out_path.sigmf>
    else:
        <write out_path.sigmf-data>
        <write out_path.sigmf-meta>
    return SigMFFile
    """
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(main.__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="sigmf_convert",
    )
    parser.add_argument("input", type=str, help="Input recording path")
    parser.add_argument("output", type=str, help="Output SigMF path (no extension)")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity level")
    exclusive_group = parser.add_mutually_exclusive_group()
    exclusive_group.add_argument("-a", "--archive", action="store_true", help="Output .sigmf archive only")
    exclusive_group.add_argument(
        "--ncd", action="store_true", help="Output .sigmf-meta only and process as a Non-Conforming Dataset (NCD)"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s v{toolversion}")
    ## TODO: Determine proper way to integrate Signal Hound files
    parser.add_argument("--signalhound", action="store_true", help="Convert a Signal Hound file pair to SigMF - provide XML file as input")
    args = parser.parse_args()

    level_lut = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }
    logging.basicConfig(level=level_lut[min(args.verbose, 2)])

    input_path = Path(args.input)
    output_path = Path(args.output)

    # for ncd check that input & output files are in same directory
    if args.ncd and input_path.parent.resolve() != output_path.parent.resolve():
        raise SigMFConversionError(
            f"NCD files must be in the same directory as input file. "
            f"Input: {input_path.parent.resolve()}, Output: {output_path.parent.resolve()}"
        )

    # check that the output path is a file and not a directory
    if output_path.is_dir():
        raise SigMFConversionError(f"Output path must be a filename, not a directory: {output_path}")

    ## TODO: Determine proper way to integrate Signal Hound files
    # First approach to integrate Signal Hound files
    if args.signalhound:
        _ = signalhound_to_sigmf(
            signalhound_path=input_path,
            out_path=output_path,
            create_archive=args.archive,
            create_ncd=args.ncd,
        )
        return

    # detect file type using magic bytes (same logic as fromfile())
    magic_bytes = get_magic_bytes(input_path, count=4, offset=0)

    if magic_bytes == b"RIFF":
        # WAV file
        _ = wav_to_sigmf(wav_path=input_path, out_path=output_path, create_archive=args.archive, create_ncd=args.ncd)

    elif magic_bytes == b"BLUE":
        # BLUE file
        _ = blue_to_sigmf(blue_path=input_path, out_path=output_path, create_archive=args.archive, create_ncd=args.ncd)

    else:
        raise SigMFConversionError(
            f"Unsupported file format. Magic bytes: {magic_bytes}. "
            f"Supported formats for conversion are WAV and BLUE/Platinum."
        )


if __name__ == "__main__":
    main()
```


### Launch JSON for debugging

Current Launch JSON for debugging

```python
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug SigMF Converter",
            "type": "python",
            "request": "launch",
            "module": "sigmf.convert",
            "args": [
                "C:\\Data1\\Ham_Radio\\SDR\\signalhound_to_sigmf_converter\\IQREC-11-13-25-17h31m10s877.xml",
                "C:\\Data1\\Ham_Radio\\SDR\\signalhound_to_sigmf_converter\\convertedsignahoundfile",
                "--signalhound"
            ],
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```


### Very rough converter code

*Some code is being retained to see if it will help with multi channel files in the future.*

```python
# Copyright: Multiple Authors
#
# This file is part of sigmf-python. https://github.com/sigmf/sigmf-python
#
# SPDX-License-Identifier: LGPL-3.0-or-later
# last updated 1-27-26

"""converter for signalhound files to SigMF format."""

import os
import json
import io
import logging
import tempfile
from pathlib import Path
import hashlib
import numpy as np
from datetime import datetime, timezone, timedelta

import xml.etree.ElementTree as ET
from typing import Optional

from .. import SigMFFile
from ..error import SigMFConversionError

from .. import __version__ as toolversion
from .. import fromfile
from ..sigmffile import get_sigmf_filenames
from ..utils import SIGMF_DATETIME_ISO8601_FMT

log = logging.getLogger()

# Define constants for Spike
ENDIANNESS = "<"
DATATYPE = "ci16_le"  # complex short int16 little-endian
# DATATYPE_SIZE = 4  # bytes per complex int16 sample (2 bytes I + 2 bytes Q)


def _to_float(x)  -> Optional[float]:
    """Convert value to float, return None if invalid."""
    try:
        return float(x)
    except Exception:
        return None


def _to_int(x) -> Optional[int]:
    """Convert value to int, return None if invalid."""
    try:
        return int(float(x))
    except Exception:
        return None


def _parse_preview_trace(text) -> list[float]:
    """Parse PreviewTrace string into list of floats."""
    if text is None:
        return []
    s = text.strip()
    if s.endswith(","):
        s = s[:-1]
    if not s:
        return []
    parts = [p.strip() for p in s.split(",") if p.strip() != ""]
    # return both list and numpy array if caller wants either
    vals = []
    for p in parts:
        try:
            vals.append(float(p))
        except Exception:
            # skip malformed entries
            continue
    return vals


def spike_to_sigmf_metadata(xml_file_path) -> dict:
    """
    Build a SigMF metadata file the spike xml file.

    Parameters
    ----------
    xml_file_path : str
        Path to the spike xml file.
    Returns
    -------
    dict
        SigMF metadata structure.

    Raises
    ------
    SigMFConversionError
        If required fields are missing or invalid.
    """
    log.info("===== Converting Spike XML metadata to SigMF format =====")

    xml_path = Path(xml_file_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    def text_of(tag) -> Optional[str]:
        el = root.find(tag)
        return el.text.strip() if (el is not None and el.text is not None) else None

    # TODO: Determine if data dictionary is best structure for this data 
 
    md = {}
    # Signal Hound data elements
    for tag in (
        "DeviceType",
        "SerialNumber",
        "DataType",
        "ReferenceLevel",
        "CenterFrequency",
        "SampleRate",
        "Decimation",
        "IFBandwidth",
        "ScaleFactor",
        "IQFileName",
        "EpochNanos",
        "SampleCount",
        "PreviewTrace",
    ):
        md[f"{tag}_raw"] = text_of(tag)
    
    # Optional log.info of data for debug >> 
    # log.info(md)

    # TODO: Consider additonal data type conversion and validation
    
    # Typed fields / normalized
    md["DataType"] = md.pop("DataType_raw")
    md["DeviceType"] = md.pop("DeviceType_raw")
    md["CenterFrequency"] = _to_float(md.pop("CenterFrequency_raw"))
    md["SampleCount"] = _to_int(md.pop("SampleCount_raw"))
    md["SampleRate"] = _to_float(md.pop("SampleRate_raw"))
    md["EpochNanos"] = _to_int(md.pop("EpochNanos_raw"))
    # Will be added as comments or annotations
    md["ReferenceLevel"] = _to_float(md.pop("ReferenceLevel_raw"))
    md["Decimation"] = _to_int(md.pop("Decimation_raw"))
    md["IFBandwidth"] = _to_float(md.pop("IFBandwidth_raw"))
    md["ScaleFactor"] = _to_float(md.pop("ScaleFactor_raw"))
    md["SerialNumber"] = md.pop("SerialNumber_raw")
    md["IQFileName"] = md.pop("IQFileName_raw")

    # PreviewTrace: list of floats and numpy array
    # TODO: Confirm np.int16 data type for preview data elements.
    preview_raw = text_of("PreviewTrace")
    md["PreviewTrace_list"] = _parse_preview_trace(preview_raw)
    md["PreviewTrace_array"] = np.array(md["PreviewTrace_list"], dtype=np.int16)

    # Create a reference to the spike XML data 
    spike_xml = md

    # Check datatype mapping based on Spike XML DataType field - should be "Complex Short"
    spike_data_type = spike_xml.get("DataType")

    if spike_data_type == "Complex Short":
        data_type= "ci16_le"  # complex int16 little-endian
    else:
        raise SigMFConversionError(f"Unsupported Spike DataType: {spike_data_type}")
 
    device_type = spike_xml.get("DeviceType")
    hardware_description = (
        device_type if device_type is not None else "Signal Hound Device"
    )

    # Strip the extension from the original file path
    base_file_name = os.path.splitext(xml_file_path)[0]

    # Build the .iq file path for data file
    data_file_path = base_file_name + ".iq"

    # Calculate sample count using the original IQ data file size
    filesize = os.path.getsize(data_file_path)
    # TODO: Fix this!
    filesize= 21045
    log.info("File size: %d", filesize)

    # complex 16-bit integer  IQ data > ci16_le in SigMF
    elem_size = np.dtype(np.int16).itemsize

    # Each complex sample = 2 int16 (I,Q)
    frame_bytes = 2 * elem_size
    
    # TODO: Fix this commented code or remove
    # if filesize % frame_bytes != 0:
    #     raise SigMFConversionError(f"File size {filesize} not divisible by {frame_bytes}; partial sample present")
    
    # Each complex sample = 2 int16 (I,Q)
    sample_count = filesize // frame_bytes

    log.info(f"Sample count: {sample_count}")
   
    # For now define static values. Perhaps take as JSON or command arg input in the future.
    spike_author = "Spike File Conversion - Unknown Author"
    spike_licence = "Spike File Conversion - Unknown License"
    spike_description = "Signal Hound Spike Zero Span File converted to SigMF format"

    # TODO: Confirm Zero Span Spike files are single channel
    channel_number = 1

    # TODO: see if this can be simplified and add error checking
    # Convert the datetime object to an ISO 8601 formatted string
    epoch_time = spike_xml.get("EpochNanos")
    if epoch_time is None:
            raise SigMFConversionError("Missing EpochNanos in Spike XML");
    
    epoch_time = int(epoch_time)
    secs = epoch_time // 1_000_000_000
    rem_ns = epoch_time % 1_000_000_000
    dt_object_utc = datetime.fromtimestamp(secs, tz=timezone.utc) + timedelta(
        microseconds=rem_ns / 1000
    )
    # Format with milliseconds and Zulu suffix for SigMF    
    iso_8601_string = dt_object_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    log.info(f"Epoch time: {epoch_time}")
    log.info(f"ISO 8601 time: {iso_8601_string}")

    # --- Base Global Metadata ---
    global_md = {
        "core:author": spike_author,
        "core:datatype": data_type,
        "core:description": spike_description,
        "core:hw": hardware_description,
        "core:license": spike_licence,
        "core:num_channels": channel_number,
        "core:sample_rate": spike_xml.get("SampleRate"),
        "core:version": "1.0.0",
        "core:spike_ReferenceLevel": spike_xml.get("ReferenceLevel"),
        "core:spike_Decimation": spike_xml.get("Decimation"),
        "core:spike_IFBandwidth": spike_xml.get("IFBandwidth"),
        "core:spike_ScaleFactor": spike_xml.get("ScaleFactor"),
        "core:spike_IQFileName": spike_xml.get("IQFileName"),
    }

    # --- Captures array ---
    captures = [
        {
            "core:datetime": iso_8601_string,
            "core:frequency": float(spike_xml.get("CenterFrequency")),
            "core:sample_start": 0,
        }
    ]

    # compute SHA‑512 hash of data file
    def compute_sha512(path, bufsize=1024 * 1024) -> str:
        """Compute SHA-512 hash of a file in chunks."""

        h = hashlib.sha512()
        with open(path, "rb") as f:
            while chunk := f.read(bufsize):
                h.update(chunk)
        return h.hexdigest()

    # Compute SHA-512 of the data file
    # TODO: Determine if we need to hash the .iq or .sigmf-data file - check blue.py code
    # TODO: Do we need to even recreate the .sigmf-data file
    data_sha512 = compute_sha512(data_file_path)  # path to the .sigmf-data file
    global_md["core:sha512"] = data_sha512

    # TODO: Confirm freq_upper_edge and  lower_frequency_edge calculations - is this correct for Spike files? ScaleFactor? Mhz? /2?
    center = float(spike_xml.get("CenterFrequency") or 0.0)
    bandwidth = float(spike_xml.get("IFBandwidth") or 0.0)
    upper_frequency_edge = center + (bandwidth / 2.0)
    lower_frequency_edge = center - (bandwidth / 2.0)

    # --- Create annotations array using calculated values---
    annotations = [
        {
            "core:sample_start": 0,
            "core:sample_count": sample_count,
            "core:freq_upper_edge": upper_frequency_edge,
            "core:freq_lower_edge": lower_frequency_edge,
            "core:label": "Spike",
        }
    ]

    # --- Final SigMF object ---
    sigmf = {
        "global": global_md,
        "captures": captures,
        "annotations": annotations,
    }

    # Write .sigmf-meta file
    base_file_name = os.path.splitext(xml_file_path)[0]
    meta_path = base_file_name + ".sigmf-meta"

    with open(meta_path, "w") as f:
        json.dump(sigmf, f, indent=2)
        log.info(f"==== Wrote SigMF metadata to {meta_path} ====")

    return sigmf


def convert_iq_data(xml_file_path, sigmfObj=None) -> np.ndarray:
    """
    Convert IQ data in .iq file to SigMF based on values in Zero Span XML file.

     Parameters
     ----------
     xml_file_path : str
         Path to the spike zero span XML file.
     sigmfObj : SigMFFile
         SigMF object with metadata information.
 
     Returns
     -------
     numpy.ndarray
         Parsed samples.
    """

    log.info("===== Parsing spike file data values =====")
    base_file_name = os.path.splitext(xml_file_path)[0]
    iq_file_path = base_file_name + ".iq"
    filesize = os.path.getsize(iq_file_path)
    log.info(f"File size: {filesize}")
  

    # Determine destination path for SigMF data file
    dest_path = xml_file_path.rsplit(".", 1)[0]

    # complex 16-bit integer  IQ data > ci16_le in SigMF
    elem_size = np.dtype(np.int16).itemsize

    # Each complex sample = 2 int16 (I,Q)
    elem_count = filesize // elem_size
    log.info(f"Element Count: {elem_count}")

    elem_size = np.dtype(np.int16).itemsize

    # Determine sample rate robustly from passed metadata (dict) or SigMFFile
    sample_rate = None
    if sigmfObj is not None:
        # sigmfObj may be the dict produced by `spike_to_sigmf_metadata()` or a SigMFFile
        if isinstance(sigmfObj, dict):
            sample_rate = (
                sigmfObj.get("global", {}).get("core:sample_rate")
                or sigmfObj.get("global", {}).get("sample_rate")
                or sigmfObj.get("core:sample_rate")
            )
        else:
            # try attributes commonly present on SigMFFile
            sample_rate = getattr(sigmfObj, "global_info", {}).get("core:sample_rate")
            if sample_rate is None:
                sample_rate = getattr(sigmfObj, "global_info", {}).get("sample_rate")

    if sample_rate is not None:
        try:
            time_interval = 1.0 / float(sample_rate)
            sample_rate = 1.0 / time_interval
            log.info(f"Sample rate: %s MHz", sample_rate / 1e6)
        except Exception:
            log.warning("Could not parse sample rate from metadata: %r", sample_rate)
            sample_rate = None
    else:
        log.debug("No sample rate available in metadata; skipping sample-rate logs")

    # Read raw interleaved int16 IQ
    samples = np.fromfile(iq_file_path, dtype=np.int16, offset=0, count=elem_count)

    # Trim trailing partial bytes
    if samples.nbytes % elem_size != 0:
        trim = samples % elem_size
        log.warning("Trimming %d trailing byte(s) to align samples", trim)
        samples -= trim

    # Write directly to SigMF data file (no normalization)
    samples.tofile(dest_path + ".sigmf-data")

    log.info(f"==== Wrote SigMF data to {dest_path + '.sigmf-data'} ====")

    # Reassemble interleaved IQ samples
    # samples = raw_samples[::2] + 1j*raw_samples[1::2] # convert to IQIQIQ...

    # Return the IQ data if needed for further processing if needed
    return samples

def signalhound_to_sigmf(
    signalhound_path: str,
    out_path: Optional[str] = None,
    create_archive: bool = False,
    create_ncd: bool = False,
) -> SigMFFile:
    """
    Read a signalhound file, optionally write sigmf archive, return associated SigMF object.

    Parameters
    ----------
    signalhound_path : str
        Path to the signalhound file.
    out_path : str, optional
        Path to the output SigMF metadata file.
    create_archive : bool, optional
        When True, package output as a .sigmf archive.
    create_ncd : bool, optional
        When True, create Non-Conforming Dataset

    Returns
    -------
    SigMFFile
        SigMF object, potentially as Non-Conforming Dataset.

    Raises
    ------
    SigMFConversionError
        If the signalhound file cannot be read.
    """
    signalhound_path = Path(signalhound_path)
    out_path = None if out_path is None else Path(out_path)

    # auto-enable NCD when no output path is specified
    if out_path is None:
        create_ncd = True

    modify_time = signalhound_path.lstat().st_mtime
    signalhound_datetime = datetime.fromtimestamp(modify_time, tz=timezone.utc)

    capture_info = {
        SigMFFile.DATETIME_KEY: signalhound_datetime.strftime(SIGMF_DATETIME_ISO8601_FMT),
    }

    # Call the SigMF conversion for metadata generation (returns dict)
    sigmfMetaData = spike_to_sigmf_metadata(signalhound_path)

    # Convert IQ data for Zero span Spike file
    base_file_name = os.path.splitext(signalhound_path)[0]
    iq_file_path = base_file_name + ".iq"
    try:
        iq_data = convert_iq_data(iq_file_path, sigmfMetaData)
    except Exception as e:
        raise SigMFConversionError(f"Failed to convert or parse IQ data values: {e}")

    # use the generated global metadata dict for SigMFFile construction
    global_info = sigmfMetaData.get("global", {})
    # TODO: Determine if boundary calculations are needed for Spike files
    header_bytes = 0  # No header bytes for IQ files
    capture_info[SigMFFile.HEADER_BYTES_KEY] = header_bytes
    
    if create_ncd:
        # create metadata-only SigMF for NCD pointing to original file
        meta = SigMFFile(global_info=global_info)
        # No data file offset for IQ files
        meta.set_data_file(data_file=signalhound_path, offset=header_bytes)
        meta.data_buffer = io.BytesIO()
        signalhound_data = meta.data_buffer
        meta.add_capture(0, metadata=capture_info)

        # write metadata file if output path specified
        if out_path is not None:
            filenames = get_sigmf_filenames(out_path)
            output_dir = filenames["meta_fn"].parent
            output_dir.mkdir(parents=True, exist_ok=True)
            meta.tofile(filenames["meta_fn"], toarchive=False)
            log.info("wrote SigMF non-conforming metadata to %s", filenames["meta_fn"])

        log.debug("created %r", meta)
        return meta

    if out_path is None:
        base_path = signalhound_path.with_suffix(".sigmf")
    else:
        base_path = Path(out_path)

    filenames = get_sigmf_filenames(base_path)

    output_dir = filenames["meta_fn"].parent
    output_dir.mkdir(parents=True, exist_ok=True)

    meta = SigMFFile(global_info=global_info)

    # No data file offset for IQ files
    # TODO: Confirm if this is correct for Spike files - perhaps set to zero?
    capture_info[SigMFFile.HEADER_BYTES_KEY] = header_bytes
    log.info(f"Header Bytes: {header_bytes}")
    data_bytes = signalhound_path.stat().st_size
    data_bytes = 100000
    log.info(f"Data Bytes: {data_bytes}")

    meta.set_data_file(data_file=signalhound_path, offset=header_bytes, skip_checksum=True, size_bytes=data_bytes)
 
    meta.data_buffer = io.BytesIO()
    signalhound_data = meta.data_buffer


    if create_archive:
        # use temporary directory for data file when creating archive
        with tempfile.TemporaryDirectory() as temp_dir:
            data_path = Path(temp_dir) / filenames["data_fn"].name
            meta.tofile(data_path)

            meta = SigMFFile(data_file=data_path, global_info=global_info)
            meta.add_capture(0, metadata=capture_info)

            meta.tofile(filenames["archive_fn"], toarchive=True)
            log.info("wrote SigMF archive to %s", filenames["archive_fn"])
            # metadata returned should be for this archive
            meta = fromfile(filenames["archive_fn"])
    else:
        # write separate meta and data files
        data_path = filenames["data_fn"]
        meta.tofile(data_path)
        log.info("wrote SigMF dataset to %s", data_path)

        meta = SigMFFile(data_file=signalhound_path, global_info=global_info)
        meta.add_capture(0, metadata=capture_info)

        meta.tofile(filenames["meta_fn"], toarchive=False)
        log.info("wrote SigMF metadata to %s", filenames["meta_fn"])

    log.debug("created %r", meta)
    return meta


```
