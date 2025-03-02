"""Wrapper of OpenAI whisper solution.

For details, please refer to:
- https://github.com/openai/whisper
"""
import logging
import os
import time
import whisper

from cockatoo_ai.utils import wrapper
from cockatoo_ai.utils.model_a import base


Audio2TextData = wrapper.Audio2TextData
ModelBase = base.ModelBase


class WhisperOfflineWrapper(ModelBase):
  """Wrapper of OpenAI whisper offline package."""

  def __init__(
      self, lang: wrapper.LangEnum, model_size: str = 'small'):
    super().__init__(lang)
    self._model = whisper.load_model(model_size)

  @property
  def name(self) -> str:
    return 'OpenAI/WhisperOffline'

  def audio_2_text(self, audio_file_path: str) -> str:
    audio_file_path = os.path.expanduser(audio_file_path)
    start_time = time.time()
    try:
      result = self._model.transcribe(audio_file_path)
      audio_text = result['text']
      time_diff_sec = time.time() - start_time
      return Audio2TextData(
          text=audio_text,
          spent_time_sec=time_diff_sec,
          audio_file_path=audio_file_path)
    except Exception as ex:
      logging.error(
          f'Failed to transform audio to text from {audio_file_path}')
      raise ex
