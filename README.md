# Parser

Parses a text file with one personal-info entry per line (in one of three
possible formats), normalizes each valid entry, and writes the result as a
single JSON object to `result.json`.

## Usage

```bash
python main.py [input_file] [output_file]
```

Defaults: `input_file=input.txt`, `output_file=result.json`.


## Project structure

```
.
├── main.py                  # entry point: reads input, writes result.json
├── EntryParser.py          # parsing / detection / normalization logic
├── Assumptions.md           # documented assumptions (required by the challenge)
├── input.txt         # example input taken from the challenge PDF
└── tests/
    └── TestParse.py # unit tests covering formats A/B/C and edge cases
```

> **Note:** the parsing module is named `entry_parser.py` (not `parser.py`)
> because `parser` collides with a built-in CPython module of the same
> name (deprecated, and only removed in Python 3.10+). On Python 3.9 that
> shadowing makes `from parser import ...` pick up the wrong module and
> fail with an `ImportError`.

## Running tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Supported input formats

| Format | Layout |
|--------|--------|
| A | `Lastname, Firstname, (XXX)-XXX-XXXX, Color, XXXXX` |
| B | `Firstname Lastname, Color, XXXXX, XXX XXX XXXX` |
| C | `Firstname, Lastname, XXXXX, XXX XXX XXXX, Color` |

The format of each line is auto-detected (see `Assumptions.md` for details
on how). Invalid lines (bad phone/zip, or lines that don't match any known
format) do not stop processing their 0 indexed line number is recorded
in the `errors` list of the output.

## Output shape

```json
{
  "entries": [
    {
      "color": "...",
      "firstname": "...",
      "lastname": "...",
      "phonenumber": "XXX-XXX-XXXX",
      "zipcode": "XXXXX"
    }
  ],
  "errors": [0, 3]
}
