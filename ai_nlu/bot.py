from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging

from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

import os
dir_path = os.path.dirname(os.path.realpath(__file__))


logger = logging.getLogger(__name__)

def train_dialogue(domain_file, model_path, training_data_file):
    agent = Agent(domain_file)

    agent.train(
            training_data_file,
            max_history=3,
            epochs=100,
            batch_size=50,
            augmentation_factor=50,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent

def train_nlu(data_path, config, model_path):
    from rasa_nlu.converters import load_data
    from rasa_nlu.config import RasaNLUConfig
    from rasa_nlu.model import Trainer

    training_data = load_data(data_path)
    trainer = Trainer(RasaNLUConfig(config))
    trainer.train(training_data)
    model_directory = trainer.persist(model_path, fixed_model_name="current")

    return model_directory

def run(msg, serve_forever=True):
    interpreter = RasaNLUInterpreter("models/nlu/default/current")
    agent = Agent.load("models/dialogue", interpreter=interpreter)

    if serve_forever:
        pass
    return agent

def create_agent():
    interpreter = RasaNLUInterpreter(dir_path + "/models/nlu/current")
    agent = Agent.load(dir_path + "/models/dialogue", interpreter=interpreter)
    return agent

def respond(msg, agent):
    return agent.handle_message(msg)[0]

def main():
    parser = argparse.ArgumentParser(description="Start or train bot")
    parser.add_argument('task', choices=[
                        "train-nlu", "train-dialogue", "all", "run"], help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    if task == "train-nlu":
        train_nlu("./data/testData.json", "config_nlu.json", "models/nlu")
    elif task == "train-dialogue":
        train_dialogue("domain.yml", "models/dialogue", "./data/story.md")
    elif task == "run":
        run()
    elif task == "all":
        train_nlu("./data/testData.json", "config_nlu.json", "models/nlu")
        train_dialogue("domain.yml", "models/dialogue", "./data/story.md")
        run()
    else:
        warnings.warn("Need to pass either 'train-nlu', 'train-dialogue' or "
                      "'run' to use the script.")
        exit(1)

if __name__ == "__main__":
    main()
