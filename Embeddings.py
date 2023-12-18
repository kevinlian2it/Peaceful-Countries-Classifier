import os
import pandas as pd
import chromadb
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()
path = os.environ.get("directory")

chroma_client = chromadb.Client()

# Create a collection in ChromaDB
collection_name = "articles_embeddings"
collection = chroma_client.get_or_create_collection(name=collection_name)

# Initialize the TextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Function to process CSV files in a directory
def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            country_code = filename[:2]  # Assuming the first two letters are the country code
            process_csv(file_path, country_code)

# Function to process a CSV file and add documents to ChromaDB
def process_csv(file_path, country_code):
    print('Initializing...')
    df = pd.read_csv(file_path, nrows=10)
    df['combined_text'] = df['article_text_Ngram_stopword_lemmatize']  # Replace with your text columns

    for index, row in df.iterrows():
        # Split text into smaller segments
        segments = text_splitter.split_text(row['combined_text'])

        # Generate embeddings for each segment and add to ChromaDB
        for segment in segments:

            # Add segment and its embedding to ChromaDB
            collection.add(
                documents=[segment],
                metadatas=[{
                    'article_id': row['article_id'],
                    'article_title': row['article_title'],
                    'publisher': row['publisher'],
                    'year': row['year'],
                    'Domestic': row['Domestic'],
                    'country_code': country_code
                }],
                ids=[f"{row['article_id']}-{index}"]  # Example of creating a unique ID for each segment
            )

    print('Processing complete.')

    print(collection.peek())
    print(collection.count())

# Path to the directory containing CSV files
directory_path = path

# Process all CSV files in the directory
# process_directory(directory_path)
process_csv(directory_path+'/TZ_domestic_Ngram_stopword_lematize.csv', 'TZ')
