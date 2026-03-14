# COVID-19 Pandemic and Cultural Values: A Weibo-based Study

## Lexicon Revision
The folder 1_Individualism-Collectivism_Lexicon_Revision is used for calculating PC values.

## Screening Weibo Users
Scripts for screening Weibo users are located in the 2_Weibo_User_Screening folder.

| File | Link | Password | Destination |
|------|------|----------|-------------|
| `1_raw_user_data.zip` | [Download](https://pan.baidu.com/s/16OOTXRC8urJMFZyKYZovpw?pwd=xent) | `xent` | `2_Weibo_User_Screening/` |
| `2_filtered_Weibo_posts.zip` | [Download](https://pan.baidu.com/s/1S6lxhBHwMxxKSTq-ci1GBw?pwd=y1mj) | `y1mj` | `2_Weibo_User_Screening/` |

### Steps
1. Download both files from Baidu Pan.
2. Move `.zip` files into `2_Weibo_User_Screening/`.
3. Run screening scripts to identify eligible users.

## Time-series Textual Data

| File | Link | Password | Action |
|------|------|----------|--------|
| `3_time-series_textual_data.zip` | [Download](https://pan.baidu.com/s/12pk_ymjn5F-OfsJ2OshC3Q?pwd=y3vx) | `y3vx` | Download → Move to **Root** → Unzip |

```bash
mv 3_time-series_textual_data.zip ./
unzip 3_time-series_textual_data.zip
```

## I-C LS Score Calculation
The folder 4_I-C_LS_Score_Calculation contains resources for calculating Individualism, Collectivism, and Life Satisfaction scores.
The data file `1_data.zip` can be found at https://pan.baidu.com/s/1a2C8v649WGjx8ju8LRuIEg?pwd=n3xt. 
Please download and move it into the folder `4_I-C_LS_score_calculation\2_life_satisfaction\1_LS_model_training`, then unzip it.

The data file `2_calculate_life_satisfaction.zip`  can be found at https://pan.baidu.com/s/1i0VvVfdScU_oivtCM8yERA?pwd=y2qn. 
Please download and move it into the folder `4_I-C_LS_score_calculation\2_life_satisfaction\2_calculate_life_satisfaction`, then unzip it.

| File | Link | Password | Destination |
|-----|------|----------|-------------|
| `1_data.zip` | [Download](https://pan.baidu.com/s/1a2C8v649WGjx8ju8LRuIEg?pwd=n3xt) | `n3xt`   | `/4_I-C_LS_Score_Calculation/2_life_satisfaction/1_LS_model_training/` |
| `2_calculate_life_satisfaction.zip` | [Download](https://pan.baidu.com/s/1i0VvVfdScU_oivtCM8yERA?pwd=y2qn) | `y2qn`   | `./4_I-C_LS_Score_Calculation/2_life_satisfaction/2_calculate_life_satisfaction/` |


### Steps
#### LS Model Training Data
```
mv 1_data.zip ./4_I-C_LS_Score_Calculation/2_life_satisfaction/1_LS_model_training/
cd ./4_I-C_LS_Score_Calculation/2_life_satisfaction/1_LS_model_training/
unzip 1_data.zip
```

#### LS Calculation Module
```
mv 2_calculate_life_satisfaction.zip ./4_I-C_LS_Score_Calculation/2_life_satisfaction/2_calculate_life_satisfaction/
cd ./4_I-C_LS_Score_Calculation/2_life_satisfaction/2_calculate_life_satisfaction/
unzip 2_calculate_life_satisfaction.zip
```

## Time Series Analysis
The folder 5_Time_Series_Analysis contains three subfolders: 1_Individualism, 2_Collectivism, and 3_Life_Satisfaction, which are used for the analysis of individualism, collectivism, and life satisfaction, respectively.

## Cross-Lagged Calculation
The folder 6_Cross-Lagged_Calculation is used for analyzing cross-lagged data.

## Overview
Project Structure Overview
```
📦 Project Root
├── 1_Individualism-Collectivism_Lexicon_Revision/
├── 2_Weibo_User_Screening/
│   ├── 1_raw_user_data.zip          [Download Required]
│   └── 2_filtered_Weibo_posts.zip   [Download Required]
├── 3_time-series_textual_data.zip   [Download → Root → Unzip]
├── 4_I-C_LS_Score_Calculation/
│   └── 2_life_satisfaction/
│       ├── 1_LS_model_training/
│       │   └── 1_data.zip           [Download & Extract Here]
│       └── 2_calculate_life_satisfaction/
│           └── 2_calculate_life_satisfaction.zip  [Download & Unzip Here]
├── 5_Time_Series_Analysis/
│   ├── 1_Individualism/
│   ├── 2_Collectivism/
│   └── 3_Life_Satisfaction/
└── 6_Cross-Lagged_Calculation/
```
