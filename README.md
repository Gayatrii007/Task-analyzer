1. Smart Task Analyzer
    A mini task management system that intelligently scores and prioritizes tasks based on urgency, importance, effort, and dependencies.

2. Overview
    This project analyzes tasks and helps users decide which task they should work on first based on multiple priority factors.
    Users can switch between different strategies to change how task scoring works.

3. Tech Stack
    3.1 Area and Technology
    | Area        | Technology                                      |
    |-------------|-------------------------------------------------|
    | Backend     | Django, Django REST Framework                   |
    | Frontend    | HTML, CSS, JavaScript (Fetch API)               |
    | Algorithm   | Custom scoring and prioritization logic         |
    | Storage     | In-memory (no database persistence required)    |


4. Features
    4.1 Add tasks via form
    4.2 Paste JSON for bulk input
    4.3 Strategy-based dynamic scoring:
        -> Smart Balance
        -> Fastest Wins
        -> High Impact
        -> Deadline Driven
    4.4 Top 3 recommended tasks
    4.5 Score explanation and color-coded priority levels

5. Scoring Algorithm Explanation
    Each task is scored based on:
 
    | Factor       | Description                                                     | Weight      |
    |--------------|-----------------------------------------------------------------|-------------|
    | Urgency      | Based on due date (overdue tasks receive a penalty boost)       | Medium–High |
    | Importance   | User rating from 1–10, multiplied ×2 to prioritize impact       | High        |
    | Effort       | Smaller tasks score higher using: `10 / (estimated_hours + 1)`  | Medium      |
    | Dependencies | Tasks that block multiple other tasks score above normal        | Medium      |

6. Formula (Simplified):
    total_score = urgency + (importance * 2) + (10 / (hours + 1)) + (dependencies * 3)

7. Strategy Impact:

    | Strategy         | What Changes / Priority Logic Focus                            |
    |------------------|----------------------------------------------------------------|
    | Fastest Wins     | Effort is weighted more — quick tasks are prioritized          |
    | High Impact      | Importance dominates — high-value tasks come first             |
    | Deadline Driven  | Urgency dominates — tasks with closer deadlines rank higher    |
    | Smart Balance    | Uses default balanced weight across all factors (recommended)  |