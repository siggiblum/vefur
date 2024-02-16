import pandas as pd 
from dur_yield import * 
import QuantLib as ql
from datetime import date
from bloomtest import * 
from datetime import datetime


def find_dur_and_yield():
    data = {
        'Nafn': [
            'RIKB 24 0415', 'RIKB 25 0612', 'RIKB 26 1015', 'RIKB 28 1115',
            'RIKB 31 0124', 'RIKB 42 0217', 'RIKS 26 0216', 'RIKS 30 0701',
            'RIKS 33 0321', 'RIKS 37 0115'
        ],
        'BID': [
            98.220000, 98.775000, 96.930000, 91.070000,
            97.410000, 80.200000, 96.225000, 102.450000,
            102.500000, 84.260000
        ],
        'ASK': [
            98.310000, 98.915000, 97.140000, 91.310000,
            97.870000, 80.950000, 96.440000, 102.860000,
            103.040000, 84.980000
        ],
        'YLD_YTM_BID': [
            10.005134, 8.899408, 8.018118, 7.249595,
            6.977909, 6.374167, 3.402787, 2.827737,
            2.688334, 2.426246
        ],
        'YLD_YTM_ASK': [
            9.608227, 8.789011, 7.928399, 7.185373,
            6.891682, 6.292187, 3.291426, 2.758645,
            2.622383, 2.354674
        ],
        'CPN': [
            2.500000, 8.000000, 6.750000, 5.000000,
            6.500000, 4.500000, 1.500000, 3.250000,
            3.000000, 1.000000
        ],
        'AMT_OUTSTANDING': [
            89387762192.000000, 109762963000.000000, 54195400000.000000, 113464801519.000015,
            124632500000.000000, 58012000000.000000, 83592700000.000000, 78683199659.000000,
            79393919842.000000, 52978600000.000000
        ],
        'CPN_FREQ': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'DUR_MID': [
            0.231950, 1.332494, 2.559747, 4.354014,
            5.486403, 11.489590, 2.029690, 5.621442,
            7.588543, 12.078951
        ],
        'DAYS_TO_NEXT_COUPON': [91, 149, 274, 305, 9, 33, 32, 168, 66, 366],
        'FINAL_MATURITY': [
            '2024-04-15', '2025-06-12', '2026-10-15', '2028-11-15',
            '2031-01-24', '2042-02-17', '2026-02-16', '2030-07-01',
            '2033-03-21', '2037-01-15'
        ]
    }
    # Convert the dictionary into a DataFrame
    tafla = pd.DataFrame(data)
    dicti = []
    [tafla, dicti]
    # [tafla, dicti] = main()
    dic = {}
    for ind in tafla.index:
        bid = tafla['BID'][ind]
        ask = tafla['ASK'][ind]
        if pd.isna(bid) == False and pd.isna(ask) == False:
            if tafla['Nafn'][ind] not in dic.keys():
                dic[tafla['Nafn'][ind]] = {}
            dic[tafla['Nafn'][ind]]['Mid Price'] = (float(tafla['BID'][ind])+float(tafla['ASK'][ind]))/2 
            dic[tafla['Nafn'][ind]]['Final Maturity'] = datetime.strptime(tafla['FINAL_MATURITY'][ind], "%Y-%m-%d")
            dic[tafla['Nafn'][ind]]['Coupon Frequency'] = tafla['CPN_FREQ'][ind]
            dic[tafla['Nafn'][ind]]['Coupon'] = tafla['CPN'][ind] 
    
    result = {}
    for key in dic.keys():
        for key2, value in dic[key].items():
            if key2 == 'Mid Price':
                market_price = float(value) 
            elif key2 == 'Final Maturity': 
                maturity_date = value 
            elif key2 == 'Coupon Frequency':
                coupon_frq = float(value) 
            else: 
                coupon = float(value)/100
        start = date.today()

        # Convert Python date objects to QuantLib date objects
        ql_maturity_date = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)
        ql_start_date = ql.Date(start.day, start.month, start.year)

        # Frequency and tenor setup
        if coupon_frq == 1:
            tenor = ql.Period(ql.Annual)
            frequency = ql.Annual
        elif coupon_frq == 2:
            tenor = ql.Period(ql.Semiannual)
            frequency = ql.Semiannual
        else:
            tenor = ql.Period(ql.Quarterly)
            frequency = ql.Quarterly

        calendar = ql.Iceland()
        business_convention = ql.Unadjusted
        date_generation = ql.DateGeneration.Backward
        month_end = False

        schedule = ql.Schedule(ql_start_date, ql_maturity_date, tenor, calendar,
                            business_convention, business_convention, 
                            date_generation, month_end)

        coupons = [coupon]
        face_value = 100
        settlement_days = 0
        fixed_rate_bond = ql.FixedRateBond(settlement_days, face_value, schedule, coupons, ql.ActualActual(ql.ActualActual.ISDA))

        # Calculate YTM
        market_yield = fixed_rate_bond.bondYield(market_price, ql.ActualActual(ql.ActualActual.ISDA), ql.Compounded, frequency)

        # Calculate duration
        interest_rate = ql.InterestRate(market_yield, ql.ActualActual(ql.ActualActual.ISDA), ql.Compounded, frequency)
        macaulay_duration = ql.BondFunctions.duration(fixed_rate_bond, interest_rate, ql.Duration.Macaulay)
        result[key] = [macaulay_duration, market_yield]
    return result
    

