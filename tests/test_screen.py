from ecourts_research.screen import screen_text


def test_social_engineering_screen():
    text = (
        "The victim received a WhatsApp call from a person posing as a police officer. "
        "The caller threatened arrest and asked the victim not to disclose the matter. "
        "Funds moved to a beneficiary bank account. CDR and SIM records were examined."
    )
    result = screen_text("SRC-TEST", text)

    assert result.score > 0
    assert "social_engineering" in result.matched_groups
    assert "digital_evidence" in result.matched_groups
    assert result.suggested_attack_category in {"digital_arrest", "impersonation", "vishing"}
