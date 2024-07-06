import chromadb
from chromadb.utils import embedding_functions

import os
import pathlib
import hashlib

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)))
CHROMA_PATH = os.path.join(DEFAULT_PATH, "chroma")
WORDLIST_PATH = os.path.join(DEFAULT_PATH, "wordlists")


from openai import OpenAI

class ChromaStorage:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.chroma_ef = embedding_functions.DefaultEmbeddingFunction()
        # following embedin function uses openai
        #self.chroma_ef = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-3-small")
        self.chroma_collection = self.chroma_client.get_or_create_collection(name="Passwords", embedding_function=self.chroma_ef)
        self.init_wordlists()

    def init_wordlists(self):
        print("chroma_storage: initiating chromadb collection")
        files = os.listdir(WORDLIST_PATH)
        print("chroma_storage: loading wordlists: " + ", ".join(files))
        for file in files:
            print("chroma_storage: loading wordlist: " + file)

            if (len(self.chroma_collection.get(where={"source": file})["ids"]) == 0):
                print("chroma_storage: adding wordlist: " + file)

                content = pathlib.Path(os.path.join(WORDLIST_PATH, file)).read_text(encoding="latin1")
                content = content.replace("\n", " ")
                self.chroma_collection.add(
                    # use hash of filename as id
                    ids=[str(hash(file))],
                    metadatas=[{"source": file}],
                    documents=[content]
                    )

        print("chroma_storage: all wordlists added")

    def search(self, password):
        print("chromadb: query for password: " + password)
        #result = self.chroma_collection.query(
        #    query_texts=["Do any of the documents contain the exact string:" + password]
        #)
        #result = self.chroma_collection.query(
        #    query_embeddings=embeddings["embeddings"],
        #    where_document={"$contains": password}
        #)
        documents = self.chroma_collection.get(include=["documents"])
        #print(documents["documents"][0])
        #result = self.chroma_collection.query(
        #    n_results=10,
        #    query_texts=["Does this exact string exist:" + password]
        #)
        #print(result["ids"])
        #print(result["metadatas"])
        for document in documents["documents"]:
            if str(password) in str(document):
                print("chromadb: password found in wordlist")
                return True

        return False
