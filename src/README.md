## Preface
TBD

## Model Utils
TBD

### Model A
Model A is used to turn speech into text. Below sample code demonstrates the usage of utilities provided in Cockatoo.AI:
```python
# Import model A
>>> from cockatoo_ai.utils import model_a

# Obtain supported model A options:
>>> model_type = model_a.ModelType
>>> list(model_type)
[<ModelType.SR_OPEN_AI_WHISPER: 'sr_open_ai_whisper'>, <ModelType.SR_GCP: 'sr_gcp'>]

# Get OpenAI whisper by `str` and test it:
>>> ma_imp1 = model_a.get('sr_open_ai_whisper')
>>> ma_imp1.audio_2_text('~/test_audio_files/en_20240316_demmi.wav')
Audio2TextData(
    text='The weather is really good today in Amsterdam....',
    spent_time_sec=3.711142063140869,
    audio_file_path='/root/test_audio_files/en_20240316_demmi.wav')

# Get GCP solution by enum and test it:
>>> ma_imp2 = model_a.get(model_type.SR_GCP)
>>> ma_imp2.audio_2_text('~/test_audio_files/en_20240316_demmi.wav')
Audio2TextData(
    text='today in Amsterdam I want to go out',
    spent_time_sec=0.9695451259613037,
    audio_file_path='/root/test_audio_files/en_20240316_demmi.wav')
```
