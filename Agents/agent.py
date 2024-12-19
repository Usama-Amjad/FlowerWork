from crewai import Agent
from langchain.tools import Tool
from tools.search_tool import WebSearcher
from tools.image_tool import ImageGenerationTool, ImageEnhancementTool
from tools.audio_tool import TextToSpeechTool
from tools.music_tool import MusicGenerationTool
from tools.sound_tool import SoundGenerationTool
from tools.dimension_tool import DimensionTool
from tools.animation_tool import AnimationTool
from tools.knowledge_base import KnowledgeBaseTool
# from crewai_tools import ScrapeWebsiteTool
from langchain_core.tools import StructuredTool
# from langchain.llms import Ollama

ollama_llm = "ollama/llama3.1"

class TextGenerationAgents:
    def text_generator(self, base:bool=False):
        tools = [
            StructuredTool.from_function(
                name="Knowledge Base Lookup",
                func=KnowledgeBaseTool().get_knowledge_base_response,
                description="Look up information in the knowledge base if there is any information related to the query",
            )
        ] if base else []
        
        return Agent(
            role="Language Expert & Knowledge Synthesizer",
            goal="Generate accurate, contextually relevant content optimized for the user's needs",
            backstory="""With expertise spanning multiple domains and a mastery of human expression, 
            you craft precise, insightful content tailored to each request. Your responses 
            combine depth of knowledge with clarity of communication.""",
            llm=ollama_llm,
            tools=tools
        )
            
class ResearchGenerationAgents:
    def researcher(self):
        scrapper = ScrapeWebsiteTool()
        return Agent(
            role='Research Analyst',
            goal='Uncover and synthesize comprehensive, accurate information efficiently',
            backstory="""You excel at rapid information gathering and verification, 
            with a particular talent for identifying key insights and credible sources.""",
            # # tools=[
            # #     StructuredTool.from_function(
            # #         name="Web Searcher and Data Extractor",
            # #         func=WebSearcher().search_and_process,
            # #         description="Searches web for relevant information and then extract content from URLs for generating answers"
            # #     ),
            # #     StructuredTool.from_function(
            # #         name= "Knowledge Base Lookup",
            # #         description= "Look up information in the knowledge base if there is any information related to the query",
            # #         function= KnowledgeBaseTool().get_knowledge_base_response
            # #     )
            # #     ,
            #     scrapper
            # ],
            verbose=True,
            allow_delegation=False,
            llm=ollama_llm
        )

    def writer(self):
        return Agent(
            role='Content Strategist',
            goal='Transform research into compelling, informative content',
            backstory="""You craft engaging narratives that make complex information 
            accessible while maintaining accuracy and depth.""",
            verbose=True,
            allow_delegation=False,
            llm=ollama_llm
        )

class AudioGenerationAgents:
    def audio_generator(self):
        return Agent(
            role="Voice Synthesis Specialist",
            goal="Create natural, context-appropriate voice content from the given text",
            backstory="""You specialize in nuanced text-to-speech conversion, 
            understanding the subtleties of tone, pacing, and emphasis.""",
            llm=ollama_llm,
            tools=[Tool(
                name="Audio Generation",
                func=TextToSpeechTool().generate_audio,
                description="Converts text to high-quality speech audio"
            )],
            verbose=True,
            allow_delegation=False
        )
        
class MusicGenerationAgents:
    def music_generator(self):
        return Agent(
            role="Compositional AI",
            goal="Create emotionally resonant music from textual descriptions",
            backstory="""You translate textual concepts into musical elements, 
            understanding both musical theory and emotional expression.""",
            llm=ollama_llm,
            tools=[StructuredTool.from_function(
                name="Music Generation",
                func=MusicGenerationTool().generate_music,
                description="Creates musical compositions based on text input"
            )],
            verbose=True,
            allow_delegation=False
        )

class DimensionnGenerationAgents:
    def dimension_generator3D(self):
        return Agent(
            role="3D Visualization Expert",
            goal="Create precise, visually striking 3D content from descriptions",
            backstory="""You excel at translating concepts into three-dimensional space, 
            with an eye for detail, scale, and visual impact.""",
            llm=ollama_llm,
            tools=[StructuredTool.from_function(
                name="3D Generator",
                func=DimensionTool().dimension_generator3d,
                description="Creates detailed 3D visualizations"
            )]
        )

class SoundGenerationAgents:
    def prompt_refiner(self):
        return Agent(
            role="Sound Design Consultant",
            goal="Optimize sound generation prompts for clarity and effectiveness",
            backstory="""You understand the nuances of sound description and how to 
            translate abstract concepts into precise, actionable sound generation prompts.""",
            llm=ollama_llm
        )

    def sound_generator(self):
        return Agent(
            role="Sonic Architect",
            goal="Generate realistic, context-appropriate sound effects",
            backstory="""You specialize in creating authentic soundscapes, 
            understanding both the technical and perceptual aspects of sound design.""",
            llm=ollama_llm,
            tools=[StructuredTool.from_function(
                name="Sound Generation",
                func=SoundGenerationTool().sound_generator,
                description="Creates high-fidelity sound effects"
            )]
        )

class AnimationGenerationAgents:
    def refiner(self):
        return Agent(
            role="Animation Concept Artist",
            goal="Refine animation prompts for maximum visual impact",
            backstory="""You excel at translating rough ideas into vivid, 
            actionable animation concepts that balance creativity with technical feasibility.""",
            llm=ollama_llm
        )

    def animation_generator(self):
        return Agent(
            role="Motion Graphics Specialist",
            goal="Create fluid, expressive animations from refined prompts",
            backstory="""You bring static concepts to life through movement, 
            understanding both the art and technical aspects of animation.""",
            llm=ollama_llm,
            tools=[Tool(
                name="Animation Generation",
                func=AnimationTool().animation_generator,
                description="Creates dynamic animations from prompts"
            )]
        )

class ImageGenerationAgents:
    def prompt_engineer(self):
        return Agent(
            role='Visual Prompt Architect',
            goal="Craft precise, evocative image generation prompts",
            backstory="""You excel at translating abstract visual concepts 
            into clear, effective prompts that produce optimal results.""",
            verbose=True,
            llm=ollama_llm
        )
    
    def image_generator(self):
        return Agent(
            role="Visual Synthesis Artist",
            goal="Generate striking, accurate images from refined prompts",
            backstory="""You combine technical precision with artistic vision 
            to create images that perfectly match the intended concept.""",
            verbose=True,
            llm=ollama_llm,
            tools=[Tool(
                name="Image Generation",
                func=ImageGenerationTool().generate_image,
                description="Creates high-quality images from prompts"
            )]
        )
    
    def image_enhancer(self):
        return Agent(
            role="Image Optimization Specialist",
            goal="Elevate image quality through targeted enhancements",
            backstory="""You understand the nuances of digital image processing, 
            knowing exactly how to adjust parameters for optimal results.""",
            verbose=True,
            llm=ollama_llm,
            tools=[StructuredTool.from_function(
                name="Image Enhancement",
                func=ImageEnhancementTool().enhance_image,
                description="Enhances images using various techniques"
            )]
        )