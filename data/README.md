# Data acquisition and provenance

Raw data are intentionally not included. They are large, versioned scientific datasets and must be acquired from authoritative providers.

Primary paper data statement:
- SWOT L2 River Single-Pass Vector data: https://podaac.jpl.nasa.gov/SWOT
- SWOT L4 DAWG SOS discharge product: https://podaac.jpl.nasa.gov/dataset/SWOT_L4_DAWG_SOS_DISCHARGE
- SWOT Confluence software: https://github.com/SWOT-Confluence

Create a manifest containing: dataset/product name, version, DOI or URL, access date, license, filenames, checksums, and processing history. Gauge data must also have source, units, datum, and temporal aggregation documented.

This repository expects a harmonized CSV for evaluation. The harmonization step is intentionally explicit because variable names, quality flags, and file formats can vary between product versions.
