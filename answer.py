#!/usr/bin/env python3

from requests import session, Request
from requests.cookies import create_cookie
from hashlib import md5
from urllib.parse import quote, unquote
from sys import argv
from base64 import b64decode as decode

server = 'www.cleverbot.com'
endpoint = 'webservicemin?uc=UseOfficialCleverbotAPI&'
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4094.0 Safari/537.36'

def route(path=''):
    return f'https://{server}/{path}'

# This is a token which must be valid for the request to work.

def icogno(text):
    string = f's={quote(text)}' + '&cb_settings_language=en&cb_settings_scripting=no&islearning=1&icognoid=wsf'
    return md5(bytes(string[:26], 'utf-8')).hexdigest()

# Ask a question to Cleverbot using a POST request.

def ask(text):
    headers = {
	  'Connection': 'keep-alive',
	  'Content-Type': 'text/plain',
	  'DNT': '1',
	  'Accept': '*/*',
	  'Host': server,
	  'User-Agent': agent
    }

    data = {
      'stimulus': text,
      'cb_settings_language': 'en',
      'cb_settings_scripting': 'no',
	  'islearning': '1',
	  'icognoid': 'wsf',
	  'icognocheck': icogno(text)
    }

    # Create a new session.
    
    user = session()
    user.get(route())
    user.cookies.set_cookie(create_cookie('_cbsid', '-1'))

    # Create and encode the POST request.
    
    query = Request('POST', route(endpoint), headers=headers, data=data)
    query = user.prepare_request(query)
    query.body = query.body.replace('+', '%20')
    query.headers['Content-Length'] = len(query.body)
    
    # Send the request and extract Cleverbot's answer.
    
    reply = user.send(query)
    answer = unquote(reply.headers['CBOUTPUT'])

    return answer

def main():
    try: 
      question = str(decode(argv[1]), 'utf-8')
      answer = ask(question)
      print(answer)
      
    except:
      print('Whoops')

main()
