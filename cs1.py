import pandas as pd 
from bloomtest import *

def calculate_weights(length_smaller, length_larger, length_corporate):
    if length_smaller == length_larger:
        # Avoid division by zero in case both lengths are equal
        return 0.5, 0.5

    weight_1 = (length_corporate - length_larger) / (length_smaller - length_larger)
    weight_2 = 1 - weight_1
    return weight_1, weight_2

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

    for index, row in data.iterrows():
        if "RIKS" in row["Nafn"]:
            rik_verd.append(row["Nafn"])
        elif "RIKB" in row["Nafn"]:
            rik_overd.append(row["Nafn"])
    
    def closest_mat(indicator, dur, krafa):
        #indicator: Ó fyrir óvertryggt. V fyrir verðtryggt
        small = 0
        small_krafa = 0
        big = 100
        big_krafa = 0   ##########Hérna gæti leynst villa
        if(indicator == "Ó"):
            for rik in rik_overd:
                liftimi = data.loc[data["Nafn"] == rik, "DUR_MID"].iloc[0]
                if(liftimi < dur and liftimi > small):
                    small_krafa = data.loc[data["Nafn"] == rik, "YLD_YTM_BID"].iloc[0]
                    small = liftimi
                elif(liftimi > dur and liftimi < big):
                    big = liftimi
                    big_krafa = data.loc[data["Nafn"] == rik, "YLD_YTM_BID"].iloc[0]
        else:
            for rik in rik_verd:
                liftimi = data.loc[data["Nafn"] == rik, "DUR_MID"].iloc[0]
                if(liftimi < dur and liftimi > small):
                    small_krafa = data.loc[data["Nafn"] == rik, "YLD_YTM_BID"].iloc[0]
                    small = liftimi
                elif(liftimi > dur and liftimi < big):
                    big = liftimi
                    big_krafa = data.loc[data["Nafn"] == rik, "YLD_YTM_BID"].iloc[0]
        if(small == 0):
            small = dur
        if(big == 100):
            big = dur

        if(small_krafa == 0):
            small_krafa = krafa
        if(big_krafa == 0):
            big_krafa = krafa
        return small, big, small_krafa, big_krafa

    result = {}
    for nafn in fyrir_overd:
        if(nafn in data["Nafn"].values):
            duration = data.loc[data["Nafn"] == nafn, "DUR_MID"].iloc[0]
            krafa = data.loc[data["Nafn"] == nafn, "YLD_YTM_BID"].iloc[0]
            liftimi_small, liftimi_big, krafa_small, krafa_big = closest_mat("Ó", duration, krafa)
            vigt1, vigt2 = calculate_weights(liftimi_small, liftimi_big, duration)

            new_rik = vigt1 * krafa_small + vigt2 * krafa_big
            cs = duration - new_rik
            result[nafn] = cs

    for nafn in fyrir_verd:
        if(nafn in data["Nafn"].values):
            duration = data.loc[data["Nafn"] == nafn, "DUR_MID"].iloc[0]
            krafa = data.loc[data["Nafn"] == nafn, "YLD_YTM_BID"].iloc[0]
            liftimi_small, liftimi_big, krafa_small, krafa_big = closest_mat("V", duration, krafa)
            vigt1, vigt2 = calculate_weights(liftimi_small, liftimi_big, duration)
            print(nafn)
            new_rik = vigt1 * krafa_small + vigt2 * krafa_big
            print("Líftímar")
            print(duration)
            print(liftimi_small, liftimi_big)
            print("Kröfur")
            print(krafa)
            print(krafa_small, krafa_big)
            # print(new_rik)
            # print(duration)
            cs = krafa - new_rik
            result[nafn] = cs

    return result

print(credit_spread())

            
