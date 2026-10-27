# Input data dictionary

One row represents a SWOT observation matched to a gauge observation at the same reach.

| Column | Type | Meaning |
|---|---|---|
| `reach_id` | string | Stable reach ID; do not use row number as an ID |
| `swot_time` | datetime | UTC timestamp of SWOT observation |
| `swot_q` | float | SWOT discharge, with units documented in metadata |
| `gauge_time` | datetime | Timestamp/period representative of gauge discharge |
| `gauge_q` | float | Gauge discharge in compatible units |
| `quality_ok` | bool/string | Whether the observation passes documented quality screening |
| `product_version` | string | SWOT product/version used |

The pipeline assumes `swot_q` and `gauge_q` have compatible units and that each row has already been paired using a documented matching rule. It parses timestamps as UTC and rejects missing discharge values. Never mix instantaneous satellite estimates and daily gauge averages without explicitly justifying the aggregation.
