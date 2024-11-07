from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer
from .models import students_data, next_id, data_lock
import requests
from django.http import JsonResponse, HttpResponse
from django.conf import settings


class StudentList(APIView):
    def get(self, request):
        return Response(list(students_data.values()))

    def post(self, request):
        with data_lock:
            global next_id
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                student = serializer.validated_data
                student['id'] = next_id
                students_data[next_id] = student
                next_id += 1
                return Response(student, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetail(APIView):
    def get(self, request, id):
        student = students_data.get(id)
        if not student:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(student)

    def put(self, request, id):
        with data_lock:
            student = students_data.get(id)
            if not student:
                return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                student.update(serializer.validated_data)
                students_data[id] = student
                return Response(student)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        with data_lock:
            if id in students_data:
                del students_data[id]
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)




# In-memory dictionary representing student data
students_data = {
    # Example: 1: {"name": "John Doe", "age": 20, "email": "john@example.com"}
}
import ollama
from django.http import JsonResponse

def get_student_summary(request, id):
    # Fetch the student data from the in-memory dictionary
    student = students_data.get(id)
    if not student:
        return JsonResponse({"error": "Student not found"}, status=404)

    # Extract student details
    name = student.get('name')
    age = student.get('age')
    email = student.get('email')

    # Generate the prompt for LLaMA 3.2
    prompt = f"Generate a brief summary for student in a paragraph  using the given details . Enhance it more . name is  {name} with roll number {id}, age {age}, and email {email}."

    try:
        # Use Ollama to generate a response from the LLaMA model
        result = ollama.generate(model="llama3.2", prompt=prompt)

        # Print the entire result for debugging (optional)
        print("Ollama Response:", result)

        # Extract the summary from the 'response' key
        summary = result.get("response", "").strip()  # Assuming the summary is in the 'response' key

        # If no summary, return a custom error message
        if not summary:
            return JsonResponse({"error": "No summary generated"}, status=500)

        return JsonResponse({"summary": summary})

    except Exception as e:
        return JsonResponse({
            "error": "Failed to fetch summary from Ollama",
            "details": str(e)
        }, status=500)
        
        
        
from django.http import JsonResponse
import asyncio

async def my_async_view(request):
    # Perform non-blocking operations
    return JsonResponse({"message": "Data from async view"})

