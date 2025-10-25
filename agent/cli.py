"""
This module is the main entry point of the application that:
1. Interacts with the user and receives their requests
2. Analyzes and processes requests using artificial intelligence
3. Performs appropriate operations (search, analysis, response, etc.)
4. Displays results to the user
"""

import os
import sys
import asyncio
import inspect
from typing import Optional, Dict, Any
from agent.executor import WebExecutor
from agent.ai.factory import AIFactory
from utils.logger import logger


def select_ai_model() -> Any:
    """Let user select AI provider and model
    
    Returns:
        An AI client instance configured with the selected provider and model
    """
    factory = AIFactory()
    providers = factory.get_available_providers()
    
    print("\nAvailable AI Providers:")
    for i, (name, provider_id) in enumerate(providers, 1):
        print(f"{i}. {name}")
    
    while True:
        try:
            choice = int(input("\nSelect AI provider (enter number): ")) - 1
            if 0 <= choice < len(providers):
                provider = providers[choice][1]
                break
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")
    
    models = factory.get_models(provider)
    print("\nAvailable Models:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    while True:
        try:
            choice = int(input("\nSelect model (enter number): ")) - 1
            if 0 <= choice < len(models):
                model = models[choice]
                break
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")
    
    try:
        client = factory.create_client(provider=provider, model=model)
        return client
    except Exception as e:
        logger.error(f"Failed to create AI client: {e}")
        print(f"\nError creating AI client with {provider}/{model}: {e}")
        print("Falling back to default configuration...")
        return factory.create_client()


async def main() -> int:
    """Main CLI entry point
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        print("Hello! I\'m an intelligent assistant and I can help you with various tasks.")
        print("For example, you can ask about:")
        print("- Product search and price comparison")
        print("- Product analysis and reviews")
        print("- Similar product recommendations")
        print("- Shopping guidance")
        print("- System management and control")
        print("- Or any other questions you have!")
        
        # Let user select AI provider and model
        client = select_ai_model()
        print("\nAI model selected successfully!")
        
        while True:
            try:
                # Get user request
                user_prompt = input("\nPlease enter your request (or \'exit\' to quit): ")
                
                if user_prompt.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break
                
                try:
                    # Process the request (support sync and async clients)
                    resp_candidate = client.process_request(user_prompt)
                    if asyncio.iscoroutine(resp_candidate) or inspect.isawaitable(resp_candidate):
                        response = await resp_candidate
                    else:
                        response = resp_candidate

                    # Normalize response dicts
                    if isinstance(response, dict):
                        rtype = response.get("type")
                        if rtype == "product_search" and "search_params" in response:
                            executor = WebExecutor()
                            results = await executor.execute_search(response["search_params"])
                            print("\nSearch Results:")
                            for result in results:
                                print(f"\nProduct: {result["title"]}")
                                print(f"Price: {result["price"]}")
                                print(f"Store: {result["store"]}")
                                print(f"Link: {result["url"]}")
                        elif rtype == "product_analysis" and "analysis" in response:
                            print("\nProduct Analysis:")
                            print(response["analysis"])
                        elif rtype == "recommendation" and "recommendations" in response:
                            print("\nRecommendations:")
                            for recommendation in response["recommendations"]:
                                print(f"- {recommendation}")
                        elif rtype == "general_response" and "response" in response:
                            print(f"\n{response["response"]}")
                        elif response.get("error"):
                            print(f"\nSorry, an error occurred: {response.get("error")}")
                        else:
                            # Fallback: print the whole dict
                            print("\n", response)
                    else:
                        print("\n", str(response))
                
                except Exception as e:
                    print(f"\nSorry, an error occurred while processing: {str(e)}")
                    logger.error(f"Request processing error: {e}")
                    print("Please try again.")
                    continue
                
            except EOFError:
                print("\nThe program ended unexpectedly.")
                break
            except KeyboardInterrupt:
                print("\nThe program was stopped by the user.")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                logger.error(f"Main loop error: {e}")
                continue
    
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        logger.exception("Fatal error in CLI")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        logger.exception("Unhandled error in CLI")
        sys.exit(1)
