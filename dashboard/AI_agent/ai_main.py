from .prompt_templates import generate_image_prompt, generate_story_prompt
from .image_generator import generate_image
from .generate_story import generate_story 
from .extract_story_data import extract_story_data, extract_story_steps, extract_visual_descriptions
from .post_image_generation.add_text_layer import add_text_to_image
from uuid import uuid4

def main_generate(question: str, img_path: str):
    # Step 3: Generate images using each visual description
    max_tries = 2
    i = 0 
    run_id = uuid4().hex[:10]
    story_response = {"story_steps": []}
    story_steps = []
    while i < max_tries:
        raw_story = generate_story(f"{question}\n\nGenerate a fresh variation. Variation token: {run_id}")
        print("Story generated successfully!")
        # Step 2: Extract structured information from the story
        story_response = extract_story_data(raw_story)
        story_steps = story_response["story_steps"]
        if len(story_steps) >= 5:
            break
        i += 1

    if not story_steps:
        raise RuntimeError("Story format parsing failed. Please try a slightly different prompt.")

    generated_images = []
    image_generation_errors = []
    total_steps = min(5, len(story_steps))
    for i in range(total_steps):
        image_prompt = generate_image_prompt(
            setting=story_response['story_setting'],
            style=story_response['story_style'],
            character=story_response['main_character'],
            visual_scene_description=story_steps[i]["visual_scene_description"],
        )
        print(i+1)
        output_filename = f"{run_id}_{i + 1}.png"
        prompt_with_variation = f"{image_prompt}\n\nVariation token for uniqueness: {run_id}-{i + 1}"
        try:
            generated_img_path = generate_image(
                prompt_with_variation,
                i + 1,
                img_path,
                filename=output_filename,
                width=768,
                height=768,
                timeout_seconds=25,
                max_retries=1,
            )
            if generated_img_path:
                add_text_to_image(generated_img_path, story_steps[i]["story_point"])
                generated_images.append(f"generated_images/{output_filename}")
        except Exception as error:
            image_generation_errors.append(str(error))

    return {
        "images": generated_images,
        "run_id": run_id,
        "story_steps": [step.get("story_point", "") for step in story_steps[:5]],
        "image_error": image_generation_errors[0] if image_generation_errors else None,
    }

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

