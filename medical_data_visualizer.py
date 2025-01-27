import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 Import the data
df = pd.read_csv('medical_examination.csv')

# 2 Add 'overweight' colum
df['BMI'] = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (df['BMI'] > 25).astype(int)
df.drop(columns=['BMI'], inplace=True)
# 3 Normalize data by ,alomg 0 always good and 1 always bad 
df['cholesterol']= (df['cholesterol'] > 1).astype(int)

df['gluc'] = (df['gluc'] > 1).astype(int)

# 4 draw categorical Plot
def draw_cat_plot():
    # 5 Create datagrame for cat plot using 'pd.melt'
    df_cat = pd.melt(
        df,
        id_vars = ['cardio'],
        value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )


    # 6 Group and reformat the data to split it by 'cardio'
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).size()
    

    # 7 Rename column for the catplot to work correctly
    df_cat = df_cat.rename(columns={'size': 'total'})


    # 8 Draw the catplot using sns.catplot()
    fig = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar'
    ).figure

    


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11 Clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12 Calculate the correlation matrix
    corr = df_heat.corr()

    # 13 Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14 Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # 15 Draw the heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        square=True,
        cbar_kws={'shrink': .5},
        cmap='coolwarm',
        ax=ax
    )


    # 16
    fig.savefig('heatmap.png')
    return fig
