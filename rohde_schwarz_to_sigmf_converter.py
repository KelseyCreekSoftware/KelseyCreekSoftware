# Copyright: Multiple Authors
#
# This file is part of sigmf-python. https://github.com/sigmf/sigmf-python
#
# SPDX-License-Identifier: LGPL-3.0-or-later
# 
# Last Updated: 3-26-2026

"""Rohde and Schwarz Converter"""

import getpass
import io
import logging
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

from .. import SigMFFile, fromfile
from ..error import SigMFConversionError
from ..sigmffile import get_sigmf_filenames
from ..utils import SIGMF_DATETIME_ISO8601_FMT

log = logging.getLogger()


def _text_of(root: ET.Element, tag: str) -> Optional[str]:
    """Extract and strip text from XML element."""
    elem = root.find(tag)
    return elem.text.strip() if (elem is not None and elem.text is not None) else None


def _parse_preview_trace(text: Optional[str]) -> List[float]:
    """
    Preview trace is a max-hold trace of the signal power across the capture, represented as a comma-separated string of values.

    Example
    -------
    >>> trace_str = "-1.0, 0.1, 0.5, 0.3, 0.7"
    >>> _parse_preview_trace(trace_str)
    [-1.0, 0.1, 0.5, 0.3, 0.7]
    """
    if text is None:
        return []
    s = text.strip()
    if s.endswith(","):
        s = s[:-1]
    if not s:
        return []
    parts = [p.strip() for p in s.split(",") if p.strip() != ""]
    vals = []
    for part in parts:
        vals.append(float(part))
    return vals


