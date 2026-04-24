from matplotlib import pyplot as plt
import numpy as np
import mne
from matplotlib.backends.backend_pdf import PdfPages



def show_single_psd(eeg_data, y_min=-50, y_max=50, picks=None, title=None):
    '''
    Plot the power spectral density (PSD) of EEG data.

    :param eeg_data: MNE Raw or Epochs object
    :param y_min: Minimum y-axis value for the plot
    :param y_max: Maximum y-axis value for the plot
    :param picks: Channels to include in the plot
    :param title: Title for the plot
    '''
    eeg_psd = eeg_data.compute_psd().plot(picks=picks, show=False)
    ax = eeg_psd.axes[0]
    y_min = y_min
    y_max = y_max
    ax.set_ylim(y_min, y_max)
    ax.set_title(title)
    plt.show()



def psd_compare(eegs, labels, title, figsize=(8, 6), picks=['FCz'], y_min=-46.4, y_max=-46, x_min=49.5, x_max=50.5):
    '''
    Compare power spectral density (PSD) of EEG data across different preprocessing strategies.

    :param eegs: List of MNE Raw or Epochs objects
    :param labels: List of labels for each EEG object
    :param title: Title for the plot
    :param figsize: Figure size tuple (width, height)
    :param picks: Channels to include in the plot
    :param y_min: Minimum y-axis value for the plot
    :param y_max: Maximum y-axis value for the plot
    :param x_min: Minimum x-axis value for the plot
    :param x_max: Maximum x-axis value for the plot
    '''
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    freqs = eegs[0].compute_psd(picks=picks).freqs  # assuming the same sfreq
    
    # Iterate through EEG objects and plot the PSD data
    for i, eeg in enumerate(eegs):
        # Compute the PSD for the selected picks
        psd = eeg.compute_psd(picks=picks)
        
        # Get the power data (it returns channels x frequencies, so we average across channels)
        # Note: If picks contains multiple channels, this averages them for a cleaner comparison.
        # 1e12 for scaling, sticking to the default psd calculation in psd
        power_data = np.mean(10 * np.log10(psd.get_data() * 1e12), axis=0)
        
        ax.plot(
            freqs, 
            power_data, 
            label=labels[i], 
            linewidth=2
        )

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power (dB/Hz)')

    #ax.set_ylim(y_min, y_max)
    #ax.set_xlim(x_min, x_max)
    
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    
    plt.show()



def iclabel_visualize(ica, ic_labels, exclude_idx=None, show=False, trials=None, save_path=None):
    '''
    Visualize Independent Component Analysis (ICA) components with their corresponding labels and probabilities.
    '''
    label_dict = ['brain', 'muscle', 'eye blink', 'eye movement', 'heart', 'line noise', 'channel noise', 'other']

    # plot out scalp picture and the auto ic label
    titles = []
    for probabilities in ic_labels:
        max_prob = np.max(probabilities)
        label_idx = np.argmax(probabilities)
        label = label_dict[label_idx]
        print(f'The label with highest probabiliy ({max_prob}) is {label}')
        
        title = f"{label.capitalize()} ({max_prob:.0%})"
        titles.append(title)


    figs = ica.plot_components(picks=exclude_idx, inst=trials, show=False)

    if not isinstance(figs, list):
        figs = [figs]

    comp_idx = 0
    for fig in figs:
        fig.set_layout_engine(None)
        fig.subplots_adjust(hspace=0.6, wspace=0.1, bottom=0.15)
        for ax in fig.axes:
            if comp_idx >= len(titles):
                break
                
            ax.text(0.5, -0.3, titles[comp_idx], 
                    transform=ax.transAxes, 
                    ha='center', va='top', fontsize=9, color='black', fontweight='bold')
            
            comp_idx += 1

    if show:
        plt.show();
    if save_path:
        with PdfPages(save_path) as pdf:
            for fig in figs:
                pdf.savefig(fig)
        print(f'Save ')




