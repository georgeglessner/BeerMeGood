#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# BeerMe
import logging
import urllib.request
import urllib.parse
import json

from keys import api_key
from random import randint
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to Brewery Locator, ask to find a brewery in a city!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Beer Me", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class BeerMeIntent(AbstractRequestHandler):
    """Handler for Beer Me Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("BeerMeIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        city = slots.get("city").value
        city = city.replace(' ', '+')
        
        f = urllib.request.urlopen('http://beermapping.com/webservice/loccity/{}/{}&s=json'.format(api_key, city))
        
        json_string = f.read()
        parsed_json = json.loads(json_string)
        totalCount = len(parsed_json)
        
        breweries = []
        
        if(totalCount>=1):
            for i in range(0, totalCount):
                if parsed_json[i]['status'] in ['Brewpub', 'Brewery']:
                    breweries.append({'name': parsed_json[i]['name'], 'street': parsed_json[i]['street'], 'locID': parsed_json[i]['id'], 'overall':parsed_json[i]['overall']})
        
        randInt = randint(0,len(breweries))

        speech_text = "{} located at {}".format(breweries[randInt].get('name'), breweries[randInt].get('street'))

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Beer Me", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class TopBreweryIntent(AbstractRequestHandler):
    """Handler for Beer Me Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TopBreweryIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        city = slots.get("topcity").value
        city = city.replace(' ', '+')
        
        f = urllib.request.urlopen('http://beermapping.com/webservice/loccity/{}/{}&s=json'.format(api_key, city))
        
        json_string = f.read()
        parsed_json = json.loads(json_string)
        totalCount = len(parsed_json)
        
        breweries = []
        
        if(totalCount>=1):
            for i in range(0, totalCount):
                if parsed_json[i]['status'] in ['Brewpub', 'Brewery']:
                    breweries.append({'name': parsed_json[i]['name'], 'street': parsed_json[i]['street'], 'locID': parsed_json[i]['id'], 'overall':parsed_json[i]['overall']})
        
        seq = []
        for x in breweries:
            seq.append([x['overall'], x['name'], x['street']])
        
        speech_text = '{} located at {}'.format(max(seq)[1], max(seq)[2])

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Beer Me", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Ask for a brewery in a certain city!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Beer Me", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Beer Me", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Beer Me skill can't help you with that.  "
            "You can ask for a brewery in a city!")
        reprompt = "You can ask for a brewery in a city!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        slots = handler_input.request_envelope.request.intent.slots
        city = slots.get("city").value
        
        speech = "Sorry, I couldn't find any results for {} Please try again!!".format(city)
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BeerMeIntent())
sb.add_request_handler(TopBreweryIntent())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
