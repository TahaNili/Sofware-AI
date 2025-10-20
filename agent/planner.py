"""
This module is responsible for analyzing and processing user requests using OpenAI.
Upon receiving a user request, it uses artificial intelligence to determine the request type
and provide an appropriate response.
"""

from typing import Dict
import os
from openai import AsyncOpenAI
import json

async def analyze_user_request(user_prompt: str) -> Dict:
    """
    Analyzes user request and generates appropriate response using OpenAI

    Args:
        user_prompt: User request in natural language

    Returns:
        A dictionary that can include these fields based on request type:
            - type: Operation type (product_search, product_analysis, recommendation, general_response)
            - search_params: Search parameters for products
            - analysis: Product analysis
            - recommendations: List of recommendations
            - response: General response

    Raises:
        ValueError: If OPENAI_API_KEY is not set in environment variables
    """
    # Check for API key in environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("کلید API برای OpenAI یافت نشد. لطفاً OPENAI_API_KEY را در متغیرهای محیطی تنظیم کنید")
    
    # Create temporary OpenAI client
    client = AsyncOpenAI(api_key=api_key)
    
    # Send request to OpenAI for analysis and decision making
    system_prompt = """شما یک دستیار هوشمند هستید که می‌تواند:
    1. جستجو و مقایسه قیمت محصولات
    2. تحلیل و بررسی محصولات
    3. پیشنهاد محصولات مشابه
    4. راهنمایی برای خرید
    5. پاسخ به سوالات عمومی

    لطفاً درخواست کاربر را تحلیل کنید و یک پاسخ JSON با این ساختار برگردانید:
    {
        "type": "product_search|product_analysis|recommendation|general_response",
        "search_params": {"query": "...", "stores": [...], "filters": {...}},
        "analysis": "متن تحلیل محصول",
        "recommendations": ["پیشنهاد 1", "پیشنهاد 2", ...],
        "response": "پاسخ عمومی"
    }
    فقط فیلدهای مرتبط با نوع درخواست را پر کنید."""

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    # Convert JSON response to dictionary
    try:
        action_plan = json.loads(response.choices[0].message.content or "{}")
    except json.JSONDecodeError:
        # If JSON is not valid, return a generic response
        action_plan = {
            "type": "general_response",
            "response": "متأسفانه در پردازش درخواست شما مشکلی پیش آمد. لطفاً درخواست خود را به شکل دیگری مطرح کنید."
        }
    
    return action_plan