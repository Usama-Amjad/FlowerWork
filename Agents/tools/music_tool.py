from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

class MusicGenerationTool:
    def generate_music(self,text:str,duration:int) -> str:
        """Generates music from the given text using MusicGen and saves it as a wav file."""   
        try:
            # torch.bfloat16
            processor = AutoProcessor.from_pretrained("facebook/musicgen-large")
            model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-large")

            inputs = processor(
                text=[text],
                padding=True,
                return_tensors="pt"
            )

            # Duration-> max_new_tokens/50
            # maxtoken=1503 -> 30s
            audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=duration*50)
            sampling_rate = model.config.audio_encoder.sampling_rate
            scipy.io.wavfile.write("musicgen_out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())
            return "Music generated and saved as 'musicgen_out.wav'"
        except Exception as e:
            return f"Failed to generate music: {str(e)}"