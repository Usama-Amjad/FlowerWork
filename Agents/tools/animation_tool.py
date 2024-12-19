import torch
from diffusers import AnimateDiffPipeline, DDIMScheduler, MotionAdapter
from diffusers.utils import export_to_gif
import gc

class AnimationTool:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if self.device == "cuda" else torch.float32
        
        # Set device-specific parameters
        self.params = {
            "cuda": {
                "num_frames": 16,
                "num_inference_steps": 25,
                "height": 1024,
                "width": 1024,
                "slice_size": "auto"
            },
            "cpu": {
                "num_frames": 8,
                "num_inference_steps": 20,
                "height": 256,
                "width": 256,
                "slice_size": 1
            }
        }[self.device]

    def animation_generator(self, text):
        try:
            # Load adapter
            adapter = MotionAdapter.from_pretrained(
                "guoyww/animatediff-motion-adapter-v1-5-2",
                torch_dtype=self.torch_dtype,
                device_map=self.device if self.device == "cuda" else None,
                low_cpu_mem_usage=True if self.device == "cpu" else False
            )
            if self.device == "cpu":
                adapter.to(self.device)

            # Load pipeline
            pipe = AnimateDiffPipeline.from_pretrained(
                "SG161222/Realistic_Vision_V6.0_B1_noVAE",
                motion_adapter=adapter,
                torch_dtype=self.torch_dtype,
                device_map=self.device if self.device == "cuda" else None,
                low_cpu_mem_usage=True if self.device == "cpu" else False
            )
            if self.device == "cpu":
                pipe.to(self.device)

            # Set up scheduler
            scheduler = DDIMScheduler.from_pretrained(
                "SG161222/Realistic_Vision_V6.0_B1_noVAE",
                subfolder="scheduler",
                clip_sample=False,
                timestep_spacing="linspace",
                beta_schedule="linear",
                steps_offset=1,
            )
            pipe.scheduler = scheduler

            # Enable optimizations
            pipe.enable_vae_slicing()
            pipe.enable_attention_slicing(slice_size=self.params["slice_size"])

            if self.device == "cpu":
                gc.collect()  # Only necessary for CPU
            elif self.device == "cuda":
                torch.cuda.empty_cache()  # Clear GPU memory

            # Generate animation
            output = pipe(
                prompt=text,
                negative_prompt="bad quality, worse quality",
                num_frames=self.params["num_frames"],
                guidance_scale=7.5,
                num_inference_steps=self.params["num_inference_steps"],
                height=self.params["height"],
                width=self.params["width"],
                generator=torch.Generator(self.device).manual_seed(42),
            )

            frames = output.frames[0]
            export_to_gif(frames, "animation.gif")
            print("Animation generated successfully!")
            return "animation.gif"  # Return the filename for further use if needed
            
        except Exception as e:
            print(f"Error during animation generation: {e}")
            raise