import pytest
from tools.skunky_preview import validate_endpoint


def test_secure_api_url():
    assert validate_endpoint("https://api.example.com/") == "https://api.example.com"
    assert validate_endpoint("http://127.0.0.1:8001") == "http://127.0.0.1:8001"
    with pytest.raises(ValueError):
        validate_endpoint("http://example.com")
    with pytest.raises(ValueError):
        validate_endpoint("https://user:pass@example.com")
