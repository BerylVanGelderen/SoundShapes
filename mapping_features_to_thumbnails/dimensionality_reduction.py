import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def list_strongest_correlations(df, n=10):
    """
    List the top n strongest correlations from the dataframe's correlation matrix.

    Parameters:
    df (pd.DataFrame): The input dataframe with columns representing labels.
    n (int): The number of top correlations to list.

    Returns:
    pd.DataFrame: A dataframe containing the strongest correlations.
    """
    correlation_matrix = df.corr()

    # Extract the upper triangle of the correlation matrix, excluding the diagonal
    corr_pairs = (
        correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
        .stack()
        .reset_index()
    )

    # Rename the columns
    corr_pairs.columns = ['Label 1', 'Label 2', 'Correlation']

    # Take the absolute value of the correlation to find the strongest correlations regardless of direction
    corr_pairs['AbsoluteCorrelation'] = corr_pairs['Correlation'].abs()

    # Sort the dataframe by the absolute correlation in descending order and take the top n
    strongest_correlations = corr_pairs.nlargest(n, 'AbsoluteCorrelation')

    return strongest_correlations[['Label 1', 'Label 2', 'Correlation']]


def plot_correlation_heatmap(df):
    """
    Plots a correlation matrix heatmap of the given DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame for which the correlation matrix heatmap is plotted.

    Returns:
    None
    """
    plt.figure(figsize=(10, 8))

    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)

    plt.title('Correlation Matrix Heatmap', fontsize=15)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.show()


def create_averaged_columns(df, pairs_to_average):
    """
    Create new columns by averaging the specified pairs of columns.

    Parameters:
    df (pd.DataFrame): The input dataframe.
    pairs_to_average (list of tuples): A list of tuples where each tuple contains two columns to be averaged and a new label.

    Returns:
    pd.DataFrame: The dataframe with new averaged columns added and the original columns removed if not used in subsequent operations.
    """
    new_df = df.copy()
    new_columns = {}  # Dictionary to keep track of newly created columns

    for col1, col2, new_label in pairs_to_average:
        # Use newly created columns if they exist, otherwise use original columns
        col1_final = new_columns.get(col1, col1)
        col2_final = new_columns.get(col2, col2)

        # Check if the columns exist in the dataframe or in the newly created columns
        if col1_final in new_df.columns and col2_final in new_df.columns:
            # Create a new column by averaging the two specified columns
            new_df[new_label] = new_df[[col1_final, col2_final]].mean(axis=1)
            new_columns[new_label] = new_label  # Add the new column to the dictionary

            new_df = new_df.drop(columns=[col1_final, col2_final])

            # print(f"Dropped columns {col1_final} and {col2_final}, and added new column {new_label}.")
        else:
            print(f"Columns {col1_final} or {col2_final} not found in the dataframe.")

    return new_df


def create_summed_columns(df, pairs_to_sum):
    """
    Create new columns by summing the specified pairs of columns.

    Parameters:
    df (pd.DataFrame): The input dataframe.
    pairs_to_sum (list of tuples): A list of tuples where each tuple contains two columns to be averaged and a new label.

    Returns:
    pd.DataFrame: The dataframe with new summed columns added and the original columns removed if not used in subsequent operations.
    """
    new_df = df.copy()
    new_columns = {}  # Dictionary to keep track of newly created columns

    for col1, col2, new_label in pairs_to_sum:
        # Use newly created columns if they exist, otherwise use original columns
        col1_final = new_columns.get(col1, col1)
        col2_final = new_columns.get(col2, col2)

        # Check if the columns exist in the dataframe or in the newly created columns
        if col1_final in new_df.columns and col2_final in new_df.columns:
            # Create a new column by summing the two specified columns
            new_df[new_label] = new_df[[col1_final, col2_final]].sum(axis=1)
            new_columns[new_label] = new_label  # Add the new column to the dictionary

            new_df = new_df.drop(columns=[col1_final, col2_final])

            # print(f"Dropped columns {col1_final} and {col2_final}, and added new column {new_label}.")
        else:
            print(f"Columns {col1_final} or {col2_final} not found in the dataframe.")

    return new_df

