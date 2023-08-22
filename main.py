import streamlit as st
from minio import Minio
import os
import random
import string
import MarkdownText as md

st.set_page_config(page_title="BlinkShare", page_icon="⏩")
def getRandomString(length=6):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown(md.hide_st_style, unsafe_allow_html=True)
st.markdown(md.MainHeading, unsafe_allow_html=True)
st.markdown(md.subHeading, unsafe_allow_html=True)

if 'minioClient' not in st.session_state:
    st.session_state.minioClient = Minio(
        endpoint="play.min.io",
        access_key="Q3AM3UQ867SPQQA43P2F",
        secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        secure=True
    )

if 'bucketName' not in st.session_state:
    st.session_state.bucketName = "blinkshare"

if 'errorMessage' not in st.session_state: st.session_state.errorMessage = ""

if 'SendOrReceive' not in st.session_state: st.session_state.SendOrReceive = None

if 'FinalSendButton' not in st.session_state: st.session_state.FinalSendButton = None
if 'FinalReceiveButton' not in st.session_state: st.session_state.FinalReceiveButton = None

if "SendingCode" not in st.session_state: st.session_state.SendingCode = None
if 'receiveCode' not in st.session_state: st.session_state.receiveCode = None
if 'file' not in st.session_state: st.session_state.file = None
if 'receivedFileNames' not in st.session_state: st.session_state.receivedFileNames = []
if 'FileLink' not in st.session_state: st.session_state.FileLink = None


col1, col2 = st.columns(2)

with col1: SendButton = st.button("Send File")
with col2: ReceiveButton = st.button("Receive File")

if SendButton: st.session_state.SendOrReceive = "Send"
elif ReceiveButton: st.session_state.SendOrReceive = "Receive"

if st.session_state.SendOrReceive == "Send":
    _, subCol1, _ = st.columns([1, 7, 1])
    with subCol1:
        try:
            st.markdown(md.sendFileText_01, unsafe_allow_html=True)
            st.session_state.file = st.file_uploader(
                "Upload File",
                type=['png', 'jpg', 'jpeg', 'mp4', 'mp3', 'pdf', 'docx', 'txt', 'xlsx', "pptx", "zip", "rar"],
                accept_multiple_files=False,
                label_visibility="collapsed",
                on_change=None)

            st.session_state.FinalSendButton = st.button("Send")
            st.markdown(md.ErrorTag.format(st.session_state.errorMessage), unsafe_allow_html=True)
            st.session_state.errorMessage = ""

        except Exception as e:
            st.session_state.errorMessage = "Error: " + str(e)
            st.session_state.SendOrReceive = None
            st.experimental_rerun()

elif st.session_state.SendOrReceive == "SendingFile":
    try:
        st.markdown(md.sendFileText_02, unsafe_allow_html=True)
        st.markdown(md.sendFileText_03, unsafe_allow_html=True)

        if st.session_state.file is not None:
            if not st.session_state.minioClient.bucket_exists(st.session_state.bucketName):
                st.session_state.minioClient.make_bucket(st.session_state.bucketName)
                print("Bucket Created")

            st.session_state.SendingCode = getRandomString()
            st.session_state.file.name = st.session_state.SendingCode + "_" + st.session_state.file.name
            with open(os.path.join("tempDir", st.session_state.file.name), "wb") as f:
                f.write(st.session_state.file.getbuffer())

            st.session_state.minioClient.fput_object(st.session_state.bucketName, st.session_state.file.name, os.path.join("tempDir", st.session_state.file.name))
            os.remove(os.path.join("tempDir", st.session_state.file.name))
            st.session_state.SendOrReceive = "SentFile_ShowCode"
            st.experimental_rerun()
        else:
            st.session_state.errorMessage = "Select Files"
            st.session_state.SendOrReceive = "Send"
            st.experimental_rerun()

    except Exception as e:
        print(e)
        st.session_state.errorMessage = "Error: " + str(e)
        st.session_state.SendOrReceive = None
        st.experimental_rerun()

elif st.session_state.SendOrReceive == "SentFile_ShowCode":
    try:
        st.markdown(md.sendFileText_04, unsafe_allow_html=True)
        st.markdown(md.sendFileText_05.format(str(st.session_state.SendingCode).upper()), unsafe_allow_html=True)
        st.markdown(md.sendFileText_06, unsafe_allow_html=True)

    except Exception as e:
        st.session_state.errorMessage = "Error: " + str(e)
        st.session_state.SendOrReceive = None
        st.experimental_rerun()

elif st.session_state.SendOrReceive == "Receive":
    try:
        st.markdown(md.ReceiveFileText_01, unsafe_allow_html=True)

        _, subCol2, _ = st.columns([1, 2, 1])
        with subCol2:
            st.session_state.receiveCode = st.text_input("Enter Code",
                                                         placeholder="Enter Code",
                                                         max_chars=6,
                                                         label_visibility="collapsed")
            st.session_state.FinalReceiveButton = st.button("Receive")

            st.markdown(md.ErrorTag.format(st.session_state.errorMessage), unsafe_allow_html=True)
            st.session_state.errorMessage = ""

    except Exception as e:
        st.session_state.errorMessage = "Error: " + str(e)
        st.session_state.SendOrReceive = None
        st.experimental_rerun()

elif st.session_state.SendOrReceive == "ReceivingFile":
    try:
        st.markdown(md.ReceiveFileText_02, unsafe_allow_html=True)
        st.markdown(md.ReceiveFileText_03, unsafe_allow_html=True)
        st.session_state.receivedFileNames = []
        if st.session_state.receiveCode is not None and st.session_state.receiveCode != "" and len(st.session_state.receiveCode) > 2 and str(st.session_state.receiveCode).isalpha():
            st.session_state.receiveCode = st.session_state.receiveCode.lower()
            if st.session_state.minioClient.bucket_exists(st.session_state.bucketName):
                for obj in st.session_state.minioClient.list_objects(st.session_state.bucketName, recursive=True):
                    if str(st.session_state.receiveCode) == str(obj.object_name.split("_")[0]):
                        st.session_state.receivedFileNames.append(obj.object_name)
                if len(st.session_state.receivedFileNames) >= 1:
                    st.session_state.FileLink = st.session_state.minioClient.presigned_get_object(
                        st.session_state.bucketName, st.session_state.receivedFileNames[0])

                    st.session_state.receiveCode = None
                    st.session_state.SendOrReceive = "ReceivedFile_ShowCode"
                    st.experimental_rerun()
                else:
                    st.session_state.errorMessage = "Invalid Code"
                    st.session_state.SendOrReceive = "Receive"
                    st.write(st.session_state.errorMessage)
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

elif st.session_state.SendOrReceive == "ReceivedFile_ShowCode":
    try:
        st.markdown(md.ReceiveFileText_04, unsafe_allow_html=True)
        st.markdown(md.ReceiveFileText_05, unsafe_allow_html=True)
        st.markdown(md.DownloadButtonTag.format(st.session_state.FileLink), unsafe_allow_html=True)
        st.markdown(md.ReceiveFileText_06.format(st.session_state.receivedFileNames), unsafe_allow_html=True)
        st.session_state.receiveCode = None

    except Exception as e:
        st.session_state.errorMessage = "Error: " + str(e)
        st.session_state.SendOrReceive = None
        st.experimental_rerun()

else:
    st.markdown(md.MainErrorTag.format(st.session_state.errorMessage), unsafe_allow_html=True)
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

st.markdown(md.Footer, unsafe_allow_html=True)