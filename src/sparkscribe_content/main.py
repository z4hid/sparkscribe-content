#!/usr/bin/env python
from sparkscribe_content.crew import SparkscribeContentCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    SparkscribeContentCrew().crew().kickoff(inputs=inputs)