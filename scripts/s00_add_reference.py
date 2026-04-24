import mne

def add_reference_channel(raw, new_ref='Fz'):
    '''
    Add a new reference channel to the raw data. This is necessary for re-referencing later on.

    :param raw: raw EEG data to which the reference channel will be added
    :param new_ref: name of the new reference channel to be added

    :return: raw data with the new reference channel added'''
    mne.add_reference_channels(raw, new_ref, copy=False)  # add new_ref as reference channel
    return raw


def reref(eeg, verbose=True):
    '''
    Reference EEG data to average of mastoids (TP9, TP10).
    Faithful to EEGLAB pop_reref behavior: applies immediately,
    keeps mastoid channels in the data.

    :param eeg: eeg data to be re-referenced
    :param verbose: whether to print out which referencing method is being used

    :return: re-referenced eeg data
    '''
    has_tp9  = 'TP9'  in eeg.ch_names
    has_tp10 = 'TP10' in eeg.ch_names

    if has_tp9 and has_tp10:
        if verbose:
            print("Mastoid Reference: TP9 + TP10 (average).")
        eeg.set_eeg_reference(ref_channels=['TP9', 'TP10'], projection=False)
        # NOTE: keep TP9/TP10 in data → matches MATLAB pop_reref behavior

    elif has_tp9:
        if verbose:
            print("Mastoid Reference: TP9 only (TP10 missing).")
        eeg.set_eeg_reference(ref_channels=['TP9'], projection=False)

    elif has_tp10:
        if verbose:
            print("Mastoid Reference: TP10 only (TP9 missing).")
        eeg.set_eeg_reference(ref_channels=['TP10'], projection=False)

    else:
        raise ValueError(
            "Neither TP9 nor TP10 found in channel list. "
            f"Available channels: {eeg.ch_names}"
        )

    return eeg

def average_reference(eeg):
    '''
    Reference EEG data to average of all channels.
    For mne ica (our pipeline), which encourages general average reference

    :param eeg: eeg data to be re-referenced

    :return: re-referenced eeg data
    '''
    eeg.set_eeg_reference(ref_channels='average', projection=False)
    return eeg