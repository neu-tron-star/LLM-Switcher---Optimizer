# LLM-Router 🚀

**LLM-Router** is a lightweight Python framework to intelligently route tasks to the most suitable Large Language Model (LLM) based on **task type, performance benchmarks, and cost efficiency**. It supports multiple LLM providers including **Gemini, Mistral, OpenAI, and Groq**, allowing seamless task execution across different models while optimizing for **cost, speed, and accuracy**.

---

## Features ✨

- **Multi-LLM orchestration**: Automatically selects the best LLM for a given task.
- **Task-based selection**: Supports task types like:
  - `small` (short text, summarization)
  - `medium` (long text, complex text generation)
  - `heavy` (code generation, long context tasks)
  - `image` (image generation prompts)
  - `video` (future support)
- **Cost-effective**: Utilizes free token quotas and ranks models by benchmark-to-cost ratio for startups and price-sensitive companies.
- **Retry and fallback mechanism**: Automatically switches to the next suitable LLM if a model fails.
- **Streaming support**: Stream outputs from LLMs where supported.
- **Extensible**: Easily add new LLM providers with minimal code changes.

---

## Supported LLM Providers

| Provider | Example Models | Task Types | Free Tokens | Price per 1k Tokens |
|----------|----------------|------------|------------|-------------------|
| Gemini   | gemini-1.5-flash, gemini-2.5-flash | small, medium, text-generation | 50k–100k | $0 – $0.001 |
| Mistral  | mistral-small-2503, mistral-large-2411, codestral-2501 | small, heavy, code-generation | 0 | $0.02 – $0.05 |
| Groq     | llama-3.1-8b-instant, llama-3.3-70b-versatile | medium, heavy, text/code generation | 0 | $0.005 – $0.01 |
| OpenAI   | gpt-3.5-turbo, gpt-4, gpt-4-32k | small, medium, heavy, image generation | 0 | Varies per plan |

> **Note:** Free token quota is utilized before billing, making it ideal for **startups and price-sensitive projects**.

---

## Installation 💻

```bash
git clone https://github.com/your-username/LLM-Router.git
cd LLM-Router
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Setup
Create a .env file in the root directory:
```bash
CHATGEMINI_API_KEY=your_gemini_key
MISTRAL_API_KEY=your_mistral_key
CHATGROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
```

## Run the project
Run this script in a new terminal
```bash
python app.py
```
# 🧠 What Makes LLM Switcher Optimizer Unique?
## Cost-Effectiveness 💸
LLM-Router prioritizes models that are free or low-cost for your task while maintaining high benchmark scores. This is particularly suitable for:

- Startups with budget constraints

- Rapid prototyping of AI features

- Price-sensitive companies scaling AI workloads

- By intelligently using free token quotas first, LLM-Router reduces operational costs without compromising on performance.

## Features ✨

- **Multi-LLM routing** – automatically selects the most suitable LLM for a task.
- **Cost-aware execution** – considers free token quotas and per-1k token pricing.
- **Task-based selection** – handles small, medium, heavy, text, code, image, and video tasks.
- **Automatic retries & failover** – switches to next best LLM if a request fails.
- **Supports streaming responses** – for models that provide streaming output.
- **Extensible** – easily add new LLMs or task types.

---

## Key Components & Architecture 🏗️

LLM-Router is organized into modular components for easy extensibility and maintenance. Here's a breakdown:

### 1. `app.py`
- Main entry point for executing tasks.
- Loads model configurations from `models.json`.
- Initializes the `LLMSwitcher`.
- Defines tasks and invokes them using the switcher.
- Prints results, estimated costs, and reasons for LLM selection.

### 2. `src/llm_router.py`
- Contains the **`LLMSwitcher`** class which:
  - Ranks LLMs based on **benchmark scores** and **estimated cost**.
  - Switches automatically if an LLM fails.
  - Consumes free token quota intelligently.
  - Supports both standard and streaming tasks.
- Handles retries and ensures robust task execution.

### 3. `src/message.py`
- Defines message types for interaction with LLMs:
  - **`HumanMessage`** – user input.
  - **`AIMessage`** – LLM responses.
  - **`SystemMessage`** – system instructions for LLMs.
  - **`ImageMessage`** – images via URL, local file path, or base64.
  - **`ToolMessage`** – structured tool calls.

### 4. `src/inference/` (LLM Wrappers)
- Each LLM has its own wrapper implementing:
  - `invoke()` – synchronous API call.
  - `async_invoke()` – asynchronous API call.
  - `stream()` – streaming output.
  - `available_models()` – lists models for the provider.
- Examples:
  - `gemini.py` → `ChatGemini`
  - `mistral.py` → `ChatMistral`
  - `openai.py` → `ChatOpenAI`
  - `groq.py` → `ChatGroq`

### 5. `models.json`
- JSON configuration with LLMs, task types, pricing, free token limits, and benchmark scores.
- Example structure:

```json
[
  {
    "provider": "gemini",
    "model": "gemini-1.5-flash",
    "tasks": ["small","medium"],
    "price_per_1k_tokens": 0,
    "free_limit_tokens": 50000,
    "benchmark_score": 90
  }
]

```

## API Optimization and Benchmarking
A product designed to help companies select the most efficient and cost-effective API models for various tasks by providing detailed benchmarking and recommendations.

---

## License 📄

MIT License. Free to use, modify, and distribute.

---

## Contributing 🤝

Want to contribute to this project? We'd love your help!  

1. Fork the repository.  
2. Create your feature branch:  
   ```bash
   git checkout -b feature/MyFeature

3. Commit your changes
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/MyFeature
   ```
5. Open a Pull Request.

## Acknowledgements 🙏

This project is made possible by the incredible work of the teams behind these models and platforms:

- [OpenAI](https://openai.com/) – for their APIs
- [Google Gemini](https://developers.generativeai.google/) 
- [Mistral AI](https://www.mistral.ai/)
- [Groq LLMs](https://www.groq.com/)

## Project Status ✅

- ✅ Basic multi-LLM routing implemented
- ✅ Task-based cost optimization
- ✅ Image & text task support
- ⚠️ Video & advanced streaming support coming soon

