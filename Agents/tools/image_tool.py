import torch
import gc
from langchain_community.llms import Ollama
from PIL import Image, ImageEnhance
from diffusers import StableDiffusionPipeline

llm = Ollama(model="llama3.1")

class PromptRefinementTool:
    def refine_prompt(self, prompt):
        refined_prompt = llm(f"Refine the following image prompt to make it more detailed but simple and it should not be more than 25 words: {prompt}")
        return refined_prompt

class ImageGenerationTool:
    def __init__(self):
        self.model = None

    def load_model(self):
        if self.model is None:
            # torch.bfloat16
            self.model = StableDiffusionPipeline.from_pretrained(
                "sd-legacy/stable-diffusion-v1-5",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            self.model.to("gpu" if torch.cuda.is_available() else "cpu")  # Use CPU instead of CUDA

    def unload_model(self):
        del self.model
        self.model = None
        torch.cuda.empty_cache()
        gc.collect()

    def generate_image(self, prompt):
        try:
            self.load_model()
            image = self.model(prompt, num_inference_steps=20).images[0]  # Reduced steps
            image.save("generated_image.png")
            return "Image generated and saved as 'generated_image.png'"
        except Exception as e:
            return f"Failed to generate image: {str(e)}"
        finally:
            self.unload_model()

class ImageEnhancementTool:
    # Modify to use structured input (single dictionary) as the agent requires
    def enhance_image(self, inputs: dict):
        # Expecting a dictionary with 'image_path' and 'enhancement_type'
        image_path = inputs.get("image_path")
        enhancement_type = inputs.get("enhancement_type")

        if not image_path or not enhancement_type:
            return "Missing required inputs: image_path and enhancement_type"

        image = Image.open(image_path)

        if enhancement_type == "contrast":
            enhancer = ImageEnhance.Contrast(image)
            enhanced_image = enhancer.enhance(1.5)
        elif enhancement_type == "sharpness":
            enhancer = ImageEnhance.Sharpness(image)
            enhanced_image = enhancer.enhance(1.5)
        elif enhancement_type == "color":
            enhancer = ImageEnhance.Color(image)
            enhanced_image = enhancer.enhance(1.2)
        else:
            return "Invalid enhancement type"
        
        enhanced_image.save("enhanced_image.png")
        return "Image enhanced and saved as 'enhanced_image.png'"