# Kraken SDR Project Notes

*Updated 1-16-26*

## SDR KrakenSDR Overview

KrakenSDR a 5-RX-channel coherent software defined radio for applications such as radio direction finding and passive radar.

(KrakenSDR - $749.00)
https://www.krakenrf.com/product-page/krakensdr

(Matched antennas)
https://www.krakenrf.com/product-page/krakentenna-set-of-five

It uses a phone App, that has to be configured and takes some time to learn how to use.
https://github.com/krakenrf/krakensdr_docs/wiki/06.-Android-&-iOS-App-Guide

## Writing SigMF

This code seems to gather the IQ data and create a SigMF file.

https://github.com/bshelters/krakenSDR_sigmf/blob/0bc3b70b591f9a67f63f2485a65cc3a6686ff7ff/src/krakenrf_sigmf.cpp#L330

## Notes on Kraken Ethernet Packet Content

https://github.com/bshelters/krakenSDR_sigmf/blob/main/KrakenSDR-Ethernet-Notes-v1.pdf

## Converter for Ethernet Stream

https://github.com/bshelters/krakenSDR_sigmf

https://github.com/bshelters/krakenSDR_sigmf/blob/main/src/krakenrf_sigmf.cpp

## Local storage option in KrakenSDR app

https://github.com/krakenrf/krakensdr_docs/wiki/05.-KrakenSDR-Web-Interface-Controls#local-data-recording

## GNU Radio Block for KrakenSDR

This is a GNU Radio Block for KrakenSDR. It connects via a TCP socket connection to the KrakenSDR DAQ server software called Heimdall. Heimdall handles all sample and phase coherence calibration via the noise source, 
and this block receives the coherent IQ sample output and makes it available for further DSP processing in GNU Radio.

https://github.com/krakenrf/krakensdr_docs/wiki/08.-GNU-Radio-Block#how-the-krakensdr-source-block-works

## GPS Tracker app for Kraken Map 

https://github.com/krakenrf/krakensdr_docs/blob/e229d71d387ecab2e82b1b37e9e3b4aa929402af/misc_scripts/gpsd_tracker_krakenmap.py

## Early draft Metadata exploration

```json
{
  "global": {
    "core:datatype": "ci16_le",
    "core:sample_rate": 2000000,
    "core:version": "1.2.0",
    "core:description": "KrakenSDR 5‑channel coherent IQ capture",
    "core:author": "YOUR_NAME_OR_SYSTEM",
    "core:recorder": "KrakenSDR Ethernet Capture Pipeline",
    "core:hw": "KrakenSDR v1.x",
    "kraken:packet_format_version": "1.0",
    "kraken:channels": 5,
    "kraken:gain": {
      "ch0": 30,
      "ch1": 30,
      "ch2": 30,
      "ch3": 30,
      "ch4": 30
    },
    "kraken:notes": "Replace fields with actual runtime values"
  },

  "captures": [
    {
      "core:sample_start": 0,
      "core:frequency": 1575420000,
      "kraken:channel": 0
    },
    {
      "core:sample_start": 0,
      "core:frequency": 1575420000,
      "kraken:channel": 1
    },
    {
      "core:sample_start": 0,
      "core:frequency": 1575420000,
      "kraken:channel": 2
    },
    {
      "core:sample_start": 0,
      "core:frequency": 1575420000,
      "kraken:channel": 3
    },
    {
      "core:sample_start": 0,
      "core:frequency": 1575420000,
      "kraken:channel": 4
    }
  ],

  "annotations": [
    {
      "core:sample_start": 0,
      "core:sample_count": 0,
      "core:comment": "Optional annotations for GPS, DOA events, calibration pulses, etc."
    }
  ]
}
```
