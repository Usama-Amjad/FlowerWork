import scipy
import torch
from diffusers import AudioLDM2Pipeline

class SoundGenerationTool:
    def sound_generator(self,text:str,duration:float|int):
        # load the pipeline
        repo_id = "cvssp/audioldm2-large"
        # torch.
        #desired_dtype = torch.bfloat16
        # torch.set_default_dtype(desired_dtype)
        pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
        pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

        # define the prompts
        prompt = text
        negative_prompt = "Low quality."

        # set the seed
        generator = torch.Generator("cuda" if torch.cuda.is_available() else "cpu").manual_seed(0)

        # run the generation
        audio = pipe(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=200,
            audio_length_in_s=duration,
            num_waveforms_per_prompt=3,
            generator=generator,
        ).audios

        # save the best audio sample (index 0) as a .wav file
        scipy.io.wavfile.write("techno.wav", rate=16000, data=audio[0])
