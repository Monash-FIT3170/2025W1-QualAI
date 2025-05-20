import requests 
import re
from backend.config.config import JWS_KEY, API_URL, MONGO_URI

# main testing imports 
from .text_transformer.text_pipeline import TextPipeline
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .text_transformer.neo4j_interactor import Neo4JInteractor
from .text_transformer.text_vectoriser import TextVectoriser
from backend.mongodb.DocumentStore import DocumentStore


class DeepSeekClient: 
    """
    A class for interacting with the deepseek-r1 model via API
    Supports basic chat functionality and context injection

    :author: Felix Chung
    """

    def __init__(self):
        """
        Initializes the Chatbot class with API URL and JWS key
        """
        self.api_url = API_URL
        self.jws_key = JWS_KEY
        self.headers = {
            'Authorization': f'Bearer {JWS_KEY}',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def remove_think_blocks(text: str) -> str:
        """
        Removes all text enclosed in deepseek-r1 model's think blocks 

        :param text: the text to clean 

        :return: the cleaned text with think block removed
        """
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    def chat_with_model(self, message):
        """
        Sends a basic message to the model and returns the response.

        :param message: The message to send to the model.
        :return: The JSON response from the API.
        """
        headers = {
            'Authorization': f'Bearer {JWS_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "deepseek-r1:1.5b",
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
        response = requests.post(API_URL, headers=self.headers, json=data)
        reply = response.json()["choices"][0]["message"]["content"]
        reply = self.remove_think_blocks(reply) # Removing think blocks
        return reply 

    def chat_with_model_context_injection(self, context_text, message):
        """
        Sends a message to the model with additional context injected as a system message.

        :param context_text: The external context (e.g., from a document).
        :param message: The user’s question.
        :return: The JSON response from the API.
        """
        data = {
            "model": "deepseek-r1:1.5b",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a helpful research assistant that provides short, to the point answers. Answer questions using the following context: \n\n{context_text} \n\n The context ends here. \n\n Now, please answer the following question: "
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
        response = requests.post(API_URL, headers=self.headers, json=data)
        reply = response.json()["choices"][0]["message"]["content"]
        reply = self.remove_think_blocks(reply) # Removing think blocks
        return reply 
    
   
if __name__ == "__main__":
    # create chatbot instance
    Neo4JInteractor().clear_database()
    chatbot = DeepSeekClient()
    
    # # Defines the path to the desired file, may have to change to suit your current mongo layout
    database = 'chatbot'
    collection_id = "files"
    fileIdentifier = "biomedical_interview"

    # Text data to be saved and vectorised, generated using chatgpt
    text_content = "Thank you for joining us today. To start off, could you tell me a bit about your current role and your work in biomedical research? " \
    "Sure. I'm a biomedical data scientist working in a translational medicine lab. My focus is on analyzing high-throughput sequencing data, especially RNA-seq datasets, " \
    "to identify biomarkers for early-stage cancer detection. We work closely with both clinicians and molecular biologists to ensure our findings are biologically and clinically " \
    "meaningful. That sounds fascinating. What kind of data are you typically working with? Mostly genomic and transcriptomic data. So, we're dealing with large datasets from " \
    "next-generation sequencing platforms. These include raw fastq files, aligned BAM files, and gene express   ion matrices. Occasionally, we also integrate clinical metadata—like " \
    "patient age, sex, disease stage—to perform multi-dimensional analyses. How do you typically approach analyzing such complex data? It usually begins with quality " \
    "control—removing low-quality reads, checking for contamination, and ensuring that sequencing depth is adequate. Then we move into normalization, differential expression analysis, " \
    "and increasingly, machine learning techniques to classify samples or predict outcomes. We rely heavily on tools like DESeq2, edgeR, and more recently, random forests " \
    "and support vector machines. Have you encountered any challenges when it comes to data quality or reproducibility? Absolutely. One major challenge is batch effects, " \
    "especially when samples are processed at different times or across different facilities. These can introduce biases that obscure real biological signals. " \
    "Reproducibility is another concern. That's why we document our pipelines carefully using RMarkdown or Jupyter Notebooks, and we've started using containerization " \
    "tools like Docker to ensure consistent computing environments. How do you handle ethical concerns, especially when working with patient data? All our data is " \
    "de-identified before it reaches the analysis stage. We work under strict institutional review board (IRB) protocols, and access is limited to authorized team members. " \
    "We also make sure that any models we develop avoid biases—for example, we regularly test for fairness across different demographic subgroups. " \
    "Do you find that machine learning is improving outcomes in biomedical research? It has potential, yes, but it’s not a silver bullet. The results are only as good as the data. " \
    "If your training data is unbalanced or flawed, your model won’t generalize well. We use ML more as a tool to explore hypotheses and guide experimental " \
    "validation rather than as a standalone solution. Looking forward, what do you see as the most exciting developments in your field? I’d say the integration of " \
    "multi-omics data—combining genomics, proteomics, and metabolomics—is really promising. And with advances in single-cell sequencing, " \
    "we’re starting to get an unprecedented view into cellular heterogeneity, which could fundamentally change how we approach disease diagnostics and treatment. T" \
    "hank you. That’s incredibly insightful. Best of luck with your ongoing work! Thank you. It was a pleasure speaking with you."


    # Insert file data into Mongo database
    client = DocumentStore()
    db = client.get_database(database)
    collection = db.get_collection(collection_id)
    file = {"title" : fileIdentifier, "content" : text_content}
    try:
        collection.add_document(fileIdentifier, fileIdentifier, file)
    except KeyError:
        pass

    # Create pipeline
    pipeline = TextPipeline()

    # # Process and store text
    pipeline.process_and_store_single_file(database, collection_id, fileIdentifier)

    # Get chunks for verification and removal
    text_converter = TextVectoriser()
    chunks = text_converter.chunk_text(text_content)
    vectors = text_converter.embed_text(chunks)

    # Check that file was vectorised
    neoInteractor = Neo4JInteractor()
        
    query_message = "What kind of data files do you use?"
    # Text to search for 
    search_vector = text_converter.chunk_and_embed_text(query_message)[0][1]
        
    context = neoInteractor.search_text_chunk(search_vector)
    
    response = chatbot.chat_with_model_context_injection(context, query_message)

    print(response)
    
    #Deletes all vectors from neo4j for most recent text, creates a clean slate
    neoInteractor.clear_database()

    # Deletes the file from the mongo database
    collection.remove_document(fileIdentifier)