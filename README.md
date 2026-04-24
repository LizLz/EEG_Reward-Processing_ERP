# EEG_Reward-Processing_ERP
# Reproduce ERP analysis from *Task-level value affects trial-level reward processing*

**Author:** *Zheng Lin*
Some code skeletons are credited to Qianyue Li and Yanhong Xu.

**Year:** *2026*

## Project Description
This is the project for EEG course. I made some adjustment based on the final version submitted to play round the parameters for further analysis.

This project aims to reproduce the ERP analysis from the study titled [*Task-level value affects trial-level reward processing*](https://www.biorxiv.org/lookup/doi/10.1101/2021.09.16.460600). The analysis focuses on understanding how task-level value influences reward processing at the trial level using EEG data.

We would compare the analysis results from our own pipeline with the original study.

## Pipeline Comparison
| Step | Authors | Us |
| ---- | -------- | -------- |
| Bad Channels | Auto Rejection | Same |
| Downsampling | 1000Hz -> 250 Hz | Same |
| Filter | 0.1Hz~30Hz | **0.1Hz~40Hz** |
| 50Hz noise removal | Notch | **Zapline** |
| Re-reference | average of left and right mastoids | **mastoids + general average** |
| ICA | Runica | **Picard (faster)** |
| Artefacts removal | IC-Label | Same |
| ERP Analysis | Mean | Same |
| Trial-level averaging | Mean | **Trimmed Mean** |
| Statistic | rmANOVA & rmT-tests | Same |

## Dataset Download
The dataset used in this project can be downloaded from the following link: [Dataset Link](https://nemar.org/dataexplorer/detail?dataset_id=ds004147). 
