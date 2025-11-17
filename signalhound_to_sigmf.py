#!/usr/bin/env python3

# Signal Hound IQ and XML file converter
# Converts the extracted metadata into SigMF format.
# This for Zero span Spike .iq and .xml files

# Author: Don Marshall (with help from AI!)
# Date: November 17, 2025

import os
import json
from pathlib import Path
import hashlib
import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# Define constants for Spike
ENDIANNESS = "<"
# DATATYPE_SIZE = 4  # bytes per complex int16 sample (2 bytes I + 2 bytes Q)
DATATYPE = "ci16_le"  # complex short int16 little-endian


def _to_float(x):
    try:
        return float(x)
    except Exception:
        return None


def _to_int(x):
    try:
        return int(float(x))
    except Exception:
        return None


def _parse_preview_trace(text):
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


def read_spike_xml(xml_file_path):
    """
    Read Spike/Signal Hound Zero Span XML and return a normalized metadata dict.

    Parameters
    ----------
    file_path : str or Path
        Path to the Spike XML file.

    Returns
    -------
    dict
        Parsed metadata dictionary with typed fields.
    """
    xml_path = Path(xml_file_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    def text_of(tag):
        el = root.find(tag)
        return el.text.strip() if (el is not None and el.text is not None) else None

    md = {}
    # Raw strings for auditing
    for tag in (
        "DataType",
        "DeviceType",
        "CenterFrequency",
        "SampleCount",
        "EpochNanos",
        "SampleRate",
        "IQFileName",
        "SerialNumber",
        "PreviewTrace",
    ):
        md[f"{tag}_raw"] = text_of(tag)
    print(md)

    # Typed fields / normalized
    md["DataType"] = md.pop("DataType_raw")
    md["DeviceType"] = md.pop("DeviceType_raw")
    md["CenterFrequency"] = _to_float(text_of("CenterFrequency"))
    md["SampleCount"] = _to_int(text_of("SampleCount"))
    md["SampleRate"] = _to_float(text_of("SampleRate"))
    md["EpochNanos"] = _to_int(text_of("EpochNanos"))
    # Will be added as comments or annotations
    md["ReferenceLevel"] = _to_float(text_of("ReferenceLevel"))
    md["Decimation"] = _to_int(text_of("Decimation"))
    md["IFBandwidth"] = _to_float(text_of("IFBandwidth"))
    md["ScaleFactor"] = _to_float(text_of("ScaleFactor"))
    md["SerialNumber"] = md.pop("SerialNumber_raw")
    md["IQFileName"] = md.pop("IQFileName_raw")

    # PreviewTrace: list of floats and numpy array (float32)
    # TODO: Confirm data type for preview data elements.
    preview_raw = text_of("PreviewTrace")
    md["PreviewTrace_list"] = _parse_preview_trace(preview_raw)
    md["PreviewTrace_array"] = np.array(md["PreviewTrace_list"], dtype=np.float32)

    return md


def spike_to_sigmf_metadata(spike_xml, xml_file_path):
    """
    Build a SigMF metadata dict from parsed spikefile spike_xml and extended header.

    Parameters
    ----------
    spike_xml : dict
        Spike XML values for metadata from read_spike_xml().
    xml_file_path : str
        Path to the spike xml file.
    Returns
    -------
    dict
        SigMF metadata structure.

    Raises
    ------
    ValueError
        If required fields are missing or invalid.
    """
    print("===== Converting Spike XML metadata to SigMF format =====")

    # Check datatype mapping based on Spike XML DataType field - should be "Complex Short"
    spike_data_type = spike_xml.get("DataType")

    if spike_data_type == "Complex Short":
        DataType= "ci16_le"  # complex int16 little-endian
    else:
        raise ValueError(f"Unsupported Spike DataType: {spike_data_type}")

    device_type = spike_xml.get("DeviceType")
    hardware_description = (
        device_type if device_type is not None else "Signal Hound Device"
    )

    # complex 16-bit integer  IQ data > ci16_le in SigMF
    elem_size = np.dtype(np.int16).itemsize

    # Calculate sample count

    filesize = os.path.getsize(xml_file_path)
    print("File size: ", filesize)

    # Each complex sample = 2 int16 (I,Q)
    sample_count = filesize // elem_size
    print(f"Sample count: {sample_count}")

    # For now define static values. Perhaps take as JSON input
    spike_author = "Spike File Conversion - Unknown Author"
    spike_licence = "Spike File Conversion - Unknown License"
    spike_description = "Signal Hound Spike Zero Span File converted to SigMF format"

    # TODO: Confirm Zero Span Spike files are single channel
    channelNumber = 1

    # TODO: see if this can be simplified and add error checking
    # Convert the datetime object to an ISO 8601 formatted string
    epoch_time = int(spike_xml.get("EpochNanos"))
    secs = epoch_time // 1_000_000_000
    rem_ns = epoch_time % 1_000_000_000
    dt_object_utc = datetime.fromtimestamp(secs, tz=timezone.utc) + timedelta(
        microseconds=rem_ns / 1000
    )
    # Format with milliseconds and Zulu suffix
    iso_8601_string = dt_object_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    print(f"Epoch time: {epoch_time}")
    print(f"ISO 8601 time: {iso_8601_string}")

    # --- Base Global Metadata ---
    global_md = {
        "core:author": spike_author,
        "core:datatype": DataType,
        "core:description": spike_description,
        "core:hw": hardware_description,
        "core:license": spike_licence,
        "core:num_channels": channelNumber,
        "core:sample_rate": spike_xml.get("SampleRate"),
        "core:version": "1.0.0",
        # TODO: Validate data types below
        "core:spike_": spike_xml.get("ReferenceLevel"),
        "core:spike_": spike_xml.get("Decimation"),
        "core:spike_": spike_xml.get("IFBandwidth"),
        "core:spike_": spike_xml.get("ScaleFactor"),
        "core:spike_": spike_xml.get("IQFileName"),
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
    def compute_sha512(path, bufsize=1024 * 1024):
        """Compute SHA-512 hash of a file in chunks."""

        h = hashlib.sha512()
        with open(path, "rb") as f:
            while chunk := f.read(bufsize):
                h.update(chunk)
        return h.hexdigest()

    # Strip the extension from the original file path
    base_file_name = os.path.splitext(xml_file_path)[0]

    # Build the .sigmf-data path
    data_file_path = base_file_name + ".sigmf-data"

    # Compute SHA-512 of the data file
    data_sha512 = compute_sha512(data_file_path)  # path to the .sigmf-data file
    global_md["core:sha512"] = data_sha512

    # TODO: Confirm freq_upper_edge calculation - is this correct for Spike files? ScaleFactor? Mhz? /2?
    upper_frequency_edge = float(spike_xml.get("CenterFrequency")) + float(
        spike_xml.get("IFBandwidth")
    )
    # TODO: Confirm freq_upper_edge calculation - is this correct for Spike files? ScaleFactor? Mhz?
    lower_freq_lower_edge = float(spike_xml.get("CenterFrequency") or 0.0)

    annotations = [
        {
            "core:sample_start": 0,
            "core:sample_count": sample_count,
            "core:freq_upper_edge": upper_frequency_edge,
            "core:freq_lower_edge": lower_freq_lower_edge,
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
    print(f"==== Wrote SigMF metadata to {meta_path} ====")

    return sigmf


def convert_data_values(spike_xml, xml_file_path):
    """
    Convert IQ data in .iq file to SigMF based on values in Zero Span XML file.

     Parameters
     ----------
     spike_xml : dict
         Spike XML  dictionary.
     xml_file_path : str
         Path to the spike zero span XML file.

     Returns
     -------
     numpy.ndarray
         Parsed samples.
    """

    print("===== Parsing spike file data values =====")
    filesize = os.path.getsize(xml_file_path)
    print("File size: ", filesize)

    # Determine destination path for SigMF data file
    dest_path = xml_file_path.rsplit(".", 1)[0]

    # complex 16-bit integer  IQ data > ci16_le in SigMF
    elem_size = np.dtype(np.int16).itemsize

    # Each complex sample = 2 int16 (I,Q)
    elem_count = filesize // elem_size

    time_interval = 1.0 / spike_xml.get("SampleRate", 1.0)
    sample_rate = 1 / time_interval
    print("Sample rate: ", sample_rate / 1e6, "MHz")

    # Read raw interleaved int16 IQ
    samples = np.fromfile(xml_file_path, dtype=np.int16, offset=0, count=elem_count)

    # Write directly to SigMF data file (no normalization)
    samples.tofile(dest_path + ".sigmf-data")

    # Reassemble interleaved IQ samples
    # samples = raw_samples[::2] + 1j*raw_samples[1::2] # convert to IQIQIQ...

    # Return the IQ data if needed for further processing if needed
    return samples


def spike_zero_span_to_sigmf_converter(xml_file_path):
    """
    Convert a Signal Hound Zero Span file to SigMF metadata and data.

    Parameters
    ----------
    xml_file_path : str
        xml_file_path to the spike XML file.

    Returns
    -------
    samples : numpy.ndarray
        IQ Data.
    """

    print("==========================================")
    print("===== Starting spike file processing =====")
    print("==========================================")

    # Read spike_xml from spike file to determine how to process the rest of the file
    try:
        spike_xml = read_spike_xml(xml_file_path)
    except Exception as e:
        raise RuntimeError(f"Failed to parse data values: {e}")

    # Call the SigMF conversion for metadata generation
    spike_to_sigmf_metadata(spike_xml, xml_file_path)

    """
    
    # Convert IQ data for Zero span Spike file   
    # iq_data will be available if needed for further processing.
    try:
        iq_data = convert_data_values(spike_xml, iq_file_path)
    except Exception as e:
        raise RuntimeError(f"Failed to parse data values: {e}")

    # Return the IQ data if needed for plotting, or further processing if needed 
    return iq_data
    """


if __name__ == "__main__":
    # Main calls spike_file_to_sigmf to convert dump spike file contents to SigMF.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("spike_xml_file")
    # Uncomment for passing input args for file name - cdif or .tmp files
    # args = parser.parse_args()
    xml_file_path = "C:\Data1\Ham_Radio\SDR\signalhound_to_sigmf_converter\IQREC-11-13-25-17h31m10s877.xml"
    iq_file_path = "C:\Data1\Ham_Radio\SDR\signalhound_to_sigmf_converter\IQREC-11-13-25-17h31m10s877.iq"
    try:
        spike_zero_span_to_sigmf_converter(xml_file_path)
        print("DONE")
    except Exception as e:
        print(f"Processing failed: {e}")
