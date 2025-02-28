import streamlit as st
import json

def load_page():
    """Uploads a JSON file"""
    st.title("Upload LegalJSON File")
    uploaded_file = st.file_uploader("Select a LegalJSON file", type=["json"])
    
    if uploaded_file:
        try:
            data = json.loads(uploaded_file.getvalue())
            st.session_state.uploaded_data = data
            st.session_state.celex = data['celex']
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please upload a valid LegalJSON file.")
        except KeyError:
            st.error("The uploaded JSON file does not contain a 'celex' key.")
    else:
        return None
    
def main():
    load_page()

if __name__ == "__main__":
    main()