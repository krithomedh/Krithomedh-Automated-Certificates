import streamlit as st 
import pandas as pd
from utils import generate
from dotenv.main import load_dotenv
import os
load_dotenv()

# Get Password
key = os.environ['PASSWORD']

# TODO
#4. deploy
#5. Text area for easy generation

st.set_page_config(
    page_title="Krithomedh Certificates",
    page_icon="🧑‍💻",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Main Header
st.header("Krithomedh Certificates Generation")

global uploaded_file

# Sidebar: Upload dataset
with st.sidebar:
    try:
        # Uploading file with except 
        uploaded_file = st.file_uploader("Choose a file")

        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)

            # Get non null columns
            notnull_columns=data.columns[~data.isna().any()].tolist()
            st.caption("Data uploaded succesfully")
            f'''
            **Total Records:** {data.shape[0]} 
        '''
    except:
        st.caption("An error has occured..Data NOT uploaded")

# -----------------

# Input Section
with st.container():
    
    # Base Condition
    if uploaded_file is None:
        st.write("Upload CSV for generating certificates")

    if uploaded_file is not None:
        st.caption("Generate Certificates")

        # genearte columns:4 columns are generated
        col1,col2,col3,col4=st.columns(4)

        # Taking Inputs: inputs for the name,team,event and date
        with col1:
            participant_name=st.selectbox('Name on the certificate',notnull_columns)
        with col2:
            team_name=st.selectbox('Team Name',notnull_columns)
        with col3:
            event_date=st.date_input(label="Date 📅")
            event_date=event_date.strftime('%d-%m-%Y')
        with col4:
            event_name=st.text_input(label="Event Name",placeholder="Ideathon")
            
        
# ------------------

# Generate Section
with st.container():
    if uploaded_file is not None and len(event_name)!=0:
        # Creating 2 coluumns in container
        col1,col2=st.columns([1,1])
    
        with col1:
            with st.form("inputs"):
                # Preview Button: generates preview of the certificate
                preview = st.form_submit_button("Preview")
                if preview:
                    with col2:
                        # Function call on 1st record in dataset
                        generate(data[participant_name][0:1],data[team_name][0:1],event_name,event_date)
                
                # folder_name: folder is created in parent folder Certificates in Gdrive
                folder_name=st.text_input(label="Folder Name")

                # Password: 16- digit pwd
                password=st.text_input(label="Password",type="password")

                # generate_certificates: button for generating certificates
                generate_certificates = st.form_submit_button("Generate")
                if generate_certificates:
                    with col2:
                        if password==key and len(folder_name)!=0:
                            # st.success("lkwadsh.")
                            # generate: returns success message with created certificate folder.
                            generate(data[participant_name],data[team_name],event_name,event_date,folder_name)
                        else:
                            # ERROR
                            st.error(" Incorrect Password or enter Folder Name",icon="❌")


# --------------------------



       














