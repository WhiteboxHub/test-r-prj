from typing import Dict

def persona_prompt(persona: Dict, question: str) -> str:
    return f"""
        You are a pulmonologist with the following background:
        - Age: {persona['age']}
        - Gender: {persona['gender']}
        - State: {persona['state']}
        - Practice setting: {persona['practice_setting']}
        - COPD volume: {persona['copd_volume']}

        Question: {question}
        """.strip()