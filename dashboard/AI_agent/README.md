# AI Story Generator

This project generates a 5-step children's story with illustrations based on a user-provided prompt. It uses AI to generate the story and images, and then combines them to create a complete storybook-style output.

## Features

-   Generates a 5-step story from a simple prompt.
-   Creates a unique image for each step of the story.
-   Adds the story text as a layer on top of each image.
-   Uses Google's Gemini Pro for story generation and Together AI for image generation.

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage the project's dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

This project requires API keys for Google and Together AI. Create a `.env` file in the root of the project and add the following lines:

```
GOOGLE_API_KEY="your_google_api_key"
TOGETHER_API_KEY="your_together_api_key"
```

**Important:** This project will not work without these API keys.

### 5. Run the Project

Execute the `main.py` script to generate a story:

```bash
python main.py
```

The generated images with text will be saved in the `images/` directory.

## Project Structure

```
.
├── AI_model/
│   ├── generate_story.py
│   ├── image_generator.py
│   ├── extract_story_data.py
│   └── prompt_templates.py
├── post_image_generation/
│   └── add_text_layer.py
├── images/
│   └── (generated images will be saved here)
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## How it Works

1.  **Story Generation:** The `generate_story` module uses the Google Generative AI model to create a 5-step story based on the user's prompt.
2.  **Data Extraction:** The `extract_story_data` module parses the generated story to extract the setting, style, main character, and the 5 story steps.
3.  **Image Generation:** For each story step, the `image_generator` module uses the Together AI model to create an image based on the visual description.
4.  **Text Overlay:** The `add_text_layer` module uses the Pillow library to add the story text to the corresponding image.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.
