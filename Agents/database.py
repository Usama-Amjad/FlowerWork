from pymongo import MongoClient
from bson import ObjectId
import datetime
from helpers import crew_output_to_dict
import logging
# Disable MongoDB connection logging
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

class CrewDatabase:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client['crew_ai_db']
        self.crews = self.db['crews']
        self.agents = self.db['agents']
        self.tasks = self.db['tasks']

    def store_crew(self, crew_name, user_prompt, agents, tasks):
        crew_data = {
            "crew_name": crew_name,
            "user_prompt": user_prompt,
            "created_at": datetime.datetime.now(datetime.timezone.utc),
            "agents": [],
            "tasks": []
        }

        for agent in agents:
            agent_data = {
                "role": agent.role,
                "goal": agent.goal,
                "backstory": agent.backstory,
                "verbose": agent.verbose,
                "allow_delegation": agent.allow_delegation,
                "tools": [str(tool) for tool in agent.tools] if hasattr(agent, 'tools') else []
            }
            agent_id = self.agents.insert_one(agent_data).inserted_id
            crew_data["agents"].append(str(agent_id))

        for task in tasks:
            task_data = {
                "description": task.description,
                "expected_output": task.expected_output,
                "agent": str(crew_data["agents"][agents.index(task.agent)])
            }
            task_id = self.tasks.insert_one(task_data).inserted_id
            crew_data["tasks"].append(str(task_id))

        crew_id = self.crews.insert_one(crew_data).inserted_id
        return str(crew_id)

    def get_crew(self, crew_id):
        crew = self.crews.find_one({"_id": ObjectId(crew_id)})
        if crew:
            crew['_id'] = str(crew['_id'])
            crew['agents'] = [self.get_agent(agent_id) for agent_id in crew['agents']]
            crew['tasks'] = [self.get_task(task_id) for task_id in crew['tasks']]
        return crew

    def get_agent(self, agent_id):
        agent = self.agents.find_one({"_id": ObjectId(agent_id)})
        if agent:
            agent['_id'] = str(agent['_id'])
        return agent

    def get_task(self, task_id):
        task = self.tasks.find_one({"_id": ObjectId(task_id)})
        if task:
            task['_id'] = str(task['_id'])
        return task

    def update_crew_result(self, crew_id, result):
        result_dict = crew_output_to_dict(result)
        self.crews.update_one({"_id": ObjectId(crew_id)}, {"$set": {"result": result_dict}})

    def list_crews(self, limit=10):
        crews = list(self.crews.find().sort("created_at", -1).limit(limit))
        for crew in crews:
            crew['_id'] = str(crew['_id'])
        return crews
    
db = CrewDatabase()
print(db.client.list_database_names())