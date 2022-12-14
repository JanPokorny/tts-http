import fastapi
import fastapi.responses
import pydantic
import pyttsx3
import tempfile
import os


# MODELS
#########
class TTSRequest(pydantic.BaseModel):
    """Text to read"""
    text: str
    voice: str
    rate: int | None


# SETUP
########
app = fastapi.FastAPI(
    title='TTS Windows server'
)


# HELPERS
##########
def create_temp_file():
    temp_dir_name = tempfile.mkdtemp()
    temp_file_name = os.path.join(temp_dir_name, 'tempfile')
    try:
        yield temp_file_name
    finally:
        os.unlink(temp_file_name)
        os.rmdir(temp_dir_name)


# ROUTES
#########
@app.get("/", include_in_schema=False)
def get_help():
    return fastapi.responses.RedirectResponse('/redoc')


@app.get("/voices")
def get_voices():
    """
    List all voices available on the system. On Windows, not all system voices are unlocked by default. See README for help.
    """
    return pyttsx3.init().getProperty('voices')


@app.post("/tts")
def text_to_speech(tts_request: TTSRequest, temp_file_name = fastapi.Depends(create_temp_file)):
    """
    Return a WAV file containing the text read by the specified voice.
    """
    engine = pyttsx3.init()
    engine.setProperty('voice', next(voice.id for voice in get_voices() if tts_request.voice in voice.name))
    if tts_request.rate:
        engine.setProperty('rate', tts_request.rate)
    
    engine.save_to_file(tts_request.text, temp_file_name)
    engine.runAndWait()
    return fastapi.responses.FileResponse(
        path=temp_file_name,
        media_type='audio/wav'
    )
