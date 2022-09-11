# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

spellings = []
incorrectWords = set()
tmp = []

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to group 4's alexa skill: spelling practice. If you would like to start, please set a list of words"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class setSpellingsIntentHandler(AbstractRequestHandler):
    """Handler for setting a spelling."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("setSpellings")(handler_input)

    def handle(self, handler_input):
        # slots = handler_input.request_envelope.request.intent.slots['spellings']

        speak_output = ""
        slot = ask_utils.request_util.get_slot(handler_input, "spellings")  
        spellings.append(slot.value)
        for x in spellings:
            for y in x.split():
                tmp.append(y)
        if tmp:
            speak_output = "Your spellings have been set"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class WordsHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("WordsIntent")(handler_input)

    def handle(self, handler_input):
        # slots = handler_input.request_envelope.request.intent.slots['spellings']
        output = ""
        
        for x in spellings:
            for y in x.split():
                output += y + ", "
        speak_output = "The spellings for this test are: " + output #spellings have been set
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class goThroughSpellingHandler(AbstractRequestHandler):
    """Handler for going through set spellings."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("goThroughSpellingIntent")(handler_input) #Ensured this intent name matched the frameword intent name

    def handle(self, handler_input):
        # slots = handler_input.request_envelope.request.intent.slots['spellings']
        string = ""
        global target
        target = tmp[0]

        word = tmp.pop(0)
        #loop goes through tmp spelling list & add each chracter to the string
        for num in range(len(word) - 1):
            string += word[num] + ", " 
        speak_output = "The word: " + word + ", is spelt: " + string + word[-1] #Ensures a letter is the last charecter of string & not a comma
        speak_output += ". Did you get this word correct?"
        # resets set words
        while spellings:
            if len(tmp) != 0:
                spellings.pop(0)
            break

        return (handler_input.response_builder
             .speak(speak_output)
                .ask(speak_output)
                .response
        )

class goThroughIncorrectSpellingHandler(AbstractRequestHandler):
    """Handler for going through incorrect spellings."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("goThroughIncorrectSpellingIntent")(handler_input) #Ensured this intent name matched the frameword intent name

    def handle(self, handler_input):
        # slots = handler_input.request_envelope.request.intent.slots['spellings']
        output = ""
        
        for x in incorrectWords:
            for y in x.split():
                output += y + ", "

        speak_output = "The spellings you got incorrect are: " + output

        return (handler_input.response_builder
             .speak(speak_output)
                .ask(speak_output)
                .response
        )

class yesHandler(AbstractRequestHandler):
    #invoked when user says yes after being asked if they got a word correct
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)
    def handle(self, handler_input):
        speak_output = "Well done! When you are ready, please move onto the next word"
        if target in incorrectWords:
            incorrectWords.remove(target)
            speak_output = "Well done! word has been removed from incorrect spellings list"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response)

class noHandler(AbstractRequestHandler):
    #invoked when user says no after being asked if they got a word correct
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)
    def handle(self, handler_input):
        if target in incorrectWords:
            speak_output = "Word was not added to incorrect spellings as it already exists"
        else:
            incorrectWords.add(target)
            speak_output = "This word has been added to the incorrect spellings list"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response)

class repeatHandler(AbstractRequestHandler):
    #invoked when user says repeat 
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.RepeatIntent")(handler_input)
    def handle(self, handler_input):
        if target:
            speak_output = "The current spelling is: " + target + ". Did you get this word correct?"
        else:
            speak_output = "Sorry, I can not do that. Please say the command: help, if you are unsure what to do next."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response)

class resetHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("clearIntent")(handler_input)
    def handle(self, handler_input):
        while spellings:
            spellings.pop(0)
        
        if len(spellings) == 0:
            speak_output = "The set words have been reset."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response)

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        
        n1 = "To set words, please either say"
        setWords = ["set list","set my words","set my words to practice","or","set my spellings to, (followed by the words you would like to be set)"]
        setWordsSpacing = ", ".join(setWords)
        
        
        n2 = "To read out set words, please either say"
        readOut = ["read out my set words","what are my spellings","what are my words","what words have been set","alexa repeat the set words"]
        readOutSpacing = ", ".join(readOut) 
        
        n3 = "To go through spellings and check whether the word is correct, please either say"
        goThroughWords = ["go through spellings","go through letters","spell out spellings","or","next word, to go through the next word"]
        readOutGTW = ", ".join(goThroughWords)
        
        n4 = "To go through wrong words, please either say"
        goThroughWrongWords = ["go through incorrect spellings", "go through incorrect words","what are my incorrect spellings","or","tell me my incorrect spellings"]
        readOutWrong = ", ".join(goThroughWrongWords)

        speak_output = n1 + ', ' + setWordsSpacing + ". " + n2 + ', ' + readOutSpacing + ". " + n3 + ', ' + readOutGTW + ". " + n4 + ', ' + readOutWrong + ". "
        
        return (    
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(setSpellingsIntentHandler())
sb.add_request_handler(WordsHandler())
sb.add_request_handler(goThroughSpellingHandler())
sb.add_request_handler(goThroughIncorrectSpellingHandler())
sb.add_request_handler(resetHandler())
sb.add_request_handler(yesHandler())
sb.add_request_handler(noHandler())
sb.add_request_handler(repeatHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
