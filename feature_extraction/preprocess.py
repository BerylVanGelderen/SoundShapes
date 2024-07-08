import librosa
import numpy as np
import onnxruntime as ort
from scipy.special import softmax
import matplotlib.pyplot as plt
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

onnx_model_path = "clmr_sample-cnn.onnx"
sample_rate = 22050
input_sample_length = 59049
MTT_LABELS = ['guitar', 'classical', 'slow', 'techno', 'strings', 'drums', 'electronic', 'rock', 'fast', 'piano', 'ambient', 'beat', 'violin', 'vocal', 'synth', 'female', 'indian', 'opera', 'male', 'singing', 'vocals', 'no vocals', 'harpsichord', 'loud', 'quiet', 'flute', 'woman', 'male vocal', 'no vocal', 'pop', 'soft', 'sitar', 'solo', 'man', 'classic', 'choir', 'voice', 'new age', 'dance', 'male voice', 'female vocal', 'beats', 'harp', 'cello', 'no voice', 'weird', 'country', 'metal', 'female voice', 'choral']


# TODO: add comments to the functions

# Function to read audio file
def read_audio_file(file_path, sample_rate=sample_rate):
    audio_data, sr = librosa.load(file_path)
    if sr != sample_rate:
        raise ValueError(f"Sample rate must be {sample_rate} Hz")
    return audio_data


# Function to make predictions from samples
def make_predictions(samples, session):
    if samples.shape == (59049, ):
        # Reshape to (1, 1, 59049)
        samples = np.expand_dims(samples, axis=0)  # Shape: (1, 59049)
        samples = np.expand_dims(samples, axis=0).astype(np.float32)  # Shape: (1, 1, 59049)
        audio_tensor = ort.OrtValue.ortvalue_from_numpy(samples)
        results = session.run(None, {'audio': audio_tensor})
        prediction = results[0][0]
        prediction = softmax(prediction)
        return prediction
    elif samples.shape == (59049, 2):
        # Reshape to (1, 1, 59049)
        samples = samples.mean(axis=1) # from stereo to mono, shape (59049,)
        samples = np.expand_dims(samples, axis=0)  # Shape: (1, 59049)
        samples = np.expand_dims(samples, axis=0).astype(np.float32)  # Shape: (1, 1, 59049)
        audio_tensor = ort.OrtValue.ortvalue_from_numpy(samples)
        results = session.run(None, {'audio': audio_tensor})
        prediction = results[0][0]
        prediction = softmax(prediction)
        return prediction
    else:
        print("Input shape is wrong!")
        return None


def plot_predictions(df_row):
    predictions = df_row.values  # Get the values (predictions)
    labels = df_row.index  # Get the index (column names as labels)

    # Sort predictions in descending order
    sorted_indices = np.argsort(predictions)[::-1]  # Get indices sorted by value (descending)
    sorted_predictions = predictions[sorted_indices]  # Sort predictions
    sorted_labels = [labels[i] for i in sorted_indices]  # Sort labels according to sorted indices

    # Plotting the top 10 predictions
    plt.figure(figsize=(10, 4))
    plt.barh(sorted_labels[:10], sorted_predictions[:10])
    plt.xlabel("Probability")
    plt.title("Top 10 Predictions")
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest prediction at the top
    plt.show()


# Process all MP3 files and make predictions.
def process_audio_files_CLMR(mp3_files, input_sample_length=input_sample_length):
    all_files_predictions = {}
    session = ort.InferenceSession(onnx_model_path)
    print("ONNX model loaded.")

    for file_path in mp3_files:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        audio_data = read_audio_file(file_path)
        tracks_predictions = []

        for i in range(0, len(audio_data) - input_sample_length, input_sample_length):
            samples = audio_data[i:i + input_sample_length]
            predictions = make_predictions(samples, session)
            tracks_predictions.append(predictions)
        tracks_predictions_avg = np.mean(tracks_predictions, axis=0)
        all_files_predictions[file_name] = tracks_predictions_avg

    all_files_predictions_df = pd.DataFrame.from_dict(all_files_predictions, orient='index', columns=MTT_LABELS)
    return all_files_predictions_df

# Computes cosine similarity between vectors and returns the similarity matrix.
def compute_similarity_matrix(df, id_column, vector_columns):
    ids = id_column
    vectors = df[vector_columns].values

    similarity_matrix = cosine_similarity(vectors)

    similarity_df = pd.DataFrame(similarity_matrix, index=ids, columns=ids)

    return similarity_df

# Finds the top N most similar IDs to the input ID based on the similarity matrix.
def find_most_similar(similarity_df, input_id, top_n):
    if input_id not in similarity_df.index:
        raise ValueError(f"ID '{input_id}' not found in the similarity matrix.")

    similarity_scores = similarity_df.loc[input_id]
    similarity_scores = similarity_scores.drop(index=input_id)
    most_similar = similarity_scores.nlargest(top_n)

    # Convert the Series to a list of tuples (ID, similarity_score)
    similar_ids = list(most_similar.items())

    return similar_ids


def save_dataframe_to_csv(df, directory='.'):
    """
    Saves the DataFrame to a CSV file with a specific naming convention.
    The file name will be YYYYMMDD_NumberOfRowsOfTheDF.csv.
    If the file already exists, a numerical suffix is added.

    Parameters:
    df (pd.DataFrame): The DataFrame to save.
    directory (str): The directory where the file should be saved (default is current directory).

    Returns:
    str: The name of the file where the DataFrame was saved.
    """
    current_date = datetime.now().strftime('%Y%m%d')
    num_rows = df.shape[0]
    base_filename = f"{current_date}_{num_rows}tracks"
    file_path = os.path.join(directory, f"{base_filename}.csv")

    # Check if the file already exists, if it does, add a suffix.
    suffix = 0
    while os.path.exists(file_path):
        suffix += 1
        file_path = os.path.join(directory, f"{base_filename}_{suffix}.csv")

    df.to_csv(file_path, index_label='track_id')

    return file_path


def load_dataframe_if_exists_else_process_and_save(directory, mp3_files, processing_function, saving_function):
    """
    Loads a CSV file to a DataFrame if it exists, based on the number of rows in mp3_files.
    If the file does not exist, executes the specified function, saves the CSV and returns
    the DataFrame.

    Parameters:
    directory (str): The directory where to look for the CSV file.
    mp3_files (list): The list of mp3 files to determine the number of rows.
    execute_function (callable): The function to execute if the file does not exist.

    Returns:
    pd.DataFrame or None: The loaded DataFrame if the file exists, otherwise None.
    """
    # Determine the number of rows to match
    num_rows = len(mp3_files)

    # Construct the file search pattern
    search_pattern = f"_{num_rows}tracks.csv"

    # Search for the file in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(search_pattern):
            file_path = os.path.join(directory, file_name)
            print(f"Found matching file: {file_path}")
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path, index_col='track_id')
            return df

    # If no matching file is found, execute the specified function
    print("No matching file found. Executing the preprocessing function.")
    df = processing_function(mp3_files)
    print("Saving to csv.")
    saving_function(df, directory)
    return df

