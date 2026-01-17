# backend/story_generator.py
# FIXED VERSION - No more KeyError for 'segment'

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from groq import Groq
import json
import random

project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env!")

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

MYTHOLOGY_SCENARIOS = [
    {"epic": "Ramayana", "wise": "Ram", "user_role": "Lakshman"},
    {"epic": "Mahabharata", "wise": "Krishna", "user_role": "Arjuna"},
]

def count_words(text: str) -> int:
    return len(text.split())

def generate_emotion_story(emotion: str, user_idea: Optional[str] = None, 
                          length: str = "medium", custom_words: int = None, 
                          custom_paragraphs: int = None) -> str:
    """Generate emotion-based story"""
    
    if length == "custom" and custom_words:
        target = custom_words
        paras = custom_paragraphs or 3
    elif length == "short":
        target = 100
        paras = 2
    elif length == "long":
        target = 300
        paras = 6
    else:
        target = 200
        paras = 4

    prompt = f"""Write a beautiful touching story about {emotion}.

Story Topic: {user_idea if user_idea else 'Create a story about ' + emotion}

REQUIREMENTS:
1. Write EXACTLY {target} words
2. Simple language suitable for children
3. Warm, emotional, and touching
4. Indian cultural setting
5. Make it meaningful and heartwarming

Write EXACTLY {target} words."""

    system = f"""You write beautiful emotional stories for children.
EXACTLY {target} words.
Focus on {emotion}."""

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=target * 2,
        )
        
        story = completion.choices[0].message.content.strip()
        print(f"📊 Generated: {count_words(story)} words")
        return story
        
    except Exception as e:
        return f"Error generating story: {str(e)}"

def generate_ancestral_story(
    your_name: str, father_name: str, mother_name: str,
    grandfather_name: str = "", grandmother_name: str = "",
    siblings: str = "", extra_idea: str = None,
    length: str = "medium", custom_words: int = None, custom_paragraphs: int = None
) -> str:
    """Generate ancestral story"""
    
    if length == "custom" and custom_words:
        target = custom_words
        paras = custom_paragraphs or 3
    elif length == "short":
        target = 100
        paras = 2
    elif length == "long":
        target = 300
        paras = 6
    else:
        target = 200
        paras = 4

    nana = grandfather_name or "my Nana"
    nani = grandmother_name or "my Nani"

    prompt = f"""I am {your_name}. Write MY ancestral story (first-person).

Family: 
- Father: {father_name}
- Mother: {mother_name}
- Grandfather: {nana}
- Grandmother: {nani}
{f"- Siblings: {siblings}" if siblings else ""}

REQUIREMENTS:
1. Write EXACTLY {target} words
2. Event before I was born
3. Start: "I, {your_name}, was not born yet..."
4. Indian cultural setting
5. Touching and emotional

{f"Additional Focus: {extra_idea}" if extra_idea else ""}

Write EXACTLY {target} words."""

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": f"Write EXACTLY {target} words."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=target * 2,
        )
        
        story = completion.choices[0].message.content.strip()
        print(f"📊 Generated: {count_words(story)} words (ANCESTRAL)")
        return story
        
    except Exception as e:
        return f"Error generating story: {str(e)}"

