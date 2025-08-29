import boto3
import logging
import uuid
from botocore.exceptions import ClientError
from config import AWS_REGION, AWS_BEDROCK_AGENT_ID, AWS_BEDROCK_ALIAS_ID, DEFAULT_SESSION_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_prompt():
    """Get the prompt from user input"""
    print("\n" + "="*60)
    print("ENTER YOUR QUESTION".center(60))
    print("="*60)
    print("Ask any question about your knowledge base:")
    print("Example: What are the financial benefits to Medicare?")
    print("Example: How do I choose between Original Medicare and Medicare Advantage?")
    print()
    
    while True:
        try:
            prompt = input("Your question: ").strip()
            if prompt:
                return prompt
            else:
                print("Please enter a question. Cannot be empty.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            exit(0)
        except EOFError:
            print("\nUnexpected end of input.")
            exit(1)

def invoke_agent(client, agent_id, alias_id, prompt, session_id):
    """Invoke the AWS Bedrock agent and return the response"""
    print(f"Invoking Bedrock Agent: {agent_id}")
    print(f"Using Alias: {alias_id}")
    print(f"Session ID: {session_id}")
    
    response = client.invoke_agent(
        agentId=agent_id,
        agentAliasId=alias_id,
        enableTrace=True,
        sessionId=session_id,
        inputText=prompt,
        streamingConfigurations={
            "applyGuardrailInterval": 20,
            "streamFinalResponse": False
        }
    )
    
    completion = ""
    print("Processing agent response...")
    
    for event in response.get("completion"):
        # Collect agent output
        if 'chunk' in event:
            chunk = event["chunk"]
            completion += chunk["bytes"].decode()
        
        # Log trace output
        if 'trace' in event:
            trace_event = event.get("trace")
            trace = trace_event['trace']
            for key, value in trace.items():
                logging.info("%s: %s", key, value)

    return completion

def main():
    """Main function to run the Bedrock agent demo"""
    print("="*60)
    print("AWS BEDROCK AGENT DEMO".center(60))
    print("="*60)
    
    # Validate configuration
    if not AWS_BEDROCK_AGENT_ID:
        print("ERROR: AWS_BEDROCK_AGENT_ID not found in environment variables")
        return
    
    if not AWS_BEDROCK_ALIAS_ID:
        print("ERROR: AWS_BEDROCK_ALIAS_ID not found in environment variables")
        return
    
    print(f"Agent ID: {AWS_BEDROCK_AGENT_ID}")
    print(f"Alias ID: {AWS_BEDROCK_ALIAS_ID}")
    print(f"Region: {AWS_REGION}")
    
    # Initialize AWS client
    try:
        client = boto3.client(
            service_name="bedrock-agent-runtime",
            region_name=AWS_REGION
        )
        print("AWS Bedrock Agent Runtime client initialized successfully")
    except Exception as e:
        print(f"Failed to initialize AWS client: {str(e)}")
        return
    
    # Get user prompt
    prompt = get_user_prompt()
    session_id = f"{DEFAULT_SESSION_ID}-{uuid.uuid4().hex[:8]}"
    
    print(f"Question: {prompt}")
    print(f"Session ID: {session_id}")
    
    # Invoke the agent
    try:
        completion = invoke_agent(client, AWS_BEDROCK_AGENT_ID, AWS_BEDROCK_ALIAS_ID, prompt, session_id)
        
        # Display results
        print("\n" + "="*60)
        print("AGENT RESPONSE".center(60))
        print("="*60)
        print(completion)
        
        print("\nDemo completed successfully!")
        
    except Exception as e:
        print(f"Demo failed: {str(e)}")
        logger.error(f"Demo failed: {str(e)}")

if __name__ == "__main__":
    main()