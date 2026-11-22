from leads import normalize_phone


def test_removes_spaces_and_country_code():
    assert normalize_phone("+91 99999 01234") == "9999901234"


def test_leaves_a_clean_number_alone():
    assert normalize_phone("9999901234") == "9999901234"


def test_empty_number_stays_empty():
    assert normalize_phone("") == ""
