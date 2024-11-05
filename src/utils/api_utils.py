import streamlit as st
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import json
from typing import Optional, Dict, Any
from config.settings import load_config


def make_api_call(prompt: str, max_tokens: int = 2000, temperature: float = 0.5) -> Optional[Dict[str, Any]]:
    """Make API call with specific JSON requirements"""
    try:
        if 'anthropic' not in st.session_state:
            if not initialize_anthropic():
                return None

        # Create a more specific role and instruction
        system_instruction = """You are a specialized marketing AI assistant that generates JSON responses for a bank's marketing system. Your role is to:
1. Generate ONLY valid JSON marketing content
2. Never provide explanations or apologies
3. Never deviate from JSON format
4. Always complete the full JSON structure
5. Focus on professional banking services

Format all responses as valid JSON only."""

        # Create the complete prompt
        complete_prompt = f"""
{system_instruction}

IMPORTANT: Your response must be a single valid JSON object.
DO NOT include any explanatory text, apologies, or additional content.
ONLY return the JSON object itself.

Required JSON structure and content:
{prompt}

Remember: Return ONLY the JSON object. No other text allowed."""

        # Make the API call with specific parameters
        response = st.session_state.anthropic.completions.create(
            model="claude-2",
            prompt=f"{HUMAN_PROMPT}{complete_prompt}{AI_PROMPT}",
            max_tokens_to_sample=max_tokens,
            temperature=temperature,
            stop_sequences=["\n\n", "Note:", "Remember:", "I apologize", "Let me"],
            top_p=0.1,  # More focused responses
            top_k=10  # More deterministic output
        )

        return {'completion': response.completion.strip()}

    except Exception as e:
        st.error(f"API Call Error: {str(e)}")
        return None


def initialize_anthropic():
    """Initialize Anthropic API client"""
    try:
        config = load_config()
        client = Anthropic(api_key=config['api_key'])
        st.session_state.anthropic = client
        return True
    except Exception as e:
        st.error(f"Error initializing Anthropic client: {str(e)}")
        return False


def test_api_connection() -> bool:
    """Test API connection"""
    try:
        response = make_api_call("Hi", max_tokens=10)
        return response is not None
    except Exception as e:
        st.error(f"API Connection Error: {str(e)}")
        return False