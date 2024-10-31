from allosaurus.app import read_recognizer
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.utils import audio_dataset_from_directory
import numpy as np
import librosa
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K


max_length = 402

def get_allo_inference(audio_name):
    model = read_recognizer("finetuned")
    output = model.recognize(audio_name, 'deu')
    return output


def load_audio_file(file_path):
    # Load an audio file as a tensor, assume the file is a WAV file
    audio_binary = tf.io.read_file(file_path)
    audio, sample_rate = tf.audio.decode_wav(audio_binary)
    # Only use the first channel if it's stereo
    audio = audio[:, 0]
    return audio, sample_rate


def preprocess_audio_mfps(audio, sample_rate):
    # Cast audio to float32 and normalize
    audio = tf.cast(audio, tf.float32)
    audio = audio / 32768.0  # Normalize audio

    # Extract mel-frequency power spectra
    def _extract_mel(audio):
        # Compute mel-frequency power spectra
        stfts = tf.signal.stft(audio, frame_length=1024, frame_step=512, fft_length=1024)
        spectrograms = tf.abs(stfts)

        num_spectrogram_bins = stfts.shape[-1]
        lower_edge_hertz, upper_edge_hertz, num_mel_bins = 80.0, 7600.0, 128
        linear_to_mel_weight_matrix = tf.signal.linear_to_mel_weight_matrix(
            num_mel_bins, num_spectrogram_bins, sample_rate, lower_edge_hertz, upper_edge_hertz)

        mel_spectrograms = tf.tensordot(spectrograms, linear_to_mel_weight_matrix, 1)
        mel_spectrograms = tf.reshape(mel_spectrograms, [1, -1, 128])  # Reshape for batch dimension if needed
        return mel_spectrograms

    # Use tf.py_function to allow for eager execution of the extraction
    mel_spectra = tf.py_function(_extract_mel, [audio], tf.float32)
    return mel_spectra

def pad_sequence(seq):
    # Pad the sequence to the maximum length found in the training data
    padded_seq = tf.pad(seq, paddings=[[0, 0], [0, max_length - tf.shape(seq)[1]], [0, 0]], constant_values=0)
    return padded_seq


def contrastive_loss(y_true, y_pred, margin=1):
    # Calculate the Euclidean distance between the two outputs
    square_pred = tf.square(y_pred)
    margin_square = tf.square(tf.maximum(margin - y_pred, 0))
    return tf.reduce_mean(y_true * square_pred + (1 - y_true) * margin_square)

# Define cosine_similarity function as it's used in your Lambda layer
def cosine_similarity(vectors):
    x, y = vectors
    x = K.l2_normalize(x, axis=-1)
    y = K.l2_normalize(y, axis=-1)
    return K.sum(x * y, axis=-1, keepdims=True)


# Defining and loading the model outside so that once loaded the inference process is fast.
siamese_model_04 = load_model('siamese_models/best_model_0-4.h5', custom_objects={'contrastive_loss': contrastive_loss, 'cosine_similarity': cosine_similarity,'K': K},safe_mode=False)
siamese_model_59 = load_model('siamese_models/best_model_5-9.h5', custom_objects={'contrastive_loss': contrastive_loss, 'cosine_similarity': cosine_similarity,'K': K},safe_mode=False)
siamese_model_1014 = load_model('siamese_models/best_model_10-14.h5', custom_objects={'contrastive_loss': contrastive_loss, 'cosine_similarity': cosine_similarity,'K': K},safe_mode=False)
siamese_model_1519 = load_model('siamese_models/best_model_15-19.h5', custom_objects={'contrastive_loss': contrastive_loss, 'cosine_similarity': cosine_similarity,'K': K},safe_mode=False)
siamese_model_2060 = load_model('siamese_models/best_model_20-60.h5', custom_objects={'contrastive_loss': contrastive_loss, 'cosine_similarity': cosine_similarity,'K': K},safe_mode=False)
siamese_model_70100 = load_model('siamese_models/best_model_70-100.h5', custom_objects={'contrastive_loss': contrastive_loss, 'cosine_similarity': cosine_similarity,'K': K},safe_mode=False)

# getting inference.
def get_siamese_inference(audio_name,base_file,word):
    file_path = audio_name
    audio, sample_rate = load_audio_file(file_path)
    processed_audio = preprocess_audio_mfps(audio, sample_rate)
    processed_padded = pad_sequence(processed_audio)

    file_path_base = base_file
    audio_base, sample_rate_base = load_audio_file(file_path_base)
    processed_audio_base = preprocess_audio_mfps(audio_base, sample_rate_base)
    processed_padded_base = pad_sequence(processed_audio_base)

    if word in ["null","eins","zwei","drei","vier"]:
        output = siamese_model_04([processed_padded, processed_padded_base])
    elif word in ["fünf","sechs","sieben","acht","neun"]:
        output = siamese_model_59([processed_padded, processed_padded_base])
    elif word in ["zehn","elf","zwölf","dreizehn","vierzehn"]:
        output = siamese_model_1014([processed_padded, processed_padded_base])
    elif word in ["fünfzehn","sechszehn","siebzehn","achtzehn","neunzehn"]:
        output = siamese_model_1519([processed_padded, processed_padded_base])
    elif word in ["zwanzig","dreizig","vierzig","fünfzig","sechzig"]:
        output = siamese_model_2060([processed_padded, processed_padded_base])
    else:
        output = siamese_model_70100([processed_padded, processed_padded_base])

    final_output = float(output)

    return final_output
