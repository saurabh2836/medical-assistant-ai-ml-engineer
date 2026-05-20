from logger import logger

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        
        # 1. Invoke the chain using the standard modern dict input pattern
        result = chain.invoke({"input": user_input})
        
        # 2. Extract sources safely. 
        # Note: In your vector loading script, PyPDFLoader stores the file path 
        # inside the metadata dictionary under the key "source" (singular).
        sources = []
        if "context" in result:
            sources = [doc.metadata.get("source", "Unknown Source") for doc in result["context"]]
        
        # 3. Construct the clean response payload matching modern LangChain keys
        response = {
            "response": result.get("answer", "No answer generated."),
            "sources": list(set(sources))  # list(set(...)) removes duplicate source pages cleanly
        } 
        
        logger.debug(f"Chain response: {response}")
        return response

    except Exception as e:  # Fixed: changed 'expect' to 'except'
        logger.exception("Error in query_chain function")
        raise e             # Fixed: explicitly re-raise the exception object