"""from src.inference import BaseInference
from src.message import BaseMessage,AIMessage

class LLMSwitcher(BaseInference):
    def __init__(self, llms:list[BaseInference]=[],max_retries:int=3):
        self.llms = llms
        self.current_llm_index = 0
        self.max_retries = max_retries

    def switch_llm(self):
        self.current_llm_index = (self.current_llm_index + 1) % len(self.llms)
    
    @property
    def current_llm(self):
        return self.llms[self.current_llm_index]

    def invoke(self, messages:list[BaseMessage],json:bool=False)->AIMessage|RuntimeError:
        retries=0
        while retries<self.max_retries:
            current_llm = self.current_llm
            try:
                return current_llm.invoke(messages=messages,json=json)
            except Exception as e:
                print(f"Error with {current_llm.__class__.__name__}: {e}")
                self.switch_llm()
                retries+=1
        raise RuntimeError("All LLM's failed after maximum retries")
    
    def stream(self, messages:list[BaseMessage],json:bool=False):
        retries=0
        while retries<self.max_retries:
            current_llm = self.current_llm
            try:
                return current_llm.stream(messages=messages,json=json)
            except Exception as e:
                print(f"Error with {current_llm.name}: {e}")
                self.switch_llm()
                retries+=1
        raise RuntimeError("All LLM's failed after maximum retries")
"""

from src.inference import BaseInference
from src.message import BaseMessage, AIMessage

class LLMSwitcher:
    def __init__(self, llms: list[dict], max_retries: int = 3):
        """
        Args:
            llms (list[dict]): Each dict must have:
                {
                    "llm": <BaseInference subclass>,
                    "tasks": [list of supported task types],
                    "price_per_1k_tokens": float,
                    "free_limit_tokens": int,
                    "benchmark_score": int
                }
            max_retries (int): Max retries per LLM before switching.
        """
        self.llms = llms
        self.max_retries = max_retries

    def estimate_tokens_for_task(self, task_type: str) -> int:
        """Rough token estimate based on task type."""
        estimates = {
            "small": 300,
            "medium": 1000,
            "heavy": 3000,
            "text-generation": 1000,
            "code-generation": 2000,
            "image": 1,
            "video": 1,
        }
        return estimates.get(task_type, 500)

    def rank_llms(self, task_type: str):
        """Rank models by benchmark score and estimated cost."""
        token_estimate = self.estimate_tokens_for_task(task_type)
        capable_llms = [l for l in self.llms if task_type in l["tasks"]]

        if not capable_llms:
            raise RuntimeError(f"No LLM available for task type '{task_type}'")

        ranked = []
        for l in capable_llms:
            # Calculate effective cost with free quota
            if token_estimate <= l["free_limit_tokens"]:
                cost = 0.0
            else:
                cost = ((token_estimate - l["free_limit_tokens"]) / 1000) * l["price_per_1k_tokens"]

            score = l["benchmark_score"] / (cost + 1e-6)  # prevent divide by zero
            ranked.append({**l, "rank_score": score, "estimated_cost": cost, "token_estimate": token_estimate})

        ranked.sort(key=lambda x: x["rank_score"], reverse=True)
        return ranked

    def _consume_quota(self, selected: dict, tokens_used: int):
        """Reduce the free token quota after usage."""
        selected["free_limit_tokens"] = max(0, selected["free_limit_tokens"] - tokens_used)

    def invoke_task(self, messages: list[BaseMessage], task_type: str) -> tuple[str, str, float, str]:
        """Invoke a task on the best-ranked LLM.

        Returns:
            response_content (str),
            model_name (str),
            estimated_cost (float),
            reason (str)
        """
        ranked_llms = self.rank_llms(task_type)

        for selected in ranked_llms:
            retries = 0
            while retries < self.max_retries:
                try:
                    result: AIMessage = selected["llm"].invoke(messages)

                    # Update free quota after successful usage
                    self._consume_quota(selected, selected["token_estimate"])

                    # Build reason
                    if selected["estimated_cost"] == 0:
                        cost_reason = "covered by free token quota"
                    else:
                        cost_reason = f"expected cost ${selected['estimated_cost']:.4f}"
                    reason = (
                        f"Selected {selected['llm'].model} due to high benchmark ({selected['benchmark_score']}) "
                        f"and {cost_reason} for {task_type} task."
                    )

                    return result.content, selected["llm"].model, selected["estimated_cost"], reason
                except Exception as e:
                    print(f"Error with {selected['llm'].model}: {e}")
                    retries += 1

        raise RuntimeError("All suitable LLMs failed for this task")

    def stream_task(self, messages: list[BaseMessage], task_type: str):
        """Stream response from the best-ranked LLM."""
        ranked_llms = self.rank_llms(task_type)

        for selected in ranked_llms:
            retries = 0
            while retries < self.max_retries:
                try:
                    stream = selected["llm"].stream(messages)

                    # Update free quota for streaming tasks
                    self._consume_quota(selected, selected["token_estimate"])

                    return stream, selected["llm"].model
                except Exception as e:
                    print(f"Streaming error with {selected['llm'].model}: {e}")
                    retries += 1

        raise RuntimeError("All suitable LLMs failed for streaming task")
