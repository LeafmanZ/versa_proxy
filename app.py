from flask import Flask, request

import requests
import json

app = Flask(__name__)
app.secret_key = "my_secret" # change this before deploying

FORWARDING_IP = '52.xxx.xxx.xxx:9182' # PROXY FOR VERSA DIRECTOR API, this is the 'IP:PORT' you want to forward all traffic to.

@app.route('/test/<path:subpath>', methods=['GET'])
def test(subpath):
    response = requests.get(f"https://{FORWARDING_IP}/test/{subpath}", verify=False)
    return response.content, response.status_code

@app.route('/auth/<path:subpath>', methods=['POST'])
def versa_auth(subpath):
    # Ensure the path is extracted correctly
    # Here, `subpath` is already provided by the route

    # Extract and validate necessary information from the request
    data = request.json
    
    print(request.headers)

    if subpath == 'refresh':
        refresh = {
            "client_id": data.get('client_id'),
            "client_secret": data.get('client_secret'),
            "grant_type": data.get('grant_type'),
            "refresh_token": data.get("refresh_token")
        }

        response = requests.post(
            f"https://{FORWARDING_IP}/auth/refresh",
            headers=request.headers,
            json=refresh,
            verify=False,
        )

        return response.content, response.status_code

    # Forward the request to the new endpoint
    response = requests.post(
        f"https://{FORWARDING_IP}/auth/token",
        headers=request.headers,
        data=json.dumps(data),
        verify=False,  # Reminder: Handle SSL verification in production
    )

    # Forward the response from the auth server back to the client
    return response.content, response.status_code

@app.route('/versa_redirect/<path:subpath>', methods=['POST', 'GET', 'DELETE'])
def versa_redirect(subpath):

    full_path = request.full_path
    url = f"https://{FORWARDING_IP}/{full_path}"

    if request.method == 'POST':
        response = requests.post(
            url, 
            headers=request.headers, 
            data=request.data,
            verify=False
        )
    elif request.method == 'GET':
        response = requests.get(
            url,
            headers=request.headers,
            verify=False,
        )
    elif request.method == 'DELETE':
        response = requests.delete(
            url,
            headers=request.headers,
            verify=False,
        )

    return response.content, response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=False)
