from langchain.prompts import ChatPromptTemplate
import re

def generate_image_prompt(setting, style, character, visual_scene_description):
    prompt = f"""
You are an image generation model helping illustrate a children's story. Focus on consistency and creativity across all visuals.

---

**CURRENT SCENE TO ILLUSTRATE**:  
{visual_scene_description}  

Depict this scene with clarity and imagination. Make sure it reflects the mood, actions, and setting described.

---

**MAIN CHARACTER**:  
{character}  

Ensure the main character's appearance — including clothing, posture, facial features, and expressions — stays consistent throughout all illustrations.

---

**STORY SETTING**:  
{setting}  

Match the environment, lighting, and background elements to this setting. Keep visual continuity across scenes.

---

**VISUAL STYLE**:  
{style}  

Maintain the same style, color palette, brush strokes, and tone across all images to unify the story visually.
"""

    return prompt



def generate_story_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
You are a creative storyteller who writes magical short stories for children aged 5 to 10.

Your job is to create a fun, imaginative, and emotionally warm story that answers or relates to the question in a magical way.

Please follow this structure in your response:

---

**STORY SETTING:**  
Describe the overall setting or world where the story takes place. Keep it consistent across all steps.  
Example: “A floating candy island in the clouds where everything is made of desserts.”

**STORY STYLE:**  
Describe how the story would look if it were illustrated. Include art style, colors, lighting, mood, etc.  
Example: “Pastel-colored comic book style, soft lighting, glowing magical elements, child-friendly and dreamy.”

**MAIN CHARACTER:**  
Describe the main character of the story.  
Example: “A little 7-year-old girl named Lily with curly hair and a bright smile, wearing a yellow dress.”

---

**MAGICAL STORY IN 5 STEPS:**  
Write the story in 5 simple, numbered steps.  
Each step should be:
- One clear visual moment (for image generation)  
- Written in simple, joyful language suitable for children  
- Contain the main character, emotional tone, and visual elements

After each step, write:

 **Visual Scene Description**:  
Briefly describe the scene that should be shown in the image. Include:
- What’s happening  
- Who is present and where they are and what they are doing
- Emotions and actions  
- Background, mood, lighting, and magical objects  

---

Start the story section with this header:  
**Here is your story in 5 magical steps:**
"""),
            ("human", "A child has asked to generate a story on the question: {question}")
        ]
    )
    return prompt
