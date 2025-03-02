"""Wrapper for pre-defined API interfaces of model A, B and C packages."""

import dataclasses
import enum
from typing import Protocol


@dataclasses.dataclass
class Audio2TextData:
  """Audio to text result."""
  text: str
  spent_time_sec: float
  audio_file_path: str


@enum.unique
class LangEnum(enum.Enum):
  en = 0
  cn = 1
  multi_lang = -1

  @classmethod
  def from_str(cls, lang_str: str):
    for supported_lang_enum in cls:
      if supported_lang_enum.name == lang_str:
        return supported_lang_enum

    raise ValueError(f'Unknown lang setting={lang_str}!')


class ModelA(Protocol):
  """Model A wrapper."""

  def __init__(self, lang: LangEnum = LangEnum.en):
    self.lang = lang

  @property
  def name(self) -> str:
    """Model/Approch name."""
    pass

  def live_2_text(
      self,
      record_time_sec: int = 5,
      output_audio_file_path: str | None = None) -> Audio2TextData:
    """Records and transform audio into text.

    Args:
      record_time_sec: Recording time in seconds.
      output_audio_file_path: Output audio fie path.

    Returns:
      `Audio2TextData` with trasnformed text.
    """
    pass

  def audio_2_text(self, audio_file_path: str) -> Audio2TextData:
    """Turns audio of given file path into text.

    Args:
      audio_file_path: Audio file path to do audio to text transformation.

    Returns:
      `Audio2TextData` with trasnformed text.
    """
    pass


class ModelAMetric(Protocol):
  """Clz to calculate metric score of model A.

  Attributes:
    - name: Name of metric.
    - lang: Language of text to calculate metric.
  """
  name: str = 'Unknown'
  do_sort_reverse: bool = True

  def __init__(self, lang: LangEnum):
    self._lang = lang

  @property
  def lang(self) -> LangEnum:
    return self._lang

  def score(
      self,
      transformed_text: str,
      ground_truth_text: str) -> float:
    """Calculates the metric score.

    Args:
      transformed_text: The text transformed by model A.
      ground_truth_text: The ground truth of text.

    Returns:
      The corresponding metric score.
    """
    pass
