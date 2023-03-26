from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
import openai
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model import Response

import config

openai.api_key = config.openai_api_key

def get_gpt_response(prompt):
    try:
        model_engine = "gpt-3.5-turbo"
        max_tokens = 200

        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )

        # Extract and return the generated text from the response
        generated_text = response.choices[0].message.content
        return generated_text.strip()

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return handler_input.request_envelope.request.object_type == "LaunchRequest"

    def handle(self, handler_input: HandlerInput) -> Response:
        speech_text = "Welcome to Cogno ai! Please ask a question by saying: Alexa, ask Chat GPT how Isaac Newton died"
        return handler_input.response_builder.speak(speech_text).response


class CognoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("CognoIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        slots = handler_input.request_envelope.request.intent.slots
        question = slots["question"].value
        print("Got to question")
        response_text = get_gpt_response(question)
        speech_text = response_text if response_text else "I'm sorry, I couldn't find an answer to your question."
        return handler_input.response_builder.speak(speech_text).response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speech_text = "You can ask me anything! Just say: Alexa, ask Chat GPT how Isaac Newton died"
        return handler_input.response_builder.speak(speech_text).response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input: HandlerInput) -> Response:
        speech_text = "Goodbye!"
        return handler_input.response_builder.speak(speech_text).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speech_text = "I'm not sure how to help with that. Please try asking a different question."
        return handler_input.response_builder.speak(speech_text).response


class CustomExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input: HandlerInput, exception: Exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception: Exception) -> Response:
        print(f"Raised exception: {exception}")
        speech = "Sorry, I encountered an error. Please try again later."
        return handler_input.response_builder.speak(speech).response


sb = SkillBuilder()

# Add handlers to the SkillBuilder
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CognoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_exception_handler(CustomExceptionHandler())

lambda_handler = sb.lambda_handler()
