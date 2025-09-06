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

