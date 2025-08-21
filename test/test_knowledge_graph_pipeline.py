from backend.chat.knowledge_graph_constructor.knowledge_graph_pipeline import KnowledgeGraphPipeline
import unittest
from backend.chat.text_transformer.neo4j_interactor import Neo4JInteractor


class TestKnowledgeGraphPipeline(unittest.TestCase):
    """
    A class for testing the KnowledgeGraphPipeline functionality.
    
    Author: Jonathan Farrand
    
    Requirements:
        - ollama running locally
        - neo4j database running locally
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment by creating an instance of KnowledgeGraphPipeline.
        """
        cls.neo4j_interactor = Neo4JInteractor()
        cls.knowledge_graph_pipeline = KnowledgeGraphPipeline(neo4j_interactor=cls.neo4j_interactor, chunk_length=300, overlap=100)
        cls.text = "Thank you for joining us today. To start off, could you tell me a bit about your current role and your work in biomedical research? " \
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
        
        cls.neo4j_interactor.clear_database()



    def test_storing_triples(self):
        """
        Test that triples are extracted correctly from the text.
        """

        self.knowledge_graph_pipeline.process_and_store_triples(self.text)
        data = self.neo4j_interactor.run_cypher_query("MATCH (n) RETURN n LIMIT 25")
        print(data)
        self.assertGreater(len(data), 0, "There should be at least one triple stored in the database.")
    
    @classmethod
    def tearDown(self):
        """
        Clean up the test environment by closing the Neo4j driver.
        """
        self.neo4j_interactor.clear_database()
        self.neo4j_interactor.close_driver()
        
        



