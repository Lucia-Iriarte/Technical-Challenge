# Assumptions

This document lists every assumption made while implementing the challenge, since the spec leaves some edge cases open to interpretation.

## Format detection

- The three formats can always be told apart from the shape of the raw fields, not from fixed field positions alone:
  - A zip-like field is a value made up of digits only (no separators),
    e.g. `10013`.
  - A phone-like field always contains digits plus at least one separator character (`-`, `(`, `)`, or a space), e.g. `(703)-742-0996` or `703 955 0373`.
- For 5-comma-field lines:
  - If field[2] is phone-like and field[4] is zip-like -> **Format A**
    (`Lastname, Firstname, Phone, Color, Zip`).
  - If field[2] is zip-like and field[3] is phone-like -> **Format C**
    (`Firstname, Lastname, Zip, Phone, Color`).
  - Any other combination is treated as unparseable (invalid line).
- For 4-comma-field lines -> **Format B**
  (`Firstname Lastname, Color, Zip, Phone`). The name field is split on the
  **last space** in it, so a possible middle name/initial stays attached to
  the first name (e.g. `"James Robert Murphy"` -> firstname
  `"James Robert"`, lastname `"Murphy"`).
- This heuristic is intentionally based on field *shape*, not validity, so that lines with an invalid phone or an invalid zip (wrong digit count) can still be correctly recognized as "Format A/B/C, but invalid" — as opposed to "unparseable" — matching the example in the PDF where `Chandler, Kerri, (623)-668-9293, pink, 123123121` is still detected as Format A but rejected for having a 9-digit zip.

## Validation

- A line is invalid if:
  - It doesn't split into exactly 4 or 5 comma-separated fields matching one of the two shapes above, **or**
  - The phone number (after stripping all non-digit characters) does not have exactly 10 digits, **or**
  - The zip code is not exactly 5 digits (checked as a string, so a zip with leading zeros like `"08540"` is valid), **or**
  - The firstname, lastname, or color field is empty after trimming whitespace.
- Blank/whitespace-only lines are treated as invalid lines (and their 0-indexed position is recorded in `errors`), rather than being silently skipped, since the spec describes the input as "n lines" and asks for 0-indexed line numbers of invalid entries — skipping blank lines would shift or hide indices.

## Normalization

- Names are preserved exactly as given (including punctuation like the middle initial in `"Booker T."`), with only leading/trailing whitespace trimmed. No case changes are applied.
- Colors are preserved exactly as given (trimmed, but not re-cased), so `"yellow"` stays lowercase as in the PDF's worked example.
- Phone numbers are normalized by extracting all digit characters and reformatting them as `XXX-XXX-XXXX`, regardless of the original separators used.
- Zip codes are kept as plain strings, not converted to integers, so leading zeros are never lost.

## Sorting & output

- `entries` are sorted ascending by `(lastname, firstname)` using standard Python string comparison (case-sensitive, ASCII order). The spec doesn't specify a case-insensitive sort, and none of the given examples have mixed-case name collisions, so the default ordering was kept.
- JSON is written with 2-space indentation and `sort_keys=True`, which alphabetically sorts keys at every nesting level, including the twotop-level keys (`entries` comes before `errors` alphabetically) and the five keys within each record.

## Program behavior

- The program never raises an exception or stops because of a bad line — any line that fails detection or validation is simply added to `errors`and processing continues, per the "robustness" requirement in the overview.
- Input/output file paths default to `input.txt` / `result.json` in the  current directory, but can be overridden via command-line arguments: `python main.py <input_file> <output_file>`.