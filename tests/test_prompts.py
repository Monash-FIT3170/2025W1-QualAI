import unittest

from src.chatbot.text_transformer.text_pipeline import TextPipeline
from src.chatbot.text_transformer.text_vectoriser import TextVectoriser
from src.chatbot.chat import Chatbot
from src.mongodb.py_client.document_store import DocumentStore 

class TestTextTransformer(unittest.TestCase):
    """ 
    A class for testing chatbot system prompts.
    Sets up testing enviorment, vectorises and stores sample text, and creates a chatbot instance.
    
    Author: Felix Chung   

    Requirements: 
        - Neo4j database running locally
        - ollama and webui running locally 
    """
    
    @classmethod
    def setUpClass(self):
        """
        Set up the test environment by vectorising and storing sample text, creating chatbot instance
        """
        # # Defines the path to the desired file, may have to change to suit your current mongo layout
        database = 'chatbot'
        collection_id = "files"
        self.fileIdentifier = "biomedical_interview"

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
        
        self.example_queries = [
            "What challenges did they face in their research?",
            "Summarise the text into 3 main points",
            "Identify the types of data the researcher commonly works with."
        ]

        # Create chatbot instance
        self.chatbot = Chatbot()

        text_converter = TextVectoriser()


        # Insert file data into Mongo database
        self.client = DocumentStore()
        db = self.client.get_database(database)
        self.collection = db.get_collection(collection_id)
        file = {"title" : self.fileIdentifier, "content" : text_content}
        try:
            self.collection.add_document(self.fileIdentifier, self.fileIdentifier, file)
        except KeyError:
            pass

        # Create pipeline
        pipeline = TextPipeline(mongodb=self.client, neo4jdb=self.chatbot.neoInteractor, vectoriser=text_converter)

        # # Process and store text
        pipeline.process_and_store_single_file(database, collection_id, self.fileIdentifier)

        # Get chunks for verification and removal
        chunks = text_converter.chunk_text(text_content)
        self.vectors = text_converter.embed_text(chunks)

    def test_zero_shot(self):
        """
        Test zero shot prompt
        """
        response = self.chatbot.chat(self.example_queries[0])
        print("zero shot: " + response)
        self.assertIsInstance(response, str, "Response should be a string.")
        self.assertGreater(len(response), 0, "Response should not be empty.")
        
    def test_one_shot(self):
        """
        Test zero shot prompt
        """
        self.chatbot.set_system_prompt("EXAMPLE: What are some challenges faced in the searched? Response: The key challenges faced in the research are {short brief sentence}")
                                    
        response = self.chatbot.chat(self.example_queries[0])
        print("oneshot: " + response)
        self.assertIsInstance(response, str, "Response should be a string.")
        self.assertGreater(len(response), 0, "Response should not be empty.")
        
    def test_system_prompting(self):
        """
        Test system prompting
        """
        self.chatbot.set_system_prompt("You are a helpful research assistant providing information based on information from an interview. Return short responses that get straight to the point")
        
        response = self.chatbot.chat(self.example_queries[0])
        print("system prompting: " + response)
        self.assertIsInstance(response, str, "Response should be a string.")
        self.assertGreater(len(response), 0, "Response should not be empty.")
        
    def test_role_prompting(self):
        """
        Test role prompting
        """
        self.chatbot.set_system_prompt("I want you to act as a pHd level research assistant. I will ask you a question about the text, and you will provide a short, concise answer based on the context, in a professional style.")
        
        response = self.chatbot.chat(self.example_queries[0])
        print("role prompting: " +response)
        self.assertIsInstance(response, str, "Response should be a string.")
        self.assertGreater(len(response), 0, "Response should not be empty.")

    @classmethod
    def tearDownClass(self):
        """
        Clean up the test environment by removing the test data from the database
        """
        # Deletes all vectors from neo4j for most recent text, creates a clean slate
        for vector_data in self.vectors:
            title = vector_data[0]
            vector = vector_data[1]
            self.chatbot.neoInteractor.remove_node_by_text(title)

        # Deletes the file from the mongo database
        self.collection.remove_document(self.fileIdentifier)

        # close connections 
        self.chatbot.close_connections()
        self.client.client().close()