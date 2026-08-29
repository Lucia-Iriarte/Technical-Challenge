import re
from typing import Optional, Tuple, Dict, List

# This module is responsible for parsing a single line of input into a structured record.

def _is_pure_digits(s: str) -> bool:
    return s.isdigit()


def _is_phone_like(s: str) -> bool:
    has_digit = any(ch.isdigit() for ch in s)
    has_separator = any(not ch.isdigit() for ch in s)
    return has_digit and has_separator


def normalize_phone(raw: str) -> Optional[str]:
    digits = re.sub(r"\D", "", raw)
    if len(digits) != 10:
        return None
    return f"{digits[0:3]}-{digits[3:6]}-{digits[6:10]}"


def normalize_zip(raw: str) -> Optional[str]:
    candidate = raw.strip()
    if candidate.isdigit() and len(candidate) == 5:
        return candidate
    return None


def _split_name(full_name: str) -> Optional[Tuple[str, str]]:
    full_name = full_name.strip()
    if " " not in full_name:
        return None
    firstname, lastname = full_name.rsplit(" ", 1)
    firstname, lastname = firstname.strip(), lastname.strip()
    if not firstname or not lastname:
        return None
    return firstname, lastname


# Format detection + field extraction

def _extract_raw_fields(line: str) -> Optional[Dict[str, str]]:
    fields = [f.strip() for f in line.split(",")]

    if len(fields) == 5:
        f0, f1, f2, f3, f4 = fields

        # Format A
        if _is_phone_like(f2) and _is_pure_digits(f4):
            return {
                "lastname": f0,
                "firstname": f1,
                "phone": f2,
                "color": f3,
                "zip": f4,
            }

        # Format C
        if _is_pure_digits(f2) and _is_phone_like(f3):
            return {
                "firstname": f0,
                "lastname": f1,
                "zip": f2,
                "phone": f3,
                "color": f4,
            }

        return None 

    if len(fields) == 4:
        f0, f1, f2, f3 = fields

        # Format B
        if _is_pure_digits(f2) and _is_phone_like(f3):
            names = _split_name(f0)
            if names is not None:
                firstname, lastname = names
                return {
                    "firstname": firstname,
                    "lastname": lastname,
                    "color": f1,
                    "zip": f2,
                    "phone": f3,
                }

        return None

    # Any other number of comma-separated fields is not a known format
    return None


# Public API

def parse_line(line: str) -> Optional[Dict[str, str]]:
    line = line.rstrip("\n").rstrip("\r")
    if not line.strip():
        return None  # blank line -> invalid

    raw = _extract_raw_fields(line)
    if raw is None:
        return None

    phone = normalize_phone(raw["phone"])
    if phone is None:
        return None

    zipcode = normalize_zip(raw["zip"])
    if zipcode is None:
        return None

    firstname = raw["firstname"].strip()
    lastname = raw["lastname"].strip()
    color = raw["color"].strip()

    if not firstname or not lastname or not color:
        return None

    return {
        "firstname": firstname,
        "lastname": lastname,
        "phonenumber": phone,
        "color": color,
        "zipcode": zipcode,
    }


def process_lines(lines: List[str]) -> Dict[str, list]:
    entries = []
    errors = []

    for idx, line in enumerate(lines):
        record = parse_line(line)
        if record is None:
            errors.append(idx)
        else:
            entries.append(record)

    entries.sort(key=lambda r: (r["lastname"], r["firstname"]))

    return {"entries": entries, "errors": errors}