def validate_rohdeschwarz(xml_path: Path) -> None:
    """
    Validate required rohdeschwarz XML metadata fields and associated IQ file.

    Parameters
    ----------
    xml_path : Path
        Path to the rohdeschwarz XML file.

    Raises
    ------
    SigMFConversionError
        If required fields are missing or invalid, or IQ file doesn't exist.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # validate CenterFrequency
    center_freq_raw = _text_of(root, "Clock")
    try:
        center_frequency = float(center_freq_raw)
    except (TypeError, ValueError) as err:
        raise SigMFConversionError(f"Invalid or missing CenterFrequency: {center_freq_raw}") from err

    # validate SampleRate
    sample_rate_raw = _text_of(root, "Samples")
    try:
        sample_rate = float(sample_rate_raw)
    except (TypeError, ValueError) as err:
        raise SigMFConversionError(f"Invalid or missing SampleRate: {sample_rate_raw}") from err

    if sample_rate <= 0:
        raise SigMFConversionError(f"Invalid SampleRate: {sample_rate} (must be > 0)")

    # validate ScalingFactor, for example, "1"
    scaling_factor_raw = _text_of(root, "ScalingFactor")
    if scaling_factor_raw is None:
        raise SigMFConversionError("Missing ScalingFactor in rohdeschwarz XML")

    # validate DataType, for example, "float32"
    data_type_raw = _text_of(root, "DataType")
    if data_type_raw is None:
        raise SigMFConversionError("Missing DataType in rohdeschwarz XML")

    # TODO: Find second format field in XML to determine if this is complex or real data
    # validate Format - for example, "complex"
    # format_raw = _text_of(root, "Format")
    # if format_raw is None:
    #     raise SigMFConversionError("Missing Format in rohdeschwarz XML")

    # validate channel for example, "1"
    numberofchannel_raw = _text_of(root, "NumberOfChannels")
    if numberofchannel_raw is None:
        raise SigMFConversionError("Missing NumberOfChannels in rohdeschwarz XML")

    # validate associated IQ file exists
    # example IQ file name "File.complex.1ch.float32"
    # iq_file_path = xml_path.with_suffix(data_type_raw)
    iq_file_path = xml_path.with_suffix(".iq")
    if not iq_file_path.exists():
        raise SigMFConversionError(f"Could not find associated IQ file: {iq_file_path}")

    # validate IQ file size is aligned to sample boundary
    filesize = iq_file_path.stat().st_size
    elem_size = np.dtype(np.int16).itemsize
    frame_bytes = 2 * elem_size  # I and Q components
    if filesize % frame_bytes != 0:
        raise SigMFConversionError(f"IQ file size {filesize} not divisible by {frame_bytes}; partial sample present")


def _build_metadata(xml_path: Path) -> Tuple[dict, dict, list, int]:
    """
    Build SigMF metadata components from the rohdeschwarz XML file.

    Parameters
    ----------
    xml_path : Path
        Path to the rohdeschwarz XML file.

    Returns
    -------
    tuple of (dict, dict, list, int)
        global_info, capture_info, annotations, sample_count

    Raises
    ------
    SigMFConversionError
        If required fields are missing or invalid.
    """
    log.info("converting rohdeschwarz xml metadata to sigmf format")

    xml_path = Path(xml_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # validate required fields and associated IQ file
    validate_rohdeschwarz(xml_path)

    # TODO: Determine how to handle center frequency, for now default to 0
    center_frequency = float("0")

    # extract and convert required fields
    numberofchannel_raw = _text_of(root, "NumberOfChannels")
    # Confirm this is corect
    sample_rate = float(_text_of(root, "Clock"))
    data_type_raw = _text_of(root, "DataType")

    # optional EpochNanos field
    epoch_nanos = None
    epoch_nanos_raw = _text_of(root, "EpochNanos")
    if epoch_nanos_raw:
        try:
            epoch_nanos = int(epoch_nanos_raw)
        except ValueError:
            log.warning(f"could not parse EpochNanos: {epoch_nanos_raw}")

    # TODO: Probably need to use logic similar to blue file for datatypes...
    # TODO: Complex, etc. 
    # TODO: Determine big or little endian
    # map datatype
    if data_type_raw == "float32":
        data_type = "cf32_le"  # complex float32 little-endian
    else:
        raise SigMFConversionError(f"Unsupported rohdeschwarz DataType: {data_type_raw}")

    # optional fields - only convert if present and valid
    scaling_factor = None
    scaling_factor_raw = _text_of(root, "ScalingFactor")
    if scaling_factor_raw:
        try:
            scaling_factor = float(scaling_factor_raw)
        except ValueError:
            log.warning(f"could not parse ScalingFactor: {scaling_factor_raw}")

    datafilename  = None
    datafilename_raw = _text_of(root, "DataFilename")
    if datafilename_raw:
        try:
            datafilename  = str(datafilename_raw)
        except ValueError:
            log.warning(f"could not parse DataFileName: {datafilename_raw}")

    scale_factor = None
    scale_factor_raw = _text_of(root, "ScaleFactor")
    if scale_factor_raw:
        try:
            scale_factor = float(scale_factor_raw)
        except ValueError:
            log.warning(f"could not parse ScaleFactor: {scale_factor_raw}")

    # parse optional preview data if present
    preview_data_raw = _text_of(root, "PreviewData")
    preview_data = _parse_preview_trace(preview_data_raw) if preview_data_raw else None

    name = _text_of(root, "Name")
    comment = _text_of(root, "Comment")
    userdata = _text_of(root, "UserData")
    datafilename = _text_of(root, "DataFilename")

    # build hardware description with available information
    hw_parts = []

    if name:
        hw_parts.append(f"{name}")
    else:
        hw_parts.append("Rohde and Schwarz Device")

    if comment:
        hw_parts.append(f"{comment}")

    if userdata:
        hw_parts.append(f"{userdata}")

    #  TODO: Consider if this should be moved. 
    if datafilename :
        hw_parts.append(f"datafilename : {datafilename }")

    hardware_description = ", ".join(hw_parts) if hw_parts else "Rohde and Schwarz Device"

    # strip the extension from the original file path
    base_file_name = xml_path.with_suffix("")
    # build the .iq file path for data file
    data_file_path = base_file_name.with_suffix(".iq")
    filesize = data_file_path.stat().st_size

    # TODO: Update for R&S
    # complex 16-bit integer IQ data > ci16_le in SigMF
    elem_size = np.dtype(np.int16).itemsize
    frame_bytes = 2 * elem_size  # I and Q components

    # calculate sample count using the original IQ data file size
    sample_count_calculated = filesize // frame_bytes
    log.debug("sample count: %d", sample_count_calculated)

    # convert the datetime object to an ISO 8601 formatted string if EpochNanos is present
    iso_8601_string = None
    if epoch_nanos is not None:
        secs = epoch_nanos // 1_000_000_000
        rem_ns = epoch_nanos % 1_000_000_000
        dt = datetime.fromtimestamp(secs, tz=timezone.utc) + timedelta(microseconds=rem_ns / 1000)
        iso_8601_string = dt.strftime(SIGMF_DATETIME_ISO8601_FMT)

    # base global metadata
    global_md = {
        SigMFFile.AUTHOR_KEY: getpass.getuser(),
        SigMFFile.DATATYPE_KEY: data_type,
        SigMFFile.HW_KEY: hardware_description,
        SigMFFile.NUM_CHANNELS_KEY: 1,
        SigMFFile.RECORDER_KEY: "Official SigMF Rohde and Schwarz converter",
        SigMFFile.SAMPLE_RATE_KEY: sample_rate,
        SigMFFile.EXTENSIONS_KEY: [{"name": "rohdeschwarz", "version": "0.0.1", "optional": True}],
    }

    # add optional rohdeschwarz-specific fields to global metadata using rohdeschwarz: namespace
    # only include fields that aren't already represented in standard SigMF metadata
    if scaling_factor:
        global_md["rohdeschwarz:scaling_factor"] = scaling_factor
    if scale_factor:
        global_md["rohdeschwarz:scale_factor_mw"] = scale_factor  # to convert raw to mW
    if datafilename:
        global_md["rohdeschwarz:iq_datafilename"] = datafilename  # provenance
    if userdata:
        global_md["rohdeschwarz:userdata"] = userdata #open ended field for user defined data.
    if preview_data:
        global_md["rohdeschwarz:preview_trace"] = preview_data  # TBD trace

    # capture info
    capture_info = {
        SigMFFile.FREQUENCY_KEY: center_frequency,
    }
    if iso_8601_string:
        capture_info[SigMFFile.DATETIME_KEY] = iso_8601_string

    # TODO: Investigate if clock maps to if_bandwidth or if there is another field in the XML that should be used for this
    raw_clock = _text_of(root, "Clock")
    if_bandwidth = float(raw_clock) if raw_clock else None

    # create annotations array using calculated values
    annotations = []
    if if_bandwidth:
        upper_frequency_edge = center_frequency + (if_bandwidth / 2.0)
        lower_frequency_edge = center_frequency - (if_bandwidth / 2.0)
        annotations.append(
            {
                SigMFFile.START_INDEX_KEY: 0,
                SigMFFile.LENGTH_INDEX_KEY: sample_count_calculated,
                SigMFFile.FLO_KEY: lower_frequency_edge,
                SigMFFile.FHI_KEY: upper_frequency_edge,
                SigMFFile.LABEL_KEY: "rohdeschwarz",
            }
        )

    return global_md, capture_info, annotations, sample_count_calculated


def convert_iq_data(xml_path: Path, sample_count: int) -> np.ndarray:
    """
    Convert IQ data in .iq file to SigMF based on values in rohdeschwarz XML file.

    Parameters
    ----------
    xml_path : Path
        Path to the rohdeschwarz XML file.
    sample_count : int
        Number of samples to read.

    Returns
    -------
    numpy.ndarray
        Parsed samples.
    """
    log.debug("parsing rohdeschwarz file data values")
    iq_file_path = xml_path.with_suffix(".iq")

    # calculate element count (I and Q samples)
    elem_count = sample_count * 2  # *2 for I and Q samples

    # complex 16-bit integer IQ data > ci16_le in SigMF
    elem_size = np.dtype(np.int16).itemsize

    # read raw interleaved int16 IQ
    samples = np.fromfile(iq_file_path, dtype=np.int16, offset=0, count=elem_count)

    # trim trailing partial bytes
    if samples.nbytes % elem_size != 0:
        trim = samples.nbytes % elem_size
        log.warning("trimming %d trailing byte(s) to align samples", trim)
        samples = samples[: -(trim // elem_size)]

    return samples


def rohdeschwarz_to_sigmf(
    rohdeschwarz_path: Path,
    out_path: Optional[Path] = None,
    create_archive: bool = False,
    create_ncd: bool = False,
    overwrite: bool = False,
) -> SigMFFile:
    """
    Read a rohdeschwarz file, optionally write sigmf archive, return associated SigMF object.

    Parameters
    ----------
    rohdeschwarz_path : Path
        Path to the rohdeschwarz file.
    out_path : Path, optional
        Path to the output SigMF metadata file.
    create_archive : bool, optional
        When True, package output as a .sigmf archive.
    create_ncd : bool, optional
        When True, create Non-Conforming Dataset
    overwrite : bool, optional
        If False, raise exception if output files already exist.

    Returns
    -------
    SigMFFile
        SigMF object, potentially as Non-Conforming Dataset.

    Raises
    ------
    SigMFConversionError
        If the rohdeschwarz file cannot be read.
    """
    rohdeschwarz_path = Path(rohdeschwarz_path)
    out_path = None if out_path is None else Path(out_path)

    # auto-enable NCD when no output path is specified
    if out_path is None:
        create_ncd = True

    # call the SigMF conversion for metadata generation
    global_info, capture_info, annotations, sample_count = _build_metadata(rohdeschwarz_path)

    # get filenames for metadata, data, and archive based on output path and input file name
    if out_path is None:
        base_path = rohdeschwarz_path
    else:
        base_path = Path(out_path)

    filenames = get_sigmf_filenames(base_path)

    # create NCD if specified, otherwise create standard SigMF dataset or archive
    if create_ncd:
        # rohdeschwarz files have no header or trailing bytes
        global_info[SigMFFile.DATASET_KEY] = rohdeschwarz_path.with_suffix(".iq").name
        global_info[SigMFFile.TRAILING_BYTES_KEY] = 0
        capture_info[SigMFFile.HEADER_BYTES_KEY] = 0

        # build the .iq file path for data file
        base_file_name = rohdeschwarz_path.with_suffix("")
        data_file_path = base_file_name.with_suffix(".iq")

        # create metadata-only SigMF for NCD pointing to original file
        meta = SigMFFile(global_info=global_info)
        meta.set_data_file(data_file=data_file_path, offset=0)
        meta.data_buffer = io.BytesIO()
        meta.add_capture(0, metadata=capture_info)

        # add annotations from metadata
        for annotation in annotations:
            start_idx = annotation.get(SigMFFile.START_INDEX_KEY, 0)
            length = annotation.get(SigMFFile.LENGTH_INDEX_KEY)
            # pass remaining fields as metadata (excluding standard annotation keys)
            annot_metadata = {
                k: v for k, v in annotation.items() if k not in [SigMFFile.START_INDEX_KEY, SigMFFile.LENGTH_INDEX_KEY]
            }
            meta.add_annotation(start_idx, length=length, metadata=annot_metadata)

        # write metadata file if output path specified
        if out_path is not None:
            output_dir = filenames["meta_fn"].parent
            output_dir.mkdir(parents=True, exist_ok=True)
            meta.tofile(filenames["meta_fn"], toarchive=False, overwrite=overwrite)
            log.info("wrote SigMF non-conforming metadata to %s", filenames["meta_fn"])

        log.debug("created %r", meta)
        return meta

    # create archive if specified, otherwise write separate meta and data files
    if create_archive:
        # use temporary directory for data file when creating archive
        with tempfile.TemporaryDirectory() as temp_dir:
            data_path = Path(temp_dir) / filenames["data_fn"].name

            # convert iq data and write to temp directory
            try:
                iq_data = convert_iq_data(rohdeschwarz_path, sample_count)
            except Exception as e:
                raise SigMFConversionError(f"Failed to convert or parse IQ data values: {e}") from e

            # write converted iq data to temporary file
            iq_data.tofile(data_path)
            log.debug("wrote converted iq data to %s", data_path)

            meta = SigMFFile(data_file=data_path, global_info=global_info)
            meta.add_capture(0, metadata=capture_info)

            # add annotations from metadata
            for annotation in annotations:
                start_idx = annotation.get(SigMFFile.START_INDEX_KEY, 0)
                length = annotation.get(SigMFFile.LENGTH_INDEX_KEY)
                annot_metadata = {
                    k: v
                    for k, v in annotation.items()
                    if k not in [SigMFFile.START_INDEX_KEY, SigMFFile.LENGTH_INDEX_KEY]
                }
                meta.add_annotation(start_idx, length=length, metadata=annot_metadata)

            output_dir = filenames["archive_fn"].parent
            output_dir.mkdir(parents=True, exist_ok=True)
            meta.tofile(filenames["archive_fn"], toarchive=True, overwrite=overwrite)
            log.info("wrote SigMF archive to %s", filenames["archive_fn"])
            # metadata returned should be for this archive
            meta = fromfile(filenames["archive_fn"])

    else:
        # write separate meta and data files
        # convert iq data for rohdeschwarz file
        try:
            iq_data = convert_iq_data(rohdeschwarz_path, sample_count)
        except Exception as e:
            raise SigMFConversionError(f"Failed to convert or parse IQ data values: {e}") from e

        # write data file
        output_dir = filenames["data_fn"].parent
        output_dir.mkdir(parents=True, exist_ok=True)
        iq_data.tofile(filenames["data_fn"])
        log.debug("wrote SigMF dataset to %s", filenames["data_fn"])

        # create sigmffile with converted iq data
        meta = SigMFFile(data_file=filenames["data_fn"], global_info=global_info)
        meta.add_capture(0, metadata=capture_info)

        # add annotations from metadata
        for annotation in annotations:
            start_idx = annotation.get(SigMFFile.START_INDEX_KEY, 0)
            length = annotation.get(SigMFFile.LENGTH_INDEX_KEY)
            # pass remaining fields as metadata (excluding standard annotation keys)
            annot_metadata = {
                k: v for k, v in annotation.items() if k not in [SigMFFile.START_INDEX_KEY, SigMFFile.LENGTH_INDEX_KEY]
            }
            meta.add_annotation(start_idx, length=length, metadata=annot_metadata)

        # write metadata file
        meta.tofile(filenames["meta_fn"], toarchive=False)
        log.info("wrote SigMF metadata to %s", filenames["meta_fn"])

    log.debug("created %r", meta)
    return meta
