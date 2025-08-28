# AWS Bedrock Agent Demo - Development Guide

## 🚀 **Quick Start**

### Environment Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\bin\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Required Environment Variables
Create a `.env` file in the project root with the following variables:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_BEDROCK_AGENT_ID=your_agent_id_here
AWS_BEDROCK_ALIAS_ID=your_alias_id_here

# MongoDB Configuration
MONGODB_CONNECTION_STRING=mongodb+srv://USERNAME:PASSWORD@CLUSTER.REGION.mongodb.net/
VOYAGE_API_KEY=your_voyage_api_key
VOYAGE_MODEL=voyage-large-2-instruct
```

## 🗄️ **MongoDB MCP Server Integration**

### What is MCP?
MCP (Model Context Protocol) allows AI agents to interact with external data sources and tools. Our MongoDB MCP server enables the Bedrock agent to query, analyze, and manipulate MongoDB data directly.

### Key Benefits
- **Runtime Discovery**: MCP functions are automatically discoverable by the agent
- **Dynamic Capabilities**: No need to hardcode database operations
- **Flexible Integration**: Agent can adapt to available MCP functions
- **Real-time Access**: Direct database connectivity without pre-defined queries

### MongoDB MCP Server Features
- **Database Operations**: Create, read, update, delete operations
- **Collection Management**: List, create, drop collections
- **Query Execution**: Complex aggregation pipelines
- **Index Management**: Create and manage database indexes
- **Schema Analysis**: Understand collection structures
- **Data Export**: Export query results in various formats

### Quick Start
```bash
# Test MongoDB connection
python -c "
from config import MONGODB_CONNECTION_STRING
import pymongo
client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
print('MongoDB connection successful!')
print(f'Available databases: {client.list_database_names()}')
"
```

### Example Use Cases
- **Customer Analytics**: Aggregate customer data by region, status, or other criteria
- **Data Migration**: Export data from legacy systems and import to new collections
- **Performance Monitoring**: Analyze query performance and optimize indexes
- **Real-time Operations**: Monitor database changes and trigger actions

### Best Practices
- **Security**: Use least-privilege access and rotate credentials regularly
- **Performance**: Create appropriate indexes and use projection for large datasets
- **Monitoring**: Track query performance and storage usage
- **Backup**: Implement regular backup and recovery testing

> **Note**: MCP functions are discoverable at runtime, so you don't need to memorize function signatures. The agent will automatically know what operations are available.

## 🔐 **Security Best Practices**

- **NEVER** commit credentials to source code
- **ALWAYS** use environment variables for sensitive data
- Keep `.env` file in `.gitignore`
- Use virtual environments for dependency isolation
- Rotate AWS credentials regularly
- Implement least-privilege access for MongoDB users

## 🏗️ **Project Structure**

```
mdb-bedrock-demo/
├── main.py              # Main application entry point
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (gitignored)
├── venv/                # Virtual environment (gitignored)
├── AGENTS.md            # This documentation
└── mcp_server/          # MongoDB MCP server (if separate)
```

## 🧪 **Testing & Development**

### Running the Demo
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Run the application
python main.py
```

### Testing MongoDB MCP Functions
```bash
# Test MongoDB connection
python -c "from config import MONGODB_CONNECTION_STRING; print('MongoDB config loaded')"

# Test specific MCP functions
python -c "
# Add your MCP function tests here
"
```

### Expected Output
The application will display:
1. ✅ Configuration validation
2. ✅ AWS client initialization
3. ✅ MongoDB connection verification
4. ✅ Query preparation
5. ✅ Agent invocation with MCP capabilities
6. ✅ Response processing

## 🚨 **Troubleshooting Common Issues**

### 1. AWS Credentials Not Found
```bash
# Check AWS configuration
aws configure list

# Verify credentials file exists
ls -la ~/.aws/credentials
```

### 2. Bedrock Agent Errors
- **`dependencyFailedException`**: Agent may need redeployment or has configuration issues
- **`AccessDeniedException`**: Check IAM permissions for Bedrock service
- **`ValidationException`**: Verify agent ID and alias ID are correct

