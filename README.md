# AWS Bedrock + MongoDB Atlas Vector Search Demo

## 🚀 **Overview**

This project demonstrates how **AWS Bedrock** leverages **MongoDB Atlas Vector Search** to provide intelligent, context-aware responses by semantically searching through document chunks stored in MongoDB.

## 🧠 **How It Works**

### 1. **Document Processing & Embedding Generation**
When documents are uploaded to AWS Bedrock, the service:
- Breaks documents into semantic chunks
- Generates vector embeddings for each chunk using AI models
- Stores both the text content and vector embeddings in MongoDB

### 2. **Vector Search & Retrieval**
When a user asks a question:
- AWS Bedrock converts the question into a vector embedding
- MongoDB Atlas Vector Search finds the most semantically similar chunks
- Returns relevant context to generate an accurate response

### 3. **Response Generation**
Using the retrieved context, Bedrock generates a comprehensive, accurate answer that draws from the most relevant parts of your knowledge base.

## 📊 **Data Structure Example**

Here's an example chunk from your `bedrock_db.test` collection:

```json
{
  "_id": "57568c15-dffe-4b81-824d-7f83674d5b9d",
  "bedrock_metadata": {
    "source": "s3://bnewell-demo/bcnc-medicare-plain-and-simple-guide.pdf"
  },
  "bedrock_text_chunk": "Plain and Simple     How to Choose the Path That's Right for You     2025     Y0079_13294_C PA 12132024 U12125, 12/24Your Path to Medicare     As you approach the age of eligibility for Medicare, you'll want to be sure you're ready to make the choices that work best for you.     When it comes to Medicare coverage, there are basically two paths you can take: Original Medicare or Medicare Advantage.     Our goal is to make you feel confident and ready to choose the path that's right for you. That's why we created this guide. You'll find information on these two paths and the options each presents.     So, read on and learn more about the benefits Medicare has to offer you.     We're here to help! You'll see our contact information below. Feel free to contact us with any questions, big or small.     Contact Blue Cross and Blue Shield of North Carolina (Blue Cross NC)     Phone: 1-800-665-8037 (TTY: 711)     Hours: 7 days a week, 8 a.m. – 8 p.m.     Online: Medicare.BlueCrossNC.com     Or contact your Blue Cross NC Authorized Agent     Blue Cross NC Centers: Your one-stop place for all things Blue Cross NC – including answers to all your Medicare questions.",
  "embedding": [0.026905512437224388, -0.0051019806414842606, 0.027637634426355362, ...],
  "x-amz-bedrock-kb-data-source-id": "YBNEIKW7XF",
  "x-amz-bedrock-kb-document-page-number": 1,
  "x-amz-bedrock-kb-source-uri": "s3://bnewell-demo/bcnc-medicare-plain-and-simple-guide.pdf"
}
```

## 🔍 **Key Components**

### **Text Chunks**
- **Semantic Units**: Each chunk represents a meaningful piece of information
- **Context Preservation**: Chunks maintain semantic coherence
- **Source Tracking**: Links back to original documents and pages

### **Vector Embeddings**
- **1536-dimensional vectors**: High-dimensional representation of semantic meaning
- **Semantic Similarity**: Similar concepts have similar vector representations
- **Fast Retrieval**: Enables sub-second search across millions of chunks

### **Metadata**
- **Source Tracking**: S3 URI and document identification
- **Page Numbers**: Specific location within source documents
- **Data Source ID**: Bedrock knowledge base identifier

## 💡 **Real-World Example**

**User Question**: *"What are my Medicare options?"*

**Vector Search Process**:
1. Question converted to vector embedding
2. MongoDB Atlas Vector Search finds chunks with similar embeddings
3. Retrieves chunks about "Original Medicare vs Medicare Advantage"
4. Bedrock generates response using retrieved context

**Result**: Accurate, context-aware answer about Medicare paths, contact information, and available options.

## 🏗️ **Architecture Benefits**

### **Semantic Understanding**
- Goes beyond keyword matching
- Understands context and meaning
- Handles synonyms and related concepts

### **Scalability**
- MongoDB Atlas handles millions of chunks
- Vector search scales with data growth
- Real-time retrieval performance

### **Accuracy**
- Context-aware responses
- Source attribution
- Up-to-date information

## 🚀 **Getting Started**

1. **Setup Environment**: Follow the setup guide in `AGENTS.md`
2. **Test Connection**: Verify MongoDB and AWS Bedrock connectivity
3. **Run Demo**: Execute `python main.py` to test the integration

## 📚 **Additional Resources**

- **AGENTS.md**: Complete development and troubleshooting guide
- **MongoDB Atlas Vector Search**: [Documentation](https://docs.atlas.mongodb.com/atlas-search/)
- **AWS Bedrock**: [Documentation](https://docs.aws.amazon.com/bedrock/)

---

*This demo showcases the power of combining AWS Bedrock's AI capabilities with MongoDB Atlas Vector Search for intelligent, context-aware information retrieval.*
