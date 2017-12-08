import logging

from rasa_core.actions import Action

class ActionFindWeather(Action):
    def name(self):
        return 'action_find_weather'

    def run(self, dispatcher, tracker, domain):
        city = tracker.get_slot('city')
        date = tracker.get_slot('date')
        dispatcher.utter_message("City: {0} and date: {1}".format(city, date))
        logger.error("City: {0} and date: {1}".format(city, date))
        return []
