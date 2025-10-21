"""
This module is the main entry point of the application that:
1. Interacts with the user and receives their requests
2. Analyzes and processes requests using artificial intelligence
3. Performs appropriate operations (search, analysis, response, etc.)
4. Displays results to the user
"""

import asyncio
from agent.executor import WebExecutor
from agent.planner import analyze_user_request

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
                    # Analyze user request and determine appropriate action
                    action_plan = await analyze_user_request(user_prompt)
                    
                    # Execute appropriate operation based on request type
                    if action_plan['type'] == 'product_search':
                        executor = WebExecutor()
                        results = await executor.execute_search(action_plan['search_params'])
                        print("\nSearch Results:")
                        for result in results:
                            print(f"\nProduct: {result['title']}")
                            print(f"Price: {result['price']}")
                            print(f"Store: {result['store']}")
                            print(f"Link: {result['url']}")
                            
                    elif action_plan['type'] == 'product_analysis':
                        print("\nProduct Analysis:")
                        print(action_plan['analysis'])
                        
                    elif action_plan['type'] == 'recommendation':
                        print("\nRecommendations:")
                        for recommendation in action_plan['recommendations']:
                            print(f"- {recommendation}")
                            
                    elif action_plan['type'] == 'general_response':
                        print(f"\n{action_plan['response']}")
                    
                except Exception as e:
                    print(f"\nSorry, an error occurred: {str(e)}")
                    print("Please try again.")
                    continue
                    
            except EOFError:
                print("\nبرنامه به طور غیرمنتظره پایان یافت.")
                break
            except KeyboardInterrupt:
                print("\nبرنامه توسط کاربر متوقف شد.")
                break
            except Exception as e:
                print(f"\nخطایی رخ داد: {str(e)}")
                continue
                
    except Exception as e:
        print(f"خطای اصلی: {str(e)}")
        return 1
    
    return 0

# Run the main program if this file is executed directly
if __name__ == "__main__":
    asyncio.run(main())