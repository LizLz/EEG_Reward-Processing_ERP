# -------- General parameters --------
BIDS_ROOT = {"zheng": "C:\\Users\\Zheng\\Desktop\\EEG Project\\EEG_Reward-Processing_ERP\\dataset\\ds004147\\ds004147"}

LOCS_FILENAME = {  
    'site2': 'site2channellocations.locs',
    'common': 'common.locs'
}

# -------- Data parameters --------
SUBJECT_INFO = {
    '27': {'learner': True,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0, 5, 12],
             'proposed': [0, 1, 2, 4, 5, 6, 7, 8, 14, 17, 18, 29]}},
    '28': {'learner': True,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0, 5, 10, 18, 20, 26],
             'proposed': [0, 1, 2, 3, 8, 11, 21, 27, 30]}},
    '29': {'learner': False,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0, 10, 20],
             'proposed': [0, 5, 6, 7, 10, 11, 16, 18, 21, 24, 25, 27, 29]}},
    '30': {'learner': False,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0, 1, 5],
             'proposed': [0, 1, 2, 3, 7, 12, 15, 18, 23]}},
    '31': {'learner': True,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0, 3, 5],
             'proposed': [0, 1, 2, 7, 10, 11, 17, 23, 27, 29]}},
    '32': {'learner': False,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0, 1, 8, 12],
             'proposed': [0, 1, 2, 3, 4, 7, 9, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 28]}},
    '33': {'learner': False,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [1, 25, 27],
             'proposed': [0, 1, 2, 7, 8, 9, 14, 16, 17, 18, 19, 20, 23, 28]}},
    '34': {'learner': True,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0, 1, 2, 10],
             'proposed': [0, 3, 6, 11, 12, 13, 20]}},
    '35': {'learner': True,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0, 6],
             'proposed': [0, 1, 2, 6, 7, 11, 13, 16, 19, 21, 22, 23, 24, 28, 29, 30]}},
    '36': {'learner': True,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0, 1, 2, 3, 7, 12, 16, 21],
             'proposed': [0, 1, 2, 6, 7, 10, 13, 14, 15, 16, 17, 24]}},
    '37': {'learner': True,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0],
             'proposed': [0, 7, 8, 14, 17, 18, 28, 29]}},
    '38': {'learner': True,
           'bad_channels': 
            {'original': [],
             'proposed': []},
           'ic_excluded':
            {'original': [0, 1, 5, 10, 14],
             'proposed': [0, 6, 7, 10, 20]}},
}

CONDITIONS_DICT = {
    'onset_locked':[
        'Stimulus:S  1', 'Stimulus:S 11', 'Stimulus:S 21', 'Stimulus:S 31'
    ],
    'feedback_locked':{
    'Low-Low Win':   ['Stimulus:S  6'], 
    'Low-Low Loss':  ['Stimulus:S  7'], 
    'Mid-Low Win':   ['Stimulus:S 16'], 
    'Mid-Low Loss':  ['Stimulus:S 17'], 
    'Mid-High Win':  ['Stimulus:S 26'], 
    'Mid-High Loss': ['Stimulus:S 27'],
    'High-High Win': ['Stimulus:S 36'], 
    'High-High Loss':['Stimulus:S 37'],
    }
}

# -------- Preprocessing parameters --------
SAMPLING_RATE = 250  # in Hz
NOTCH_FREQS = 50  # in Hz

# -------- Pipeline parameters --------
PIPELINES = {
    'original':{
        'ica_method': 'infomax',
        'ica_criteria': None, 
        'bandpass_filter': {
            'f_low': 0.1,
            'f_high': 30,
            },
        'rejection_params': { #trial rejection
            'ica':{
                'maxMin': 500e-6,
                'level': 500e-6,
                'step': 40e-6,
                'lowest': 0.1e-6,
                'tmin': 0,
                'tmax': 3,
                'baseline': None
            },
            'erp':{
                'maxMin': 150e-6,
                'level': 150e-6,
                'step': 40e-6,
                'lowest': 0.1e-6,
                'tmin': -0.2,
                'tmax': 0.6,
                'baseline': (-0.2, 0)
            }
        },
        'bad_channels_rejection_criteria': 0.2, # 20%
        'epoch_tmin': -0.2,
        'epoch_tmax': 0.6,
        'early_trial_deletion': 10, # delete first 10 trials to avoid learning effects
        'evoked_proportiontocut': 0.00 # no trimming
    },
    'proposed':{
        'ica_method': 'picard',
        'ica_criteria': None,
        'bandpass_filter': {
            'f_low': 0.1,
            'f_high': 50,
            },
        'rejection_params': { #trial rejection
            'ica':{
                'maxMin': 500e-6,
                'level': 500e-6,
                'step': 40e-6,
                'lowest': 0.1e-6,
                'tmin': 0,
                'tmax': 3,
                'baseline': None
            },
            'erp':{
                'maxMin': 150e-6,
                'level': 150e-6,
                'step': 40e-6,
                'lowest': 0.1e-6,
                'tmin': -0.2,
                'tmax': 0.6,
                'baseline': (-0.2, 0)
            }
        },
        'bad_channels_rejection_criteria': 0.2, # 20%
        'epoch_tmin': -0.2,
        'epoch_tmax': 0.6,
        'early_trial_deletion': 10, # delete first 10 trials to avoid learning effects
        'evoked_proportiontocut': 0.05 # 5% trimming
    }
}

N_BINS = 5