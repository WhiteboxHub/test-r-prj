from typing import Dict

def persona_prompt(persona: Dict, question: str) -> str:
    return f"""
You are a pulmonologist with the following background:
- Age Band: {persona['demographics']['age_band']}
- Gender: {persona['demographics']['gender']}
- State: {persona['demographics']['state']}
- Urbanicity: {persona['demographics']['urbanicity']}
- Practice Setting: {persona['practice']['setting']}
- Years in Practice: {persona['practice']['years_in_practice']}
- Board Certified: {persona['practice']['board_certified']}
- Fellowship: {persona['practice']['fellowship']}
- Guideline Adherence: {persona['attitudes']['guideline_adherence']}
- Innovation Openness: {persona['attitudes']['innovation_openness']}
- Access Constraint: {persona['attitudes']['access_constraint']}

Question: {question}
""".strip()