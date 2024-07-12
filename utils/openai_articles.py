__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import openai
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
import re

# Load environment variables from .env file
api_key = st.secrets["api_key"] ##open('openaiapikey.txt').read()##os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

CHROMA_DATA_PATH = 'family_code'
COLLECTION_NAME = "family_code_embeddings"

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
def return_top_articles(user_input, _collection, n_results=1):
    query_result = collection.query(query_texts=[user_input], n_results=n_results)
    
    if not query_result['ids'] or not query_result['ids'][0]:
        print("No game found matching the query.")
        return None, None  # No results found

    #Get top Results
    top_result_ids = query_result['ids'][0]
    top_result_metadatas = query_result['metadatas'][0]
    top_result_documents = query_result['documents'][0]
    
    #Combine the Articles of top results
    top_articles_combined = ''
    for idx, d in enumerate(top_result_documents):
        d_split = d.split('Section')
        article = ' '.join(d_split[0:-1])
        top_result_metadatas[idx]['article'] = article
        top_articles_combined += f"\n\n{article}"

    
    return top_result_metadatas, top_articles_combined

@st.cache_data(show_spinner = '')
def extract_numbers(s):
    # Regular expression to find all numbers (integer or decimal)
    numbers = re.findall(r'\d+\.\d+|\d+', s)
    return [float(num) if '.' in num else int(num) for num in numbers]

@st.cache_data(show_spinner = '')
def articles_to_answer(user_input,top_articles_combined, top_article_numbers):
    system_prompt = 'You are an assistant tasked to determine which articles of Family Code of the Philippines can answer the question'

    main_prompt = f"""
    ###TASK###
    - Determine which the article numbers can answer the question 
    - Article Numbers must be listed in a comma-separated list. 
    - Example: Article 1, Article 2, Article 3
    - If not answerable output 'NOT ANSWERABLE'
    
    ###ARTICLES###
    {top_articles_combined}

    ###QUESTION###
    {user_input}
    """

    
    response = client.chat.completions.create(
        model='gpt-3.5-turbo', 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{main_prompt}"}
        ]
    )
    related_articles = response.choices[0].message.content


    try:   
        if related_articles == 'NOT ANSWERABLE':
            return []
        else:
            related_article_numbers = extract_numbers(related_articles)
            related_article_numbers = list(set(related_article_numbers).intersection(set(top_article_numbers)))
            return related_article_numbers
    except:
        return []


@st.cache_data(show_spinner = '')
def answer_the_question(user_input, related_articles_combined):
    system_prompt = "You are a chatbot that answers question regarding the articles. Your goal is to answer the queries concisely and simply, in layman’s terms."

    main_prompt = f"""
    ###ARTICLES###
    {related_articles_combined}

    ###QUESTION###
    {user_input}
    """

    response = client.chat.completions.create(
        model='gpt-3.5-turbo', 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{main_prompt}"}
        ]
    )
    answer = response.choices[0].message.content
    return answer

error_message = 'Apologies, but we cannot provide a response solely based on the Family Code of the Philippines.'
@st.cache_data(show_spinner = '')
def related_articles_answer(user_input):
    # print('TOP ARTICLES RELATED:')
    top_result_metadatas, top_articles_combined = return_top_articles(user_input, collection,5)
    # print(top_articles_combined)
    # print('-----------------\n')
    
    if top_result_metadatas:
        # print('WHICH OF THE TOP ARTICLE NUMBERS CAN ANSWER THE QUESTION')
        top_article_numbers = [m['article_number'] for m in top_result_metadatas]
        related_article_numbers = articles_to_answer(user_input,top_articles_combined, top_article_numbers)
        # print(related_article_numbers)
        # print('-----------------\n')
        #We can use the cohere ranking to do this
        if len(related_article_numbers)>0:
            related_articles_combined = ''
            related_articles_metadatas = []
            for m in top_result_metadatas:
                if m['article_number'] in related_article_numbers:
                    related_articles_combined += f"\n\n{m['article']}"
                    related_articles_metadatas += [m]

            print('TOP ARTICLES RELATED:')
            print(related_articles_combined)
            print('-----------------\n')
            answer = answer_the_question(user_input, related_articles_combined)
            print('ANSWER:')
            print(answer)
            return related_articles_metadatas, related_articles_combined, answer
            
        else:
            answer = error_message
            print(answer)
            return None, None, answer
    else:
        answer = error_message
        print(answer)
        return None, None, answer


