# %%
import pandas as pd
import csv
# %%

# data = pd.read_csv(
#     "/Volumes/Sandisk/Projects/data_samples/ml/footer_candidate_stat.txt",
#     delimiter=',',
# 	quoting=csv.QUOTE_ALL,
#     quotechar='\"',
#     error_bad_lines=False)

df = pd.read_csv(
    "/Volumes/Sandisk/Projects/data_samples/ml/footer_candidate_stat.csv")
# %%

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# %%

df["is_footer_header"] = None
# %%

df.loc[(df.stop_word_count != '0'), 'is_footer_header'] = 0
# %%

df.head(10)

df.info()

# %%

df['english_word_percent'] = df['english_word_percent'].astype(
    str).astype(float)
# %%
