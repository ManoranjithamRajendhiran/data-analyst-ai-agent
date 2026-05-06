import os
import time
from anthropic import Anthropic, APIError, APITimeoutError, RateLimitError
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# --- config from .env (never hardcode these) ---
API_KEY   = os.getenv("ANTHROPIC_API_KEY")
MODEL     = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
MAX_TOK   = int(os.getenv("MAX_TOKENS", 700))
MAX_RETRY = 3

if not API_KEY:
    raise EnvironmentError("ANTHROPIC_API_KEY is missing from .env")

client = Anthropic(api_key=API_KEY)

# --- logger goes to file + console ---
logger.add("logs/agent.log", rotation="1 MB", retention="7 days", level="INFO")


def ask_claude(prompt: str) -> str:
    """
    Send a prompt to Claude with retry logic and proper error handling.
    Returns the response text, or a user-friendly error string.
    """
    if not prompt or not prompt.strip():
        logger.warning("Empty prompt received — skipping API call")
        return "Please enter a valid question."

    for attempt in range(1, MAX_RETRY + 1):
        try:
            logger.info(f"Claude API call | attempt={attempt} | prompt_len={len(prompt)}")
            start = time.time()

            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOK,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )

            duration = round(time.time() - start, 2)
            result = response.content[0].text
            logger.success(f"Claude responded in {duration}s | output_len={len(result)}")
            return result

        except RateLimitError:
            wait = 2 ** attempt          # 2s, 4s, 8s
            logger.warning(f"Rate limited — waiting {wait}s before retry {attempt}")
            time.sleep(wait)

        except APITimeoutError:
            logger.warning(f"Timeout on attempt {attempt}")
            if attempt == MAX_RETRY:
                return "Request timed out. Please try again."

        except APIError as e:
            logger.error(f"Anthropic API error: {e}")
            return f"API error: {e.message}"

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return "Something went wrong. Check logs/agent.log for details."

    return "Claude could not respond after multiple retries. Please try again."