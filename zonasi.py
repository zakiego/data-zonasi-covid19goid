from numpy import int64
import requests as req
import pandas as pd


def hit_api():
    resp = req.get("https://data.covid19.go.id/public/api/skor.json")
    respjson = resp.json()
    t = respjson["tanggal"]
    df = pd.DataFrame(respjson["data"])
    df.insert(0, 'tanggal', t)
    df["kode_prov"] = df["kode_prov"].astype(int64)
    df["kode_kota"] = df["kode_kota"].astype(int64)
    return df


def save():
    zonasi_api = hit_api()
    zonasi_csv = pd.read_csv("zonasi.csv")
    zonasi_combine = pd.concat([zonasi_csv, zonasi_api]
                               ).drop_duplicates().reset_index(drop=True)

    zonasi_combine = zonasi_combine.sort_values(
        by=['prov', 'kota'], ascending=[True, True])
    zonasi_combine.to_csv("zonasi.csv", index=False)


save()

header = \
    '''# Data Zonasi Covid-19 Indonesia dari covid19.go.id\n
#### Sumber API\n
```url
https://data.covid19.go.id/public/api/skor.json
```\n
Data tanggal yang tersedia:
'''


def update_readme():
    with open('readme.md', 'w') as f:
        f.write(header)
        zonasi_csv = pd.read_csv("zonasi.csv")
        for tanggal in zonasi_csv['tanggal'].unique():
            f.write(f'* {tanggal}\n')


update_readme()
