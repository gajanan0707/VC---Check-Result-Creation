
import os
import requests
import json

# Functional Tests

def test_func_api_key_authentication_missing():
    # Test case for missing API key
    response = requests.get("http://localhost:5000/")
    assert response.status_code == 401
    assert response.json()["success"] == False
    assert "Authentication failed" in response.json()["message"]

def test_func_api_key_authentication_invalid():
    # Test case for invalid API key
    headers = {"x-api-key": "invalid_key"}
    response = requests.get("http://localhost:5000/", headers=headers)
    assert response.status_code == 401
    assert response.json()["success"] == False
    assert "Authentication failed" in response.json()["message"]

def test_func_root_endpoint_success():
    # Test case for successful access to the root endpoint with a valid API key
    api_key = os.environ.get("SECRET_API_KEY", "test_api_key")
    headers = {"x-api-key": api_key}
    response = requests.get("http://localhost:5000/", headers=headers)
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "Translate api" in response.json()["message"]

def test_func_translate_missing_target_language():
    # Test case for missing targetLanguage query parameter
    api_key = os.environ.get("SECRET_API_KEY", "test_api_key")
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    data = ["hello"]
    response = requests.post("http://localhost:5000/translate", headers=headers, data=json.dumps(data))
    assert response.status_code == 400
    assert response.json()["success"] == False
    assert "targetLangauge is required" in response.json()["message"]

def test_func_translate_empty_body():
    # Test case for empty request body
    api_key = os.environ.get("SECRET_API_KEY", "test_api_key")
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    response = requests.post("http://localhost:5000/translate?targetLanguage=es", headers=headers, data=json.dumps([]))
    assert response.status_code == 400
    assert response.json()["success"] == False
    assert "texts is required" in response.json()["messsage"]

def test_func_translate_successful_translation():
    # Test case for a successful translation (mocking external API and Redis if possible)
    # For now, we'll assume a successful call and check the structure.
    # In a real scenario, this would involve mocking the external API and Redis.
    api_key = os.environ.get("SECRET_API_KEY", "test_api_key")
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    data = ["hello", "world"]
    response = requests.post("http://localhost:5000/translate?targetLanguage=es", headers=headers, data=json.dumps(data))
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert isinstance(response.json()["data"], list)
    assert len(response.json()["data"]) == 2
    assert "main_text" in response.json()["data"][0]
    assert "translate_text" in response.json()["data"][0]

# Style Tests

def test_style_file_naming_convention():
    # Check if the main route file is named 'translate.js' within the 'routes' directory
    assert os.path.exists("translate_language/routes/translate.js")

def test_style_env_file_usage():
    # Check if .env file is mentioned in .gitignore (implies proper env var usage)
    with open("translate_language/.gitignore", "r") as f:
        gitignore_content = f.read()
    assert ".env" in gitignore_content

def test_style_dependencies_in_package_json():
    # Check for specific dependencies in package.json
    with open("translate_language/package.json", "r") as f:
        package_json = json.load(f)
    dependencies = package_json.get("dependencies", {})
    assert "express" in dependencies
    assert "axios" in dependencies
    assert "redis" in dependencies
    assert "dotenv" in dependencies
    assert "morgan" in dependencies
    assert "cors" in dependencies



