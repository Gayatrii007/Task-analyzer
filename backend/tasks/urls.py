from django.urls import path
from .views import AnalyzeTasksAPI, SuggestTasksAPI

urlpatterns = [
    path("analyze/", AnalyzeTasksAPI.as_view(), name="analyze_tasks"),
    path("suggest/", SuggestTasksAPI.as_view(), name="suggest_tasks"),
]
