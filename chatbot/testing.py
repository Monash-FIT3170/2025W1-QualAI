from text_transformer.text_pipeline import TextPipeline
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from text_transformer.neo4j_interactor import Neo4JInteractor
from text_transformer.text_vectoriser import TextVectoriser

from config import MONGO_URI

# Defines the path to the desired file, may have to change to suit your current mongo layout
database = 'chatbot'
collection_id = "files"
fileIdentifier = "biomedical_interview"

# Text data to be saved and vectorised, generated using chatgpt
text_content = "Thank you for joining us today. To start off, could you tell me a bit about your current role and your work in biomedical research? " \
"Sure. I'm a biomedical data scientist working in a translational medicine lab. My focus is on analyzing high-throughput sequencing data, especially RNA-seq datasets, " \
"to identify biomarkers for early-stage cancer detection. We work closely with both clinicians and molecular biologists to ensure our findings are biologically and clinically " \
"meaningful. That sounds fascinating. What kind of data are you typically working with? Mostly genomic and transcriptomic data. So, we're dealing with large datasets from " \
"next-generation sequencing platforms. These include raw fastq files, aligned BAM files, and gene expression matrices. Occasionally, we also integrate clinical metadata—like " \
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
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client[database]
collection = db[collection_id]
collection.insert_one({"title" : fileIdentifier, "content" : text_content})

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

# Text to search for 
search_text = vectors[0][0]
search_vector = text_converter.chunk_and_embed_text(search_text)[0][1]
print(search_vector)
print(neoInteractor.search(search_vector))

# Deletes all vectors from neo4j for most recent text, creates a clean slate
for vector_data in vectors:
    title = vector_data[0]
    vector = vector_data[1]
    neoInteractor.remove_node_by_name(title)

# Deletes the file from the mongo database
collection.delete_one({"title" : fileIdentifier})

# Other functions
# MATCH (e:Embedding) RETURN e.name, e.vector LIMIT 100; : Run in cypher NEO4J localhost terminal, returns 100 vectors
# MATCH (e:Embedding) DELETE e; Deletes all vectors in NEO4J

