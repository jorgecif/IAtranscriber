
import streamlit as st
import os
from tempfile import NamedTemporaryFile
from openai import OpenAI
import PIL.Image
from streamlit_option_menu import option_menu
from streamlit_extras.let_it_rain import rain



st.set_page_config(
    page_title="Herramientas AI - Qüid Lab",
    page_icon="random",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Logo sidebar
image = PIL.Image.open('logo_blanco.png')
st.sidebar.image(image, width=None, use_column_width=None)



# Set your OpenAI API key
#openai_api_key=os.environ.get("OPENAI_API_KEY") # Opcion para Streamlit local
openai_api_key=st.secrets["openai_api_key"] # Opción para Streamlit share



client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai_api_key,
)

# Functions

# Funtion success
def success():
	rain(
		emoji="🎈",
		font_size=54,
		falling_speed=5,
		animation_length=1, #'infinite'
	)

# Function to transcribe audio using OpenAI API
def transcribe_audio(audio_file):
    # Transcribe using OpenAI API
    with NamedTemporaryFile(suffix="mp3", delete=False) as temp:
        temp.write(audio_file.getvalue())
        temp.seek(0)
        result = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="text"
        )
    # Extract transcribed text from the API response
    transcribed_text = result

    return transcribed_text





# Title
st.header("Sube tu archivo de audio y transcríbelo a texto")

col1, col2 = st.columns(2)

# File upload
audio_file = st.sidebar.file_uploader("Subir audio de máximo 5 MB", type=["wav", "mp3", "m4a"])
st.sidebar.audio(audio_file)


if st.sidebar.button("Transcribir audio"):
    if audio_file is not None:
            # Transcribe audio
            transcribed_text = transcribe_audio(audio_file)

            st.sidebar.success("Transcripción completada")
            col1.subheader("Resultado transcripción")
            col1.write(transcribed_text)
            col1.download_button('Descargar transcripción', transcribed_text, file_name='transcripcion.txt')
            resumen = client.completions.create(
                model="gpt-3.5-turbo-instruct", 
                max_tokens=200,
                prompt= "Genera resumen de un párrafo del texto: "+str({transcribed_text})
            )
            success()
            resultado_resumen=resumen.choices[0].text
            col2.subheader("Resumen de la transcripción")

            col2.write(resultado_resumen)




    else:
        st.error("Por favor subir el archivo de audio")