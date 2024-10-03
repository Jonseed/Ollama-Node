# Ollama-Node
[Invoke](https://github.com/invoke-ai/InvokeAI) node that uses [Ollama](https://github.com/ollama/ollama) API to expand text prompts for text-to-image generation using local LLMs. It is very basic node. It loads all the models you have installed in Ollama into a dropdown selector, provides a prompt text area, and a sytem prompt (to tell the LLM how you want to transform the prompt), and a switch to unload the LLM model from memory after generation (to free up VRAM for the image generation process). It sends the prompt to the local LLM, which expands the prompt with more detail, and then returns it to Invoke as an output that can be connected to any other prompt field in your workflow.

You give it a simple prompt like this: `A photographic portrait of an elderly man.`

![Screenshot 2024-10-01 154455](https://github.com/user-attachments/assets/b589853a-4635-466c-a984-a62699ba52e5)

And your local LLM expands the prompt into something like this (which works well with text-to-image models like Flux that like detailed natural language prompts):

> A dignified black-and-white photograph of a mature gentleman with a kind face and wispy white hair. The subject is seated in a worn leather armchair, his eyes cast downward as he holds a worn wooden cane in one hand and a well-loved book in the other. His gentle smile suggests a life filled with love and laughter, despite the lines and creases etched into his weathered skin. A warm golden light casts a comforting glow over the scene, illuminating the soft folds of his rumpled suit jacket and the threads of a faded sweater peeking from beneath his collar. In the background, a vintage typewriter and stacks of worn paperbacks sit atop a cluttered desk, hinting at a life spent writing stories and sharing wisdom with others. The image exudes a sense of nostalgia and quiet contemplation, as if the subject is lost in thought while reminiscing about a lifetime of memories. The photographic style is reminiscent of a classic portrait from the mid-20th century, with soft focus and subtle texture adding depth and character to the scene.

![75bfa53a-f657-4878-b543-33c09658aeb9](https://github.com/user-attachments/assets/c6768643-8095-4a8c-a894-b4fb7f2cb678)

# Installation

The [Community Nodes](https://invoke-ai.github.io/InvokeAI/nodes/communityNodes/) page in Invoke's docs notes how to install custom nodes:

> To use a node, add the node to the `nodes` folder found in your InvokeAI install location.
> 
> The suggested method is to use `git clone` to clone the repository the node is found in. This allows for easy updates of the node in the future.
> 
> If you'd prefer, you can also just download the whole node folder from the linked repository and add it to the `nodes` folder.
> 
> To use a community workflow, download the `.json` node graph file and load it into Invoke AI via the **Load Workflow** button in the Workflow Editor.

Please note, by default it looks for the Ollama server at `http://localhost:11434`. If you have Ollama installed at a different address or port, this will need to be manually adjusted in the `ollama_node.py` file in two places.

# Credit

This node was inspired by the [Oobabooga node](https://github.com/sammyf/oobabooga-node) by [Sammy Fischer](https://github.com/sammyf), but that repo now seems to be defunct.

invokeai-node
