import streamlit as st
from minio import Minio
import os
import random
import string

def getRandomString(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {background-color: #C5DFF8;}
    </style>       
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown(
    """<h1 style='text-align: center; color: black;'>
            Blink
            <span style='color: #4A55A2; font-size: 1.3em'>
                Share
            </span>
            <hr style='padding:0; margin:0; width: 50%; left:25%; position:absolute; border: none; border-top: 2px solid black;'>
        </h1>
    """, unsafe_allow_html=True)

st.markdown(
    """<h3 style='text-align: center; color: black; margin-bottom: 5%;'>
            A simple way to send and receive your files
        </h3>
    """, unsafe_allow_html=True)

if 'SendOrReceive' not in st.session_state:
    st.session_state.SendOrReceive = None
if 'FinalSendButton' not in st.session_state:
    st.session_state.FinalSendButton = None
if 'FinalReceiveButton' not in st.session_state:
    st.session_state.FinalReceiveButton = None
if 'file' not in st.session_state:
    st.session_state.file = None

if 'bucketName' not in st.session_state:
    st.session_state.bucketName = None
if 'receiveCode' not in st.session_state:
    st.session_state.receiveCode = None
if 'errorMessage' not in st.session_state:
    st.session_state.errorMessage = ""

if 'minioClient' not in st.session_state:
    st.session_state.minioClient = Minio(
        endpoint="play.min.io",
        access_key="Q3AM3UQ867SPQQA43P2F",
        secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        secure=True
    )

col1, col2 = st.columns(2)
with col1:
    SendButton = st.button("Send File")
with col2:
    ReceiveButton = st.button("Receive File")

if SendButton:
    st.session_state.SendOrReceive = "Send"
elif ReceiveButton:
    st.session_state.SendOrReceive = "Receive"

if st.session_state.SendOrReceive == "Send":
    _, subCol1, _ = st.columns([1, 7, 1])
    with subCol1:
        try:
            st.markdown(
                """<h5 style='text-align: center; color: Black; margin-top: 5%;'>
                    Select Your Files To Send
                    </h5>
                """, unsafe_allow_html=True)
            st.session_state.file = st.file_uploader(
                "Upload File",
                type=['png', 'jpg', 'jpeg', 'mp4', 'mp3', 'pdf', 'docx', 'txt', 'xlsx'],
                accept_multiple_files=True,
                label_visibility="collapsed",
                on_change=None)

            st.session_state.FinalSendButton = st.button("Send")

            st.markdown(
                f"""<p style='text-align: center; color: #B31312;'> {st.session_state.errorMessage} </p>""", unsafe_allow_html=True)
            st.session_state.errorMessage = ""

        except Exception as e:
            st.session_state.errorMessage = "Error: " + str(e)
            st.session_state.SendOrReceive = None
            st.experimental_rerun()


elif st.session_state.SendOrReceive == "Receive":
    try:
        st.markdown(
            """<h5 style='text-align: center; color: Black; margin-top: 5%;'>
                    Enter The Code To Receive File
                </h5>
            """, unsafe_allow_html=True)

        _, subCol2, _ = st.columns([1, 2, 1])
        with subCol2:
            st.session_state.receiveCode = st.text_input("Enter Code",
                                                         placeholder="Enter Code",
                                                         max_chars=6,
                                                         label_visibility="collapsed")

            st.markdown(
                """<style> 
                        div[data-baseweb="base-input"]{border: 2px; border-radius: 3px; background-color: white;} 
                        input[class]{font-weight: bold; font-size:120%; text-align: center; background-color: white;} 
                    </style> 
                """, unsafe_allow_html=True)

            st.session_state.FinalReceiveButton = st.button("Receive")

            st.markdown(
                f"""<p style='text-align: center; color: #B31312;'> {st.session_state.errorMessage} </p>""", unsafe_allow_html=True)
            st.session_state.errorMessage = ""

    except Exception as e:
        print("HII2")
        st.session_state.errorMessage = "Error: " + str(e)
        st.session_state.SendOrReceive = None
        st.experimental_rerun()


elif st.session_state.SendOrReceive == "ReceivingFile":
    try:
        st.markdown(
            """<h5 style='text-align: center; color: Black; margin-top: 5%;'>
                    Receiving File
                </h5>
            """, unsafe_allow_html=True)
        st.markdown(
            """<h6 style='text-align: center; color: Black;'>
                    Please Wait...
                </h6>
            """, unsafe_allow_html=True)

        if st.session_state.receiveCode is not None and st.session_state.receiveCode != "" and len(st.session_state.receiveCode) > 2 and str(st.session_state.receiveCode).isalpha():
            st.session_state.receiveCode = st.session_state.receiveCode.lower()
            if st.session_state.minioClient.bucket_exists(st.session_state.receiveCode):
                for file in st.session_state.minioClient.list_objects(st.session_state.receiveCode, recursive=True):
                    st.session_state.minioClient.fget_object(
                        st.session_state.receiveCode,
                        file.object_name,
                        os.path.join(os.path.join(os.path.expanduser('~'), 'Downloads'), file.object_name))
                    st.session_state.minioClient.remove_object(st.session_state.receiveCode, file.object_name)

                st.session_state.minioClient.remove_bucket(st.session_state.receiveCode)
                st.session_state.receiveCode = None
                st.session_state.SendOrReceive = "ReceivedFile_ShowCode"
                st.experimental_rerun()

            else:
                st.session_state.errorMessage = "Invalid Code"
                st.session_state.SendOrReceive = "Receive"
                st.write(st.session_state.errorMessage)
                st.experimental_rerun()
        else:
            if st.session_state.receiveCode is None or st.session_state.receiveCode == "":
                st.session_state.errorMessage = "Enter Code"
            else:
                st.session_state.errorMessage = "Invalid Code"
            st.session_state.SendOrReceive = "Receive"
            st.write(st.session_state.errorMessage)
            st.experimental_rerun()

    except Exception as e:
        print("HII")
        st.session_state.errorMessage = "Error: " + str(e)
        st.session_state.SendOrReceive = None
        st.experimental_rerun()


elif st.session_state.SendOrReceive == "SendingFile":
    try:
        st.markdown(
            """<h5 style='text-align: center; color: Black; margin-top: 5%;'>
                    Sending File
                </h5>
            """, unsafe_allow_html=True)
        st.markdown(
            """<h6 style='text-align: center; color: Black;'>
                    Please Wait...
                </h6>
            """, unsafe_allow_html=True)
        if st.session_state.file is not None and len(st.session_state.file) > 0:
            st.session_state.bucketName = getRandomString()
            print(st.session_state.bucketName)
            st.session_state.minioClient.make_bucket(st.session_state.bucketName)
            for file in st.session_state.file:
                with open(os.path.join("tempDir", file.name), "wb") as f:
                    f.write(file.getbuffer())
                st.session_state.minioClient.fput_object(st.session_state.bucketName, file.name,
                                                         os.path.join("tempDir", file.name))
                os.remove(os.path.join("tempDir", file.name))
            st.session_state.SendOrReceive = "SentFile_ShowCode"
            st.experimental_rerun()
        else:
            st.session_state.errorMessage = "Select Files"
            st.session_state.SendOrReceive = "Send"
            st.experimental_rerun()

    except Exception as e:
        st.session_state.errorMessage = "Error: " + str(e)
        st.session_state.SendOrReceive = None
        st.experimental_rerun()


elif st.session_state.SendOrReceive == "SentFile_ShowCode":
    try:
        st.markdown("<h5 style='text-align: center; color: Black; margin-top: 5%;'>File Sent Successfully</h5>",
                    unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: Black;'>" + str(st.session_state.bucketName).upper() + "</h1>",
                    unsafe_allow_html=True)
        st.markdown(
            """<h6 style='text-align: center; color: Black;'>
                Please share Above code with the person you want to send the file.<br>
                Once the person enters the code, the file will be sent to them.
            </h6>""", unsafe_allow_html=True)

    except Exception as e:
        st.session_state.errorMessage = "Error: " + str(e)
        st.session_state.SendOrReceive = None
        st.experimental_rerun()

elif st.session_state.SendOrReceive == "ReceivedFile_ShowCode":
    try:
        st.markdown("<h5 style='text-align: center; color: Black; margin-top: 5%;'>File Received Successfully</h5>",
                    unsafe_allow_html=True)
        st.markdown(
            f"<h6 style='text-align: center; color: Black;'>Your file has been downloaded to your Downloads folder.</h6>",
            unsafe_allow_html=True)
    except Exception as e:
        st.session_state.errorMessage = "Error: " + str(e)
        st.session_state.SendOrReceive = None
        st.experimental_rerun()

else:
    st.markdown(f"<h5 style='text-align: center; color: Black; margin-top: 5%;'>{st.session_state.errorMessage}</h5>",
                unsafe_allow_html=True)
    st.session_state.errorMessage = ""

if st.session_state.FinalSendButton is not None:
    if st.session_state.FinalSendButton:
        st.session_state.SendOrReceive = "SendingFile"
        st.session_state.FinalSendButton = None
        st.experimental_rerun()

if st.session_state.FinalReceiveButton is not None:
    if st.session_state.FinalReceiveButton:
        st.session_state.SendOrReceive = "ReceivingFile"
        st.session_state.FinalReceiveButton = None
        st.experimental_rerun()

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 10%;
        bottom: 0;
        width: 80%;
        text-align: center;
        background-color: #C5DFF8;
        padding: 10px 0;
        border-top: 1px solid black;
    }
    </style>
    <div class="footer">
        <h6 style='color: Black;'>
            <span style='color: #B31312; font-size: 1.4em'>
                Note:
            </span>
            This Website Currently uses an open source server to send and receive files.
            So, the files you send and receive are not encrypted and can be seen by anyone during time of of transfer.
            We are working on a better solution to this problem.
            Also this website is created for educational purposes only and not for professional use.
            We are not responsible for any misuse of this website.
        </h6>
    </div>
    """,
    unsafe_allow_html=True,
)