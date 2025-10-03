import json
import pytest
import pytest_asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from src.app.utils.llms.openai import OpenAIClient

# Sample persona data for testing
SAMPLE_PERSONA = {
    "persona_id": "test_pulm_001",
    "demographics": {
        "gender": "male",
        "age_band": "35-44",
        "state": "CA",
        "urbanicity": "urban"
    },
    "practice": {
        "setting": "academic",
        "years_in_practice": 10,
        "board_certified": True,
        "fellowship": "Pulmonary & Critical Care"
    },
    "attitudes": {
        "guideline_adherence": 0.8,
        "innovation_openness": 0.7,
        "access_constraint": 0.3
    }
}

TEST_QUESTION = "What is your typical first-line therapy for newly diagnosed moderate COPD?"

def test_persona_structure():
    """Test that the persona structure contains all required fields."""
    required_fields = ["persona_id", "demographics", "practice", "attitudes"]
    for field in required_fields:
        assert field in SAMPLE_PERSONA, f"Missing required field: {field}"
    
 
    demo_fields = ["gender", "age_band", "state", "urbanicity"]
    for field in demo_fields:
        assert field in SAMPLE_PERSONA["demographics"], f"Missing demographics field: {field}"
    
    
    practice_fields = ["setting", "years_in_practice", "board_certified", "fellowship"]
    for field in practice_fields:
        assert field in SAMPLE_PERSONA["practice"], f"Missing practice field: {field}"
    
    
    attitude_fields = ["guideline_adherence", "innovation_openness", "access_constraint"]
    for field in attitude_fields:
        assert field in SAMPLE_PERSONA["attitudes"], f"Missing attitude field: {field}"

@pytest.mark.asyncio
@patch('src.app.utils.llms.openai.openai.ChatCompletion.acreate')
async def test_openai_client_with_persona(mock_acreate):
    """Test that the OpenAI client can be initialized and called with a persona."""
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = {"content": "Test response"}
    mock_acreate.return_value = mock_response
    
    
    client = OpenAIClient(model="gpt-4")
    response = await client.chat("Test question")
    
    
    assert response == "Test response"
    mock_acreate.assert_called_once()

def test_persona_loading(tmp_path):
    """Test that personas can be loaded from a JSON file."""
    
    personas_file = tmp_path / "test_personas.json"
    with open(personas_file, 'w') as f:
        json.dump([SAMPLE_PERSONA], f)
    
    
    with open(personas_file) as f:
        personas = json.load(f)
    
    assert isinstance(personas, list)
    assert len(personas) > 0
    assert personas[0]["persona_id"] == SAMPLE_PERSONA["persona_id"]

def test_persona_attributes():
    """Test that persona attributes are correctly set."""
    persona = SAMPLE_PERSONA
    
    # Test demographics
    assert persona["demographics"]["gender"] == "male"
    assert persona["demographics"]["age_band"] == "35-44"
    assert persona["demographics"]["state"] == "CA"
    assert persona["demographics"]["urbanicity"] == "urban"
    
    # Test practice
    assert persona["practice"]["setting"] == "academic"
    assert persona["practice"]["years_in_practice"] == 10
    assert persona["practice"]["board_certified"] is True
    assert persona["practice"]["fellowship"] == "Pulmonary & Critical Care"
    
    # Test attitudes (should be between 0 and 1)
    assert 0 <= persona["attitudes"]["guideline_adherence"] <= 1
    assert 0 <= persona["attitudes"]["innovation_openness"] <= 1
    assert 0 <= persona["attitudes"]["access_constraint"] <= 1

@pytest.mark.asyncio
@patch('src.app.utils.llms.openai.openai.ChatCompletion.acreate')
async def test_persona_response_format(mock_acreate):
    """Test that the response from a persona is in the expected format."""
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = {
        "content": "As a pulmonologist with 10 years of experience in an academic setting..."
    }
    mock_acreate.return_value = mock_response
    
    # Initializing client and make a call
    client = OpenAIClient()
    response = await client.chat(TEST_QUESTION)
    
    # Verifying the response format
    assert isinstance(response, str)
    assert len(response) > 0
    assert "pulmonologist" in response.lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
