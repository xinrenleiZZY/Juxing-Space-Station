import pandas as pd
import os
from config.settings import PROCESSED_DATA_DIR


def merge_historical_and_realtime(historical_files: list, realtime_df: pd.DataFrame):
    """示例合并函数：将历史CSV文件列表与实时DataFrame合并、去重并保存"""
    dfs = []
    for f in historical_files:
        try:
            dfs.append(pd.read_csv(f, encoding='utf-8-sig'))
        except Exception:
            continue
    if realtime_df is not None and not realtime_df.empty:
        dfs.append(realtime_df)
    if not dfs:
        return None
    combined = pd.concat(dfs, ignore_index=True)
    combined = combined.drop_duplicates()
    out_path = os.path.join(PROCESSED_DATA_DIR, 'combined_aqi.csv')
    combined.to_csv(out_path, index=False, encoding='utf-8-sig')
    return out_path
