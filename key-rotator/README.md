# Key Rotator

A free API key aggregator and proxy. Add keys from Gemini, Groq, OpenRouter, Cohere, Mistral — and get one unified OpenAI-compatible endpoint that rotates across them automatically.

## Quick start

```bash
cd key-rotator

# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your keys
cp .env.example .env
# Edit .env with your free-tier keys

# 3. Run
python main.py
```

Dashboard → http://localhost:7860  
Endpoint  → http://localhost:7860/v1

## Using the endpoint

Drop this into any OpenAI-compatible client:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:7860/v1",
    api_key="rotator",  # any non-empty string
)

response = client.chat.completions.create(
    model="gpt-4o-mini",   # mapped to gemini-1.5-flash
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

## Model aliases (OpenAI → free model)

| Alias | Routes to |
|---|---|
| `gpt-3.5-turbo` | Groq llama-3.1-8b-instant |
| `gpt-4` | Groq llama-3.3-70b-versatile |
| `gpt-4o` | Gemini 2.0 Flash |
| `gpt-4o-mini` | Gemini 2.0 Flash |

Or pass a native model name like `groq/llama-3.1-8b-instant` directly.

## How rotation works

- **Round-robin** by fewest requests among available keys
- **Cooldown** — a key that returns a rate-limit error is paused for 60s, then retried
- **Auth errors** cool down for 1 hour
- **Fallback** — retries up to 3 times across different keys per request

## Adding keys

- **.env** — comma-separate multiple keys per provider, loaded on startup
- **Dashboard** — add/delete keys live without restarting
