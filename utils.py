# Import Dependencies
from Google import Create_Service
from googleapiclient.http import MediaIoBaseUpload
from PIL import Image, ImageDraw, ImageFont
import io,streamlit as st

# Fonts: SnellBoundhand -> name , Times New roman -> content
font=ImageFont.FreeTypeFont(r"fonts/SnellRoundhand-BoldScript.otf",150,encoding="unic")
font1=ImageFont.FreeTypeFont(r"fonts/Times New Roman Font.ttf",110,encoding="unic")

# Google Oauth
CLIENT_SECRET_FILE='client_secret_oauth.json'
API_NAME='drive'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/drive']

# Oauth Service
# Create Gdrive folder: returns the link created by gdrive folder.
def createFolder(folder_name):
    global service
    service=Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents':['1shGwOic6EYHKW3EdJyXcRy5GKgXcNKq4']
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    # print(F'FolderID: {folder.get("id")}')
    return folder.get("id")


# createFolder("testing")


# Generate: generates a certificate with flag:0 -> Preview, flag:1 -> Generation
def generate(name,team,event,date,folder_name=None):

    # Check folder
    if folder_name!=None: 
        folder=createFolder(folder_name) # call function to create a folder in GDrive and return link 
        st.success(f"{folder_name} is created in Certificates Gdrive folder")
        
    st.warning("Generating Certificates ",icon="⏳")
    for name,team in zip(name,team):
        
        # opens and creates an object: img, draw
        img=Image.open(r"images/participation.png")
        draw=ImageDraw.Draw(img)

        # modify name: call funtion modifyText
        name=modifyText(name)

        # Draw on image: name,team,event,date in order
        draw.text(xy=(2400,1520),text=name,fill="#000000",font=font,anchor="mm",align="center",stroke_width=1)
        draw.text(xy=(1490,1840),text=team,fill="#000000",font=font1,anchor="mm",align="center",stroke_width=1)
        draw.text(xy=(3420,1840),text=event,fill="#000000",font=font1,anchor="mm",align="center",stroke_width=1)
        draw.text(xy=(2100,2060),text=date,fill="#000000",font=font1,anchor="mm",align="center",stroke_width=1)

        # Check Flag: flag:0 -> show images flag:1 -> upload images onto Gdrive 
        if folder_name==None: img.save("preview.png")
        else:
            img_file = io.BytesIO()
            img.save(img_file, 'PNG')
            img_file.seek(0)

            file_metadata = {'name': name+".png",'parents':[folder]}
            media = MediaIoBaseUpload(img_file, mimetype='image/png')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            # print(F'File ID: {file.get("id")}')
        
    st.success("Certificates Generated")

        



# Modify the text: returns clean capitailazed text
def modifyText(name):
    name = name.strip() # remove leading and trailing whitespaces
    name = " ".join(name.split()) # remove extra whitespaces in between words
    return " ".join(word.capitalize() for word in name.split())



        