### 3. MongoDB Connection Issues
```bash
# Test MongoDB connection
python -c "
import pymongo
from config import MONGODB_CONNECTION_STRING
try:
    client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
    client.admin.command('ping')
    print('MongoDB connection successful!')
except Exception as e:
    print(f'MongoDB connection failed: {e}')
"

# Check connection string format
echo $MONGODB_CONNECTION_STRING
```

### 4. Environment Variable Issues
```bash
# Test environment variable loading
python -c "from config import *; print(f'Agent ID: {AWS_BEDROCK_AGENT_ID}')"
python -c "from config import *; print(f'MongoDB URI: {MONGODB_CONNECTION_STRING[:20]}...')"
```

### 5. Dependency Issues
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt
pip install -r requirements.txt

# Check Python version compatibility
python --version
```

## 🔧 **Development Workflow**

### Adding New Features
1. Create feature branch
2. Update requirements.txt if adding new packages
3. Test in virtual environment
4. Update documentation
5. Submit pull request

### Adding New MCP Functions
1. Define function signature and parameters
2. Implement MongoDB operation logic
3. Add error handling and validation
4. Update documentation with examples
5. Test with various data scenarios

### Code Quality
- Use type hints where possible
- Follow PEP 8 style guidelines
- Add docstrings to functions
- Include error handling for all external calls
- Implement proper MongoDB connection management

## 📚 **Useful Commands**

### Environment Management
```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Recreate virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### AWS CLI Commands
```bash
# List Bedrock agents
aws bedrock-agent list-agents --region us-east-1

# Get agent details
aws bedrock-agent get-agent --agent-id YOUR_AGENT_ID --region us-east-1

# List agent aliases
aws bedrock-agent list-agent-aliases --agent-id YOUR_AGENT_ID --region us-east-1
```

### MongoDB Commands
```bash
# Connect to MongoDB shell
mongosh "mongodb+srv://USERNAME:PASSWORD@CLUSTER.REGION.mongodb.net/"

# List databases
show dbs

# Use specific database
use bedrock_db

# List collections
show test

# Sample query
db.your_collection.find().limit(5)
```

### Logging & Debugging
```bash
# Run with verbose logging
python main.py 2>&1 | tee debug.log

# Check AWS CloudTrail for API calls
aws logs describe-log-groups --log-group-name-prefix "/aws/bedrock"

# Monitor MongoDB operations
tail -f /var/log/mongodb/mongod.log
```

## 🎯 **Future Enhancements**

### Potential Features
- [ ] Support for multiple Bedrock agents
- [ ] Conversation history persistence in MongoDB
- [ ] Streaming response handling
- [ ] Advanced MongoDB aggregation templates
- [ ] Web interface for agent interaction
- [ ] Batch processing capabilities
- [ ] Real-time MongoDB change streams
- [ ] Automated data backup and recovery

### Performance Optimizations
- [ ] Connection pooling for AWS clients
- [ ] MongoDB connection pooling and optimization
- [ ] Async/await for concurrent requests
- [ ] Response caching with MongoDB
- [ ] Rate limiting and retry logic
- [ ] Query result caching
- [ ] Index optimization recommendations

### MCP Server Enhancements
- [ ] Additional MongoDB operations (bulk operations, transactions)
- [ ] Support for MongoDB Atlas specific features
- [ ] GraphQL-like query interface
- [ ] Real-time data streaming
- [ ] Advanced analytics functions
- [ ] Machine learning model integration

## 📞 **Support & Resources**

- **AWS Bedrock Documentation**: https://docs.aws.amazon.com/bedrock/
- **Boto3 Documentation**: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- **Python Virtual Environments**: https://docs.python.org/3/tutorial/venv.html
- **MongoDB Documentation**: https://docs.mongodb.com/
- **MongoDB Python Driver**: https://pymongo.readthedocs.io/
- **Model Context Protocol**: https://modelcontextprotocol.io/

## 🔄 **Version History**

- **v1.0.0**: Initial implementation with basic Bedrock agent integration
- **v1.1.0**: Added colorized output, improved error handling, and configuration management
- **v1.2.0**: Integrated MongoDB MCP server with comprehensive database operations
- **Future**: Enhanced logging, monitoring, multi-agent support, and advanced MCP capabilities