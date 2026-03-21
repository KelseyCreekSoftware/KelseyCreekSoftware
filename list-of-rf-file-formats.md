# Overview of IQ file recording

*Updated 3-20-2026*

There are different methods of saving RF recordings to a file.  If any demod has occured (eg FM), it's no longer considered an RF recording in this context and we aren't worried about it (because you can't go backwards, back to RF).  RF recordings are often called IQ files, although technically it's possible to record RF using real-only, if you do direct sampling, but 99.9% of RF recordings are going to be complex valued, and use IQ samples, because they sampled a baseband signal.

## Data-only, eg binary IQ file with no metadata in it

Not actually a format, there's no way to simply convert this to SigMF

You end up using bespoke method of saving the metadata (eg filename)

A lot of vendors might have a recording option to save it as a binary IQ file with no header

## Converters for SigMF

- XMIDAS BLUEFILES (aka cdif) and variants

- WAV file

- oog audio recording format

- Rohde and Schwarz - I/Q Data File Format (iq-tar)

- KeySight - Spectrum Analysis IQ File

- HDF5 <not actually a format, it's not RF specific, it doesn't specify how to store the metadata>. It is more of a container, it doesnt define the metadata, and a lot of people will make HDF5 RF recordings using SigMF metadata standard

- ITU-R SM.2117-0 - The ITU-R SM.2117-0 spec fits within the larger spectrum management suite of ITU specs, and only for systems doing spectrum management or sensors feeding those systems, which is an extremely specific application, it makes sense for them to have ITU specs for interoperability sake. Additional information here:  https://www.crfs.com/blog/the-importance-of-compliance-with-itu-regulations-for-spectrum-monitoring This may be too application specific to create a converter for. This format is just how the spectrum management sensors talk to each other, they won't care about SigMF or using open source software like Inspectrum.

- Pcap (or other capture) of VITA-49 (DIFI is a subset of VITA-49)

- SATNOGs appears to normally store demodulated data in most cases.

