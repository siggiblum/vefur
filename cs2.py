import pandas as pd 
from bloomtest import *
from scipy.interpolate import CubicSpline

# Vantar inn græn skuldabréf
def credit_spread():
    [data, tafla] = main()
    rik_overd = []
    rik_verd = []
    fyrir_overd = ["RVKN 35 1", "ARION CB 27", "ARION CB 24", "LBANK CB 25","LBANK CB 27", "LBANK CB 29", "ISB CB 27",
                "ISB CBF 27"]
    fyrir_verd = ["RVK 32 1","RVK 53 1", "HFF150224", "HFF150434", "HFF150644", "LSS150224", "LSS150434", "LSS151155",
                "LSS 39 0303", "OR020934 GB", "OR090546", "OR180255 GB", "ARION CBI 48", "ARION CBI 30", "ARION CBI 29",
                "ARION CBI 25""LBANK CBI 24","LBANK CBI 26", "LBANK CBI 28", "ISB CBI 24","ISB CBI 26","ISB CBI 28",
                "ISB CBI 29","ISB CBI 30"]

    riks_bonds = data[data["Nafn"].str.contains("RIKS")].copy()
    rikb_bonds = data[data["Nafn"].str.contains("RIKB")].copy()

    for df in [riks_bonds, rikb_bonds]:
        df['DUR_MID'] = pd.to_numeric(df['DUR_MID'], errors='coerce')
        df['YLD_YTM_BID'] = pd.to_numeric(df['YLD_YTM_BID'], errors='coerce')

    # Sort by 'DUR_MID'
    riks_bonds = riks_bonds.sort_values(by="DUR_MID")
    rikb_bonds = rikb_bonds.sort_values(by="DUR_MID")
    
    if not riks_bonds.empty:
        x_v = riks_bonds["DUR_MID"].dropna()
        y_v = riks_bonds["YLD_YTM_BID"].dropna()
        cs_v = CubicSpline(x_v, y_v)
        xv = np.linspace(x_v.min(), x_v.max(), 1000)
        yv = cs_v(xv)
        verd = pd.DataFrame({'Líftími': xv, 'Krafa': yv})


    if not rikb_bonds.empty:
        x_o = rikb_bonds["DUR_MID"].dropna()
        y_o = rikb_bonds["YLD_YTM_BID"].dropna()
        cs_o = CubicSpline(x_o, y_o)
        xo = np.linspace(x_o.min(), x_o.max(), 1000)
        yo = cs_o(xo)

        overd = pd.DataFrame({'Líftími': xo, 'Krafa': yo})


    
    def closest_mat(df, liftimi):
        abs_diff = np.abs(df['Líftími'] - liftimi)
        closest_index = abs_diff.idxmin()
    
        return df.loc[closest_index, 'Krafa']

    result = []
    for nafn in fyrir_overd:
        if(nafn in data["Nafn"].values):
            duration = data.loc[data["Nafn"] == nafn, "DUR_MID"].iloc[0]
            krafa = data.loc[data["Nafn"] == nafn, "YLD_YTM_BID"].iloc[0]
            
            new_rik = closest_mat(overd, duration)
            cs = krafa - new_rik
            
            result.append([nafn, krafa, new_rik, cs])

    for nafn in fyrir_verd:
        if(nafn in data["Nafn"].values):
            duration = data.loc[data["Nafn"] == nafn, "DUR_MID"].iloc[0]
            krafa = data.loc[data["Nafn"] == nafn, "YLD_YTM_BID"].iloc[0]

            new_rik = closest_mat(verd, duration)
            cs = krafa - new_rik
            
            result.append([nafn, krafa, new_rik, cs])
    return result

print(credit_spread())