

def drop_bad_channels(bad_channels, eeg):
    '''
    Drop bad channels based on subject ID. Bad channels are found after the first trial processing step.
    
    :param bad_channels: list of bad channels to drop
    :param eeg: eeg data to drop bad channels from

    :return: eeg data with bad channels dropped
    '''
    eeg.info['bads'] = bad_channels
    eeg_ica = eeg.copy().drop_channels(bad_channels)

    return eeg_ica


def reref(eeg):
    '''
    Reference EEG data to average of mastoids (TP9, TP10). If one mastoid is missing, reference to the other. If both are missing, raise an error.

    :param eeg: eeg data to be re-referenced

    :return: re-referenced eeg data
    '''
    has_tp9 = 'TP9' in eeg.ch_names
    has_tp10 = 'TP10' in eeg.ch_names

    if has_tp9 and has_tp10:
        eeg.set_eeg_reference(ref_channels=['TP9', 'TP10'])
    elif has_tp9:
        eeg.set_eeg_reference(ref_channels=['TP9'])
    elif has_tp10:
        eeg.set_eeg_reference(ref_channels=['TP10'])
    
    return eeg

def average_reference(eeg):
    '''
    Reference EEG data to average of all channels.

    :param eeg: eeg data to be re-referenced

    :return: re-referenced eeg data
    '''
    eeg.set_eeg_reference(ref_channels='average')
    return eeg