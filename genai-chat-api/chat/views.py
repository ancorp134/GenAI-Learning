from rest_framework.views import APIView
from rest_framework.response import Response
import ollama

conversation_history = [
    {
        "role": "system",
        "content": """
You are a programming and software development assistant.

Rules:
1. ONLY answer programming and software questions.
2. If unrelated, say:
"I can only answer programming and software development related questions."
3. Keep answers concise and accurate.
""",
    }
]


class ChatAPIView(APIView):

    def post(self, request):

        question = request.data.get("question")

        if not question:
            return Response({"error": "Question is required"})

        conversation_history.append({"role": "user", "content": question})

        response = ollama.chat(
            model="deepseek-coder:1.3b", messages=conversation_history
        )

        assistant_answer = response["message"]["content"]

        conversation_history.append({"role": "assistant", "content": assistant_answer})

        print("Conversation history:", conversation_history)

        return Response(
            {
                "answer": assistant_answer,
                "conversation_length": len(conversation_history),
            }
        )
