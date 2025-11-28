from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TaskInputSerializer, TaskOutputSerializer
from .scoring import analyze_tasks


class AnalyzeTasksAPI(APIView):

    def post(self, request):
        data = request.data

        # 🔥 FIX: Convert single object → list
        if isinstance(data, dict):
            data = [data]

        strategy = request.query_params.get("strategy", "smart_balance")

        serializer = TaskInputSerializer(data=data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tasks = serializer.validated_data

        scored_tasks = analyze_tasks(tasks, strategy=strategy)

        output = TaskOutputSerializer(scored_tasks, many=True)

        return Response({
            "strategy_used": strategy,
            "count": len(scored_tasks),
            "results": output.data
        }, status=status.HTTP_200_OK)


class SuggestTasksAPI(APIView):

    def post(self, request):
        data = request.data

        # 🔥 FIX: Convert single task → list
        if isinstance(data, dict):
            data = [data]

        strategy = request.query_params.get("strategy", "smart_balance")

        serializer = TaskInputSerializer(data=data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tasks = serializer.validated_data

        scored_tasks = analyze_tasks(tasks, strategy=strategy)

        top_three = scored_tasks[:3]

        output = TaskOutputSerializer(top_three, many=True)

        return Response({
            "suggested_tasks": output.data,
            "strategy_used": strategy,
            "count": len(top_three)
        }, status=status.HTTP_200_OK)
