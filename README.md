# Crawl YT subscribers

This repository contain scripts to crawl canonical channel IDs and subscriber count from SocialBlade's [sitemap](https://socialblade.com/sitemaps/sb_sitemap_index.xml).

The data folder is populated by the scripts. The final output is provided in zipped form [here](https://drive.google.com/file/d/1ulJOybfj1C6V71wnWqGhOVJ2ROofOfbM/view?usp=sharing).

To install python dependencies in a conda terminal use the command:

    conda create -n <environment-name> --file req.txt


## Description of the scripts

- `1_get_social_blade_sitemaps.py`: this systematically downloads all sitemaps from Social Blade.
- `2_bash_script_channels_canonical_ids.sh` this downloads the canonical ids of channels for which the Social Blade url does not contain the canonical id. You should change the script to contain the path to your instalation of yt-dlp (which can be obtained via the command `which yt-dlp`).
- `3_finalize_canonical_ids.py` minor preprocessing of the canonical ids.
- `4_bash_script_channels_subs.sh` gets number of subscribers using yt-dlp. Again, replace path as needed.
- `5_final_filtered_dataset.ipynb` final processing and visualization.

---