"""
Utility functions for handling caching in Streamlit
"""
import streamlit as st
from functools import wraps
from typing import Any, Callable, Optional
import time
import pickle


def is_serializable(obj: Any) -> bool:
    """Check if an object is pickle-serializable"""
    try:
        pickle.dumps(obj)
        return True
    except (pickle.PickleError, TypeError):
        return False


def async_cache_data(ttl: int = 3600):
    """
    Custom cache decorator that ensures data is serializable

    Args:
        ttl (int): Time to live in seconds
    """

    def decorator(func: Callable) -> Callable:
        cache_key = f"cache_{func.__name__}"
        timestamp_key = f"timestamp_{func.__name__}"

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_time = time.time()

            # Check if we need to refresh the cache
            if (cache_key not in st.session_state or
                    timestamp_key not in st.session_state or
                    current_time - st.session_state[timestamp_key] > ttl):

                # Clear old cache if it exists
                if cache_key in st.session_state:
                    del st.session_state[cache_key]

                # Generate new data
                result = func(*args, **kwargs)

                # Verify result is serializable
                if not is_serializable(result):
                    st.error(f"Cache error: Result from {func.__name__} is not serializable")
                    return result

                # Update cache
                st.session_state[cache_key] = result
                st.session_state[timestamp_key] = current_time

                return result

            return st.session_state[cache_key]

        return wrapper

    return decorator