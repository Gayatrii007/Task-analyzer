import datetime

def _get_today():
    return datetime.date.today()

def calculate_urgency_score(due_date, today=None):
    if due_date is None:
        return 0

    if today is None:
        today = _get_today()

    days_left = (due_date - today).days
    urgency = max(0, 20 - days_left)

    if days_left < 0:
        urgency += 10

    return urgency

def calculate_importance_score(importance):
    if importance is None:
        importance = 5
    return importance * 2

def calculate_effort_score(estimated_hours):
    if estimated_hours is None:
        # treat as medium effort
        estimated_hours = 4

    return 10 / (estimated_hours + 1)


def calculate_dependency_score(dependencies):
    if dependencies is None:
        return 0
    return len(dependencies) * 3


def calculate_task_score(task, strategy="smart_balance", today=None):
    title = task.get("title")
    due_date = task.get("due_date")
    estimated_hours = task.get("estimated_hours")
    importance = task.get("importance")
    dependencies = task.get("dependencies", [])

    # individual components
    urgency = calculate_urgency_score(due_date, today=today)
    importance_score = calculate_importance_score(importance)
    effort_score = calculate_effort_score(estimated_hours)
    dependency_score = calculate_dependency_score(dependencies)

    # different strategies -> weights change
    if strategy == "fastest_wins":
        # low effort heavily rewarded
        total = (effort_score * 3) + importance_score + urgency + dependency_score

    elif strategy == "high_impact":
        # importance sabse zyada
        total = (importance_score * 2) + urgency + dependency_score + effort_score

    elif strategy == "deadline_driven":
        # due date almost everything
        total = (urgency * 3) + importance_score + effort_score + dependency_score

    else:
        # "smart_balance" default
        total = urgency + importance_score + effort_score + dependency_score

    explanation_parts = []

    if importance and importance >= 8:
        explanation_parts.append("High importance task")
    elif importance and importance <= 3:
        explanation_parts.append("Low importance task")

    if due_date:
        if today is None:
            today = _get_today()
        days_left = (due_date - today).days
        if days_left < 0:
            explanation_parts.append("Task is overdue")
        elif days_left == 0:
            explanation_parts.append("Due today")
        elif days_left <= 2:
            explanation_parts.append("Deadline is very near")
        else:
            explanation_parts.append(f"Due in {days_left} days")

    if estimated_hours is not None:
        if estimated_hours <= 2:
            explanation_parts.append("Quick to complete")
        elif estimated_hours >= 8:
            explanation_parts.append("Large effort task")

    if dependencies:
        explanation_parts.append(
            f"Blocks {len(dependencies)} other task(s)"
        )

    if not explanation_parts:
        explanation_parts.append("Balanced priority based on default factors")

    explanation = "; ".join(explanation_parts)

    return {
        **task,
        "score": round(total, 2),
        "explanation": explanation,
    }


def analyze_tasks(tasks, strategy="smart_balance", today=None):
    scored = [
        calculate_task_score(task, strategy=strategy, today=today)
        for task in tasks
    ]

    # high score -> higher priority
    scored.sort(key=lambda t: t["score"], reverse=True)
    return scored
