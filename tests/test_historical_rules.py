from app.services.historical_rules import load_rules
def test_historical_rules_load():
    rules = load_rules()
    assert len(rules) == 6
def test_historical_rules_have_expected_fields():
    rules = load_rules()
    for rule in rules:
        assert set(rule.keys()) == {"id", "type", "description"}
def test_sql_security_rule_exists():
    rules = load_rules()
    descriptions = [rule["description"] for rule in rules]
    assert "Never interpolate raw user input directly into SQL queries" in descriptions
