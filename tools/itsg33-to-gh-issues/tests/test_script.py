from unittest.mock import patch,Mock
import pytest
import script
import secrets


@patch("script.get_controls")
@patch("script.post_request")
def test_main(mock_post_request, mock_get_controls):
    mock_get_controls.return_value = [
        ["Family1", "Control1", "E1", "Control1 name", "Class1", "Definition1", "Supplemental guidance1", "References1", "IT Security Function", "", "", "", "", "", "Medium", "", "", ""],
        ["Family2", "Control2", "E2", "Control2 name", "Class2", "Definition2", "Supplemental guidance2", "References2", "", "IT Operation Group", "", "", "", "", "Low", "", "", ""]
    ]
    mock_post_request.return_value.status_code = 201

    script.main()

    assert mock_post_request.call_count == 2

@patch("script.requests.post")
def test_post_request_failure():
    issues_url = "https://api.github.com/repos/owner/repo/issues"
    headers = {'Authorization': 'Bearer token'}
    issues_json = {"title": "Test Issue", "body": "This is a test issue"}
    response_mock = Mock(status_code=400, text="Bad request")
    
    with patch('requests.post', return_value=response_mock):
        response = script.post_request(issues_url, headers, issues_json)
        assert response == response_mock
        assert "Failed to create issue for control" in pytest.capsys.readouterr().out
        assert "Response: Bad request" in pytest.readouterr().out

@patch("script.requests.post")
def test_post_request_success():
    issues_url = "https://api.github.com/repos/owner/repo/issues"
    headers = {'Authorization': 'Bearer token'}
    issues_json = {"title": "Test Issue", "body": "This is a test issue"}
    response_mock = Mock(status_code=201, text="Created")

    with patch('requests.post', return_value=response_mock):
        response = script.post_request(issues_url, headers, issues_json)
        assert response == response_mock
        assert "Created issue for control" in pytest.capsys.readouterr().out
        assert "Response: Created" in pytest.readouterr().out

@patch("script.GITHUB_TOKEN", "DuMMyToKeN125795")
def test_get_github_token_exists():
    token = script.get_github_token()
    assert token == "DuMMyToKeN125795"

@patch("script.GITHUB_TOKEN", "")
def test_get_github_token_not_exists():
    with pytest.raises(Exception) as excinfo:
        script.get_github_token()
    assert str(excinfo.value) == 'GITHUB_TOKEN env var not set'

@patch("script.REPO", "owner/repo")
def test_get_issues_url():
    issues_url = script.get_issues_url()
    assert issues_url == "https://api.github.com/repos/owner/repo/issues"

@patch("script.REPO", "")
def test_get_issues_url_not_exists():
    with pytest.raises(Exception) as excinfo:
        script.get_issues_url()
    assert str(excinfo.value) == 'REPO env var not set'

@patch("script.GITHUB_TOKEN", "DuMMyToKeN125795")
def test_get_headers():
    header = script.get_headers()
    assert header["Accept"] == "application/vnd.github+json"
    assert header["Authorization"] == "Bearer DuMMyToKeN125795"
    assert header["X-GitHub-Api-Version"] == "2022-11-28"

@patch("script.get_title", return_value="title")
@patch("script.get_body", return_value="body")
@patch("script.get_labels", return_value=["label1", "label2"])
def test_get_issues_json():
    row = []
    issues_json = script.get_issues_json(row)
    assert issues_json == {"title": "title", "body": "body", "labels":["label1", "label2"]}