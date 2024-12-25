from django.test import TestCase
import os
import requests

class RunGemini(TestCase):
    def test_api_real_gemini(self):
        pass

    def test_cli_real_gemini(self):
        api_key = os.getenv("GEMINI_API_KEY")
        data = {
            "prompt": "say hi!",
            "temperature": 0.7,  
            "maxTokens":  100  
        }

        gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        headers = {"Content-Type": "application/json"}
        gemini_payload = {"contents": [{
            "parts": [{"text": data.get("prompt")}]
        }]}

        # Send the request to the Gemini API
        response = requests.post(f"{gemini_url}?key={api_key}", headers=headers, json=gemini_payload)

        gemini_response = response.json()
        # print(gemini_response)
        response_content = gemini_response['candidates'][0]['content']['parts'][0]['text']
        finish_reason = gemini_response['candidates'][0]['finishReason']
        avg_logprobs = gemini_response['candidates'][0].get('avgLogprobs')
        prompt_token_count = gemini_response['usageMetadata']['promptTokenCount']
        candidates_token_count = gemini_response['usageMetadata']['candidatesTokenCount']
        total_token_count = gemini_response['usageMetadata']['totalTokenCount']
        model_version = gemini_response['modelVersion']

        # Assertions
        self.assertIsNotNone(response_content) 
        self.assertIsNotNone(finish_reason) 
        # Check if avgLogprobs exists (it might be optional)
        if avg_logprobs:
            self.assertIsInstance(avg_logprobs, float) 
        self.assertIsInstance(prompt_token_count, int)
        self.assertIsInstance(candidates_token_count, int)
        self.assertIsInstance(total_token_count, int)
        self.assertIsNotNone(model_version) 