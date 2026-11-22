# Restaurant Agent

A terminal agent that takes restaurant orders and simulates cooking and serving.

## Setup

From the repository root, install the dependencies:

```powershell
cd my-agents
python -m pip install -r requirements-restro.txt
```

Add your Groq API key to the `.env` file at the repository root:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Optionally set `GROQ_MODEL` in the same file. The default is `openai/gpt-oss-120b`.

## Run

From `my-agents`:

```powershell
python restro-agent.py
```

Try `Table 4 ke liye 2 lassi`. Type `menu` to see available items or `exit` to quit.

To simulate one cooking failure and one serving failure and observe the retries:

```powershell
python restro-agent.py --cook-failures 1 --serve-failures 1
```

To run the offline graph checks without a Groq API key:

```powershell
python restro-agent.py --self-test
```
