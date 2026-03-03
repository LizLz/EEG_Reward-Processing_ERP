import numpy as np
def interpolation(eeg, montage, verbose=True):
    '''
    Interpolates bad channels in the EEG data using common location.
    1. Adds placeholders for channels in the template but missing in the data.
    2. Maps coordinates from the template to all channels.
    3. Verifies coordinates to prevent [0,0,0] overlap crashes.
    4. Interpolates hardware bads and missing placeholders.
    
    :param eeg: eegh object with bad channels marked
    :param montage: MNE montage object with standard channel locations
    :param verbose: whether to print information about the interpolation process

    :return: eeg object with bad channels interpolated
    '''

    data = eeg.copy()

    # 1. Identify and remove extra channels (channels in data but NOT in location file)
    extra_channels = [ch for ch in data.ch_names if ch not in montage.ch_names]
    if extra_channels:
        if verbose:
            print(f"Removing extra channels: {extra_channels}")
        data.drop_channels(extra_channels, on_missing='ignore')

    # 2. identify channels the location file has but data doesn't
    missing_channels = [ch for ch in montage.ch_names if ch not in data.ch_names]
    if missing_channels:
        if verbose:
            print(f"Adding placeholders for missing channels: {missing_channels}")
        data.add_reference_channels(missing_channels)
        data.set_channel_types({ch: 'eeg' for ch in missing_channels})

    # 3. set montage
    data.set_montage(montage, on_missing='warn')

    # 4. verify coordinates to avoid [0,0,0] overlap crashes
    ch_indices = [data.ch_names.index(ch) for ch in missing_channels]
    invalid_placeholders = []

    for idx in ch_indices:
        pos = data.info['chs'][idx]['loc'][:3]
        if np.allclose(pos, 0, atol=1e-9):
            invalid_placeholders.append(data.ch_names[idx])

    if invalid_placeholders:
        if verbose:
            print(f"{invalid_placeholders} not found in common location file, removing placeholders.")
        data.drop_channels(invalid_placeholders)
        missing_channels = [ch for ch in missing_channels if ch not in invalid_placeholders]

    # 5. interpolation
    interpolated_names = list(set(data.info['bads'] + missing_channels))
    data.info['bads'] = interpolated_names

    if data.info['bads']:
        if verbose:
            print(f"Interpolating channels: {data.info['bads']}")
        data.interpolate_bads(reset_bads=True, origin='auto')
    elif verbose:
        print("No channels to interpolate.")

    return data