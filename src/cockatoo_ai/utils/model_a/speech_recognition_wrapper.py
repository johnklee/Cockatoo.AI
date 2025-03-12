"""Wrapper of package `speech_recognition`."""
from google.cloud import speech
import logging
from openai import OpenAI
import speech_recognition as sr
import os
import time
import wave
from cockatoo_ai.utils import wrapper
from cockatoo_ai.utils.model_a import base


Audio2TextData = wrapper.Audio2TextData
ModelBase = base.ModelBase


class SRWhisperWrapper(ModelBase):
  """Wrapper of speech_recognition.Recognizer (for Whisper API users)."""

  def __init__(self, lang: wrapper.LangEnum):
    super().__init__(lang)
    self._client = OpenAI()

  @property
  def name(self) -> str:
    return 'SpeechRecognition/WhisperAPI'

  def audio_2_text(self, audio_file_path: str) -> str:
    audio_file_path = os.path.expanduser(audio_file_path)
    start_time = time.time()
    try:
      # Using Whisper API
      transcription = self._client.audio.transcriptions.create(
          model="whisper-1",
          file=open(audio_file_path, 'rb'))

      audio_text = transcription.text
      time_diff_sec = time.time() - start_time
      return Audio2TextData(
          text=audio_text,
          spent_time_sec=time_diff_sec,
          audio_file_path=audio_file_path)
    except Exception as ex:
      logging.error(
          f'Failed to transform audio to text from {audio_file_path}')
      raise ex


class SRGoogleWrapper(ModelBase):
  """Wrapper of speech_recognition.Recognizer.

  For this version, it will delegate the operation to Google Cloud Speech API:
  - https://cloud.google.com/speech-to-text?hl=zh_tw  # noqa: E501
  - https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages  # noqa: E501
  """

  def __init__(self, lang: wrapper.LangEnum):
    super().__init__(lang)
    self.language = 'en-US'
    if lang == wrapper.LangEnum.cn:
      self.language = 'zh-TW'

    self._speech_recognizer = sr.Recognizer()

  @property
  def name(self) -> str:
    return 'SpeechRecognition/GCP_speech_to_text'

  def audio_2_text(self, audio_file_path: str) -> str:
    audio_file_path = os.path.expanduser(audio_file_path)
    start_time = time.time()
    with sr.AudioFile(audio_file_path) as source:
      try:
        # using google speech recognition
        audio_text = self._speech_recognizer.listen(source)
        text = self._speech_recognizer.recognize_google(
            audio_text, language=self.language)
        time_diff_sec = time.time() - start_time
        return Audio2TextData(
            text=text,
            spent_time_sec=time_diff_sec,
            audio_file_path=audio_file_path)
      except sr.exceptions.UnknownValueError:
        logging.warning(
            f'Can not transform the input audio file from {audio_file_path}')
        time_diff_sec = time.time() - start_time
        return Audio2TextData(
            text='', spent_time_sec=time_diff_sec)
      except Exception as ex:
        logging.error(
            f'Failed to transform audio to text from {audio_file_path}')
        raise ex


class GCPSpeech2TextWrapper(ModelBase):
  """Wrapper of GCP Speech to text API.

  For details of this wrapper, please refer to below doc:
  - https://cloud.google.com/speech-to-text/docs/samples?hl=en  # noqa: E501

  For this class to work correctly, we have to provide below environment variable(s):  # noqa: E501
  - GOOGLE_API_KEY: GCP API key.

  Also, you need to enable Speech to text API from your GCP project:
  - https://cloud.google.com/speech-to-text/docs/before-you-begin
  """

  def __init__(
      self, lang: wrapper.LangEnum):
    super().__init__(lang)
    self.language = 'en-US'
    if lang == wrapper.LangEnum.cn:
      self.language = 'zh-TW'

    self._client = speech.SpeechClient()

  @property
  def name(self) -> str:
    return 'GCP/speech-to-text'

  def audio_2_text(self, audio_file_path: str) -> str:
    audio_file_path = os.path.expanduser(audio_file_path)
    if not audio_file_path.endswith('.wav'):
      raise ValueError('Only support wav file only now!')

    start_time = time.time()
    channels = None
    audio_content = None
    with open(audio_file_path, 'rb') as f:
        audio_content = f.read()

    with wave.open(audio_file_path, 'rb') as wave_file:
        channels = wave_file.getnchannels()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=self.language,
        # Enable automatic punctuation
        enable_automatic_punctuation=True,
        audio_channel_count=channels)

    response = self._client.recognize(config=config, audio=audio)
    text_list = []
    for i, result in enumerate(response.results):
      alternative = result.alternatives[0]
      text_list.append(alternative.transcript.strip())

    time_diff_sec = time.time() - start_time
    return Audio2TextData(
        text=' '.join(text_list),
        spent_time_sec=time_diff_sec,
        audio_file_path=audio_file_path)
