import streamlit as st
import openai
from openai import OpenAI

# Load environment variables from .env file
api_key = st.secrets["api_key"]##open('openaiapikey.txt').read()##os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

#Initialize OpenAI client for the prompts
client = OpenAI(api_key=api_key)

@st.cache_data(show_spinner = '')
def translate_to_english(text, language):
    system_prompt = f"You are an assistant tasked to translate a text from {language} to English"

    main_prompt = f"""
        ###TASK###
        Translate the following text from {language.upper()} into ENGLISH\n
        - Output the translated text only \n
        
        ###TEXT###    
            '{text}'
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

@st.cache_data(show_spinner = '')
def translate_from_english(text, language):
    system_prompt = f"You are an assistant tasked to translate a text from English to {language}"

    main_prompt = f"""
        ###TASK###
        Translate the following text from ENGLISH into {language.upper()}:\n\n
        - Output the translated text only \n
        
        ###TEXT###    
            '{text}'
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
