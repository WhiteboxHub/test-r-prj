from pathlib import Path
from distributions_extractor.clients.nppes_client import NPPESClient
from distributions_extractor.clients.cms_physician_compare_client import CMSPhysicianCompareClient
from distributions_extractor.clients.hrsa_client import HRSAClient
from distributions_extractor.clients.medscape_client import MedscapeClient
from distributions_extractor.distributions.pulmonologist_distribution_builder import PulmonologistDistributionBuilder
from persona_generator.persona_generator import PersonaGenerator
from persona_generator.prompt_templates import build_persona_prompt


def run_persona_generation(state: str = "CA"):
    
    nppes = NPPESClient()
    cms = CMSPhysicianCompareClient()
    hrsa = HRSAClient()
    medscape = MedscapeClient()

    builder = PulmonologistDistributionBuilder(nppes, cms, hrsa, medscape)
    distribution = builder.build_distribution(state=state)

    base_dir = Path(__file__).parent.parent 
    distribution_file = base_dir / "distributions_extractor" / "sample_distributions.json"
    output_personas_file = base_dir / "data" / "personas.json"

  
    generator = PersonaGenerator(distribution_file)

  
    generator.save_personas(output_personas_file, n=20)


    personas = generator.generate_personas(n=20)

  
    sample_prompt = build_persona_prompt(
        personas[0],
        "What is your typical first-line therapy for newly diagnosed moderate COPD?"
    )
    print("\n--- Example Persona Prompt ---\n")
    print(sample_prompt)


if __name__ == "__main__":
    run_persona_generation("CA")