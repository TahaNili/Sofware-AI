"""
This module is the main entry point of the application that:
1. Interacts with the user and receives their requests
2. Analyzes and processes requests using artificial intelligence
3. Performs appropriate operations (search, analysis, response, etc.)
4. Displays results to the user
"""

import asyncio
from agent.executor import WebExecutor
from agent.ai.factory import AIFactory

async def main():
    try:
        print("Hello! I'm an intelligent assistant and I can help you with various tasks.")
        print("For example, you can ask about:")
        print("- Product search and price comparison")
        print("- Product analysis and reviews")
        print("- Similar product recommendations")
        print("- Shopping guidance")
        print("- System management and control")
        print("- Or any other questions you have!")
        
        while True:
            try:
                # Get user request
                user_prompt = input("\nPlease enter your request (or 'exit' to quit): ")
                
                if user_prompt.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                
                try:
                    # Use the AI factory to get a client (mock if no keys)
                    client = AIFactory.create_client()
                    # Let the client process the request
                    response = await client.process_request(user_prompt)

                    # Normalize response dicts
                    if isinstance(response, dict):
                        rtype = response.get('type')
                        if rtype == 'product_search' and 'search_params' in response:
                            executor = WebExecutor()
                            results = await executor.execute_search(response['search_params'])
                            print("\nSearch Results:")
                            for result in results:
                                print(f"\nProduct: {result['title']}")
                                print(f"Price: {result['price']}")
                                print(f"Store: {result['store']}")
                                print(f"Link: {result['url']}")
                        elif rtype == 'product_analysis' and 'analysis' in response:
                            print("\nProduct Analysis:")
                            print(response['analysis'])
                        elif rtype == 'recommendation' and 'recommendations' in response:
                            print("\nRecommendations:")
                            for recommendation in response['recommendations']:
                                print(f"- {recommendation}")
                        elif rtype == 'general_response' and 'response' in response:
                            print(f"\n{response['response']}")
                        elif response.get('error'):
                            print(f"\nSorry, an error occurred: {response.get('error')}")
                        else:
                            # Fallback: print the whole dict
                            print("\n", response)
                    else:
                        print("\n", str(response))
                    
                except Exception as e:
                    print(f"\nSorry, an error occurred: {str(e)}")
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
                continue
                
    except Exception as e:
        print(f"Main error: {str(e)}")
        return 1
    
    return 0

# Run the main program if this file is executed directly
if __name__ == "__main__":
    asyncio.run(main())