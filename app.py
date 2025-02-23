import streamlit as st
import sounddevice as sd
import soundfile as sf
import io
import base64

st.title("Microphone Audio Recorder")

recording = False
audio_data = []
fs = 44100  # Sample rate

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None


def record_audio(duration):
    global recording, audio_data
    recording = True
    st.write("Recording started...")
    audio_data = sd.rec(int(fs * duration), samplerate=fs, channels=1, dtype='int16')  # Use int16 for better quality
    sd.wait()  # Wait until recording is finished
    recording = False
    st.write("Recording finished.")

    # Convert audio data to bytes
    audio_bytes_io = io.BytesIO()
    sf.write(audio_bytes_io, audio_data, fs, format='WAV')  # Use WAV format
    st.session_state.audio_bytes = audio_bytes_io.getvalue()


def download_audio():
    if st.session_state.audio_bytes:
        b64 = base64.b64encode(st.session_state.audio_bytes).decode()
        href = f'<a href="data:audio/wav;base64,{b64}" download="recorded_audio.wav">Download Audio</a>'  # Correct MIME type
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.write("No audio recorded yet.")



duration = st.slider("Recording Duration (seconds)", 1, 30, 5)

if st.button("Start Recording"):
    record_audio(duration)

if st.button("Download Recording"):
    download_audio()

if st.session_state.audio_bytes: # Display audio player if recording exists
    st.audio(st.session_state.audio_bytes, format='audio/wav')