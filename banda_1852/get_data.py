import pandas as pd

def get_cleaned_data(
    samples='full_samples.csv',
    geoclaw_inputs='full_params.csv',
    geoclaw_outputs='full_output.csv'
):
    """Samples are the sample parameters we are trying to find the posterior
    distribution for. Params are the Okada model parameters (which are
    determined using the sample parameters). The Okada model parameters are
    used as the input to the GeoClaw model. Output is the output of the GeoClaw
    model, which is a set of wave heights, wave arrival times, and inundation
    levels.

    We load all of these samples below, clean them up a bit, then return them.
    """
    full_output = pd.read_csv(geoclaw_outputs, index_col=0).reset_index(drop=True)
    full_params = pd.read_csv(geoclaw_inputs, index_col=0).reset_index(drop=True)
    full_samples = pd.read_csv(samples, index_col=0).reset_index(drop=True)

    # Combine depth and depth_offset.
    full_params['depth'] += full_params['depth_offset']
    # Drop rake (since it's constant), and drop depth_offset (since it's now
    # encapsulated by depth)
    full_params.drop(columns=['rake', 'depth_offset'], inplace=True)
    # Drop the inundation outputs (since they are so highly correlated with
    # wave height)
    full_output.drop(
        columns=['Banda Neira inundation', 'Saparua inundation'], inplace=True
    )

    # Drop duplicated input rows (there are many).
    full_samples = full_samples[~full_params.duplicated()]
    full_output = full_output[~full_params.duplicated()]
    full_params = full_params[~full_params.duplicated()]

    # Drop the rows where 'Banda Neira arrival' is less than 0.
    full_samples.drop(
        index=full_output[full_output['Banda Neira arrival'] < 0].index,
        inplace=True
    )
    full_params.drop(
        index=full_output[full_output['Banda Neira arrival'] < 0].index,
        inplace=True
    )
    full_output.drop(
        index=full_output[full_output['Banda Neira arrival'] < 0].index,
        inplace=True
    )

    return full_samples, full_params, full_output
