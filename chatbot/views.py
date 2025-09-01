# chat/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import groq

GROQ_API_KEY = "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"

# Store first-time greeting state per session (simple approach)
# For production, use session, DB, or cache
session_greeting_done = {}

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            session_id = data.get("session_id", "default")  # identify user session

            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            client = groq.Client(api_key=GROQ_API_KEY)

            # Only include greeting for the first response per session
            if not session_greeting_done.get(session_id, False):
                system_message = "Hi there! Welcome to the Hostel Finder Assistant."
                session_greeting_done[session_id] = True
            else:
                system_message = ""

            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": user_message})

            # Call Groq chat API
            response = client.chat.completions.create(
                model="llama3-70b-8192",  # your model
                messages=messages
            )

            bot_reply = response.choices[0].message.content.strip()
            return JsonResponse({"response": bot_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"response": "Send a POST request with a message"})
