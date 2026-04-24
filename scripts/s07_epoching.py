import mne
from s03_07_trial_rejection import trial_rejection
from tools import get_event_dict

def epoching(eeg, conditions_dict, maxMin=150e-6, level=150e-6, step=40e-6, lowest=0.1e-6, tmin=-0.2, tmax=0.6, baseline=(-0.2, 0)):
    '''
    Epoching the continuous EEG data based on the provided conditions dictionary,
    and applying trial rejection.

    :param conditions_dict: dictionary mapping condition names to event markers
    :param eeg: MNE Raw object containing the continuous EEG data
    :param maxMin: max-min threshold for trial rejection
    :param level: level threshold for trial rejection
    :param step: step size for trial rejection
    :param lowest: lowest threshold for trial rejection
    :param tmin: start time for epoching
    :param tmax: end time for epoching
    :param baseline: tuple defining the baseline correction period

    :return: MNE Epochs object containing the epoched and cleaned data
    '''

    # get all the feedback-locked stimulus
    stim_dict = []
    for condition in conditions_dict.values():
        stim_dict.extend(condition)
    unique_stim = list(set(stim_dict)) # remove duplicates to avoid double-epoching

    epochs_all, rejected_info = trial_rejection(eeg, unique_stim, maxMin=maxMin, level=level, step=step, lowest=lowest,  tmin=tmin, tmax=tmax, baseline=baseline)

    return epochs_all, rejected_info

