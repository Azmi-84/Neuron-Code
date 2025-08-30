from urllib import response
import requests

login_url = 'http://192.168.0.1/'
pppoe_url = 'http://192.168.0.1/#networkBasic'

response = requests.get(login_url)
print(response.status_code)

response_post = requests.post(login_url)
print(response_post.status_code)

pppoe_response = requests.get(pppoe_url)
print(pppoe_response.status_code)

pppoe_response_post = requests.post(pppoe_url)
print(pppoe_response_post.status_code)