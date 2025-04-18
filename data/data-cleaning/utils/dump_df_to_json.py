import json
import os
import pandas as pd




def dump_df_to_json(df: pd.DataFrame, export_file: str) -> None:
    try:
        records = df.to_dict('records')
        os.makedirs(os.path.dirname(export_file), exist_ok=True)
        with open(export_file, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"❌ Error occured while dumping DataFrame to json: {e}")
