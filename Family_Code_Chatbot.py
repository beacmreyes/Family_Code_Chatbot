import streamlit as st
import time
from utils.openai_articles import related_articles_answer
from utils.openai_cases import return_top_cases
from utils.translators import translate_to_english, translate_from_english
from utils.home_page import page_details

# Initialize state variables
def init():
    if 'data' not in st.session_state:
        st.session_state.data = {
            'question': '', 
            'home_translate_filipino': False,
            'answer_translate_filipino': False,
            'question_language': 'English',
            # 'answer_language': 'English',
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

@st.experimental_fragment()
def answers_on_language(question,answer, question_language):
    # a_language_col3.markdown("<div style='padding-top:35px; text-align:right;font-size: 14px' >Answer Language: </div>", unsafe_allow_html=True)
    # answer_language = a_language_col3.selectbox('', language_options, get_index_selected(question_language,language_options) ,key = 'answer_language')
    # a_language_col4.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
    # translate_answer = a_language_col4.button('Translate', key = 'translate_answer',type="secondary", use_container_width=True)
    ans_lang_col1, ans_lang_col2= st.columns([6,3])
    language_bool =  {'Filipino': True,
                      'English': False
                     }
    translate_answer_to_filipino = ans_lang_col2.toggle('Translate to Filipino', value= language_bool[question_language])
    if translate_answer_to_filipino:
        answer_language = 'Filipino'
    else:
        answer_language = 'English'
            
    if answer_language != 'English':
        answer_translated = translate_from_english(answer, answer_language)
        display_answer = answer_translated 
    else:
        display_answer = answer

    st.markdown(display_answer.replace('\n', '<br>'), unsafe_allow_html=True)
    save_data('answer_language', answer_language)


                
def main():
    init()
    st.set_page_config(layout="wide")

    my_page = st.sidebar.radio('Page Navigation',
                           ['Home', 'PAMiLYA (Philippine Family Law Chatbot)'])



    if my_page == 'Home':
        
        home_col1, home_col2= st.columns([6,3])
        translate_to_filipino = home_col2.toggle('Translate to Filipino', value= get_saved_data('home_translate_filipino'))
        if translate_to_filipino:
            page_language =  'Filipino'
        else:
            page_language = 'English'
        pages = page_details(page_language)
        st.title(pages[page_language]["title"])
        st.header(pages[page_language]["about"])
        st.write(pages[page_language]["description"])
        st.header(pages[page_language]["how_to"])
        st.write(pages[page_language]["how_to_use"])
        st.header(pages[page_language]["limitations_header"])
        st.write(pages[page_language]["limitations"])
        st.markdown("---")
        st.write('Citations')
        st.caption(pages[page_language]["citations"])


    else:
        st.title('PAMiLYA (Philippine Family Law Chatbot)')
        q_col1, q_col2, q_col3, q_col4= st.columns([1, 2, 5,1])
    
        q_col1.markdown("<div style='padding-top:35px; text-align:right;font-size: 14px' > Question: </div>", unsafe_allow_html=True)
        question_language_temp = q_col2.selectbox('', language_options, key = 'q_language')
        question_temp = q_col3.text_input('', key = 'question')
        q_col4.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
        submit_question = q_col4.button('Enter', key = 'submit_question',type="primary", use_container_width=True)
    
        if submit_question and (len(question_temp.strip())>0):
            save_data('question_language', question_language_temp)
            save_data('question', question_temp)
        
        
            question = get_saved_data('question')
            question_language = get_saved_data('question_language')
            
            st.header(question)
    
            if question_language != 'English':
                question_english = translate_to_english(question, question_language)
            else:
                question_english = question
            related_articles_metadatas, related_articles_combined, answer = related_articles_answer(question_english)
            # st.write(related_articles_metadatas)
            
        
    
            answers_on_language(question,answer, question_language)
    
            if related_articles_metadatas:
                st.header('\n\nLegal Basis:')
                #st.markdown('Articles From Family Code', unsafe_allow_html=True) 
                # st.write(related_articles_metadatas)
                article_col1, article_col2= st.columns([1, 40])
                for m in related_articles_metadatas:
                    
                    article_text = m['article'].split(':')
                    article_text = ':'.join(article_text[1:]).replace('\n', '<br>')
                    article_html = f"""
                        - <span style="font-size: 15px"><strong>ARTICLE {m['article_number']}:</strong>{article_text}</span>
                        """
                    article_col2.markdown(article_html, unsafe_allow_html=True) 
    
            if related_articles_metadatas:
                top_cases = return_top_cases(question_english,5)
                if top_cases:
                    st.header('\n\nRelated Cases:')
                    #st.markdown('Articles From Family Code', unsafe_allow_html=True) 
                    case_col1, case_col2= st.columns([1, 40])
                    for c in top_cases:    
                        case_html = f"""
                        - <span style="font-size: 15px"><strong style="font-size: 16px">{c['title']}</strong>
                          </br>{c['GR']}</span>
                        
                        """
                        
                        case_col2.markdown(case_html, unsafe_allow_html=True) 
                                
        
if __name__ == '__main__':
    main()
    
