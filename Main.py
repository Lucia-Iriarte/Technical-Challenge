import json
import sys

from EntryParser import process_lines

# Main entry point for the program. Reads input from a file, processes it, and writes output to a JSON file.


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "result.json"

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    result = process_lines(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"Processed {len(lines)} line(s): "
          f"{len(result['entries'])} valid, {len(result['errors'])} invalid.")
    print(f"Output written to {output_path}")


if __name__ == "__main__":
    main()