# agent/executor.py
from browser_use import Agent, ChatBrowserUse, BrowserSession
import csv
import time

class LocalExecutor:
    def __init__(self, headful=True):
        self.headful = headful

    def run_search_and_extract(self, steps: str, item: str, max_results=3):
        task = f"Find prices for '{item}' from the first page search results. Extract seller and price in a short table."

        agent = Agent(
            task=task,
            llm=ChatBrowserUse(),
            browser=BrowserSession(
                headless=not self.headful
            )
        )

        out = agent.run_sync()

        filename = f"results_{int(time.time())}.csv"
        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["raw_output"])
        writer.writerow([out])

        return filename