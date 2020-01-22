from v20 import Context

# Pricing
response = api.instrument.candles('USD_CAD', granularity='M1')

if response.status != 200:
    print(response)
    print(response.body)

# stream = Context(
#     'stream-fxpractice.oanda.com',
#     443,
#     token='d9239a7c4e8dcad5d6c70ed6769e81e9-6f3637c29d8583d11f1336a9788071b4'
# )
# response = stream.pricing.stream(
#     '101-001-13004448-001',
#     instruments='AUD_USD',
# )
# for msg_type, msg in response.parts():
#     print(msg_type, msg)
# response = api.account.summary('101-001-13004448-001')
# summary = response.body['account']
# print(summary.balance)
