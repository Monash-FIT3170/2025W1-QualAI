import unittest

from backend.chat.text_transformer.text_pipeline import TextPipeline
from backend.chat.text_transformer.text_vectoriser import TextVectoriser
from chatbot import Chatbot
from backend.mongodb.DocumentStore import DocumentStore

class TestTextTransformer(unittest.TestCase):
    """ 
    A class for testing chat backend functionality.
    Integration testing between deepseek-r1 client and Neo4J interactor

    Author: Felix Chung   

    Requirements: 
        - Neo4j database running locally
        - ollama and webui running locally 
    """
    
    @classmethod
    def setUpClass(self):
        """
        Set up the test environment by vectorising and storing sample text, creating chat instance
        """
        # # Defines the path to the desired file, may have to change to suit your current mongo layout
        database = 'chat'
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

        # Create chat instance
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

    def test_request(self):
        """
        Test that the chat can process a request and return a response.
        """
        query_message = "Hi!"
        response = self.chatbot.chat_with_model(query_message)
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