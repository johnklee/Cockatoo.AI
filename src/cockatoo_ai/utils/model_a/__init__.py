"""Module to hold base class or protocols used in model A."""
import enum
from typing import Any
from cockatoo_ai.utils import wrapper
from cockatoo_ai.utils.model_a import open_ai
from cockatoo_ai.utils.model_a import speech_recognition_wrapper


LangEnum = wrapper.LangEnum


class ModelType(enum.StrEnum):
  """Model A types."""
  OPEN_AI_WHISPER_OFFLINE = 'open_ai_whisper_offline'
  SR_OPEN_AI_WHISPER = 'sr_open_ai_whisper'
  SR_GCP = 'sr_gcp'
  GCP_SPEECH_2_TEXT = 'gcp_speech_2_text'


def get(
    model_type: ModelType | str,
    settings: dict[str, Any] | None = None) -> wrapper.ModelA:
  """Gets model A.

  Args:
    model_type: Model type.
    settings: Model settings.

  Returns:
    Model A wrapper implementation.
  """
  match model_type:
    case ModelType.OPEN_AI_WHISPER_OFFLINE:
      if not settings:
        settings = {'lang': LangEnum.en}
      return open_ai.WhisperOfflineWrapper(**settings)
    case ModelType.SR_OPEN_AI_WHISPER:
      if not settings:
        settings = {'lang': LangEnum.en}
      return speech_recognition_wrapper.SRWhisperWrapper(**settings)
    case ModelType.SR_GCP:
      if not settings:
        settings = {'lang': LangEnum.en}
      return speech_recognition_wrapper.SRGoogleWrapper(**settings)
    case ModelType.GCP_SPEECH_2_TEXT:
      if not settings:
        settings = {'lang': LangEnum.en}
      return speech_recognition_wrapper.GCPSpeech2TextWrapper(**settings)
    case _:
      raise ValueError('Invalid model type="{model_type}"!')
