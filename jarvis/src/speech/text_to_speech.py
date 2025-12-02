import sounddevice as sd
import torch
from datasets import load_dataset
from transformers import (
    SpeechT5ForTextToSpeech,
    SpeechT5HifiGan,
    SpeechT5Processor,
)


class TextToSpeach:
    def __init__(self) -> None:
        self.processor = SpeechT5Processor.from_pretrained(
            "microsoft/speecht5_tts"
        )
        self.model = SpeechT5ForTextToSpeech.from_pretrained(
            "microsoft/speecht5_tts"
        )
        self.vocoder = SpeechT5HifiGan.from_pretrained(
            "microsoft/speecht5_hifigan"
        )
        self.embeddings_dataset = load_dataset(
            "Matthijs/cmu-arctic-xvectors", split="validation"
        )
        self.speaker_embeddings = torch.tensor(
            self.embeddings_dataset[4000]["xvector"]
        ).unsqueeze(0)

    def speak(self, text):
        inputs = self.processor(text=text, return_tensors="pt")
        speech = self.model.generate_speech(
            inputs["input_ids"], self.speaker_embeddings, vocoder=self.vocoder
        )
        speech_numpy = speech.squeeze().cpu().numpy()
        sd.play(speech_numpy, samplerate=16000)
        sd.wait()


if __name__ == "__main__":
    pass
