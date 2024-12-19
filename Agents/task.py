from crewai import Task, Agent

class TextGenerationTasks:
    def text_task(self, agent: Agent, text: str):
        return Task(
            description=f"""Synthesize knowledge to address: '{text}'
            
            Requirements:
            1. Leverage domain expertise to provide accurate information
            2. Craft a response that is both precise and insightful
            3. Ensure content is tailored to the specific request
            4. Combine depth of knowledge with clarity of communication
            5. If knowledge base tool is provided ,use it to get answers""",
            agent=agent,
            expected_output="""A comprehensive response that:
            1. Demonstrates expertise across relevant domains
            2. Provides precise and insightful content
            3. Is tailored specifically to the user's query
            4. Balances depth with clarity and accessibility"""
        )

class ResearchGenerationTasks:
    def research_task(self, agent: Agent, topic: str):
        return Task(
            description=f"""Conduct comprehensive research on: '{topic}'
            
            Requirements:
            1. Utilize web search and scraping tools effectively
            2. Identify and verify information from credible sources
            3. Synthesize findings into a cohesive summary
            4. Highlight key insights and patterns discovered""",
            agent=agent,
            expected_output=f"""A detailed research report that:
            1. Presents verified information from credible sources
            2. Identifies and synthesizes key insights
            3. Provides a comprehensive overview of {topic}
            4. Includes citations and links to primary sources"""
        )
    
    def writing_task(self, agent: Agent, context_task: Task):
        return Task(
            description="""Transform the provided research into engaging content
            
            Requirements:
            1. Create a narrative that makes complex information accessible
            2. Maintain accuracy while ensuring content is compelling
            3. Structure the article for optimal readability
            4. Incorporate all key points from the research""",
            agent=agent,
            expected_output="""An informative article that:
            1. Presents complex information in an engaging, accessible manner
            2. Maintains accuracy and depth of the original research
            3. Uses a clear, logical structure
            4. Effectively communicates all key insights""",
            context=[context_task]
        )

class ImageGenerationTasks:
    def refine_prompt_task(self, agent: Agent, prompt: str):
        return Task(
            description=f"""Architect a 30 words precise visual prompt from: '{prompt}'
            
            Requirements:
            1. Translate abstract concepts into clear visual descriptions
            2. Optimize the prompt for optimal image generation results
            3. Balance creativity with technical feasibility
            4. Ensure all key visual elements are specified""",
            agent=agent,
            expected_output="""A refined image prompt that:
            1. Clearly describes all necessary visual elements
            2. Is optimized for high-quality image generation
            3. Balances creativity with technical constraints
            4. Captures the essence of the original request"""
        )
    
    def generate_image_task(self, agent: Agent, context_task: Task):
        return Task(
            description="""Create a high-quality image from the refined prompt
            
            Requirements:
            1. Generate an image that matches the prompt precisely
            2. Ensure technical excellence in the output
            3. Apply artistic vision while maintaining accuracy
            4. Save the result as 'generated_image.png'""",
            agent=agent,
            context=[context_task],
            expected_output="""A high-quality image that:
            1. Accurately reflects the refined prompt
            2. Demonstrates technical and artistic excellence
            3. Is saved as 'generated_image.png'
            4. Includes confirmation of successful generation"""
        )
    
    def enhance_image_task(self, agent: Agent, context_task: Task):
        return Task(
            description="""Optimize the generated image
            
            Requirements:
            1. Analyze the image for potential improvements
            2. Apply targeted enhancements to elevate quality
            3. Ensure enhancements serve the original vision
            4. Save enhanced version as 'enhanced_image.png'""",
            agent=agent,
            context=[context_task],
            expected_output="""An enhanced image that:
            1. Demonstrates improved quality over the original
            2. Maintains the integrity of the initial concept
            3. Is saved as 'enhanced_image.png'
            4. Includes details of enhancements applied"""
        )

