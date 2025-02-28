import streamlit as st
import json


def export_annotations():
    if 'annotations' not in st.session_state:
        st.error("No annotations have been made yet.")
        return

    if 'celex' not in st.session_state:
        st.error("CELEX number is not set.")
        return

    # Output annotations to JSON file
    annotations = st.session_state['annotations']
    annotations_json = json.dumps(annotations, indent=4)

    file_name = f"{st.session_state.celex}_annotations.json"

    st.download_button(
        label="Download Annotations",
        data=annotations_json,
        file_name=file_name,
        mime="application/json"
    )

    st.success("Annotations ready for download.")

st.title("Export Annotations")
st.write("Ensure you have completed all required annotations.")
export_annotations()