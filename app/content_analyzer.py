import boto3
import streamlit as st
import constants 
from utils import call_anthropic, upload_get_summary
import os


s3 = boto3.client(
        service_name='s3',
        region_name=constants.region
    )


if 'img_summary' not in st.session_state:
    st.session_state['img_summary'] = None
if 'csv_summary' not in st.session_state:
    st.session_state['csv_summary'] = None
if 'new_contents' not in st.session_state:
    st.session_state['new_contents'] = None
if 'label_text' not in st.session_state:
    st.session_state['label_text'] = None


comprehend = boto3.client(service_name='comprehend',region_name=constants.region)
rekognition = boto3.client(service_name='rekognition',region_name=constants.region)

p_summary = ''
st.set_page_config(page_title="GenAI Content Analyzer", page_icon="sparkles", layout="wide")

st.markdown("## Analyze any content with Amazon Bedrock")
st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 25%;
        }
    </style>
    """, unsafe_allow_html=True
)
st.sidebar.image("./bedrock.png")
st.sidebar.header("GenAI Content Analyzer")
values = [1, 2, 3, 4, 5]
default_ix = values.index(3)

p_count = st.sidebar.selectbox('Select the number of top topic suggestions to generate...', values, index=default_ix)
model = 'Anthropic Claude'



c1, c2 = st.columns(2)
c1.subheader("Upload your file")
uploaded_file = c1.file_uploader("**Select a file**", type=constants.file_types)
default_lang_ix = constants.languages.index('English')
c2.subheader("Select an output language")
language = c2.selectbox(
    'Bedrock should answer in...',
    options=constants.languages, index=default_lang_ix)

img_summary = ''
csv_summary = ''
file_type = ''
new_contents = ''
flag_summary = False

#uploaded file
if uploaded_file is not None:
    if str(uploaded_file.name).split('.')[1] in constants.file_types:
        file_type = str(uploaded_file.name).split('.')[1]            
        c1.success(uploaded_file.name + ' is ready for upload')
        if c1.button('Upload & Submit'):
            with st.spinner('Uploading file and starting summarization...'):
                s3.upload_fileobj(uploaded_file, constants.s3_bucket, constants.s3_prefix+'/'+uploaded_file.name)
                try:
                    new_contents, csv_summary = upload_get_summary(file_type, uploaded_file.name, language)
                    csv_summary = csv_summary.replace("$","\\$")
                    if len(csv_summary) > 5:
                        st.session_state['csv_summary'] = csv_summary
                    new_contents = new_contents.replace("$","\\$")
                    flag_summary=True
                    st.session_state.new_contents = new_contents
                    st.success('File uploaded and summary generated')
                except:
                    if os.path.exists(uploaded_file.name):
                        os.remove(uploaded_file.name)
                    flag_summary=False
                    st.success('The summary could not be generated')
                
    else:
        st.write('Incorrect file type provided. Please check and try again')


if uploaded_file is not None and flag_summary:
    if st.session_state.img_summary:
        if len(st.session_state.img_summary) > 5:
            st.image(uploaded_file)
            st.markdown('**Image summary**: \n')
            st.write(str(st.session_state['img_summary']))
            if model.lower() == 'anthropic claude':  
                p_text = call_anthropic('Generate'+str(p_count)+' central topic of 25 words maximum each topic from the following text: '+ st.session_state.img_summary+' en ' +language)
                p_text1 = []
                p_text2 = ''
                if p_text != '':
                    p_text.replace("$","\\$")
                    p_text1 = p_text.split('\n')
                    for i,t in enumerate(p_text1):
                        if i > 1:
                            p_text2 += t.split('\n')[0]+'\n\n'
                    p_summary = p_text2
            st.sidebar.markdown('### Suggested \n\n' + p_summary)
    elif st.session_state.csv_summary:
        if len(st.session_state.csv_summary) > 5:
            st.markdown('**Summary**: \n')
            st.write(str(st.session_state.csv_summary).replace("$","\\$"))
            if model.lower() == 'anthropic claude':
                p_text = call_anthropic('Generate'+str(p_count)+' central topic of 25 words maximum each topic from the following text: '+ st.session_state.csv_summary+' en ' +language)
                p_text1 = []
                p_text2 = ''
                if p_text != '':
                    p_text.replace("$","\\$")
                    p_text1 = p_text.split('\n')
                    for i,t in enumerate(p_text1):
                        if i > 1:
                            p_text2 += t.split('\n')[0]+'\n\n'
                    p_summary = p_text2
            st.sidebar.markdown('### Suggested \n\n' + p_summary)

