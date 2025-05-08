"""
`DownloadDex` is an intelligent file and folder management tool that efficiently organizes the contents of
your `Downloads` folder, whether you're using `Windows`, `macOS`, or `Linux`. It automatically categorizes
files into their respective folders, ensuring easy access and a streamlined experience for users.

Give it a try and support the repository. Thank you!
"""

import streamlit as st
import os
from pathlib import Path
import platform
import configparser

# Load config file
config = configparser.ConfigParser()
config.read('extensions.ini')

# Extract only the extensions into lists
IMAGE_EXTENSIONS = sum([config['ImageExtensions'][key].split(', ') for key in config['ImageExtensions']], [])
VIDEO_EXTENSIONS = sum([config['VideoExtensions'][key].split(', ') for key in config['VideoExtensions']], [])
DOCUMENT_EXTENSIONS = sum([config['DocumentExtensions'][key].split(', ') for key in config['DocumentExtensions']], [])
AUDIO_EXTENSIONS = sum([config['AudioExtensions'][key].split(', ') for key in config['AudioExtensions']], [])

# Detect the operating system
os_name = platform.system()

#Define the absolute path for the Downloads folder based on OS
downloads_path = ''
if os_name == "Windows":
    downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")
elif os_name == "Darwin":  # macOS
    downloads_path = os.path.join(os.environ["HOME"], "Downloads")
elif os_name == "Linux":
    downloads_path = os.path.join(os.environ["HOME"], "Downloads")
else:
    raise RuntimeError(f"Unsupported OS: {os_name}")

#Define constant DownloadDex folders path
DOWNLOADDEXFOLDER = os.path.join(downloads_path,'DownloadDex_Content')
DOWNLOADDEXIMAGES = os.path.join(DOWNLOADDEXFOLDER,"Images")
DOWNLOADDEXVIDEO = os.path.join(DOWNLOADDEXFOLDER,"Videos")
DOWNLOADDEXDOCUMENT = os.path.join(DOWNLOADDEXFOLDER,"Documents")
DOWNLOADDEXAUDIO = os.path.join(DOWNLOADDEXFOLDER,"Audios")
DOWNLOADDEXOTHER = os.path.join(DOWNLOADDEXFOLDER,"Others")

# Set the title of the web app
st.title("DownloadDex!")
st.subheader("Smart management for your `downloaded` files.")
st.markdown('<hr style="border:2px solid #ccc;">', unsafe_allow_html=True)

# Downloads folder inspection section
folders_count = 0
files_count = 0
download_inspect_col1, download_inspect_col2 = st.columns(2)

with download_inspect_col1:
    # The 'Check Downloads folder content' used for checking all the files and
    # folder present in the 'Downloads' folder excluding the one this app creates.

    if st.button("Check `Downloads` folder content"):
        files_and_folders = list((Path(downloads_path)).iterdir())
        folders_count = len([folder for folder in files_and_folders if folder.is_dir() and folder.name != "DownloadDex_Content"])
        files_count = len([file for file in files_and_folders if file.is_file()])

with download_inspect_col2:
    # Display section for the 'files' and 'folders'.

    files_and_folder_count_col1, files_and_folder_count_col2 = st.columns(2)
    with files_and_folder_count_col1:
        st.write(f'Total **Folders**: **{folders_count}**')
    with files_and_folder_count_col2:
        st.write(f'Total **Files**: **{files_count}**')

st.markdown('<hr style="border:1px solid #ccc;">', unsafe_allow_html=True)
st.markdown(
    """
    <style>
    div.stButton > button {
        display: block;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
if st.button("Organize all the content of `Downloads` folder."):
    # Main organizing button for listing the files and folders in
    # the `Downloads` folder and then moved them into a new
    # `DownloadDex_Content` folder by categorizing them into
    # their respective categories.

    imgs = []
    auds = []
    vids = []
    docs = []
    fols = []
    others = []
    if len(list((Path(downloads_path)).iterdir())) != 1 and str(list((Path(downloads_path)).iterdir())[0]) != "DownloadDex_Content":
        for files_and_folders in (Path(downloads_path)).iterdir():
            if files_and_folders.is_dir(): #Folder check
                if files_and_folders.name == "DownloadDex_Content":
                    continue
                fols.append(str(files_and_folders))
            else: #Files check
                if len(["" for img_ext in IMAGE_EXTENSIONS if str(img_ext).lower() == str(files_and_folders.suffix).lower()]) > 0:
                    imgs.append(str(files_and_folders))

                elif len(["" for aud_ext in AUDIO_EXTENSIONS if str(aud_ext).lower() == str(files_and_folders.suffix).lower()]) > 0:
                    auds.append(str(files_and_folders))

                elif len(["" for vid_ext in VIDEO_EXTENSIONS if str(vid_ext).lower() == str(files_and_folders.suffix).lower()]) > 0:
                    vids.append(str(files_and_folders))

                elif files_and_folders.suffix == "":
                    docs.append(str(files_and_folders) + ".TXT")

                elif len(["" for doc_ext in DOCUMENT_EXTENSIONS if str(doc_ext).lower() == str(files_and_folders.suffix).lower()]) > 0:
                    docs.append(str(files_and_folders))

                else:
                    others.append(str(files_and_folders))

        #Create the new `DownloadDex_Content` folder and their subfolders for categorizing the content.
        os.makedirs(DOWNLOADDEXFOLDER, exist_ok = True)
        if os.path.isdir(DOWNLOADDEXFOLDER):
            for directory in [DOWNLOADDEXIMAGES, DOWNLOADDEXVIDEO, DOWNLOADDEXDOCUMENT, DOWNLOADDEXAUDIO, DOWNLOADDEXOTHER]:
                os.makedirs(directory, exist_ok = True)

            _ = [os.rename(img,img.replace(downloads_path, DOWNLOADDEXIMAGES)) for img in imgs]
            _ = [os.rename(vid,vid.replace(downloads_path, DOWNLOADDEXVIDEO)) for vid in vids]
            _ = [os.rename(doc,doc.replace(downloads_path, DOWNLOADDEXDOCUMENT)) if doc[-4:] != '.TXT' else  os.rename(doc[:-4],doc[:-4].replace(downloads_path, DOWNLOADDEXDOCUMENT))
                 for doc in docs]
            _ = [os.rename(aud,aud.replace(downloads_path, DOWNLOADDEXAUDIO)) for aud in auds]
            _ = [os.rename(other1,other1.replace(downloads_path, DOWNLOADDEXOTHER)) for other1 in fols]
            _ = [os.rename(other2,other2.replace(downloads_path, DOWNLOADDEXOTHER)) for other2 in others]

            st.success("All the files and folders now organized in the **DownloadDex_Content** folder")
        else:
            st.warning("Unable to create the `DownloadDex_Content` folder, Check Permissions!")

    else:
        st.warning("The content already organized in the `DownloadDex_Content` folder!")

    #Uncomment to check all the files and folder categorized by DownloadDex manually
    print(f"Total: {len(imgs) + len(vids) + len(docs) + len(auds) + len(others) + len(fols)}")
    print(f"IMAGES: {sorted(imgs)}, len(imgs): {len(imgs)}")
    print(f"VIDEOS: {sorted(vids)}, len(vids): {len(vids)}")
    print(f"DOCUMENTS: {sorted(docs)}, len(docs): {len(docs)}")
    print(f"AUDIOS: {sorted(auds)}, len(auds): {len(auds)}")
    print(f"OTHERS: {sorted(others)}, len(others): {len(others)}")
    print(f"FOLDERS: {sorted(fols)}, len(fols): {len(fols)}")