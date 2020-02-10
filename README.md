# TD

## Authorization (Every 90 days)

- Allow access to the app https://auth.tdameritrade.com/oauth?client_id=ULGR9QXGJPZMHTHHFJDM8SC7XLBKLNQZ@AMER.OAUTHAP&response_type=code&redirect_uri=https://tick.labstack.com
- Copy code from url and decode it for use
- Get `access_token` & `refresh_token` via https://api.tdameritrade.com/v1/oauth2/token (See Postman collection)