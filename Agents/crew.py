from crewai import Crew
from agent import TextGenerationAgents, ResearchGenerationAgents, ImageGenerationAgents, AudioGenerationAgents, MusicGenerationAgents, DimensionnGenerationAgents, SoundGenerationAgents, AnimationGenerationAgents
from task import TextGenerationTasks, ResearchGenerationTasks, ImageGenerationTasks, AudioGenerationTasks, MusicGenerationTasks, DimensionGenerationTasks, SoundGenerationTasks, AnimationGenerationTasks
from database import CrewDatabase
from tools.knowledge_base import KnowledgeBaseTool
import logging

# Disable LiteLLM debug logs
logging.getLogger("litellm").setLevel(logging.WARNING)


class BaseCrew:
    def __init__(self):
        self.db = CrewDatabase()

    def store_crew_info(self, crew_name, user_prompt, agents, tasks):
        return self.db.store_crew(crew_name, user_prompt, agents, tasks)

    def update_crew_result(self, crew_id, result):
        self.db.update_crew_result(crew_id, result)

class TextGenerationCrew(BaseCrew):
    def __init__(self, text):
        super().__init__()
        self.text = text
    
    def run(self):
        base = KnowledgeBaseTool().add_to_knowledge_base(file_paths="./files/computer.pdf")
        print('\n\n\n\n'+base+'\n\n\n\n')
        writer = TextGenerationAgents().text_generator(base)
        writing_task = TextGenerationTasks().text_task(writer, self.text)
        
        crew = Crew(
            agents=[writer],
            tasks=[writing_task],
            verbose=True,
        )
        
        # crew_id = self.store_crew_info("Text Generation Crew", self.text, [writer], [writing_task])
        
        results = crew.kickoff()
        # self.update_crew_result(crew_id, results)
        return results

class ResearchGenerationCrew(BaseCrew):
    def __init__(self, topic):
        super().__init__()
        self.topic = topic

    def run(self):
        writer = ResearchGenerationAgents().writer()
        researcher = ResearchGenerationAgents().researcher()
        
        research_task = ResearchGenerationTasks().research_task(researcher, self.topic)
        writing_task = ResearchGenerationTasks().writing_task(writer, research_task)
    
        crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            verbose=True,
        )

        crew_id = self.store_crew_info("Research Generation Crew", self.topic, [researcher, writer], [research_task, writing_task])
        
        result = crew.kickoff()
        self.update_crew_result(crew_id, result)
        return result

class ImageGenerationCrew(BaseCrew):
    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt
    
    def run(self):
        prompt_engineer = ImageGenerationAgents().prompt_engineer()
        image_generator = ImageGenerationAgents().image_generator()
        image_enhancer = ImageGenerationAgents().image_enhancer()

        refine_prompt_task = ImageGenerationTasks().refine_prompt_task(prompt_engineer, self.prompt)
        generate_image_task = ImageGenerationTasks().generate_image_task(image_generator, refine_prompt_task)
        enhance_image_task = ImageGenerationTasks().enhance_image_task(image_enhancer, generate_image_task)

        image_generation_crew = Crew(
            agents=[prompt_engineer, image_generator],
            tasks=[refine_prompt_task, generate_image_task],
            verbose=True,
        )
        
        crew_id = self.store_crew_info("Image Generation Crew", self.prompt, 
                                       [prompt_engineer, image_generator],
                                       [refine_prompt_task, generate_image_task])
        
        result = image_generation_crew.kickoff()
        self.update_crew_result(crew_id, result)
        return result

class AudioGenerationCrew(BaseCrew):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        audio_agent = AudioGenerationAgents().audio_generator()
        audio_task = AudioGenerationTasks().audio_task(audio_agent, self.text)
    
        crew = Crew(
            agents=[audio_agent],
            tasks=[audio_task],
            verbose=True,
        )
        
        crew_id = self.store_crew_info("Audio Generation Crew", self.text, [audio_agent], [audio_task])
        
        result = crew.kickoff()
        self.update_crew_result(crew_id, result)
        return result

class MusicGenerationCrew(BaseCrew):
    def __init__(self, text, duration):
        super().__init__()
        self.text = text
        self.duration = duration

    def run(self):
        music_agent = MusicGenerationAgents().music_generator()
        music_task = MusicGenerationTasks().music_task(music_agent, self.text, self.duration)
    
        crew = Crew(
            agents=[music_agent],
            tasks=[music_task],
            verbose=True,
        )
        
        crew_id = self.store_crew_info("Music Generation Crew", f"{self.text} (Duration: {self.duration}s)", [music_agent], [music_task])
        
        result = crew.kickoff()
        self.update_crew_result(crew_id, result)
        return result

class DimensionGenerationCrew(BaseCrew):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        agent = DimensionnGenerationAgents().dimension_generator3D()
        task = DimensionGenerationTasks().dimension_task(text=self.text,agent=agent)
    
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True,
        )
        
        crew_id = self.store_crew_info("3D Dimension Generation Crew", self.text, [agent], [task])
        
        result = crew.kickoff()
        self.update_crew_result(crew_id, result)
        return result

class SoundGenerationCrew(BaseCrew):
    def __init__(self,topic,duration):
        super().__init__()
        self.topic = topic
        self.duration = duration

    def run(self):
        # refiner = SoundGenerationAgents().prompt_refiner()
        sound = SoundGenerationAgents().sound_generator()
        
        # refiner_task = SoundGenerationTasks().sound_prompt_refiner(refiner,self.topic)
        sound_task = SoundGenerationTasks().sound_generation(sound,self.topic,self.duration)
    
        crew = Crew(
            agents=[sound],
            tasks=[sound_task],
            verbose=True,
        )

        crew_id = self.store_crew_info("Sound Generation Crew", f"{self.topic} (Duration: {self.duration}s)", [sound], [sound_task])

        result = crew.kickoff()
        self.update_crew_result(crew_id, result)
        return result

class AnimationGenerationCrew(BaseCrew):
    def __init__(self,text):
        super().__init__()
        self.text = text
    
    def run(self):
        refiner = AnimationGenerationAgents().refiner()
        animation = AnimationGenerationAgents().animation_generator()
        
        refiner_task = AnimationGenerationTasks().animation_prompt_refiner(refiner,self.text)
        animation_task = AnimationGenerationTasks().animation_generation(animation)
    
        crew = Crew(
            agents=[refiner, animation],
            tasks=[refiner_task, animation_task],
            verbose=True,
        )

        crew_id = self.store_crew_info("Animation Generation Crew", self.text, [refiner, animation], [refiner_task, animation_task])

        result = crew.kickoff()
        self.update_crew_result(crew_id, result)
        return result

# Main execution
if __name__ == '__main__':
    prompt = input("Enter the prompt: ")
    crew = TextGenerationCrew(prompt)
    results = crew.run()