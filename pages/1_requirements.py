import streamlit as st
import pandas as pd

from streamlit_text_label import label_select

# Constants
DIGITAL_DIMENSIONS = {
    "Process Automation": "Process Automation",
    "Data": "Data",
    "Digital Solutions": "Digital Solutions",
    "Digital Public Services": "Digital Public Services"
}

HIGH_LEVEL_PROCESSES = ["Process A", "Process B", "Process C", "Process D"]

# Initialize session state variables
def initialize_state():
    if 'annotations' not in st.session_state:
        st.session_state['annotations'] = []
    if 'current_article_index' not in st.session_state:
        st.session_state.current_article_index = 0

# Display article information
def display_article(uploaded_data, article_index):
    articles = uploaded_data['content']['articles']
    current_article = articles[article_index]
    st.write(f"{current_article['num']}: {current_article['heading']}")
    st.sidebar.write(f"{current_article['num']}: {current_article['heading']}")

    text = [child['text'] for child in current_article['children']]
    text = "\n\n".join(text)

    st.markdown(text)

    #actors = []
    #selections = label_select(body=str(text), labels=["Actor"])#, "Digital Solution"])
    
    #for selection in selections:        
    #    if selection.labels[0] == 'Actor':
    #        text = selection.text
    #        actors.append(text)
    
    #return actors

# Display multiselect input with session state management
def display_multiselect(options, key, label):
    return st.multiselect(label, options)

# Handle user annotations on the article or child
def handle_annotations(article_eId,  index=0, actors=None):
    dimension_values = [
        st.checkbox(dim, key=f"{dim}-{article_eId}")
        for dim in DIGITAL_DIMENSIONS
    ]
    
    # Check if at least one checkbox is ticked
    if any(dimension_values):
        checked_dimensions = [dim for dim, checked in zip(DIGITAL_DIMENSIONS, dimension_values) if checked]
        
        # Initialize an empty list to store the affected processes
        #if 'affected_processes' not in st.session_state:
        #    st.session_state.affected_processes = []
#
        ## Create a text input for the user to enter a label
        #label_input = st.text_input("Enter the high-level processes affected by the requirement")
#
        ## Create a button to add the label to the list
        #if st.button("Add process"):
        #    st.session_state.affected_processes.append(label_input)
        #    label_input = ""  # Clear the text input after adding the label
#
        ## Display the list of labels
        #st.write("Labels:")
        #for i, label in enumerate(st.session_state.affected_processes):
        #    st.write(f"{i+1}. {label}")
            
        fragment_annotations = {            
                'Reference': article_eId,
                #'Actors': actors,
                #'High-level Processes': st.session_state.affected_processes,
                'Digital Dimensions': checked_dimensions
            }
    else:
        fragment_annotations = {
                'Reference': article_eId,
                #'Description': None,
                #'Actors': None,
                #'High-level Processes': None,
                'Digital Dimensions': None

            }
            
    if st.button("Save annotation"):
        if index < len(st.session_state['annotations']):
            st.session_state['annotations'][index] = fragment_annotations
        else:
            st.session_state['annotations'].extend([None] * (index - len(st.session_state['annotations']) + 1))
            st.session_state['annotations'][index] = fragment_annotations

    if st.button(label="Delete annotations"):
        if 'annotations' in st.session_state:
            st.session_state['annotations'] = [annotation for annotation in st.session_state['annotations'] if annotation is None or annotation['Reference'] != article_eId]

# Display navigation controls for articles and children
def display_navigation_controls(article_index, max_articles, position):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous article", key=f"prev-article-{position}"):
            st.session_state.current_article_index = max(0, article_index - 1)
            st.session_state.affected_processes = []


    with col2:
        if st.button("Next article", key=f"next-article-{position}"):
            st.session_state.current_article_index = min(max_articles - 1, article_index + 1)
            st.session_state.affected_processes = []


# Display the binding requirements page
def binding_requirements_page(uploaded_data):
    initialize_state()

    articles = uploaded_data['content']['articles']
    max_article_index = len(articles)
    current_article = articles[st.session_state.current_article_index]
    display_navigation_controls(st.session_state.current_article_index, max_article_index, 'top')

    #actors = 
    display_article(uploaded_data, st.session_state.current_article_index)
    handle_annotations(current_article['eId'], index = st.session_state.current_article_index) # , actors = actors)

    display_navigation_controls(st.session_state.current_article_index, max_article_index, 'bottom')
    df = pd.DataFrame([x for x in st.session_state['annotations'] if x is not None])
    st.table(df)

# Main function
def main():
    st.set_page_config(layout="wide")
    st.title("Annotate the articles")
    st.sidebar.write(st.session_state['celex'])

    if 'uploaded_data' not in st.session_state or st.session_state.uploaded_data is None:
        st.write("No data")
    else:
        binding_requirements_page(st.session_state.uploaded_data)

if __name__ == "__main__":
    main()