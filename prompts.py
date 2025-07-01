def get_idea_prompt(interest, region):
    return f"""
    You are an expert in brainstorming innovative startup ideas. Follow this chain-of-thought process to generate exactly one unique EdTech startup idea for college students in India:

    1. Identify a specific pain point for Indian college students (e.g., employability gaps, lack of affordable content, limited access to niche skills, or academic stress).
    2. Consider current EdTech trends in India: AI-driven personalization, vernacular content (e.g., Hindi, Tamil), hybrid learning, gamification, blockchain credentials, or AR/VR education.
    3. Propose a novel solution that is distinct from existing platforms like BYJU’S, Unacademy, UpGrad, Simplilearn, or PhysicsWallah, avoiding overlap in test prep or generic upskilling.
    4. Ensure the idea is feasible, scalable, and tailored to the 43.3 million college students in India, with 60% smartphone ownership and 900M projected internet users by 2025.
    5. Craft a concise description (100-150 words) that is unique, avoiding any repetition of previously generated ideas. Focus on niche areas like mental health, peer learning, or industry-specific skills.

    Generate one startup idea for the {interest} domain targeting {region}.
    """

def get_business_canvas_prompt(idea, section):
    return f"""
    Given the startup idea: '{idea}', provide a concise {section} analysis for a business model canvas, focusing on a {section} relevant to an edtech startup for college students in India.
    """