import os
import webbrowser
import msal
import json

def generate_access_token(api_token_access, secrets_path):
    with open(secrets_path, "r") as data:
        secrets = json.load(data)

    APP_ID = secrets["MS_APP_ID"]
    SCOPES = ["User.Read"]

    # save Session Token as a token file
    access_token_cache = msal.SerializableTokenCache()

    # read the token file
    if os.path.exists(api_token_access):
        access_token_cache.deserialize(open(api_token_access, "r").read())

    # assign a SerializableTokenCache object to the client instance
    client = msal.PublicClientApplication(client_id=APP_ID, token_cache=access_token_cache)

    accounts = client.get_accounts()

    if accounts:
        # load the session
        token_response = client.acquire_token_silent(SCOPES, account=accounts[0])
    else:
        # authenticate your account as usual
        flow = client.initiate_device_flow(scopes=SCOPES)
        print(f"user_code: {flow['user_code']}")
        webbrowser.open(flow["verification_uri"])

        token_response = client.acquire_token_by_device_flow(flow)
        print(token_response)

    with open(api_token_access, "w") as _f:
        _f.write(access_token_cache.serialize())
    return token_response

if __name__ == "__main__":

    token_response = generate_access_token("api_token_access.json", "../secrets.json")
    print(token_response["access_token"])

