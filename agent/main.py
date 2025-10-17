# agent/main.py
import os
from dotenv import load_dotenv
from planner import plan_search_task
from executor import LocalExecutor

load_dotenv()

item_to_search = input("Enter the item to search for prices: ")

if __name__ == "__main__":
    item_to_search = item_to_search.strip()

    print(f"Planning search task for item: {item_to_search}")
    steps = plan_search_task(item_to_search)
    print(f"Planned Steps: {steps}")

    executor = LocalExecutor(headful=True)
    result_file = executor.run_search_and_extract(str(steps), item_to_search)
    print(f"Results saved to: {result_file}")