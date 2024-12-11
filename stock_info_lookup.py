import pandas as pd

def get_instrument_token():
    df = pd.read_csv('api-scrip-master.csv', dtype={'SEM_TRADING_SYMBOL': str, 'SEM_EXM_EXCH_ID': str, 'SEM_SMST_SECURITY_ID': str, 'SEM_INSTRUMENT_NAME': str}, low_memory=False)
    data_dict = {}
    for index, row in df.iterrows():
        trading_symbol = row['SEM_TRADING_SYMBOL']  
        exm_exch_id = row['SEM_EXM_EXCH_ID']
        if trading_symbol not in data_dict:
            data_dict[trading_symbol] = {} 
        data_dict[trading_symbol][exm_exch_id] = row.to_dict()
    return data_dict

def get_security_name_by_id(security_id, instrument_type=None):
    df = pd.read_csv('api-scrip-master.csv', dtype={'SEM_TRADING_SYMBOL': str, 'SEM_EXM_EXCH_ID': str, 'SEM_SMST_SECURITY_ID': str, 'SEM_INSTRUMENT_NAME': str}, low_memory=False)
    security_rows = df[df['SEM_SMST_SECURITY_ID'] == security_id]
    if instrument_type:
        security_rows = security_rows[security_rows['SEM_INSTRUMENT_NAME'] == instrument_type]
    if not security_rows.empty:
        return security_rows[['SEM_TRADING_SYMBOL', 'SEM_EXM_EXCH_ID']].to_dict(orient='records')
    else:
        return None

def get_security_id_by_name(company_name, instrument_type=None):
    df = pd.read_csv('api-scrip-master.csv', dtype={'SEM_TRADING_SYMBOL': str, 'SEM_EXM_EXCH_ID': str, 'SEM_SMST_SECURITY_ID': str, 'SEM_INSTRUMENT_NAME': str}, low_memory=False)
    security_rows = df[df['SEM_TRADING_SYMBOL'] == company_name]
    if instrument_type:
        security_rows = security_rows[security_rows['SEM_INSTRUMENT_NAME'] == instrument_type]
    if not security_rows.empty:
        return security_rows[['SEM_SMST_SECURITY_ID', 'SEM_EXM_EXCH_ID']].to_dict(orient='records')
    else:
        return None

def fetch_security_id_by_name(company_name, instrument_type=None):
    security_info = get_security_id_by_name(company_name, instrument_type)
    results = []
    if security_info:
        for info in security_info:
            security_id = info['SEM_SMST_SECURITY_ID']
            exchange_segment = info['SEM_EXM_EXCH_ID']
            results.append([security_id, exchange_segment])
    else:
        print(f"No security found for company {company_name}")
    return results

def fetch_company_name_by_id(security_id, instrument_type=None):
    company_info = get_security_name_by_id(security_id, instrument_type)
    results = []
    if company_info:
        for info in company_info:
            company_name = info['SEM_TRADING_SYMBOL']
            exchange_segment = info['SEM_EXM_EXCH_ID']
            results.append([company_name, exchange_segment])
    else:
        print(f"No company found for security ID {security_id}")
    return results

# company_name = 'HDFCBANK'
# security_id = '1333' #'2885'
# instrument_type = 'EQUITY'

# print(get_security_id_by_name(company_name, instrument_type))
# print(get_security_name_by_id(security_id, instrument_type))
# print(fetch_security_id_by_name(company_name, instrument_type)[1][0])
# print(fetch_company_name_by_id(security_id, instrument_type)[0][0])