result = find_dur_and_yield()


def verdlag():
    def calculate_weights(length_smaller, length_larger, length_corporate):
        """
        Calculate the weights based on bond lengths.
        Ensure that weighted length of two bonds is the same as the corporate bond length.
        """
        if length_smaller == length_larger:
            # Avoid division by zero in case both lengths are equal
            return 0.5, 0.5
        weight_1 = (length_corporate - length_larger) / (length_smaller - length_larger)
        weight_2 = 1 - weight_1
        return weight_1, weight_2



    data = {}
    for key in result.keys():
        if key not in data.keys():
            data[key] = {}
        data[key]['Mid Yield'] = result[key][1]
        data[key]['Duration'] = result[key][0]
    
    ov_dict = {}
    alagslengdir = [0.5, 1,2,3,4,5,6,7,8,9,10, 11, 12, 13]
    overdtryggd_rikisbref = ["RIKB 24 0415", "RIKB 25 0612", "RIKB 26 1015", "RIKB 28 1115", "RIKB 31 0124", "RIKB 42 0217"]
    for bref in data.keys():
        if bref in overdtryggd_rikisbref:
            alagslengdir.append(data[bref]['Duration'])
            ov_dict[data[bref]['Duration']] = bref
    rikisbref= {}
    
    for key in data.keys():
        if key in overdtryggd_rikisbref:
            if key not in rikisbref.keys():
                rikisbref[key] = {}
            rikisbref[key]['Mid Yield'] = data[key]['Mid Yield']
            rikisbref[key]['Duration'] = data[key]['Duration']
                



    rikisbref_df = pd.DataFrame.from_dict(rikisbref, orient="index")



    krofur = {}
    less = {}
    bref = None
    for j1 in alagslengdir: 
        maxval = 0
        for ind in rikisbref.keys():
            if j1 not in krofur.keys():
                krofur[j1] = {}
            if float(rikisbref[ind]['Duration']) > maxval and float(rikisbref[ind]['Duration']) <= float(j1):
                maxval = float(rikisbref[ind]['Duration'])
                bref = ind
                krafa = float(rikisbref[ind]['Mid Yield'])
        krofur[j1]['Bréf sem er styttra'] = bref
        krofur[j1]['Lengd'] = maxval 
        krofur[j1]['Krafa'] = krafa 



    krofur_df = pd.DataFrame.from_dict(krofur)
    krofur_df = krofur_df.T



    krafa2 = {}
    for j1 in alagslengdir:
        minval =  25 
        go = False 
        for ind in rikisbref.keys():
            for test in rikisbref.keys():
                if float(rikisbref[test]['Duration']) >= float(j1):
                    go = True 
                    break
            if j1 not in krafa2.keys():
                krafa2[j1] = {}
            if go == True:
                if float(rikisbref[ind]['Duration']) < minval and float(rikisbref[ind]['Duration']) >= float(j1):
                    minval = float(rikisbref[ind]['Duration'])
                    bref = ind
                    krafa = float(rikisbref[ind]['Mid Yield'])
                krafa2[j1]['Bréf sem er lengra'] = bref
                krafa2[j1]['Lengd'] = minval 
                krafa2[j1]['Krafa'] = krafa 
            elif go == False:
                minval = krofur[j1]['Lengd']
                bref = krofur[j1]['Bréf sem er styttra']
                krafa = krofur[j1]['Krafa']
                krafa2[j1]['Bréf sem er lengra'] = bref 
                krafa2[j1]['Lengd'] = minval 
                krafa2[j1]['Krafa'] = krafa



    krafa2_df = pd.DataFrame.from_dict(krafa2)
    krafa2_df = krafa2_df.T
    finalkrofudict = krofur_df.join(krafa2_df, lsuffix = '_Minni', rsuffix ='_Stærri')
    finalkrofudict = finalkrofudict.reset_index()

    vigtir = {}
    for ind in finalkrofudict.index:
        length_smaller = finalkrofudict['Lengd_Minni'][ind]
        length_larger = finalkrofudict['Lengd_Stærri'][ind]
        length_corporate = finalkrofudict['index'][ind]

        w1, w2 = calculate_weights(length_smaller, length_larger, length_corporate)

        vigtir[ind] = {
            'Vigt 1': w1,
            'Vigt 2': w2,
            'Vigtuð krafa': w1 * finalkrofudict['Krafa_Minni'][ind] + w2 * finalkrofudict['Krafa_Stærri'][ind],
        }


    vigtir_df = pd.DataFrame.from_dict(vigtir)
    vigtir_df = vigtir_df.transpose()
    final = finalkrofudict.join(vigtir_df)
    # print(final)



    ########################################################################################################## 
    verdtryggd_rikisbref = ["RIKS 26 0216", "RIKS 30 0701", "RIKS 33 0321", "RIKS 37 0115"]
    rikisbref= {}
    for key in data.keys():
        if key in verdtryggd_rikisbref:
            if key not in rikisbref.keys():
                rikisbref[key] = {}
            rikisbref[key]['Mid Yield'] = data[key]['Mid Yield']
            rikisbref[key]['Duration'] = data[key]['Duration']
                



    rikisbref_df = pd.DataFrame.from_dict(rikisbref, orient="index")


    krofur = {}
    less = {}
    bref = "RIKS 26 0216"
    krafa = rikisbref["RIKS 26 0216"]['Mid Yield']
    for j1 in alagslengdir: 
        maxval = 0
        for ind in rikisbref.keys():
            if j1 not in krofur.keys():
                krofur[j1] = {}
            if float(rikisbref[ind]['Duration']) > maxval and float(rikisbref[ind]['Duration']) <= float(j1):
                maxval = float(rikisbref[ind]['Duration'])
                bref = ind
                krafa = float(rikisbref[ind]['Mid Yield'])
        if maxval == 0:
            maxval = rikisbref["RIKS 26 0216"]['Duration']
        krofur[j1]['Bréf sem er styttra'] = bref
        krofur[j1]['Lengd'] = maxval 
        krofur[j1]['Krafa'] = krafa 



    krofur_df = pd.DataFrame.from_dict(krofur)
    krofur_df = krofur_df.T




    krafa2 = {}
    for j1 in alagslengdir:
        minval =  25 
        go = False 
        for ind in rikisbref.keys():
            for test in rikisbref.keys():
                if float(rikisbref[test]['Duration']) >= float(j1):
                    go = True 
                    break
            if j1 not in krafa2.keys():
                krafa2[j1] = {}
            if go == True:
                if float(rikisbref[ind]['Duration']) < minval and float(rikisbref[ind]['Duration']) >= float(j1):
                    minval = float(rikisbref[ind]['Duration'])
                    bref = ind
                    krafa = float(rikisbref[ind]['Mid Yield'])
                krafa2[j1]['Bréf sem er lengra'] = bref
                krafa2[j1]['Lengd'] = minval 
                krafa2[j1]['Krafa'] = krafa 
            elif go == False:
                minval = krofur[j1]['Lengd']
                bref = krofur[j1]['Bréf sem er styttra']
                krafa = krofur[j1]['Krafa']
                krafa2[j1]['Bréf sem er lengra'] = bref 
                krafa2[j1]['Lengd'] = minval 
                krafa2[j1]['Krafa'] = krafa



    krafa2_df = pd.DataFrame.from_dict(krafa2)
    krafa2_df = krafa2_df.T
    finalkrofudict = krofur_df.join(krafa2_df, lsuffix = '_Minni', rsuffix ='_Stærri')
    finalkrofudict = finalkrofudict.reset_index()

    vigtir = {}
    for ind in finalkrofudict.index:
        length_smaller = finalkrofudict['Lengd_Minni'][ind]
        length_larger = finalkrofudict['Lengd_Stærri'][ind]
        length_corporate = finalkrofudict['index'][ind]

        w1, w2 = calculate_weights(length_smaller, length_larger, length_corporate)

        vigtir[ind] = {
            'Vigt 1': w1,
            'Vigt 2': w2,
            'Vigtuð krafa': w1 * finalkrofudict['Krafa_Minni'][ind] + w2 * finalkrofudict['Krafa_Stærri'][ind],
        }


    vigtir_df = pd.DataFrame.from_dict(vigtir)
    vigtir_df = vigtir_df.transpose()
    final2 = finalkrofudict.join(vigtir_df)
    # print(final2)

    reikna_alag = final.join(final2, lsuffix='_Óverðtryggð', rsuffix='_Verðtryggð')
    reikna_alag.to_excel('Valag.xlsx')
    alag_final = {}
    alag_bref = {}
    for ind in reikna_alag.index:
        if reikna_alag['index_Óverðtryggð'][ind] not in ov_dict:
            if reikna_alag['index_Óverðtryggð'][ind] not in alag_final.keys():
                alag_final[reikna_alag['index_Óverðtryggð'][ind]] = {}

            alag_final[reikna_alag['index_Óverðtryggð'][ind]]['Verðbólguálag'] = (float(reikna_alag['Vigtuð krafa_Óverðtryggð'][ind]) - float(reikna_alag['Vigtuð krafa_Verðtryggð'][ind])) * 100
        else: 
            if ov_dict[reikna_alag['index_Óverðtryggð'][ind]] not in alag_bref.keys():
                alag_bref[ov_dict[reikna_alag['index_Óverðtryggð'][ind]]] = {}
            alag_bref[ov_dict[reikna_alag['index_Óverðtryggð'][ind]]]['Duration'] = reikna_alag['index_Óverðtryggð'][ind]
            alag_bref[ov_dict[reikna_alag['index_Óverðtryggð'][ind]]]['Verðbólguálag'] = (float(reikna_alag['Vigtuð krafa_Óverðtryggð'][ind]) - float(reikna_alag['Vigtuð krafa_Verðtryggð'][ind])) * 100
    
    df = pd.DataFrame.from_dict(alag_final)
    df = df.T
    df2 = pd.DataFrame.from_dict(alag_bref)
    df2 = df2.T
    # print(df)


    listi1 = []
    listi2 = []
    for ind in df.index:
        listi1.append([ind, alag_final[ind]['Verðbólguálag']])
    for ind in df2.index:
        listi2.append([ind, df2['Duration'][ind], df2['Verðbólguálag'][ind]])
    return listi1, listi2