def generate_mythology_dialogue(
    previous_context: Optional[str] = None,
    user_answer: Optional[str] = None,
    correct_answer: Optional[str] = None,
    scenario: Optional[dict] = None
) -> dict:
    """Interactive friendly dialogue - Like talking with a wise friend"""
    
    try:
        if scenario is None:
            scenario = random.choice(MYTHOLOGY_SCENARIOS)

        wise = scenario["wise"]
        user_role = scenario["user_role"]
        epic = scenario["epic"]

        if user_answer is None:
            # Starting new dialogue - Ask about user's problem
            prompt = f"""You are {wise} from {epic}, speaking as a caring friend to help someone with their life problems.

Start a warm, friendly conversation:
1. Greet warmly and ask what problem or worry they have
2. Be compassionate and understanding like a close friend
3. DON'T ask about war, battles, or epic stories
4. Ask about REAL LIFE problems: family issues, career confusion, relationship problems, self-doubt, difficult decisions, etc.
5. Keep it conversational and natural (about 60-80 words)

Format your response as a natural dialogue:
"{wise} speaks: [Your warm greeting and question about their problem]"

You MUST respond ONLY with valid JSON in this exact format:
{{
  "segment": "{wise} speaks: Your full dialogue here",
  "question": "What personal problem or worry do you have?",
  "correct_answer": "any life problem",
  "context": "Starting friendly conversation"
}}

IMPORTANT: Write "{wise} speaks:" not "Arjuna speaks" or any other name."""
        else:
            # Continuing dialogue - Help with their problem
            prompt = f"""Continue as {wise}, helping your friend with their problem.

Previous context: {previous_context}
Their problem/response: {user_answer}

Now respond as a wise, caring friend:
1. Acknowledge their problem with empathy
2. Share relevant wisdom from your experiences
3. Give practical, helpful advice
4. Ask a follow-up question to understand better or help them think deeper
5. Be supportive and encouraging (about 80-100 words)
6. NO questions about war or battles - focus on their PERSONAL LIFE issue

Format: "{wise} speaks: [Your empathetic response and advice]"

You MUST respond ONLY with valid JSON:
{{
  "segment": "{wise} speaks: Your complete caring response here",
  "question": "A thoughtful follow-up question about their problem",
  "correct_answer": "any reasonable response",
  "context": "Updated summary of the conversation"
}}

IMPORTANT: Always write "{wise} speaks:" at the start."""

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": f"You are {wise}, a wise and caring friend helping someone with life problems. Respond ONLY with valid JSON. Use '{wise} speaks:' format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=600
        )
        
        text = completion.choices[0].message.content.strip()
        
        # Clean JSON formatting
        text = text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        result = json.loads(text)
        
        # CRITICAL FIX: Ensure 'segment' always exists and has correct format
        if "segment" not in result:
            if "dialogue" in result:
                result["segment"] = result["dialogue"]
            elif "response" in result:
                result["segment"] = result["response"]
            else:
                result["segment"] = f"{wise} speaks: " + text[:200] + "..."
        
        # Ensure segment starts with correct format
        if not result["segment"].startswith(f"{wise} speaks:"):
            result["segment"] = f"{wise} speaks: " + result["segment"]
        
        # Ensure all required keys exist
        result.setdefault("question", "How can I help you further?")
        result.setdefault("correct_answer", "any response")
        result.setdefault("context", "Friendly conversation")
        result["scenario"] = scenario
        
        print(f"✅ Dialogue generated successfully")
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")
        wise_name = scenario.get('wise', 'Krishna') if scenario else 'Krishna'
        return {
            "segment": f"{wise_name} speaks: Greetings, my friend! I sense you have something weighing on your heart. Please, share with me - what troubles you today?",
            "question": "What problem or worry is on your mind?",
            "correct_answer": "any problem",
            "context": "Beginning friendly conversation",
            "scenario": scenario or MYTHOLOGY_SCENARIOS[0],
            "error": "JSON parsing failed"
        }
    except Exception as e:
        print(f"❌ Dialogue Error: {e}")
        wise_name = scenario.get('wise', 'Krishna') if scenario else 'Krishna'
        return {
            "segment": f"{wise_name} speaks: I'm here to listen and help, my friend. What's troubling you?",
            "question": "What would you like guidance on?",
            "correct_answer": "any issue",
            "context": "Starting conversation",
            "scenario": scenario or MYTHOLOGY_SCENARIOS[0],
            "error": str(e)
        }

def generate_cultural_story(topic: str, user_idea: str = None,
                           length: str = "medium", custom_words: int = None,
                           custom_paragraphs: int = None) -> str:
    """Generate cultural/historical story"""
    
    if length == "custom" and custom_words:
        target = custom_words
        paras = custom_paragraphs or 3
    elif length == "short":
        target = 100
        paras = 2
    elif length == "long":
        target = 300
        paras = 6
    else:
        target = 200
        paras = 4

    prompt = f"""Write a story about {topic}.

{f"Focus on: {user_idea}" if user_idea else ""}

REQUIREMENTS:
1. Write EXACTLY {target} words
2. Include cultural or historical context
3. Make it informative and engaging
4. Indian cultural setting
5. Educational and meaningful

Write EXACTLY {target} words."""

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": f"Write cultural stories. EXACTLY {target} words."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=target * 2,
        )
        
        story = completion.choices[0].message.content.strip()
        print(f"📊 Generated: {count_words(story)} words (Cultural)")
        return story
        
    except Exception as e:
        return f"Error generating story: {str(e)}"