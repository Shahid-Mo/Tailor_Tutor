from typing import List, Dict, Union, Literal
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AnswerGenerator:
    def __init__(
        self, 
        openai_api_key: str, 
        groq_api_key: str,  
        provider: Literal["openai", "groq"] = "groq"
    ):
        """
        Initialize the AnswerGenerator with support for both OpenAI and Groq.
        
        Args:
            openai_api_key: OpenAI API key
            groq_api_key: Groq API key
            model: Model name to use
            provider: Which provider to use ("openai" or "groq")
        """
        self.provider = provider
        
        # Initialize both LLMs
        self.llm_openai = ChatOpenAI(
            openai_api_key=openai_api_key,
            model='gpt-4o-mini',
            temperature=0
        )
        
        self.llm_groq = ChatGroq(
            groq_api_key=groq_api_key,
            model="llama-3.3-70b-versatile",  # Groq supports various models including "mixtral-8x7b-32768"
            temperature=0
        )
        
        # Select the active LLM based on provider
        self.llm = self.llm_groq if provider == "groq" else self.llm_openai
        
        # Define the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI tutor. Answer questions based on the provided context. "
                      "If you cannot answer based on the given context, explicitly say so."),
            ("user", """
Here are the relevant contexts:
{contexts}

Question: {question}

Please provide an answer based solely on the above contexts.
""")
        ])
        
        # Create the chain
        self.chain = (
            {
                "contexts": self._format_contexts, 
                "question": RunnablePassthrough()
            }
            | self.prompt 
            | self.llm 
            | StrOutputParser()
        )

    def _format_contexts(self, contexts: List[Union[str, Dict]]) -> str:
        """
        Format the contexts into a string.
        
        Args:
            contexts: List of either strings or dictionaries containing context information
            
        Returns:
            Formatted string of all contexts
        """
        formatted_contexts = []
        for i, ctx in enumerate(contexts, 1):
            if isinstance(ctx, dict):
                # If context is a dictionary, extract text
                text = ctx.get('text', '')
            else:
                # If context is a string, use it directly
                text = str(ctx)
            formatted_contexts.append(f"Context {i}:\n{text}\n")
        return "\n".join(formatted_contexts)

    def switch_provider(self, provider: Literal["openai", "groq"]):
        """
        Switch between OpenAI and Groq providers.
        
        Args:
            provider: The provider to switch to ("openai" or "groq")
        """
        if provider not in ["openai", "groq"]:
            raise ValueError("Provider must be either 'openai' or 'groq'")
        
        self.provider = provider
        self.llm = self.llm_groq if provider == "groq" else self.llm_openai
        
        # Recreate the chain with the new LLM
        self.chain = (
            {
                "contexts": self._format_contexts, 
                "question": RunnablePassthrough()
            }
            | self.prompt 
            | self.llm 
            | StrOutputParser()
        )

    async def generate_answer(self, question: str, contexts: List[Union[str, Dict]]) -> Dict:
        """
        Generate an answer using retrieved contexts with LangChain.
        
        Args:
            question: The user's question
            contexts: List of context strings or dictionaries with 'text' and 'source' keys
            
        Returns:
            Dict containing the answer and source documents
        """
        try:
            # Invoke the chain with a single input dictionary
            answer = await self.chain.ainvoke({
                "question": question,
                "contexts": contexts
            })
            
            # Extract sources if available
            sources = []
            for ctx in contexts:
                if isinstance(ctx, dict) and 'source' in ctx:
                    sources.append(ctx['source'])
            
            return {
                "answer": answer,
                "sources": sources,
                "provider": self.provider
            }

        except Exception as e:
            logger.error(f"Error generating answer with {self.provider}: {e}")
            raise
