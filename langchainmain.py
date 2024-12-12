import os
import sys
import constants

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAi
from langchain.chat_models import ChatOpenAi

os.environ["OPENAI_API_KEY"] = constants.APIKEY

query = sys.argv[1]

loader = TextLoader('data.txt')
index = VectorstoreIndexCreator().from_loaders([loader])

print(index.query(query, llm=ChatOpenAi()))