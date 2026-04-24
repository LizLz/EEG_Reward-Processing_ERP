import mne
from mne_icalabel import label_components
from mne_icalabel.iclabel import iclabel_label_components
from logger import log_ica_exclusion
import config
from visualization import iclabel_visualize

def get_ica(trials, method='picard', save_path=None):
    '''
    Fit ICA on the given MNE Epochs object.
    
    :param trials_mne: MNE Epochs object containing EEG data.
    :param method: ICA method to use.
    :param save_path: Path to save the fitted ICA object.

    :return: Fitted ICA object.
    '''
    if method == 'picard':
        ica = mne.preprocessing.ICA(method=method, fit_params=dict(ortho=False, extended=True), random_state=2016)     # random_state for reproducibility (the authors used 2016)
    else:
        ica = mne.preprocessing.ICA(method=method, fit_params=dict(extended=True), random_state=2016)     # random_state for reproducibility
    ica.fit(trials,verbose=True)

    if save_path:
        ica.save(save_path, overwrite=True)
        print(f"ICA object saved to {save_path}")

    return ica


def get_iclabel(trials, ica, method='iclabel'):
    '''
    Get IC labels using the specified method.

    :param trials: MNE Epochs object containing EEG data.
    :param ica: Fitted ICA object.
    :param method: Method to use for labeling components.

    :return: IC labels.
    '''
    # IC_label expects filtered between 1 and 100 Hz, reference to be common average and ica method to be infomax
    trials.load_data()
    ic_labels = label_components(trials, ica, method=method)

    return ic_labels

def iccomponent_removal(eeg, trials, ica, subject_id, active_pipeline,logger=None, save_path=None):
    '''
    Remove bad IC components based on the given criteria.

    :param eeg: MNE Raw object containing EEG data.
    :param ica: Fitted ICA object.
    :param exclude_idx: List of indices of IC components to exclude.
    :param logger: Logger object to log the exclusion.
    :param save_path: Path to save the cleaned MNE Raw object.

    :return: Cleaned MNE Raw object.
    '''

    exclude_idx = config.SUBJECT_INFO[subject_id]['ic_excluded'][active_pipeline]   # check is exclude idx is already saved

    if not exclude_idx:
        exclude_idx = []
        label_dict = {
            'brain': 0,
            'muscle': 1,
            'eye blink': 2,
            'eye movement': 3,
            'heart': 4,
            'line noise': 5,
            'channel noise': 6,
            'other': 7
        }
        trials.load_data()  # ensure data is loaded before labeling
        all_labels = iclabel_label_components(trials, ica)
        for i, probabilities in enumerate(all_labels):
            if active_pipeline == 'original':
                if probabilities[label_dict['eye blink']] > probabilities[label_dict['brain']] or \
                    probabilities[label_dict['eye movement']] > probabilities[label_dict['brain']]:
                    exclude_idx.append(i)
            elif active_pipeline == 'proposed':
                 if probabilities[label_dict['brain']] < 0.3: # set this because lowest probability for each component to be the most imporant label is around 0.3
                    exclude_idx.append(i)
            else:
                raise ValueError(f'Unknown pipeline: {active_pipeline}')
        if save_path:
        # Save a plot of the excluded components to a folder
            iclabel_visualize(ica, all_labels[exclude_idx], exclude_idx=exclude_idx, show=False, save_path=save_path)
    # logging 
    if logger:
        log_ica_exclusion(logger, subject_id, exclude_idx, ica.n_components_)


    ica.exclude = exclude_idx
    ica.apply(eeg)

    return eeg
