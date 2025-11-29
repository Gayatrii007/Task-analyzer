import datetime


def _get_today():
    # Returns today's date. Helps with testing by allowing a custom date.
    return datetime.date.today()


def calculate_urgency_score(due_date, today=None):
    """
    Calculates urgency based on how close the due date is.
    The closer the deadline, the higher the urgency score.

    Rules:
    - Future tasks: Score increases as days_left decreases.
    - Overdue tasks: Extra penalty is added.
    - No due date: Urgency = 0
    """
    if due_date is None:
        return 0

    today = today or _get_today()
    days_left = (due_date - today).days

    # A base urgency formula (tasks become critical when < 20 days remain)
    urgency = max(0, 20 - days_left)

    # If already overdue, add penalty
    if days_left < 0:
        urgency += 10

    return urgency


def calculate_importance_score(importance):
    """
    Converts importance (1–10 scale) to weight.
    Higher importance means the task has more long-term value.
    """
    return (importance or 5) * 2


def calculate_effort_score(hours):
    """
    Rewards tasks that take less effort.
    Smaller tasks are easier to start, so they receive a higher score.
    """
    if hours is None:
        hours = 4  # default medium complexity

    return 10 / (hours + 1)


def calculate_dependency_score(dependencies):
    """
    If a task blocks other tasks, its priority should increase.
    """
    return len(dependencies or []) * 3


def calculate_consistency_score(completed_count, streak_enabled=True):
    """
    Rewards habit-forming tasks.
    Example: Daily workouts or reading.

    More completions → higher priority to keep the streak alive.

    Can be disabled if not needed.
    """
    if not streak_enabled or completed_count is None:
        return 0
    return min(10, completed_count * 1.5)


def calculate_task_score(task, strategy="smart_balance", today=None, streak_enabled=True):
    """Calculates final priority score by combining different factors."""

    # Extract data from task dictionary
    due_date = task.get("due_date")
    estimated_hours = task.get("estimated_hours")
    importance = task.get("importance")
    dependencies = task.get("dependencies", [])
    completed_count = task.get("completed_count", 0)

    # Scoring components
    urgency = calculate_urgency_score(due_date, today)
    importance_score = calculate_importance_score(importance)
    effort_score = calculate_effort_score(estimated_hours)
    dependency_score = calculate_dependency_score(dependencies)
    streak_score = calculate_consistency_score(completed_count, streak_enabled)

    # Different strategy formulas
    if strategy == "fastest_wins":
        total = (effort_score * 3) + urgency + importance_score + dependency_score + streak_score

    elif strategy == "high_impact":
        total = (importance_score * 2) + urgency + dependency_score + effort_score + streak_score

    elif strategy == "deadline_driven":
        total = (urgency * 3) + importance_score + effort_score + dependency_score + streak_score

    else:  # smart_balance default
        total = urgency + importance_score + effort_score + dependency_score + streak_score

    # Build a simple, human-readable explanation
    explanation = []

    if importance:
        explanation.append("Highly impactful task" if importance >= 8 else "Low importance task" if importance <= 3 else "Moderate importance")

    if due_date:
        today = today or _get_today()
        days_left = (due_date - today).days
        if days_left < 0: explanation.append("Task is overdue")
        elif days_left == 0: explanation.append("Due today")
        elif days_left <= 2: explanation.append("Deadline is approaching soon")
        else: explanation.append(f"Due in {days_left} days")

    if estimated_hours:
        explanation.append("Quick task" if estimated_hours <= 2 else "Long task" if estimated_hours >= 8 else "Medium effort")

    if dependencies:
        explanation.append(f"Blocking {len(dependencies)} other task(s)")

    if completed_count and streak_enabled:
        explanation.append("Streak bonus: keep going!")

    if not explanation:
        explanation.append("Balanced priority based on available factors")

    return {
        **task,
        "score": round(total, 2),
        "explanation": "; ".join(explanation)
    }


def analyze_tasks(tasks, strategy="smart_balance", today=None):
    """Scores all tasks and returns them sorted by highest priority first."""
    results = [calculate_task_score(task, strategy=strategy, today=today) for task in tasks]
    return sorted(results, key=lambda t: t["score"], reverse=True)
