# A1 artefact pool

The pool is built by `merged_course/scripts/build_a1_pool.py` and lives in
`pool/POOL-01` … `pool/POOL-12`. It contains twelve published charts covering
all nine Visual Vocabulary categories. Each entry holds a published or
source-linked chart, corresponding `source_data.csv`, data dictionary,
and provenance sheet. Each provenance sheet gives the exact canonical domain
and publication value students must copy into the notebook. Internal build
metadata and validation results are not included in the student archive.

Canonical domains are: POOL-01 climate science; POOL-02 public health;
POOL-03 astronomy; POOL-04 wellbeing; POOL-05 and POOL-07 economics; POOL-06
and POOL-10 energy; POOL-08 ecology; POOL-09 astronomy; POOL-11 geophysics;
and POOL-12 transportation.

The approved printable chart-card examples are the only course-reproduction
exception. The CSVs come from the corresponding publisher or official example
source; no values were digitised from chart pixels. Students preserve the
source fields, document transformations, and create an alternative view for a
stated claim.

Known source limitations are stated both in the assignment brief and the
affected provenance sheets: POOL-04's chart card shows ranks 1–48 while its
CSV contains all 143 countries and no simultaneous rank intervals; several
POOL-06 published Sankey labels do not add exactly to displayed node totals;
and POOL-12 is an undirected historical airport-pair extract whose
`airline_record_count` is not passenger or flight volume.