class AudioGenerationTasks:
    def audio_task(self, agent: Agent, text: str):
        return Task(
            description=f"""Convert to natural speech: '{text}'
            
            Requirements:
            1. Apply appropriate tone, pacing, and emphasis
            2. Ensure high-quality audio output
            3. Consider context for appropriate voice synthesis
            4. Generate in a standard audio format""",
            agent=agent,
            expected_output="""A high-quality audio file that:
            1. Naturally conveys the provided text
            2. Uses appropriate tone and pacing
            3. Is saved in a standard audio format
            4. Includes confirmation of successful generation"""
        )

class MusicGenerationTasks:
    def music_task(self, agent: Agent, text: str, duration: int):
        return Task(
            description=f"""Compose music from the following text: '{text}' (Duration: {duration}s)
            
            Requirements:
            1. Translate textual concepts into musical elements
            2. Apply musical theory for emotional expression
            3. Ensure composition matches specified duration
            4. Save as high-quality audio file""",
            agent=agent,
            expected_output="""A musical composition that:
            1. Effectively expresses the textual concept
            2. Demonstrates musical theory expertise
            3. Is exactly {duration} seconds long
            4. Is saved as 'musicgen_out.wav'"""
        )

class DimensionGenerationTasks:
    def dimension_task(self, agent: Agent, text: str):
        return Task(
            description=f"""Create 3D visualization from: '{text}'
            
            Requirements:
            1. Translate concept into precise 3D space
            2. Apply attention to detail, scale, and impact
            3. Ensure visual striking and accurate representation
            4. Save as an accessible format""",
            agent=agent,
            expected_output="""A 3D visualization that:
            1. Accurately represents the provided concept
            2. Demonstrates attention to detail and scale
            3. Is visually striking and precise
            4. Is saved as an accessible .gif file"""
        )

class SoundGenerationTasks:
    def sound_prompt_refiner(self, agent: Agent, text: str):
        return Task(
            description=f"""Optimize sound prompt: '{text}'
            
            Requirements:
            1. Translate abstract concepts into actionable sound descriptions
            2. Consider technical feasibility and constraints
            3. Ensure clarity and effectiveness of prompt
            4. Apply sound design expertise to refinement""",
            agent=agent,
            expected_output="""A refined sound prompt that:
            1. Clearly describes the desired sound effect
            2. Is technically feasible to generate
            3. Captures the essence of the original concept
            4. Is optimized for high-quality sound generation"""
        )
    
    def sound_generation(self, agent: Agent,sound_prompt: str, duration: int):
        return Task(
            description=f"""Produce following sound effect:{sound_prompt} (Duration: {duration}s)
            
            Requirements:
            1. Generate authentic, high-fidelity sound
            2. Ensure technical excellence in output
            3. Match specified duration exactly
            4. Save in a standard audio format""",
            agent=agent,
            expected_output="""A high-quality sound effect that:
            1. Matches the refined prompt perfectly
            2. Is exactly {duration} seconds long
            3. Demonstrates technical excellence
            4. Is saved as 'soundgen_out.wav'"""
        )

class AnimationGenerationTasks:
    def animation_prompt_refiner(self, agent: Agent, text: str):
        return Task(
            description=f"""Refine animation concept: '{text}'
            
            Requirements:
            1. Translate ideas into actionable animation concepts
            2. Balance creativity with technical feasibility
            3. Specify key movements and visual elements
            4. Consider timing and pacing in refinement""",
            agent=agent,
            expected_output="""A refined animation prompt that:
            1. Clearly describes the desired animation
            2. Is technically feasible to generate
            3. Balances creativity with practicality
            4. Includes all necessary details for generation"""
        )

    def animation_generation(self, agent: Agent):
        return Task(
            description="""Create fluid, expressive animation
            
            Requirements:
            1. Generate animation based on refined prompt
            2. Ensure smooth, professional movement
            3. Apply both artistic and technical expertise
            4. Save in an accessible format""",
            agent=agent,
            expected_output="""A high-quality animation that:
            1. Accurately reflects the refined prompt
            2. Demonstrates fluid, professional movement
            3. Balances artistic vision with technical excellence
            4. Is saved as '.gif'"""
        )