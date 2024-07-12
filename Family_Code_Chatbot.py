import streamlit as st
import time
from utils.openai_articles import related_articles_answer
from utils.translators import translate_to_english, translate_from_english


# Initialize state variables
def init():
    if 'data' not in st.session_state:
        st.session_state.data = {
            'question': '', 
            'question_language': 'English',
            'answer_language': 'English',
        }

# Set data state
def save_data(data_name, data_value):
    st.session_state.data[data_name] = data_value

# Get data state
def get_saved_data(data_name):
    return st.session_state.data[data_name]

def get_index_selected(selected, options):
    
    if (selected is None) or (len(options) == 0) :
        return 0        
    else:
        try:
            return options.index(selected)
        except:
            return 0



language_options = ['English', 'Filipino']

def main():
    init()
    st.set_page_config(layout="wide")
    st.title('PAMiLYA (Philippine Family Law Chatbot)')
    q_col1, q_col2, q_col3, q_col4= st.columns([1, 1, 5,1])

    q_col1.markdown("<div style='padding-top:35px; text-align:right;font-size: 14px' > Question: </div>", unsafe_allow_html=True)
    question_language_temp = q_col2.selectbox('', language_options, key = 'q_language')
    question_temp = q_col3.text_input('', key = 'question')
    q_col4.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
    submit_question = q_col4.button('Enter', key = 'submit_question',type="primary", use_container_width=True)

    if submit_question:
        save_data('question_language', question_language_temp)
        save_data('question', question_temp)
    
    
        question = get_saved_data('question')
        question_language = get_saved_data('question_language')
        
        question_col1, question_col2, question_col3 = st.columns([0.5,7,0.5])
        question_col2.header(question)

        if question_language != 'English':
            question_english = translate_to_english(question, question_language)
        else:
            question_english = question
        related_articles_metadatas, related_articles_combined, answer = related_articles_answer(question_english)
        # st.write(related_articles_metadatas)
        
    
        @st.experimental_fragment()
        def answers_on_language(question,answer):
            a_language_col1, a_language_col2, a_language_col3 = st.columns([6,1,1])
            a_language_col2.markdown("<div style='padding-top:35px; text-align:right;font-size: 14px' >Answer Language: </div>", unsafe_allow_html=True)
            answer_language = a_language_col3.selectbox('', language_options, get_index_selected(question_language,language_options) ,key = 'answer_language')
            # a_language_col4.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
            # translate_answer = a_language_col4.button('Translate', key = 'translate_answer',type="secondary", use_container_width=True)

            if answer_language != 'English':
                answer_translated = translate_from_english(answer, answer_language)
                display_answer = answer_translated 
            else:
                display_answer = answer

            answer_col1, answer_col2, answer_col3 = st.columns([1,6,1])
            answer_col2.markdown(display_answer.replace('\n', '<br>'), unsafe_allow_html=True)
            save_data('answer_language', answer_language)


        answers_on_language(question,answer)

        @st.experimental_fragment()
        def related_articles_combined_on_language(related_articles_metadatas):  
            article_h_col1, article_h_col2, article_h_col3, article_h_col4 = st.columns([0.5,5.5,1,1])
            article_h_col2.header('\n\nLegal Basis:')
            #st.markdown('Articles From Family Code', unsafe_allow_html=True) 
            answer_col1, answer_col2, answer_col3 = st.columns([1,6,1])
            for m in related_articles_metadatas:
                article = m['article']
                display_article = article            
                answer_col2.markdown(display_article.replace('\n', '<br>'), unsafe_allow_html=True) 
        related_articles_combined_on_language(related_articles_metadatas)

        
        #     st.write(related_articles_combined)
        #     st.write(related_articles_metadatas)
        
if __name__ == '__main__':
    main()
    
