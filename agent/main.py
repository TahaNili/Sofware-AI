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
    print("سلام! من یک دستیار هوشمند هستم و می‌توانم در موارد مختلف به شما کمک کنم.")
    print("مثلا می‌توانید درباره:")
    print("- جستجو و مقایسه قیمت محصولات")
    print("- تحلیل و بررسی محصولات")
    print("- پیشنهاد محصولات مشابه")
    print("- راهنمایی برای خرید")
    print("- و هر سوال دیگری از من بپرسید!")
    
    while True:
        # Get user request
        user_prompt = input("\nلطفا درخواست خود را وارد کنید (یا 'خروج' برای پایان): ")
        
        if user_prompt.lower() in ['خروج', 'exit', 'quit']:
            print("خدانگهدار!")
            break
            
        try:
            # Analyze user request and determine appropriate action
            action_plan = await analyze_user_request(user_prompt)
            
            # Execute appropriate operation based on request type
            if action_plan['type'] == 'product_search':
                executor = WebExecutor()
                results = await executor.execute_search(action_plan['search_params'])
                print("\nنتایج جستجو:")
                for result in results:
                    print(f"\nمحصول: {result['title']}")
                    print(f"قیمت: {result['price']}")
                    print(f"فروشگاه: {result['store']}")
                    print(f"لینک: {result['url']}")
                    
            elif action_plan['type'] == 'product_analysis':
                print("\nتحلیل محصول:")
                print(action_plan['analysis'])
                
            elif action_plan['type'] == 'recommendation':
                print("\nپیشنهادات:")
                for recommendation in action_plan['recommendations']:
                    print(f"- {recommendation}")
                    
            elif action_plan['type'] == 'general_response':
                print(f"\n{action_plan['response']}")
                
        except Exception as e:
            print(f"\nمتأسفانه مشکلی پیش آمد: {str(e)}")
            print("لطفاً دوباره تلاش کنید.")

# Run the main program if this file is executed directly
if __name__ == "__main__":
    asyncio.run(main())