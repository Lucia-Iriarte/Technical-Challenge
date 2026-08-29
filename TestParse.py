import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# This module contains unit tests for the EntryParser module, which is responsible for parsing lines of input into structured records.

from EntryParser import parse_line, process_lines, normalize_phone, normalize_zip

def test_format_a():
    line = "Washington, Booker T., (703)-742-0996, Blue, 10013"
    record = parse_line(line)
    assert record == {
        "firstname": "Booker T.",
        "lastname": "Washington",
        "phonenumber": "703-742-0996",
        "color": "Blue",
        "zipcode": "10013",
    }

def test_format_b():
    line = "James Murphy, Red, 11237, 703 955 0373"
    record = parse_line(line)
    assert record == {
        "firstname": "James",
        "lastname": "Murphy",
        "phonenumber": "703-955-0373",
        "color": "Red",
        "zipcode": "11237",
    }

def test_format_c():
    line = "Kerri, Chandler, 10013, 646 111 0101, Green"
    record = parse_line(line)
    assert record == {
        "firstname": "Kerri",
        "lastname": "Chandler",
        "phonenumber": "646-111-0101",
        "color": "Green",
        "zipcode": "10013",
    }

def test_invalid_phone_wrong_digit_count():
    # phone has only 9 digits
    line = "Kerri, Chandler, 10013, 646 111 010, Green"
    assert parse_line(line) is None


def test_invalid_zip_too_long():
    # zip is too long (9 digits)
    line = "Chandler, Kerri, (623)-668-9293, pink, 123123121"
    assert parse_line(line) is None


def test_unparseable_garbage_line():
    assert parse_line("error500") is None


def test_blank_line_is_invalid():
    assert parse_line("   ") is None
    assert parse_line("") is None


def test_normalize_phone_various_separators():
    assert normalize_phone("(703)-742-0996") == "703-742-0996"
    assert normalize_phone("703 955 0373") == "703-955-0373"
    assert normalize_phone("7039550373") == "703-955-0373"
    assert normalize_phone("703-955-037") is None  # only 9 digits


def test_normalize_zip():
    assert normalize_zip("10013") == "10013"
    assert normalize_zip(" 10013 ") == "10013"
    assert normalize_zip("123123121") is None
    assert normalize_zip("100") is None
    assert normalize_zip("1001a") is None


def test_process_lines_matches_spec_example():
    lines = [
        "Booker T., Washington, 87360, 373 781 7380, yellow",
        "Chandler, Kerri, (623)-668-9293, pink, 123123121",
        "James Murphy, yellow, 83880, 018 154 6474",
        "error500",
    ]
    result = process_lines(lines)
    assert result["errors"] == [1, 3]
    assert result["entries"] == [
        {
            "firstname": "James",
            "lastname": "Murphy",
            "phonenumber": "018-154-6474",
            "color": "yellow",
            "zipcode": "83880",
        },
        {
            "firstname": "Booker T.",
            "lastname": "Washington",
            "phonenumber": "373-781-7380",
            "color": "yellow",
            "zipcode": "87360",
        },
    ]

def test_sorting_is_by_lastname_then_firstname():
    lines = [
        "Alice Zorro, Blue, 10001, 111 222 3333",
        "Bob Alonso, Red, 10002, 111 222 3334",
        "Amy Alonso, Green, 10003, 111 222 3335",
    ]
    result = process_lines(lines)
    lastnames_firstnames = [(e["lastname"], e["firstname"]) for e in result["entries"]]
    assert lastnames_firstnames == [
        ("Alonso", "Amy"),
        ("Alonso", "Bob"),
        ("Zorro", "Alice"),
    ]

if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-v"]))