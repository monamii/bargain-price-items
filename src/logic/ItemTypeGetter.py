import pandas as pd
from flask import jsonify


class ItemTypeGetter:

    def get(self):
        df = pd.read_csv('data/perfectWorld.csv', encoding='utf8')
        return jsonify(df.type.dropna().drop_duplicates().sort_values().tolist())
