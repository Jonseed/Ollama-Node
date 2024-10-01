import requests
from typing import Literal, List
from invokeai.invocation_api import (
    BaseInvocation,
    BaseInvocationOutput,
    InvocationContext,
    invocation,
    invocation_output,
    InputField,
    OutputField,
    UIComponent
)

# Helper functions to interact with the Ollama API

def get_models() -> List[str]:
    """Fetch available models from the Ollama API."""
    url = "http://localhost:11434/api/tags"
    response = requests.get(url)
    models = response.json().get('models', [])
    return [model['name'] for model in models]

# Define the known models as a Literal (you can update this based on expected models)
# This needs to be updated manually if models change
models_list = get_models()
# Create a Literal type for the models
ModelTypes = Literal[tuple(models_list)]  # This will require you to update it if models change.

def generate_prompt(model: str, prompt: str, system_prompt: str, unload_model: bool) -> str:
    """Send a prompt to the Ollama API with a system context and conditionally include keep_alive."""
    url = "http://localhost:11434/api/generate"
    
    # Base payload
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,  # Include the system prompt to guide the model's response
        "stream": False
    }
    
    # Conditionally include keep_alive if unload_model is True
    if unload_model:
        payload["keep_alive"] = 0  # If unload_model is True, set keep_alive to 0

    response = requests.post(url, json=payload)
    return response.json().get('response', '')

# Output Class
@invocation_output("generated_prompt_output")
class OllamaOutput(BaseInvocationOutput):
    generated_prompt: str = OutputField(description="Generated text prompt.")

# Invocation Node
@invocation(
    "ollama_prompt_node",
    title="Ollama Prompt Generator",
    tags=["prompt", "llm", "ollama", "text-generation"],
    category="prompt",
    version="1.0.0",
    use_cache=False,
)
class OllamaNode(BaseInvocation):
    """Node that communicates with Ollama API to generate text prompts."""

    model: ModelTypes = InputField(
        default=models_list[0],  # Default to the first available model
        description="Choose the LLM model.",
        ui_component=UIComponent.Textarea  # Use textarea for input (dropdowns not directly supported)
    )
    prompt: str = InputField(
        default="Describe a mystical creature.", 
        description="Prompt to generate.",
        ui_component=UIComponent.Textarea  # Use textarea for multi-line input
    )
    system_prompt: str = InputField(
        default="You are creating a prompt for an AI text-to-image generator. You will start with a brief prompt provided by the user. You will expand the brief prompt into a detailed natural language prompt, including:\n\n"
                "Medium: Briefly state the type of visual medium, whether photograph, painting, sculpture, printmaking, digital art, etc.\n"
                "Subjects: Describe the main subjects, their appearance, clothing, expressions, and actions.\n"
                "Setting: Elaborate on the setting, including time of day, weather, and environment details.\n"
                "Background Elements: Add details about the background, secondary characters, and relevant objects or props.\n"
                "Sensory Details: Incorporate sensory experiences such as sounds, smells, and textures.\n"
                "Artistic Style: Include details about the artistic style, color palette, and stylistic choices, as well as any additional details about the medium, such as camera model and type and lens, if photography.\n\n"
                "Here is an example of receiving a user input prompt and expanding it:\n\n"
                "User Input Prompt: “sunset on a beach”\n\n"
                "Your expanded Prompt response: “A serene sunset scene on a tranquil beach. The sky is painted with hues of orange, pink, and purple as the sun dips below the horizon. Gentle waves lap against the shore, where a young woman in a flowing white dress stands barefoot, gazing out at the sea. Her hair is tousled by a light breeze, and she holds a small bouquet of wildflowers. In the background, a lighthouse stands tall on a rocky outcrop, its light beginning to flicker on. Seagulls call softly as they glide overhead, and the scent of saltwater mingles with the fragrance of blooming jasmine. The scene is reminiscent of an impressionist painting, with soft, blended brushstrokes and a warm, inviting color palette.”\n\n"
                "Don't say anything else except the expanded prompt itself. No introductory phrase, and no quotation marks.\n\n"
                "The user will now give you the input brief prompt to expand:",
        description="Context to guide the model's generation.",
        ui_component=UIComponent.Textarea  # Use textarea for multi-line input
    )
    
    # Use bool to create a checkbox for unloading the model
    unload_model: bool = InputField(
        default=True, 
        description="Unload the model after generation to free up memory."
    )

    def invoke(self, context: InvocationContext) -> OllamaOutput:
        """Invoke the model and return the generated prompt."""
        available_models = get_models()
        if self.model not in available_models:
            raise ValueError(f"Model '{self.model}' is not available. Choose from: {', '.join(available_models)}")

        # Pass unload_model to generate_prompt, which conditionally includes keep_alive
        generated_text = generate_prompt(self.model, self.prompt, self.system_prompt, self.unload_model)
        
        return OllamaOutput(generated_prompt=generated_text)

