import pandas as pd
import numpy as np

def calcular_mediacg(_df):
    final_df = _df.copy()

    def calcular_media(row):
        date, home, away = row['Date'], row['Home'], row['Away']

        df_cum = _df[(_df['Date'] < date) & ((_df['Home'] == home) | (_df['Away'] == home))].tail(3)
        if len(df_cum) == 3:
            df_cum.loc[(df_cum['Home'] == home), 'real_cg'] = df_cum['CustoGolHome']
            df_cum.loc[(df_cum['Away'] == home), 'real_cg'] = df_cum['CustoGolAway']
            media_CG = df_cum['real_cg'].mean()
            dp_CG = df_cum['real_cg'].std()
            cv_CG = dp_CG / media_CG
            final_df.loc[row.name, 'Avg_CG_H'] = media_CG
            final_df.loc[row.name, 'DP_CG_H'] = dp_CG
            final_df.loc[row.name, 'CV_CG_H'] = cv_CG
        else:
            final_df.loc[row.name, 'Avg_CG_H'] = 0
            final_df.loc[row.name, 'DP_CG_H'] = 0
            final_df.loc[row.name, 'CV_CG_H'] = 0

        df_cum = _df[(_df['Date'] < date) & ((_df['Home'] == away) | (_df['Away'] == away))].tail(3)
        if len(df_cum) == 3:
            df_cum.loc[(df_cum['Home'] == away), 'real_cg'] = df_cum['CustoGolHome']
            df_cum.loc[(df_cum['Away'] == away), 'real_cg'] = df_cum['CustoGolAway']
            media_CG = df_cum['real_cg'].mean()
            dp_CG = df_cum['real_cg'].std()
            cv_CG = dp_CG / media_CG
            final_df.loc[row.name, 'Avg_CG_A'] = media_CG
            final_df.loc[row.name, 'DP_CG_A'] = dp_CG
            final_df.loc[row.name, 'CV_CG_A'] = cv_CG
        else:
            final_df.loc[row.name, 'Avg_CG_A'] = 0
            final_df.loc[row.name, 'DP_CG_A'] = 0
            final_df.loc[row.name, 'CV_CG_A'] = 0

    _df.apply(calcular_media, axis=1)

    return final_df


# Cria classes do target
def cria_alvos(_df):
    # Back Home
    _df.loc[(_df['Home_Pts'] > _df['Away_Pts']), 'Back_Home'] = 1
    _df.loc[(_df['Home_Pts'] < _df['Away_Pts']), 'Back_Home'] = 0
    _df.loc[(_df['Back_Home'] == 1), 'PL_Home'] = _df['Odds_H'] - 1
    _df.loc[(_df['Back_Home'] == 0), 'PL_Home'] = - 1

    # Back Away
    _df.loc[(_df['Home_Pts'] < _df['Away_Pts']), 'Back_Away'] = 1
    _df.loc[(_df['Home_Pts'] > _df['Away_Pts']), 'Back_Away'] = 0
    _df.loc[(_df['Back_Away'] == 1), 'PL_Away'] = _df['Odds_A'] - 1
    _df.loc[(_df['Back_Away'] == 0), 'PL_Away'] = - 1
    
    # Over/Under
    _df.loc[(_df['Home_Pts'] + _df['Away_Pts']) > _df['Over_Line'], 'Back_Over'] = 1
    _df.loc[(_df['Home_Pts'] + _df['Away_Pts']) < _df['Over_Line'], 'Back_Over'] = 0
    _df.loc[(_df['Home_Pts'] + _df['Away_Pts']) == _df['Over_Line'], 'Back_Over'] = 2

    _df.loc[(_df['Home_Pts'] + _df['Away_Pts']) > _df['Over_Line'], 'Back_Under'] = 0
    _df.loc[(_df['Home_Pts'] + _df['Away_Pts']) < _df['Over_Line'], 'Back_Under'] = 1
    _df.loc[(_df['Home_Pts'] + _df['Away_Pts']) == _df['Over_Line'], 'Back_Under'] = 2
    
    _df.loc[(_df['Back_Over'] == 1), 'PL_Over'] = _df['Odds_Over'] - 1
    _df.loc[(_df['Back_Over'] == 0), 'PL_Over'] = - 1
    _df.loc[(_df['Back_Under'] == 1), 'PL_Under'] = _df['Odds_Under'] - 1
    _df.loc[(_df['Back_Under'] == 0), 'PL_Under'] = - 1
    _df.loc[(_df['Back_Over'] == 2), 'PL_Over'] = 0
    _df.loc[(_df['Back_Under'] == 2), 'PL_Under'] = 0
    
    # HA
    
    # Back H
    _df.loc[((_df['Home_Pts'] + _df['HA_Line'])) > _df['Away_Pts'], 'Back_HA_H'] = 1
    _df.loc[((_df['Home_Pts'] + _df['HA_Line'])) < _df['Away_Pts'], 'Back_HA_H'] = 0
    _df.loc[((_df['Home_Pts'] + _df['HA_Line'])) == _df['Away_Pts'], 'Back_HA_H'] = 2
    # Back A
    _df.loc[((_df['Home_Pts'] + _df['HA_Line'])) > _df['Away_Pts'], 'Back_HA_A'] = 0
    _df.loc[((_df['Home_Pts'] + _df['HA_Line'])) < _df['Away_Pts'], 'Back_HA_A'] = 1
    _df.loc[((_df['Home_Pts'] + _df['HA_Line'])) == _df['Away_Pts'], 'Back_HA_A'] = 2
    # PL H
    _df.loc[(_df['Back_HA_H'] == 1), 'PL_HA_H'] = _df['HA_Odds_H'] - 1
    _df.loc[(_df['Back_HA_H'] == 0), 'PL_HA_H'] = - 1
    _df.loc[(_df['Back_HA_H'] == 2), 'PL_HA_H'] = 0
    # PL A
    _df.loc[(_df['Back_HA_A'] == 1), 'PL_HA_A'] = _df['HA_Odds_A'] - 1
    _df.loc[(_df['Back_HA_A'] == 0), 'PL_HA_A'] = - 1
    _df.loc[(_df['Back_HA_A'] == 2), 'PL_HA_A'] = 0

    
    return _df


