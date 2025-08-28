import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# AWS Configuration - Only from environment variables
AWS_REGION = os.getenv('AWS_REGION')  # Default to us-east-1 if not specified
AWS_BEDROCK_AGENT_ID = os.getenv('AWS_BEDROCK_AGENT_ID')
AWS_BEDROCK_ALIAS_ID = os.getenv('AWS_BEDROCK_ALIAS_ID')

# MongoDB Configuration (from existing .env)
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
VOYAGE_API_KEY = os.getenv('VOYAGE_API_KEY')
VOYAGE_MODEL = os.getenv('VOYAGE_MODEL', 'voyage-large-2-instruct')

# Session configuration
DEFAULT_SESSION_ID = "demo-session-123"
