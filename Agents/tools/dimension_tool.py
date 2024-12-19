import torch
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_gif

class DimensionTool:
    def dimension_generator3d(self,text):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        repo = "openai/shap-e"
        # torch.bfloat16
        pipe = DiffusionPipeline.from_pretrained(repo, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
        pipe = pipe.to(device)

        images = pipe(
            text,
            guidance_scale=15,
            num_inference_steps=64,
            frame_size=256,
        ).images

        export_to_gif(images[0], "{text}.gif")