################################################################################
# Prepara o _DF
################################################################################

def prepara_df(_df):
    _df = _df[_df['Home_Pts'] != _df['Away_Pts']]

    _df.reset_index(drop=True, inplace=True)

    _df = cria_alvos(_df)

    _df['P(H)'] = 1 / _df['Odds_H']
    _df['P(A)'] = 1 / _df['Odds_A']
    _df['P(O)'] = 1 / _df['Odds_Over']
    _df['P(U)'] = 1 / _df['Odds_Under']
    
    _df['P_Diff'] = ((1 / _df['Odds_H']) + (1 / _df['Odds_A'])) - 1

    _df['Porc_Over_Home'] = _df.groupby('Home')['Back_Over'].rolling(3).mean().reset_index(level=0, drop=True)
    _df['Porc_Over_Away'] = _df.groupby('Away')['Back_Over'].rolling(3).mean().reset_index(level=0, drop=True)
    _df['Porc_Over_Home']  = _df.groupby('Home')['Porc_Over_Home'].shift(1)
    _df['Porc_Over_Away']  = _df.groupby('Away')['Porc_Over_Away'].shift(1)
    _df['Porc_Over_Home'] = _df['Porc_Over_Home'].replace(np.nan, 0)
    _df['Porc_Over_Away'] = _df['Porc_Over_Away'].replace(np.nan, 0)
    _df.reset_index(inplace=True, drop=True)

    # Custo do gol
    _df['CustoGolHome'] = _df['Home_Pts'] / (1 / _df['Odds_H'])
    _df['CustoGolAway'] = _df['Away_Pts'] / (1 / _df['Odds_A'])
    _df['CustoGolHome'] = _df['CustoGolHome'].replace(np.inf, 0)
    _df['CustoGolAway'] = _df['CustoGolAway'].replace(np.inf, 0)
    _df.reset_index(drop=True, inplace=True)

    # Média, dp e cv do custo do gol
    _df = calcular_mediacg(_df)

    _df['MediaCustoGolHome'] = _df.groupby('Home')['CustoGolHome'].rolling(window=3).mean().reset_index(level=0, drop=True)
    _df['MediaCustoGolAway'] = _df.groupby('Away')['CustoGolAway'].rolling(window=3).mean().reset_index(level=0, drop=True)
    _df['MediaCustoGolHome']  = _df.groupby('Home')['MediaCustoGolHome'].shift(1)
    _df['MediaCustoGolAway']  = _df.groupby('Away')['MediaCustoGolAway'].shift(1)
    _df['MediaCustoGolHome'] = _df['MediaCustoGolHome'].replace(np.nan, 0)
    _df['MediaCustoGolAway'] = _df['MediaCustoGolAway'].replace(np.nan, 0)

    # Último custo do gol
    _df['Last_CG_H']  = _df.groupby('Home')['CustoGolHome'].shift(1)
    _df['Last_CG_A']  = _df.groupby('Away')['CustoGolAway'].shift(1)
    _df['Last_CG_H'] = _df['Last_CG_H'].replace(np.nan, 0)
    _df['Last_CG_A'] = _df['Last_CG_A'].replace(np.nan, 0)
    
    limit_up_h = _df.CustoGolHome.mean() + _df.CustoGolHome.std()
    limit_up_a = _df.CustoGolAway.mean() + _df.CustoGolAway.std()
    _df.loc[(_df['CustoGolHome'] > limit_up_h), 'Acima_Last_CG_H'] = 1
    _df.loc[(_df['CustoGolHome'] <= limit_up_h), 'Acima_Last_CG_H'] = 0
    _df.loc[(_df['CustoGolAway'] > limit_up_a), 'Acima_Last_CG_A'] = 1
    _df.loc[(_df['CustoGolAway'] <= limit_up_a), 'Acima_Last_CG_A'] = 0
    _df['Acima_Last_CG_H']  = _df.groupby('Home')['Acima_Last_CG_H'].shift(1)
    _df['Acima_Last_CG_A']  = _df.groupby('Away')['Acima_Last_CG_A'].shift(1)
    _df['Acima_Last_CG_H'] = _df['Acima_Last_CG_H'].replace(np.nan, 0)
    _df['Acima_Last_CG_A'] = _df['Acima_Last_CG_A'].replace(np.nan, 0)

    limit_down_h = _df.CustoGolHome.mean() - _df.CustoGolHome.std()
    limit_down_a = _df.CustoGolAway.mean() - _df.CustoGolAway.std()
    _df.loc[(_df['CustoGolHome'] < limit_down_h), 'Abaixo_Last_CG_H'] = 1
    _df.loc[(_df['CustoGolHome'] >= limit_down_h), 'Abaixo_Last_CG_H'] = 0
    _df.loc[(_df['CustoGolAway'] < limit_down_a), 'Abaixo_Last_CG_A'] = 1
    _df.loc[(_df['CustoGolAway'] >= limit_down_a), 'Abaixo_Last_CG_A'] = 0
    _df['Abaixo_Last_CG_H']  = _df.groupby('Home')['Abaixo_Last_CG_H'].shift(1)
    _df['Abaixo_Last_CG_A']  = _df.groupby('Away')['Abaixo_Last_CG_A'].shift(1)
    _df['Abaixo_Last_CG_H'] = _df['Abaixo_Last_CG_H'].replace(np.nan, 0)
    _df['Abaixo_Last_CG_A'] = _df['Abaixo_Last_CG_A'].replace(np.nan, 0)

    _df['CV_ML'] = (_df[['Odds_H', 'Odds_A']].std(axis=1)) / (_df[['Odds_H', 'Odds_A']].mean(axis=1))
    _df['CV_Over'] = (_df[['Odds_Over', 'Odds_Under']].std(axis=1)) / (_df[['Odds_Over', 'Odds_Under']].mean(axis=1))
    
    # Custo do retorno
    _df['Avg_Retornos_H_Liga'] = _df['PL_Home'].rolling(window=10, min_periods=5).mean().reset_index(level=0, drop=True)
    _df['Avg_Retornos_H_Liga'] = _df['Avg_Retornos_H_Liga'].shift(1)
    _df['Avg_Retornos_H_Liga'] = _df['Avg_Retornos_H_Liga'].fillna(0)
    _df['Custo_Retorno_H'] = _df['Odds_H'] / _df['Avg_Retornos_H_Liga']
    _df['Custo_Retorno_H'] = _df['Custo_Retorno_H'].replace([np.inf, -np.inf], np.nan)
    
    _df['Avg_Retornos_A_Liga'] = _df['PL_Away'].rolling(window=10, min_periods=5).mean().reset_index(level=0, drop=True)
    _df['Avg_Retornos_A_Liga'] = _df['Avg_Retornos_A_Liga'].shift(1)
    _df['Avg_Retornos_A_Liga'] = _df['Avg_Retornos_A_Liga'].fillna(0)
    _df['Custo_Retorno_A'] = _df['Odds_H'] / _df['Avg_Retornos_A_Liga']
    _df['Custo_Retorno_A'] = _df['Custo_Retorno_A'].replace([np.inf, -np.inf], np.nan)

    return _df