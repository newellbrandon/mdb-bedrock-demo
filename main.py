import boto3
import logging
import uuid
from botocore.exceptions import ClientError
from colorama import init, Fore, Back, Style
from config import AWS_REGION, AWS_BEDROCK_AGENT_ID, AWS_BEDROCK_ALIAS_ID, DEFAULT_SESSION_ID

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_section_header(title, color=Fore.CYAN):
    """Print a formatted section header"""
    print(f"\n{color}{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}{Style.RESET_ALL}")

def print_step(step_num, description, color=Fore.GREEN):
    """Print a formatted step"""
    print(f"\n{color}Step {step_num}: {description}{Style.RESET_ALL}")

def print_success(message, color=Fore.GREEN):
    """Print a success message"""
    print(f"{color}✓ {message}{Style.RESET_ALL}")

def print_error(message, color=Fore.RED):
    """Print an error message"""
    print(f"{color}✗ {message}{Style.RESET_ALL}")

def print_info(message, color=Fore.BLUE):
    """Print an info message"""
    print(f"{color}ℹ {message}{Style.RESET_ALL}")

def get_user_prompt():
    """Get the prompt from user input"""
    print_section_header("ENTER YOUR QUESTION", Fore.YELLOW)
    print(f"{Fore.WHITE}Ask any question about your knowledge base:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Example: What are the benefits of Medicare Advantage?{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Example: How do I choose between Original Medicare and Medicare Advantage?{Style.RESET_ALL}")
    print()
    
    while True:
        try:
            prompt = input(f"{Fore.GREEN}Your question: {Style.RESET_ALL}").strip()
            if prompt:
                return prompt
            else:
                print_error("Please enter a question. Cannot be empty.")
        except KeyboardInterrupt:
            print("\n")
            print_error("Operation cancelled by user.")
            exit(0)
        except EOFError:
            print("\n")
            print_error("Unexpected end of input.")
            exit(1)

def invoke_agent(client, agent_id, alias_id, prompt, session_id):
    """Invoke the AWS Bedrock agent and return the response"""
    print_info(f"Invoking Bedrock Agent: {agent_id}")
    print_info(f"Using Alias: {alias_id}")
    print_info(f"Session ID: {session_id}")
    
    try:
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
        print_info("Processing agent response...")
        
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
                    logger.info(f"Trace - {key}: {value}")

        return completion
        
    except Exception as e:
        print_error(f"Error invoking agent: {str(e)}")
        raise

def main():
    """Main function to run the Bedrock agent demo"""
    print_section_header("AWS BEDROCK AGENT DEMO", Fore.MAGENTA)
    
    # Step 1: Validate configuration
    print_step(1, "Validating Configuration")
    
    if not AWS_BEDROCK_AGENT_ID:
        print_error("AWS_BEDROCK_AGENT_ID not found in environment variables")
        return
    
    if not AWS_BEDROCK_ALIAS_ID:
        print_error("AWS_BEDROCK_ALIAS_ID not found in environment variables")
        return
    
    print_success(f"Agent ID: {AWS_BEDROCK_AGENT_ID}")
    print_success(f"Alias ID: {AWS_BEDROCK_ALIAS_ID}")
    print_success(f"Region: {AWS_REGION}")
    
    # Step 2: Initialize AWS client
    print_step(2, "Initializing AWS Bedrock Agent Runtime Client")
    
    try:
        client = boto3.client(
            service_name="bedrock-agent-runtime",
            region_name=AWS_REGION
        )
        print_success("AWS Bedrock Agent Runtime client initialized successfully")
    except Exception as e:
        print_error(f"Failed to initialize AWS client: {str(e)}")
        return
    
    # Step 3: Get user prompt
    print_step(3, "Getting User Question")
    
    prompt = get_user_prompt()
    session_id = f"{DEFAULT_SESSION_ID}-{uuid.uuid4().hex[:8]}"
    
    print_info(f"Question: {prompt}")
    print_info(f"Session ID: {session_id}")
    
    # Step 4: Invoke the agent
    print_step(4, "Invoking Bedrock Agent")
    
    try:
        completion = invoke_agent(client, AWS_BEDROCK_AGENT_ID, AWS_BEDROCK_ALIAS_ID, prompt, session_id)
        
        # Step 5: Display results
        print_step(5, "Agent Response")
        print_section_header("AGENT RESPONSE", Fore.YELLOW)
        print(f"{Fore.WHITE}{completion}{Style.RESET_ALL}")
        
        print_success("Demo completed successfully!")
        
    except Exception as e:
        print_error(f"Demo failed: {str(e)}")
        logger.error(f"Demo failed: {str(e)}")

if __name__ == "__main__":
    main()