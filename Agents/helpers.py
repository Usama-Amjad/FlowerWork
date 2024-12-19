def crew_output_to_dict(crew_output):
    return {
        "raw": crew_output.raw,
        "tasks_output": [
            {
                "description": task.description,
                "name": task.name,
                "expected_output": task.expected_output,
                "summary": task.summary,
                "raw": task.raw,
                "agent": task.agent,
                "output_format": task.output_format.value
            } for task in crew_output.tasks_output
        ],
        "token_usage": {
            "total_tokens": crew_output.token_usage.total_tokens,
            "prompt_tokens": crew_output.token_usage.prompt_tokens,
            "completion_tokens": crew_output.token_usage.completion_tokens,
            "successful_requests": crew_output.token_usage.successful_requests
        }
    }
