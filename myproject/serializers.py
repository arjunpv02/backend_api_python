import re
from rest_framework import serializers

# Simulate in-memory storage of existing emails (global variable to track emails)
existing_emails = ['existing@example.com', 'test@example.com']  # Example existing emails

class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(min_value=3)
    email = serializers.EmailField()

    def validate_name(self, value):
        # Validate that name contains only letters and spaces
        if not re.match(r'^[A-Za-z\s]+$', value):
            raise serializers.ValidationError("Name should only contain letters and spaces.")
        return value

    def validate_email(self, value):
        # Check if the email already exists in our in-memory storage
        if value in existing_emails:
            raise serializers.ValidationError("This email is already in use.")
        
        # Add the newly validated email to the in-memory list (store it)
        existing_emails.append(value)  # Store the new email
        
        return value
