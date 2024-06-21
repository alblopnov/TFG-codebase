from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def gpt_consumption(progress_file, json_data, script_description):

    completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": script_description},
                {"role": "user", "content": json.dumps(json_data)}
            ]
        )
    with open(progress_file, 'w') as f:
            f.write(str("90"))
    return completion.choices[0].message.content

def tts_consumption(text_response, audio_path,progress_file):
    tts_response = client.audio.speech.create(
            model="tts-1",
            input=text_response,
            voice="alloy",
        )
    audio_file_path = os.path.join(audio_path, "script.mp3")
    tts_response.write_to_file(audio_file_path)
    with open(progress_file, 'w') as f:
        f.write(str("100"))