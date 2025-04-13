def prioritize_tasks(todos):
    # Assign scores based on keywords in task and priority field
    def score(task_dict):
        text = task_dict['task'].lower()
        score = 0
        if 'urgent' in text or task_dict['priority'] == 'High':
            score += 3
        if 'email' in text or 'call' in text:
            score += 2
        if 'review' in text or task_dict['priority'] == 'Medium':
            score += 1
        return score

    return sorted(todos, key=score, reverse=True)

def suggest_task(mood):
    mood = mood.lower()
    suggestions = {
        "tired": "Organize your desktop or rename your files.",
        "motivated": "Finish a high-priority task you've been avoiding.",
        "stressed": "Take 5 minutes to write down everything on your mind.",
        "bored": "Start a small creative task like brainstorming ideas.",
    }
    return suggestions.get(mood, "Take a break or do something you enjoy.")