# def related_articles_answer(user_input):
#     related_articles_metadatas = [{'article_number': 184, 'chapter': 'N/A', 'chapter_number': 0, 'section': 'N/A', 'section_number': 0, 'title': 'ADOPTION', 'title_number': 'TITLE VII', 'article': ' Article 184: The following persons may not adopt:\n(1) The guardian with respect to the ward prior to the approval of the final accounts rendered upon the termination of their guardianship relation;\n(2) Any person who has been convicted of a crime involving moral turpitude;\n(3) An alien, except:\n(a) A former Filipino citizen who seeks to adopt a relative by consanguinity;\n(b) One who seeks to adopt the legitimate child of his or her Filipino spouse; or\n(c) One who is married to a Filipino citizen and seeks to adopt jointly with his or her spouse a relative by consanguinity of the latter.\nAliens not included in the foregoing exceptions may adopt Filipino children in accordance with the rules on inter-country adoptions as may be provided by law. (28a, E. O. 91 and PD 603)\n'}, {'article_number': 188, 'chapter': 'N/A', 'chapter_number': 0, 'section': 'N/A', 'section_number': 0, 'title': 'ADOPTION', 'title_number': 'TITLE VII', 'article': " Article 188: The written consent of the following to the adoption shall be necessary:\n(1) The person to be adopted, if ten years of age or over,\n(2) The parents by nature of the child, the legal guardian, or the proper government instrumentality;\n(3) The legitimate and adopted children, ten years of age or over, of the adopting parent or parents;\n(4) The illegitimate children, ten years of age or over, of the adopting parent, if living with said parent and the latter's spouse, if any; and\n(5) The spouse, if any, of the person adopting or to be adopted. (31a, E. O. 91 and PD 603)\n"}, {'article_number': 187, 'chapter': 'N/A', 'chapter_number': 0, 'section': 'N/A', 'section_number': 0, 'title': 'ADOPTION', 'title_number': 'TITLE VII', 'article': ' Article 187: The following may not be adopted:\n(1) A person of legal age, unless he or she is a child by nature of the adopter or his or her spouse, or, prior to the adoption, said person has been consistently considered and treated by the adopter as his or her own child during minority.\n(2) An alien with whose government the Republic of the Philippines has no diplomatic relations; and\n(3) A person who has already been adopted unless such adoption has been previously revoked or rescinded. (30a, E. O. 91 and PD 603)\n'}, {'article_number': 183, 'chapter': 'N/A', 'chapter_number': 0, 'section': 'N/A', 'section_number': 0, 'title': 'ADOPTION', 'title_number': 'TITLE VII', 'article': ' Article 183: A person of age and in possession of full civil capacity and legal rights may adopt, provided he is in a position to support and care for his children, legitimate or illegitimate, in keeping with the means of the family.\nOnly minors may be adopted, except in the cases when the adoption of a person of majority age is allowed in this Title.\nIn addition, the adopter must be at least sixteen years older than the person to be adopted, unless the adopter is the parent by nature of the adopted, or is the spouse of the legitimate parent of the person to be adopted. (27a, E. O. 91 and PD 603)\n'}, {'article_number': 189, 'chapter': 'N/A', 'chapter_number': 0, 'section': 'N/A', 'section_number': 0, 'title': 'ADOPTION', 'title_number': 'TITLE VII', 'article': ' Article 189: Adoption shall have the following effects:\n(1) For civil purposes, the adopted shall be deemed to be a legitimate child of the adopters and both shall acquire the reciprocal rights and obligations arising from the relationship of parent and child, including the right of the adopted to use the surname of the adopters;\n(2) The parental authority of the parents by nature over the adopted shall terminate and be vested in the adopters, except that if the adopter is the spouse of the parent by nature of the adopted, parental authority over the adopted shall be exercised jointly by both spouses; and\n(3) The adopted shall remain an intestate heir of his parents and other blood relatives. (39(1)a, (3)a, PD 603)\n'}]
    
    
#     related_articles_combined = """
    
    
#      Article 184: The following persons may not adopt:
#     (1) The guardian with respect to the ward prior to the approval of the final accounts rendered upon the termination of their guardianship relation;
#     (2) Any person who has been convicted of a crime involving moral turpitude;
#     (3) An alien, except:
#     (a) A former Filipino citizen who seeks to adopt a relative by consanguinity;
#     (b) One who seeks to adopt the legitimate child of his or her Filipino spouse; or
#     (c) One who is married to a Filipino citizen and seeks to adopt jointly with his or her spouse a relative by consanguinity of the latter.
#     Aliens not included in the foregoing exceptions may adopt Filipino children in accordance with the rules on inter-country adoptions as may be provided by law. (28a, E. O. 91 and PD 603)
    
    
#      Article 188: The written consent of the following to the adoption shall be necessary:
#     (1) The person to be adopted, if ten years of age or over,
#     (2) The parents by nature of the child, the legal guardian, or the proper government instrumentality;
#     (3) The legitimate and adopted children, ten years of age or over, of the adopting parent or parents;
#     (4) The illegitimate children, ten years of age or over, of the adopting parent, if living with said parent and the latter's spouse, if any; and
#     (5) The spouse, if any, of the person adopting or to be adopted. (31a, E. O. 91 and PD 603)
    
    
#      Article 187: The following may not be adopted:
#     (1) A person of legal age, unless he or she is a child by nature of the adopter or his or her spouse, or, prior to the adoption, said person has been consistently considered and treated by the adopter as his or her own child during minority.
#     (2) An alien with whose government the Republic of the Philippines has no diplomatic relations; and
#     (3) A person who has already been adopted unless such adoption has been previously revoked or rescinded. (30a, E. O. 91 and PD 603)
    
    
#      Article 183: A person of age and in possession of full civil capacity and legal rights may adopt, provided he is in a position to support and care for his children, legitimate or illegitimate, in keeping with the means of the family.
#     Only minors may be adopted, except in the cases when the adoption of a person of majority age is allowed in this Title.
#     In addition, the adopter must be at least sixteen years older than the person to be adopted, unless the adopter is the parent by nature of the adopted, or is the spouse of the legitimate parent of the person to be adopted. (27a, E. O. 91 and PD 603)
    
    
#      Article 189: Adoption shall have the following effects:
#     (1) For civil purposes, the adopted shall be deemed to be a legitimate child of the adopters and both shall acquire the reciprocal rights and obligations arising from the relationship of parent and child, including the right of the adopted to use the surname of the adopters;
#     (2) The parental authority of the parents by nature over the adopted shall terminate and be vested in the adopters, except that if the adopter is the spouse of the parent by nature of the adopted, parental authority over the adopted shall be exercised jointly by both spouses; and
#     (3) The adopted shall remain an intestate heir of his parents and other blood relatives. (39(1)a, (3)a, PD 603)
#     """
    

#     answer = """
#     To adopt a child in the Philippines as a non-biological parent, you generally need to:
#     1. Make sure you are qualified to adopt, meaning you are of legal age, able to support the child, and meet other specific criteria outlined in the law.
#     2. Obtain written consent from various parties, such as the child to be adopted (if 10 years old or older), the child's parents or legal guardian, the current children of the adopting parent if they are 10 years old or older, and the spouse of the adopting parent if applicable.
#     3. Ensure you are not disqualified from adopting, such as being convicted of a crime involving moral turpitude or falling under certain other prohibited categories like a person of legal age or an alien with whom the Philippines has no diplomatic relations.
#     4. Follow the rules on inter-country adoptions if you are an alien not falling under specific exceptions like former Filipino citizens or spouses of Filipino citizens.
#     5. Understand that through adoption, the child will be considered as your legitimate child with reciprocal rights and obligations, your parental authority will replace that of the child's biological parents, and the child will have inheritance rights similar to biological children. 
#     """

#     return related_articles_metadatas, related_articles_combined, answer