def plot_erp(evokeds, channel='FCz', mean_window=[0.240, 0.340], ylim=[-10, 20], diff=False, title=None):

    '''
    Plot ERP waveforms with mean amplitude window shading.
    
    :param evokeds: Dictionary of MNE Evoked objects
    :param channel: Channel name to plot
    :param mean_window: Tuple indicating the start and end of the mean amplitude window (in seconds)
    :param colors: colors for each condition
    :param linestyles: linestyles for each condition
    :param title: Title for the plot
    '''
    if diff:
        colors = {
        'Low-Low': '#4C72B0',   # Muted Blue
        'Mid-Low': '#64B5CD',   # Soft Cyan
        'Mid-High': '#E1BC66',  # Sand/Gold
        'High-High': '#C44E52'  # Muted Crimson 
        }
        linestyles = None
    else:
        colors = {
        'Low-Low Win': 'red', 'Low-Low Loss': 'blue',
        'Mid-Low Win': 'red', 'Mid-Low Loss': 'blue',
        'Mid-High Win': 'red', 'Mid-High Loss': 'blue',
        'High-High Win': 'red', 'High-High Loss': 'blue'
        }
        linestyles = {
            'Low-Low Win': '-', 'Low-Low Loss': '-',
            'Mid-Low Win': '--', 'Mid-Low Loss': '--',
            'Mid-High Win': '-.', 'Mid-High Loss': '-.',
            'High-High Win': ':', 'High-High Loss': ':'
        }

    # Create figure
    fig, axes = plt.subplots(1, 1, figsize=(12, 5), sharex=True, sharey=True)
    mne.viz.plot_compare_evokeds(
        evokeds,
        picks=[channel],
        colors=colors,
        linestyles=linestyles,
        axes=axes,
        title=title,   #NOTE: to be changed
        legend='upper right',
        ci=True,
        show=False,
        show_sensors=False,
        ylim=dict(eeg=ylim)
    )
    # Add shading for Mean Amplitude window
    axes.axvspan(mean_window[0], mean_window[1], color='gray', alpha=0.2, label=f'Mean Window ({mean_window[0]*1000:.0f}-{mean_window[1]*1000:.0f}ms)')
    plt.show();


def plot_topo_serires(evokeds, times=[0.18, 0.22, 0.26, 0.30, 0.34, 0.38], vlimit=(-5, 5)):
    '''
    Plot topo series for the grand average erps
    '''
    # 1. Load the standard 10-05 montage (includes PO7, POz, PO8) outside the loop for speed
    montage = mne.channels.make_standard_montage('standard_1005')

    for condition, evoked in evokeds.items():
        print(f"Plotting Topomap for: {condition}")
        
        # 2. Apply the montage to give MNE the physical coordinates
        # match_case=False fixes capitalization issues (e.g., 'POz' vs 'poz')
        # on_missing='ignore' prevents crashes if a weird channel name slipped through
        evoked.set_montage(montage, match_case=False, on_missing='ignore')
        
        # 3. Generate the 2D plot
        evoked.plot_topomap(times=times, ch_type='eeg', colorbar=True, vlim=vlimit)

def plot_cleaning_compare(before_eeg, after_eeg, tmin=100, tmax=105, title=None):
    '''
    Plot butterfly plot comparing EEG data before and after cleaning.
    '''
    mask_before = (before_eeg.times >= tmin) & (before_eeg.times <= tmax)
    mask_after = (after_eeg.times >= tmin) & (after_eeg.times <= tmax)

    data_before = before_eeg.get_data()[:, mask_before] * 1e6
    data_after = after_eeg.get_data()[:, mask_after] * 1e6

    times_before = before_eeg.times[mask_before]
    times_after = after_eeg.times[mask_after]

    n_channels = data_before.shape[0]
    ch_names = before_eeg.ch_names

    fig, axes = plt.subplots(n_channels, 1, figsize=(14, n_channels * 0.4), sharex=True)
    fig.subplots_adjust(hspace=0)

    for i, ax in enumerate(axes):
        ch_std = np.std(data_after[i])
        ylim = (-15 * ch_std, 15 * ch_std)
        
        # demean each channel so DC offset doesn't push lines off scale
        before_demeaned = data_before[i] - np.mean(data_before[i])
        after_demeaned = data_after[i] - np.mean(data_after[i])
        
        ax.plot(times_after, after_demeaned, color="blue", alpha=0.4, linewidth=0.5, clip_on=False)
        ax.plot(times_before, before_demeaned, color="red", alpha=0.7, linewidth=0.5, clip_on=False)
        ax.set_ylim(ylim)
        ax.set_ylabel(ch_names[i], rotation=0, labelpad=40, fontsize=7)
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    axes[0].set_title(title)
    axes[-1].set_xlabel("Time (s)")
    axes[0].plot([], color="red", label="before")
    axes[0].plot([], color="blue", label="after")
    axes[0].legend(fontsize=7, loc="upper right")

    plt.tight_layout()
    plt.show()

def plot_butterfly_evokeds(evokeds_dict, title=None):
    '''
    Plot butterfly plot for evoked data across all conditions.
    '''
    all_condition_evoked = mne.grand_average(list(evokeds_dict.values()))
    all_condition_evoked.plot(titles=title);