# Voice Clone – Talk to an AI Version of Yourself

A small voice assistant that listens to you through your microphone, thinks with an LLM, and answers out loud **in your own cloned voice**. Everything runs through [AssemblyAI](https://www.assemblyai.com/): speech-to-text, the LLM Gateway, and text-to-speech.

The default persona is **"AI somaii"**, an AI clone of Yassine Somai (AI engineer) who chats about programming, Python and AI.

## How it works

Each turn of the conversation goes through three steps:

```
 🎤 listen()  ──►  🧠 think()  ──►  🔊 speak()
 mic → WAV →       conversation →    reply → cloned-voice
 AssemblyAI STT    LLM Gateway       TTS, streamed to speakers
```

1. **`listen()`** records 16 kHz mono audio from your mic until you press Enter, saves it to `you.wav`, and transcribes it with AssemblyAI.
2. **`think()`** adds your message to the chat history and sends the whole conversation to the AssemblyAI LLM Gateway (`/v1/chat/completions`). The bot remembers what was said earlier in the session.
3. **`speak()`** turns the reply into speech with your cloned voice and plays the 24 kHz audio while it streams in.

Say **"goodbye"** to end the conversation.

## Requirements

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A working microphone and speakers/headphones
- An AssemblyAI account with:
  - an **API key**
  - a **cloned voice ID** (create one from a recording of your voice in the AssemblyAI dashboard)

## Setup

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd "voice clone"
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   pip install assemblyai httpx python-dotenv sounddevice
   ```

3. **Create a `.env` file** in the project root:

   ```env
   ASSEMBLYAI_API_KEY=your_api_key_here
   ASSEMBLYAI_VOICE_ID=your_cloned_voice_id_here
   ```

   `.env` is already listed in `.gitignore`, so your keys won't be committed.

## Usage

```bash
uv run main.py
```

Then:

1. Press **Enter** and start talking.
2. Press **Enter** again when you're done.
3. Listen to the reply in your cloned voice.
4. Repeat, or say **"goodbye"** to quit.

Example session:

```
AI SOMAii is ready. Say 'goodbye' to exit.

Press Enter and start talking ...
Listening ... press Enter when you're done.
You: What's the difference between a list and a tuple in Python?
AI somai: A list is mutable so you can change it after creating it, while a tuple is immutable and fixed once made.
```

## Customization

All settings are at the top of [main.py](main.py):

| Setting | What it does |
|---|---|
| `MODEL` | Which LLM to use on the AssemblyAI LLM Gateway (default: `qwen3.5-4b-32k-fast`). |
| `SYSTEM_PROMPT` | The bot's personality. Change the name, topics, or tone here. Keep the instruction to answer in short, plain sentences, since the reply is spoken aloud. |
| `max_tokens` (in `think()`) | Maximum reply length (default: 200). |

## Project structure

```
voice clone/
├── main.py                    # The voice assistant (listen → think → speak loop)
├── src/voice_clone/__init__.py  # Package stub (placeholder entry point)
├── pyproject.toml             # Project metadata and dependencies
├── uv.lock                    # Locked dependency versions
├── .python-version            # Python 3.13
└── .env                       # Your API key and voice ID (not committed)
```

> **Note:** the `voice-clone` script in `pyproject.toml` currently points to the placeholder in `src/voice_clone/__init__.py`, which only prints a greeting. Use `uv run main.py` to start the assistant.

## Troubleshooting

- **`KeyError: 'ASSEMBLYAI_API_KEY'`**: the `.env` file is missing or the variable name is wrong.
- **"Didn't catch that, try again."**: nothing was transcribed. Check that the right microphone is selected as your system default and speak a bit longer.
- **No sound or audio device errors**: run `python -m sounddevice` to list devices and check your default input/output.
- **HTTP 401 / 403**: your API key is invalid or your account doesn't have access to the LLM Gateway or voice features.

## Tech stack

- [AssemblyAI Python SDK](https://github.com/AssemblyAI/assemblyai-python-sdk): transcription and text-to-speech
- [AssemblyAI LLM Gateway](https://www.assemblyai.com/): chat completions
- [httpx](https://www.python-httpx.org/): HTTP client
- [sounddevice](https://python-sounddevice.readthedocs.io/): microphone recording and audio playback
- [python-dotenv](https://github.com/theskumar/python-dotenv): loads the `.env` file
