---
type: analyze-data
default_target: claude-ai
---
# analyze-data: answer a question with data

## Slots
1. **question** (high): the decision or hypothesis behind "analyze". Offer 2–3
   candidate questions read from the data's columns and the request; suggest
   the most likely.
2. **definitions** (high): what counts for the key metric (churn, active,
   revenue) and which rows to exclude (trials, test accounts, refunds).
   Suggest definitions from the column names, marked as suggestions.
3. **audience and output** (high): exec summary, chart, table, notebook,
   numbers only. Suggest a short summary plus one chart for a manager audience.
4. **data** (medium): where it is and what one row is, if not pasted.
5. **tools** (low): SQL, Python, spreadsheet; where results go.

## Prompt skeleton
Question and why it matters (from the brief) → the data and what a row is →
metric definitions and exclusions → method expectations (check data quality
first, state assumptions) → output shape for the audience → stop line.

## Type guidance
- Pin the metric definition; most wrong analyses use a plausible but wrong one.
- Ask the receiver to report data-quality problems before conclusions.
- Separate what the data shows from what it suggests.

## Sources
Vendor docs on data analysis features; thin public guidance, so lean on slots.
