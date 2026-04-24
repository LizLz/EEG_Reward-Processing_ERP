from meegkit.dss import dss_line
import numpy as np

def down_sampling(eeg, new_sfreq=250, verbose=True):
    '''
    Downsample the eeg signal.
    
    :param eeg: eeg signal to be processed
    :param new_sfreq: the frequency after downsampling

    :return: downsampled eeg signal
    '''
    eeg_down = eeg.copy().resample(new_sfreq, npad='auto')

    if verbose:
        print(f"Original Sampling Rate: {eeg.info['sfreq']} Hz")
        print(f"New Sampling Rate: {eeg_down.info['sfreq']} Hz")

    return eeg_down


def band_filter(eeg, f_low=0.1, f_high=30):
    '''
    Perform bandpass filtering on the downsampled eeg signal.
    
    :param eeg: eeg signal to be processed
    :param f_low: low cutoff frequency
    :param f_high: high cutoff frequency

    :return: bandpass filtered eeg signal
    '''
    eeg_band = eeg.copy().filter(l_freq=f_low, h_freq=f_high, n_jobs=-1)

    return eeg_band


def notch_filter(eeg, line_freq=50):
    '''
    Perform notch filtering on the bandpass filtered eeg signal.
    Automatically removes all harmonics within the signal bandwidth.

    :param eeg: eeg signal to be processed
    :param line_freq: line frequency to be removed

    :return: notch filtered eeg signal
    '''
    nyquist = eeg.info['sfreq'] / 2
    freqs = [line_freq * i for i in range(1, int(nyquist // line_freq) + 1)]
    
    print(f"[Notch] Removing: {freqs} Hz")

    eeg_notch = eeg.copy().notch_filter(freqs=freqs, n_jobs=-1)

    return eeg_notch


def zapline_filter(eeg, line_freq=50, nremove=3):
    band_sfreq = eeg.info['sfreq']
    nyquist = band_sfreq / 2

    # Collect all harmonics within bandwidth
    harmonics = [line_freq * i for i in range(1, int(nyquist // line_freq) + 1)]
    
    print(f"[Zapline] Removing harmonics: {harmonics} Hz with nremove={nremove}")

    # (n_samples, n_channels, n_trials)
    eeg_array = np.expand_dims(eeg.get_data().T, axis=2)

    for freq in harmonics:
        eeg_array, artifact = dss_line(
            eeg_array,
            fline=freq,
            sfreq=band_sfreq,
            nremove=nremove,
        )

    eeg._data = eeg_array.squeeze().T
    return eeg