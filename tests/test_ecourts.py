from ecourts_research.ecourts import is_valid_cnr, normalize_cnr, portal_url


def test_cnr_normalization():
    assert normalize_cnr("MHAU-0199 9999 2015") == "MHAU019999992015"


def test_cnr_validation():
    assert is_valid_cnr("MHAU019999992015")
    assert not is_valid_cnr("short")


def test_official_portal_mapping():
    assert portal_url("case-status").startswith("https://services.ecourts.gov.in/")
