import cohere

from .api_client import APIClient


class CohereClient(APIClient):

    def __init__(self):
        self.company = "COHERE"
        self.temperature = 0.8
        self.chat_messages = []
        
    def submit_api_key(self):
        self.co = cohere.Client(self.get_api_key())

    def submit_prompt(self, prompt):
        # generate a response with the current chat history
        response = self.co.chat(
            prompt,
            temperature=self.temperature,
            chat_history=self.chat_messages
        )
        answer = response.text

        # add message and answer to the chat history
        user_message = {"user_name": "User", "text": prompt}
        bot_message = {"user_name": "Chatbot", "text": answer}

        self.chat_messages.append(user_message)
        self.chat_messages.append(bot_message)
        return answer

    def on_chat_reset(self):
        self.chat_messages = []

    def validate_api_key(self, api_key):
        test_co = cohere.Client(api_key)
        try:
            test_co.generate(prompt='test')
            return True
        except cohere.CohereError as e:
            return False
