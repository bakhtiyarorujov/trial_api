import pandas as pd
from database import engine

csv_file = 'trial_data.csv'
df = pd.read_csv(csv_file)

# Insert wrestlers
wrestlers_df = df[['Wrestler']].drop_duplicates().reset_index(drop=True)
wrestlers_df.columns = ['full_name']
wrestlers_df.to_sql('wrestlers', con=engine, if_exists='append', index=False)

# Insert actions
actions_df = df[['Action']].drop_duplicates().reset_index(drop=True)
actions_df.columns = ['name']
actions_df.to_sql('actions', con=engine, if_exists='append', index=False)

# Insert techniques
techniques_df = df[['Action', 'Technique']].drop_duplicates().reset_index(drop=True)
techniques_df.columns = ['action_name', 'name']
techniques_df = pd.merge(techniques_df, actions_df, how='left', left_on='action_name', right_on='name')
techniques_df = techniques_df[['name_x', 'id']]
techniques_df.columns = ['name', 'action_id']
techniques_df.to_sql('techniques', con=engine, if_exists='append', index=False)

# Insert authors
authors_df = df[['Author']].drop_duplicates().reset_index(drop=True)
authors_df.columns = ['name']
authors_df.to_sql('authors', con=engine, if_exists='append', index=False)

# Insert status
status_df = df[['Status']].drop_duplicates().reset_index(drop=True)
status_df.columns = ['name']
status_df.to_sql('status', con=engine, if_exists='append', index=False)

# Insert records
records_df = df.copy()
records_df = pd.merge(records_df, wrestlers_df, how='left', left_on='Wrestler', right_on='name')
records_df = pd.merge(records_df, wrestlers_df, how='left', left_on='Opponent', right_on='name', suffixes=('_wrestler', '_opponent'))
records_df = pd.merge(records_df, actions_df, how='left', left_on='Action', right_on='name')
records_df = pd.merge(records_df, authors_df, how='left', left_on='Author', right_on='name')
records_df = pd.merge(records_df, status_df, how='left', left_on='Status', right_on='name')
records_df = pd.merge(records_df, techniques_df, how='left', left_on=['Action', 'Technique'], right_on=['action_name', 'name'])
records_df = records_df[['Second', 'Successful', 'Score', 'Defense', 'Flag', 'id_wrestler', 'id_opponent', 'id', 'id_1', 'id_2', 'id_3']]
records_df.columns = ['second', 'successful', 'score', 'defense', 'flag', 'wrestler1_id', 'wrestler2_id', 'author_id', 'status_id', 'technique_id', 'action_id']
records_df.to_sql('records', con=engine, if_exists='append', index=False)