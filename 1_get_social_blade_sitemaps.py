import os.path as path
import pandas as pd
import requests
import glob
import time
import re 



url = 'https://socialblade.com/sitemaps/sb_sitemap_index.xml'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url, headers=headers).text

sitemaps = re.findall(r'<loc>(.*http://socialblade.com/sitemaps/sbyoutube_sitemap.*)</loc>', response)

def get_sitemap(sitemap, headers):
    response =  requests.get(sitemap, headers=headers)
    print(response.status_code)

    response = response.text
    urls = re.findall(r'<loc>.*http://socialblade.com/youtube/([a-zA-Z]+)/([^/]*)(/.*)+</loc>', response)
    
    df = pd.DataFrame(urls)
    df = df.loc[:, [0, 1]]
    df = df.drop_duplicates().sort_values(0)
    df["url"] = "https://www.youtube.com/" + df[0] + "/" + df[1]
    df = df.loc[:, ["url"]]
    df.to_csv(
                "./data/urls/" + sitemap.split("/")[-1].replace("xml", "csv"),
                index=False
                )
    
for sitemap in sitemaps[::-1]:
    print(sitemap)
    if path.exists("./data/urls/" + sitemap.split("/")[-1].replace("xml", "csv")):
        continue
    try:
        get_sitemap(sitemap, headers)
    except:
        print("error in sitemap:", sitemap)
        time.sleep(10)
        try:
            get_sitemap(sitemap, headers)
        except:
            pass


acc = [pd.read_csv(filename) for filename in glob.glob("./data/urls/*.csv")]
all_df = pd.concat(acc).to_csv("./data/all.csv", index=False)


df_not_channel_id = all_df.loc[~all_df.url.apply(lambda x: "/channel/" in x)].to_csv('./data/all_to_disambiguate.csv', header=False)
