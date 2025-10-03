from persona_generator.prompt_templates import build_persona_prompt

def test_build_persona_prompt():
    # Arrange
    persona = {
        "demographics": {
            "age_band": "35-44",
            "gender": "male",
            "state": "CA",
            "urbanicity": "urban"
        },
        "practice": {
            "setting": "academic",
            "years_in_practice": "11-20",
            "board_certified": True,
            "fellowship": "Pulmonary & Critical Care"
        },
        "attitudes": {
            "guideline_adherence": 0.85,
            "innovation_openness": 0.75,
            "access_constraint": 0.3
        }
    }
    question = "What is your approach to treating COPD?"
    
    # Act
    result = build_persona_prompt(persona, question)
    
    # Assert
    assert "You are an expert pulmonologist. Use the following profile to tailor your responses:" in result
    assert "•⁠  ⁠Age Band: 35-44" in result
    assert "•⁠  ⁠Gender: male" in result
    assert "•⁠  ⁠State: CA" in result
    assert "•⁠  ⁠Urbanicity: urban" in result
    assert "•⁠  ⁠Practice Setting: academic" in result
    assert "•⁠  ⁠Years in Practice: 11-20" in result
    assert "•⁠  ⁠Board Certified: True" in result
    assert "•⁠  ⁠Fellowship Training: Pulmonary & Critical Care" in result
    assert "•⁠  ⁠Guideline Adherence: 0.85" in result
    assert "•⁠  ⁠Openness to Innovation: 0.75" in result
    assert "•⁠  ⁠Access Constraints Awareness: 0.3" in result
    assert "Question: What is your approach to treating COPD?" in result

def test_build_persona_prompt_with_minimal_data():
    # Test with minimal required fields
    persona = {
        "demographics": {
            "age_band": "35-44",
            "gender": "male",
            "state": "CA",
            "urbanicity": "urban"
        },
        "practice": {
            "setting": "academic",
            "years_in_practice": "11-20",
            "board_certified": True,
            "fellowship": ""
        },
        "attitudes": {
            "guideline_adherence": 0.5,
            "innovation_openness": 0.5,
            "access_constraint": 0.5
        }
    }
    question = "Brief question?"
    
    result = build_persona_prompt(persona, question)
    assert "Question: Brief question?" in result
    assert "•⁠  ⁠Fellowship Training: " in result  # Should handle empty string gracefully
