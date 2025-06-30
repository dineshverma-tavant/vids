import streamlit as st
import yt_dlp
import os
import tempfile

st.title("YouTube Downloader")

# URL input
url = st.text_input("Enter the YouTube link:")

# Download choice
choice = st.radio("Choose download option:", ("Audio only (M4A)", "Video + Audio (720p)"))

# Temporary directory management
temp_dir = tempfile.TemporaryDirectory()
if st.button("Download"):
    if not url:
        st.error("Please enter a YouTube link.")
    else:
        try:
            if choice == "Audio only (M4A)":
                ydl_opts = {
                    'outtmpl': os.path.join(temp_dir.name, '%(title)s.%(ext)s'),
                    'format': 'bestaudio[ext=m4a]',
                    'merge_output_format': None,
                    'postprocessors': [],  # Disable post-processing to avoid FFmpeg issues
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info)  # Get the exact file path
                    if os.path.exists(file_path):
                        st.success(f"Downloaded audio: {info['title']}")
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="Download Audio",
                                data=file,
                                file_name=f"{info['title']}.m4a",
                                mime="audio/m4a"
                            )
                    else:
                        st.error("File not found after download. Please try again.")
            elif choice == "Video + Audio (720p)":
                ydl_opts = {
                    'outtmpl': os.path.join(temp_dir.name, '%(title)s.%(ext)s'),
                    'format': 'best[ext=mp4][height<=720]',
                    'merge_output_format': None,
                    'postprocessors': [],  # Disable post-processing
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info)
                    if os.path.exists(file_path):
                        st.success(f"Downloaded video: {info['title']} at {info.get('resolution', 'unknown resolution')}")
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="Download Video",
                                data=file,
                                file_name=f"{info['title']}.mp4",
                                mime="video/mp4"
                            )
                    else:
                        st.error("File not found after download. Please try again.")
        except Exception as e:
            st.error(f"Error in download: {str(e)}")
        finally:
            temp_dir.cleanup()  # Clean up the temporary directory after the process

st.write(f"Current working directory: {os.getcwd()}")
