import pytest
import json
import numpy as np
from pathlib import Path
from unittest.mock import patch, mock_open

from persona_generator.persona_generator import PersonaGenerator, BEHAVIOR_RULES


# Sample distribution data for testing
SAMPLE_DISTRIBUTION = {
    "gender": {"male": 0.6, "female": 0.4},
    "age_band": {"25-34": 0.1, "35-44": 0.3, "45-54": 0.3, "55-64": 0.2, "65+": 0.1},
    "urbanicity": {"urban": 0.7, "suburban": 0.2, "rural": 0.1},
    "practice_setting": {"academic": 0.3, "community": 0.5, "private": 0.2},
    "state": {"CA": 0.15, "NY": 0.1, "TX": 0.1, "Other": 0.65},
    "years_in_practice": {"0-5": 0.1, "6-10": 0.2, "11-20": 0.4, "21-30": 0.2, "31+": 0.1},
    "board_certified": {"true": 0.9, "false": 0.1}
}

# Mock for the file read operation
def mock_json_file():
    return json.dumps(SAMPLE_DISTRIBUTION)

@patch('builtins.open', new_callable=mock_open, read_data=mock_json_file())
def test_persona_generator_init(mock_file):
    # Test initialization with a valid distribution file
    generator = PersonaGenerator("dummy_path.json")
    assert generator.distributions == SAMPLE_DISTRIBUTION
    mock_file.assert_called_once_with("dummy_path.json", "r")

def test_sample_from_probs():
    # Set up generator with mock data
    with patch('builtins.open', new_callable=mock_open, read_data=mock_json_file()):
        generator = PersonaGenerator("dummy.json")
    
    
    options = ['a', 'b', 'c']
    probs = {'a': 0.5, 'b': 0.3, 'c': 0.2}
    
   
    results = []
    for _ in range(1000):
        results.append(generator._sample_from_probs(options, probs))
    
    assert all(r in options for r in results)
    
    counts = {opt: results.count(opt) for opt in options}
    assert counts['a'] > counts['b'] > counts['c']

@patch('builtins.open', new_callable=mock_open, read_data=mock_json_file())
@patch('persona_generator.persona_generator.RNG')
def test_generate_persona(mock_rng, mock_file):
    mock_instance = mock_rng.return_value
    mock_instance.choice.side_effect = [
        'male',      # gender
        '45-54',     # age_band
        'urban',     # urbanicity
        'community', # practice_setting
        'CA',        # state
        '11-20',     # years_in_practice
        'true'       # board_certified
    ]
    mock_instance.integers.return_value = 15  
    mock_instance.uniform.return_value = 0.7  
    
    generator = PersonaGenerator("dummy.json")
    persona = generator._generate_persona(1)
    
    # Verify basic structure
    assert 'persona_id' in persona
    assert persona['persona_id'] == 'pulm_001'
    
    # Verify demographics
    assert persona['demographics'] == {
        'gender': 'male',
        'age_band': '45-54',
        'state': 'CA',
        'urbanicity': 'urban'
    }
    
    # Verify practice details
    assert persona['practice'] == {
        'setting': 'community',
        'years_in_practice': '11-20',
        'board_certified': True,
        'fellowship': 'Pulmonary & Critical Care'
    }
    
    # Verify attitudes are within expected ranges based on behavior rules
    assert 0.55 <= persona['attitudes']['guideline_adherence'] <= 0.85
    assert 0.45 <= persona['attitudes']['innovation_openness'] <= 0.8
    assert 0.1 <= persona['attitudes']['access_constraint'] <= 0.4

@patch('builtins.open', new_callable=mock_open, read_data=mock_json_file())
def test_generate_personas(mock_file, tmp_path):
    # Test generating multiple personas
    with patch('numpy.random.default_rng') as mock_rng:
        # Mock the RNG to return predictable values
        mock_instance = mock_rng.return_value
        mock_instance.choice.side_effect = [
            0, 0, 0, 0, 0, 0, 0,  # First persona
            1, 1, 1, 1, 1, 1, 1   # Second persona
        ]
        mock_instance.integers.return_value = 10
        mock_instance.random.return_value = 0.7
        
        generator = PersonaGenerator("dummy.json")
        personas = generator.generate_personas(n=2)
    
    # Verify we got the correct number of personas
    assert len(personas) == 2
    
    # Verify all personas have required fields
    for i, persona in enumerate(personas):
        assert 'persona_id' in persona
        assert persona['persona_id'] == f'pulm_{i+1:03d}'
        assert 'demographics' in persona
        assert 'practice' in persona
        assert 'attitudes' in persona

def test_save_personas(tmp_path):
    # Test saving personas to a file
    output_file = tmp_path / "test_personas.json"
    
    # Create a sample distribution file
    dist_file = tmp_path / "distributions.json"
    with open(dist_file, 'w') as f:
        json.dump(SAMPLE_DISTRIBUTION, f)
    
    with patch('numpy.random.default_rng') as mock_rng:
        # Mock the RNG to return predictable values
        mock_instance = mock_rng.return_value
        mock_instance.choice.side_effect = [0, 0, 0, 0, 0, 0, 0]  # One persona
        mock_instance.integers.return_value = 10
        mock_instance.random.return_value = 0.7
        
        generator = PersonaGenerator(str(dist_file))
        generator.save_personas(str(output_file), n=1)
    
    # Verify file was written
    assert output_file.exists()
    
    # Verify file contents
    with open(output_file, 'r') as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 1
        assert 'persona_id' in data[0]
        assert data[0]['persona_id'] == 'pulm_001'
