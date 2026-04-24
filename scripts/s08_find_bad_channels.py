from logger import log_bad_channels

def find_bad_channels(epochs, reject_criteria, subject_id, rejection_info=None, logger=None, verbose=True):
    '''
    Find and print channels that exceed the rejection criteria based on epoch drops.

    :param epochs: MNE Epochs object
    :param reject_criteria: rejection criteria (e.g., 0.2 for 20%)
    :param rejection_info: dictionary mapping trial indices to lists of dropped channels
    :param subject_id: subject ID
    :param logger: logger object for logging bad channels
    :param verbose: boolean indicating whether to print detailed information
    :return: List of bad channels exceeding the rejection criteria


    :return: List of bad channels exceeding the rejection criteria
    '''
    n_total_epochs = len([log for log in epochs.drop_log if 'IGNORED' not in log])
    
    if n_total_epochs == 0:
        if verbose: print("No valid epochs found to analyze.")
        return []

    # Count drops per channel using the rejection_info dictionary
    channel_drop_counts = {ch: 0 for ch in epochs.info['ch_names']}

    if rejection_info:
        for reasons in rejection_info.values():
            for ch_name in reasons:
                if ch_name in channel_drop_counts:
                    channel_drop_counts[ch_name] += 1

    bad_channels_to_mark = []
    if verbose: print(f"--- Channel Rejection Summary (Total Epochs: {n_total_epochs}) ---")

    for ch_name in epochs.info['ch_names']:
        drop_count = channel_drop_counts.get(ch_name, 0)
        rejection_rate = drop_count / n_total_epochs

        if verbose and drop_count > 0: # Only print if there was at least one drop
            print(f"{ch_name}: {drop_count}/{n_total_epochs} drops ({rejection_rate:.1%})")

        if rejection_rate > reject_criteria:
            bad_channels_to_mark.append(ch_name)
    
    if verbose:
        print("---------------------------------")
        print(f"Channels exceeding {reject_criteria:.0%} threshold: {bad_channels_to_mark}")

    if logger:
        log_bad_channels(logger, subject_id, bad_channels_to_mark)

    return bad_channels_to_mark