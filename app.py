import os
import json
from dotenv import load_dotenv

from src.llm_switcher import LLMSwitcher
from src.message import HumanMessage, SystemMessage, ImageMessage

# Inference wrappers
from src.inference.gemini import ChatGemini
from src.inference.mistral import ChatMistral
from src.inference.openai import ChatOpenAI
from src.inference.groq import ChatGroq

load_dotenv()

# -----------------------
# Load models from JSON
# -----------------------
llms = []
with open("models.json", "r") as f:
    models_data = json.load(f)

provider_map = {
    "gemini": (ChatGemini, "CHATGEMINI_API_KEY"),
    "groq": (ChatGroq, "CHATGROQ_API_KEY"),
    "mistral": (ChatMistral, "MISTRAL_API_KEY"),
    "openai": (ChatOpenAI, "OPENAI_API_KEY"),
}

for model in models_data:
    provider = model["provider"]
    if provider not in provider_map:
        continue

    LLMClass, api_env = provider_map[provider]
    api_key = os.getenv(api_env)
    if not api_key:
        continue  # Skip if API key not set

    llms.append({
        "llm": LLMClass(model=model["model"], api_key=api_key),
        "tasks": model["tasks"],
        "price_per_1k_tokens": model["price_per_1k_tokens"],
        "free_limit_tokens": model["free_limit_tokens"],
        "benchmark_score": model["benchmark_score"]
    })

# -----------------------
# Initialize switcher
# -----------------------
switcher = LLMSwitcher(llms=llms, max_retries=3)

# -----------------------
# Example tasks
# -----------------------
tasks = [
    {"prompt": "Summarize the following text: 'Artificial Intelligence is transforming the world...'", "type": "small"},
    {"prompt": "Generate an image related to AI ethics", "type": "image"},
]

# -----------------------
# Execute tasks
# -----------------------
for t in tasks:
    print("\n========================================")
    print(f"Task: {t['prompt']}\n")
    messages = [SystemMessage("You are a helpful AI assistant."), HumanMessage(t["prompt"])]

    # Filter LLMs that support this task type
    suitable_llms = [l for l in llms if t["type"] in l["tasks"]]

    if not suitable_llms:
        print(f"None LLM found suitable for the task: {t['type']}")
        continue

    # Use switcher with only suitable LLMs
    task_switcher = LLMSwitcher(llms=suitable_llms, max_retries=3)
    try:
        # For image tasks, wrap prompt in ImageMessage if model supports it
        if t["type"] == "image":
            image_messages = [SystemMessage("You are an AI that can generate images."), ImageMessage((t["prompt"], None))]
            response, selected_model, cost_estimate, reason = task_switcher.invoke_task(image_messages, t["type"])
        else:
            response, selected_model, cost_estimate, reason = task_switcher.invoke_task(messages, t["type"])

        print(f"--- Using LLM: {selected_model} ---")
        print(f"Task type: {t['type']}")
        print(f"Estimated cost: ${cost_estimate:.4f}")
        print(f"Reason for selection: {reason}\n")
        print("Response:")
        print(response)
    except Exception as e:
        print(f"Task failed: {e}")
