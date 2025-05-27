import spacy
from torch import Tensor
from sentence_transformers import SentenceTransformer

class TextVectoriser:
    """
    A class for converting files and text to vectors

    :author: Jonathan Farrand
    """
    def __init__(self, chunker_name: str = "en_core_web_sm", model_name: str = "all-MiniLM-L6-v2"):
        """
            Initializes the TextVectoriser class with the chunker name and the model name. 
            Creates variables to store whether the chunker and sentence transformer model have already been used.

            :param chunker_name: the name of the chunker model being used
            :param model_name: the type of LLM being used
        """
        self._chunker = spacy.load(chunker_name)
        self._model = SentenceTransformer(model_name)
    
    def chunk_text(self, text:str, max_length: int = 200, overlap: int = 50) -> list[str]:
        """
            Chunks the text into semanitcally meaningful divisions, with a maxium given length. 
            Gives overlap between chunks to ensure provide further context to the model
            
            :param str text: the text to be chunked
            :param int max_length: the maximum length of each chunk
            :param int overlap: the number of tokens to overlap between chunks
            
            :return list[str]: a list containing the chunks processed from the text
        """
        chunker = self._chunker
        doc = chunker(text)

        tokens = [token.text_with_ws for token in doc]
        chunks = []
        start = 0

        while start < len(tokens):
            end = start + max_length
            chunk_tokens = tokens[start:end]
            chunk_text = "".join(chunk_tokens).strip()
            chunks.append(chunk_text)

            # Shift start index back by overlap to include previous context
            start = end - overlap if end - overlap > start else end 

        return chunks

    def embed_text(self, chunks: list[str]) -> list[tuple[str, list[Tensor]]]:
        """
            Generates a vector embedding for each of the provided chunks of text using a sentence transformer model.

            :param list[str] chunks:    the list of chunks

            :return list[tuple[str, list[Tensor]]]:  a list of tuples containing chunks and corresponding embeddings
        """
        model = self._model
        embeddings = model.encode(chunks)
        return list(zip(chunks, embeddings))


    def chunk_and_embed_text(self, text: str) -> list[tuple[str, list[Tensor]]]:
        """
            Chunks text and generates a vector embedding for each chunk. See #chunk_text and #embed_chunks.
        """
        return self.embed_text(self.chunk_text(text))
    
if __name__ == "__main__":
    # Example usage
    vectoriser = TextVectoriser()
    text = "Thank you for joining us today. To start off, could you tell me a bit about your current role and your work in biomedical research? " \
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
    chunks = vectoriser.chunk_and_embed_text(text)
    for chunk in chunks:
        print(f"Chunk: {chunk}")