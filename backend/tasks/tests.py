from django.test import TestCase
from datetime import date, timedelta
from .scoring import analyze_tasks, calculate_task_score


class TaskScoringTests(TestCase):

    def setUp(self):
        self.today = date.today()

        self.task_high_importance = {
            "title": "Critical Fix",
            "due_date": self.today + timedelta(days=2),
            "estimated_hours": 3,
            "importance": 9,
            "dependencies": []
        }

        self.task_low_importance = {
            "title": "Minor Update",
            "due_date": self.today + timedelta(days=2),
            "estimated_hours": 3,
            "importance": 2,
            "dependencies": []
        }

        self.overdue_task = {
            "title": "Missed Deadline Task",
            "due_date": self.today - timedelta(days=1),
            "estimated_hours": 4,
            "importance": 5,
            "dependencies": []
        }

    def test_high_importance_scores_higher(self):
        score_high = calculate_task_score(self.task_high_importance, today=self.today)["score"]
        score_low = calculate_task_score(self.task_low_importance, today=self.today)["score"]
        self.assertTrue(score_high > score_low)

    def test_overdue_task_gets_bonus(self):
        result = calculate_task_score(self.overdue_task, today=self.today)
        explanation = result["explanation"]

        self.assertIn("overdue", explanation.lower())
        self.assertGreater(result["score"], 20)  # sanity check boost happened

    def test_strategy_changes_result(self):
        score_default = calculate_task_score(self.task_high_importance, strategy="smart_balance", today=self.today)["score"]
        score_fast = calculate_task_score(self.task_high_importance, strategy="fastest_wins", today=self.today)["score"]

        self.assertNotEqual(score_default, score_fast)
