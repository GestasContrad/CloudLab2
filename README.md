# Lab 2 - REST API and Message Queues

## Description
This project implements a REST API and an asynchronous message queue system using Python and Flask.

## Prerequisites
- Python 3.9+
- Packages: `flask`, `requests`

## Installation
1. Create a virtual environment: `python -m venv .venv`
2. Activate the environment.
3. Install dependencies: `pip install -r requirements.txt`

## Running the Services
To run the full system, open separate terminal windows for each component:

1. **REST API**: 
   `python api.py` (Runs on port 5000)
2. **Queue Broker**: 
   `python broker.py` (Runs on port 6000)
3. **Producer**: 
   `python producer.py` (Sends tasks to the broker)
4. **Consumer**: 
   `python consumer.py` (Processes tasks from the broker)