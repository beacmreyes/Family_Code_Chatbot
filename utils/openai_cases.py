import streamlit as st
import openai
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
import re

# Load environment variables from .env file
api_key = st.secrets["api_key"] #open('openaiapikey.txt').read()##os.getenv('OPENAI_API_KEY')#  
openai.api_key = api_key

CHROMA_DATA_PATH = 'family_code_cases'
COLLECTION_NAME = "family_code_case_embeddings"

# Initialize ChromaDB client
client_chromadb = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=openai.api_key, model_name="text-embedding-ada-002")

# Create or get the collection
collection = client_chromadb.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=openai_ef,
    metadata={"hnsw:space": "cosine"}
)

#Initialize OpenAI client for the prompts
client = OpenAI(api_key=api_key)


@st.cache_data(show_spinner = '')
def return_top_cases(user_input, n_results=1):

    query_result = collection.query(query_texts=[user_input], n_results=n_results)
    
    if not query_result['ids'] or not query_result['ids'][0]:
        return None  # No results found

    #Get top Results
    top_result_ids = query_result['ids'][0]
    top_result_metadatas = query_result['metadatas'][0]
    top_result_documents = query_result['documents'][0]
        
    return top_result_metadatas

 #    return [{'GR': 'G.R. No. 173540, SECOND DIVISION, January 22, 2014, PEREZ , J.',
 #  'summary': 'In Adong v. Cheong Seng Gee, the Court elucidated on the rationale behind the presumption of marriage: The basis of human society throughout the civilized world is that of marriage. Marriage in this jurisdiction is not only a civil contract, but it is a new relation, an institution in the maintenance of which the public is deeply interested. Consequently, every intendment of the law leans toward legalizing matrimony. Persons dwelling together in apparent  matrimony are presumed, in the absence of any counter -presumption or evidence special to the case, to be in fact married. The reason is that such is the common order of society, and if the parties were not what they thus hold themselves out as being, they would be living in the constant violation of decency and of law. A presumption established by our Code of Civil Procedure is that a man and a woman deporting themselves as husband and wife have entered into a lawful contract of marriage. (Sec. 334, No. 28 ) Semper praesumitur pro matrimonio  Always presume marriage. Here, the establishment of the fact of marriage between Tecla and Eustaquio was completed by the testimonies of the witnesses; the unrebutted fact of the birth within the cohabitation of Tecla  and Eustaquio of four (4) children coupled with the certificates of the childrens birth and baptism; and the certifications of marriage issued by the parish priest.',
 #  'title': 'PEREGRINA MACUA VDA. DE AVENIDO, petitioner , -versus - TECLA HOYBIA AVENIDO, respondent.',
 #  'topic': 'MARRIAGE'},
 # {'GR': 'G.R. No. 139789, FIRST DIVISION, May 12, 2000, PARDO, J.',
 #  'summary': '',
 #  'title': 'ERLINDA ILUSORIO K. ILUSORIO Petitioner, -versus - SYLVIA K. ILUSORIO, JOHN DOE AND JANE DOE, Respondents.',
 #  'topic': 'RIGHTS AND OBLIGATIONS BETWEEN HUSBAND & WIFE:'},
 # {'GR': 'G.R. No. 135216, THIRD DIVISION, August 19, 1999, PANGANIBAN , J.',
 #  'summary': 'The prima facie presumption is that a man and a woman deporting themselves as husband and wife have entered into a lawful contract of marriage. Here, given the  undisputed, even accepted, fact that Dr. Jacob and petitioner lived together as husband and wife, the Court finds that the presumption of marriage was not rebutted in this case.',
 #  'title': 'TOMASA VDA. DE JACOB, as Special Administratrix of the Intestate Estate of Deceased Alfredo E. Jacob, petitioner , -versus - COURT OF APPEALS, PEDRO PILAPIL, THE REGISTER OF DEEDS for the Province of Camarines Sur, and JUAN F. TRIVINO as publish er of Balalong, respondents.',
 #  'topic': 'MARRIAGE'},
 # {'GR': 'G.R. No. 103047, SECOND DIVISION, September 2, 1994, PUNO , J.',
 #  'summary': 'At the time the subject marriage was solemnized on June 24, 1970, the law governing marital relations was the New Civil Code. The law provides that no  marriage shall be solemnized without a marriage license first issued by a local civil registrar. Being one of the essential requisites of a valid marriage, absence of a license would render the marriage void ab initio. Here, the Court held that, under the circumstances of the case, the documentary and testimonial evidence presented by private respondent Castro sufficiently established the absence of the subject marriage license.',
 #  'title': 'REPUBLIC OF THE PHILIPPINES, petitioner , -versus - COURT OF AP PEALS AND ANGELINA M. CASTRO, respondents.',
 #  'topic': 'MARRIAGE'},
 # {'GR': 'G.R. No. 191936, THIRD DIVISION, June 1, 2016, REYES , J.',
 #  'summary': 'Jurisprudence teaches that the fact of marriage may be proven by relevant evidence other than the marriag e certificate. Hence, even a persons birth certificate may be recognized as competent evidence of the marriage between his parents. Here, in order to prove their legitimate filiation, the respondents presented their respective Certificates of Live Birth i ssued by the National Statistics Office where Fidela signed as the Informant in item no. 17 of both documents.',
 #  'title': 'VIRGINIA D. CALIMAG, petitioner , -versus - HEIRS OF SILVESTRA N. MACAPAZ, represented by ANASTACIO P. MACAPAZ, JR., respondents.',
 #  'topic': 'MARRIAGE'}]