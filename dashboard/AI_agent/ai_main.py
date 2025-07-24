from .prompt_templates import generate_image_prompt, generate_story_prompt
from .image_generator import generate_image
from .generate_story import generate_story 
from .extract_story_data import extract_story_data, extract_story_steps, extract_visual_descriptions
from .post_image_generation.add_text_layer import add_text_to_image

def main_generate(question: str, img_path: str) -> str:
    # Step 3: Generate images using each visual description
    max_tries = 3
    i = 0 
    while i < max_tries:
        raw_story = generate_story(question)
        print("Story generated successfully!")
        # Step 2: Extract structured information from the story
        story_response = extract_story_data(raw_story)
        story_steps = story_response["story_steps"]
        if len(story_steps) == 5:
            break
        i += 1
        
    for i in range(5):
        image_prompt = generate_image_prompt(
            setting=story_response['story_setting'],
            style=story_response['story_style'],
            character=story_response['main_character'],
            visual_scene_description=story_steps[i]["visual_scene_description"],
        )
        print(i+1)
        generated_img_path = generate_image(image_prompt,i+1,img_path)
        add_text_to_image(generated_img_path, story_steps[i]["story_point"])

if __name__ == "__main__":
    # Step 1: Generate the story from question
    question = "A detective duck wearing a detective suit is solving a mystery of an egg"
    raw_story = generate_story(question)
    print("Story generated successfully!")
    # Step 2: Extract structured information from the story
    story_response = extract_story_data(raw_story)
    story_steps = story_response["story_steps"]
    # Step 3: Generate images using each visual description
    for i in range(5):
        image_prompt = generate_image_prompt(
            setting=story_response['story_setting'],
            style=story_response['story_style'],
            character=story_response['main_character'],
            visual_scene_description=story_steps[i]["visual_scene_description"],
        )
        print(i+1)
        generated_img_path = generate_image(image_prompt,i+1)
        add_text_to_image(generated_img_path, story_steps[i]["story_point"])

