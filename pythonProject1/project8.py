import speech_recognition as sr
import pyttsx3
import openai
import time


# Set Your Open AI key


openai.api_key = "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"

engine = pyttsx3.init()


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response["choices"][0]["text"]

def generate_response(prompt):
    friendly_prompt = f"Please provide an explanation of '{prompt}' in a conversational and friendly tone suitable for a trainer to narrate to students."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=friendly_prompt,  # Include the context in the prompt
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:

        # wait for user to say "genius"
        print("Say 'genius' to start recording your question")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)

                if transcription.lower() == "genius":
                    # Record Audio
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                            # Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"you said: {text}"

                        # Generate Response

                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        # Read Response Using Text-to-Speech
                        speak_text(response)

            except Exception as e:
                print("An error occurred: {}".format(e))


if __name__ == "__main__":
    main()