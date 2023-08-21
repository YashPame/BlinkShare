hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {background-color: #C5DFF8;}
    </style>       
    """

MainHeading = """
    <h1 style='text-align: center; color: black;'>
        Blink
        <span style='color: #4A55A2; font-size: 1.3em'>
            Share
        </span>
        <hr style='padding:0; margin:0; width: 50%; left:25%; position:absolute; border: none; border-top: 2px solid black;'>
    </h1>"""

subHeading = """
    <h3 style='text-align: center; color: black; margin-bottom: 5%;'>
        A simple way to send and receive your files
    </h3>"""

sendFileText_01 = """
    <h5 style='text-align: center; color: Black; margin-top: 5%;'>
        Select Your Files To Send
    </h5>"""
sendFileText_02 = """
    <h5 style='text-align: center; color: Black; margin-top: 5%;'>
        Sending File
    </h5>"""
sendFileText_03 = """
    <h6 style='text-align: center; color: Black;'>
        Please Wait...
    </h6>"""
sendFileText_04 = "<h5 style='text-align: center; color: Black; margin-top: 5%;'>File Sent Successfully</h5>"
sendFileText_05 = "<h1 style='text-align: center; color: Black;'> {} </h1>"
sendFileText_06 = """
    <h6 style='text-align: center; color: Black;'>
        Please share Above code with the person you want to send the file.<br>
        Once the person enters the code, the file will be sent to them.
    </h6>"""

ReceiveFileText_01 = """
    <h5 style='text-align: center; color: Black; margin-top: 5%;'>
        Enter The Code To Receive File
    </h5>"""
ReceiveFileText_02 = """
    <h5 style='text-align: center; color: Black; margin-top: 5%;'>
        Receiving File
    </h5>"""
ReceiveFileText_03 = """
    <h6 style='text-align: center; color: Black;'>
        Please Wait...
    </h6>"""
ReceiveFileText_04 = "<h5 style='text-align: center; color: Black; margin-top: 5%;'>File Received Successfully</h5>"
ReceiveFileText_05 = "<h6 style='text-align: center; color: Black;'>Click Download Button To Download The File</h6>"
ReceiveFileText_06 = "<h6 style='text-align: center; color: Black;'>File Name: {}</h6>"


ErrorTag = """<p style='text-align: center; color: #B31312;'> {} </p>"""
MainErrorTag = "<h5 style='text-align: center; color: Black; margin-top: 5%;'>{}</h5>"

DownloadButtonTag = """
<div style='text-align: center; border: 1px solid #BD9D9DFF; padding: 5px; margin: 2% auto; width:30%; background-color: #FAF0D7; border-radius: 8px;'>
    <a href="{}" style='text-align: center; color: red; text-decoration: none; font-size: 1.2em;' ' target="_blank">Download File</a>
</div>
"""


Footer = """
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
    </div>"""