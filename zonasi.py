from numpy import int64
import requests as req
import pandas as pd

zonasi_csv = pd.read_csv("zonasi.csv")


def hit_api():
    resp = req.get("https://data.covid19.go.id/public/api/skor.json")
    respjson = resp.json()
    t = respjson["tanggal"]
    df = pd.DataFrame(respjson["data"])
    df.insert(0, 'tanggal', t)
    df["kode_prov"] = df["kode_prov"].astype(int64)
    df["kode_kota"] = df["kode_kota"].astype(int64)
    return df


zonasi_api = hit_api()
zonasi_combine = pd.concat([zonasi_csv, zonasi_api]
                           ).drop_duplicates().reset_index(drop=True)

zonasi_combine.to_csv("zonasi.csv", index=False)
