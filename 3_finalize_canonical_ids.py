import pandas as pd

df_mapping = pd.read_csv("./data/3_mapping.csv", names=["index", "url", "url_", "id"])
df = pd.read_csv("./data/1_all.csv")

df = df.merge(df_mapping.loc[:, ["url", "id"]], on="url", how="left")

# If the channel did not have channel_id and exists
condition_1 = (~(df["id"].isna()) & (~df.url.apply(lambda x: "/channel/" in x)))

# If the channel had channel_id
condition_2 = (df.url.apply(lambda x: "/channel/" in x))

df_filtered = df.loc[(condition_1 |  condition_2), :]

# Updates id column with canonical ids
df_filtered.loc[df_filtered["id"].isna(), "id"] = df_filtered.loc[df_filtered["id"].isna(), "url"]

# Drop duplicates
df_filtered = df_filtered.drop_duplicates()

df_filtered.to_csv("./data/4_all_filtered.csv", index=False)