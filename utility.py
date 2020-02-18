from datetime import datetime, timedelta

def tomorrow():
    return (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
