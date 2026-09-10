from app.services.language_config import get_language_config


def test_python_language():
    config = get_language_config("python")

    assert config["name"] == "Python"
    assert ".py" in config["extensions"]


def test_javascript_language():
    config = get_language_config("javascript")

    assert config["name"] == "JavaScript"
    assert ".js" in config["extensions"]


def test_sql_language():
    config = get_language_config("sql")

    assert config["name"] == "SQL"
    assert ".sql" in config["extensions"]


def test_language_is_case_insensitive():
    config = get_language_config("PYTHON")

    assert config["name"] == "Python"


def test_unsupported_language():
    try:
        get_language_config("rust")
        assert False
    except ValueError as exc:
        assert "Unsupported language" in str(exc)