from io  import BytesIO 
import soundfile 
import numpy as np 

## check audio .ipynb for more detial

def audio_array_to_buffer(audio_array: np.array, sample_rate: int) -> BytesIO:
    buffer = BytesIO()
    soundfile.write(buffer, audio_array, sample_rate, format="wav")
    buffer.seek(0) ## start reading file from beggining of the file 
    return buffer
