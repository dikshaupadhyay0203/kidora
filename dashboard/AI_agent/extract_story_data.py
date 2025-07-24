import re

import re

def extract_story_data(llm_output: str) -> dict:
    """Extracts structured story data: setting, style, character, story steps (story point + visual description)."""
    
    setting_match = re.search(r"\*\*STORY SETTING:\*\*\n(.*?)\n\n", llm_output, re.DOTALL)
    style_match = re.search(r"\*\*STORY STYLE:\*\*\n(.*?)\n\n", llm_output, re.DOTALL)
    character_match = re.search(r"\*\*MAIN CHARACTER:\*\*\n(.*?)\n\n", llm_output, re.DOTALL)

    story_steps = []
    steps_section_match = re.search(r"\*\*Here is your story in 5 magical steps:\*\*\n\n(.*)", llm_output, re.DOTALL)
    
    if steps_section_match:
        steps_text = steps_section_match.group(1).strip()

        # Split on steps: "**1. " through "**5. "
        raw_steps = re.split(r"\*\*(\d+)\.\s", steps_text)
        raw_steps = raw_steps[1:]  # first item is junk

        for i in range(0, len(raw_steps), 2):
            step_number = raw_steps[i].strip()
            full_step = raw_steps[i + 1].strip()

            story_point_match = re.search(r"^(.*?)(?=\*\*Visual Scene Description\*\*:)", full_step, re.DOTALL)
            visual_description_match = re.search(r"\*\*Visual Scene Description\*\*:\s*(.*)", full_step, re.DOTALL)

            story_point = story_point_match.group(1).strip() if story_point_match else ""
            visual_description = visual_description_match.group(1).strip() if visual_description_match else ""

            story_steps.append({
                "story_point": story_point,
                "visual_scene_description": visual_description
            })

    return {
        "story_setting": setting_match.group(1).strip() if setting_match else "",
        "story_style": style_match.group(1).strip() if style_match else "",
        "main_character": character_match.group(1).strip() if character_match else "",
        "story_steps": story_steps
    }


def extract_story_steps(story_dict: dict) -> list:
    """Extracts visual scene descriptions from the story text."""
    return [step["story_point"] for step in story_dict.get("story_steps", []) if step["story_point"]]


def extract_visual_descriptions(story_dict: dict) -> list:
    """Extracts all visual scene descriptions from the story dictionary."""
    return [step["visual_scene_description"] for step in story_dict.get("story_steps", []) if step["visual_scene_description"]]

