import requests

domain_name = "sandbox0d28dc02b59f4d0ba70eb4b5436db42c.mailgun.org"
public_key = "91f57a1070944302d7984ed82f2e2a51-324e0bb2-eec6c793"


def send_email(email, text):
    if text == 'accepted':
        text = 'Authentication Completed'
    else:
        text = 'Authentication Error'
    return requests.post(
        f"https://api.mailgun.net/v3/{domain_name}/messages",
        auth=("api", public_key),
        data={"from": "Excited User <mailgun@{domain_name}>",
              "to": [email],
              "subject": "Authentication Result",
              "text": text})


if __name__ == '__main__':
    response = send_email("kamyar.hassanzadeh.78@gmail.com", "salam")
    print(response)