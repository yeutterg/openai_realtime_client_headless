# Headless OpenAI Realtime API Client for Python

This is a fork of the [OpenAI Realtime API Client for Python](https://github.com/run-llama/openai_realtime_client) that removes the pynput dependency and allows the library to respond to hardware-based button presses on a Raspberry Pi microcontroller.

The following files have been modified from the original library:
* `.gitignore`
* `openai_realtime_client/handlers/input_handler.py`
* `pyproject.toml`
* `README.md`

The example files `examples/manual_cli.py` and `examples/streaming_cli.py` have NOT been modified to work with the headless setup.

## Original README

This is an experimental OpenAI Realtime API client for Python and LlamaIndex. It integrates with LlamaIndex's tools, allowing you to quickly build custom voice assistants.

Include two examples that run directly in the terminal -- using both manual and Server VAD mode (i.e. allowing you to interrupt the chatbot).

## Installation

Install system deps:

```bash
brew install ffmpeg
```

Install python deps:

```bash
pip install openai-realtime-client

# Optional: clone the repo and run the examples locally
git clone https://github.com/run-llama/openai_realtime_client.git
cd openai_realtime_client
```

Set your openai key:

```bash
export OPENAI_API_KEY="sk-..."
```

## Usage

Assuming you installed and cloned the repo (or copy-pasted the examples), you can immediately run the examples.

Run the interactive CLI with manual VAD (try asking for your phone number to see function calling in action):

```bash
python ./examples/manual_cli.py
```

Or to use streaming mode (which allows you to interrupt the chatbot):

```bash
python ./examples/streaming_cli.py
```

**NOTE:** Streaming mode can be a little janky, best to use headphones in a quiet environment.

Take a look at the examples, add your own tools, and build something amazing!
