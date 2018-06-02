#!/usr/bin/env python3

# Workaround to make sure HomeAssistant state is correct for smartthings due to:
# https://github.com/stjohnjohnson/smartthings-mqtt-bridge/issues/113

import json
import sys
import time
import logging
import urllib.request 
import urllib.parse
from pprint import pprint, pformat
from functools import wraps

def urlopen_with_retry(req):
  tries = 6
  delay = 3
  backoff = 2
  while tries > 1:
    try:
      return urllib.request.urlopen(req)
    except urllib.error.URLError as e:
      msg = "%s, Retrying in %d seconds..." % (str(e), delay)
      logging.warn(msg)
      time.sleep(delay)
      tries -= 1
      delay *= backoff 


statefile = sys.argv[2]
logging.info("Opening state file: %s" % statefile)
data = json.load(open(statefile))
logging.info("Data:\n %s" % json.dumps(data["history"], indent=2, sort_keys=False))
statusurl = 'http://' + sys.argv[1] + '/status'
url = 'http://' + sys.argv[1] + '/push'

currentstatus = json.loads('{"status":"NOTOK"}')
currentstatus = currentstatus["status"]
while currentstatus != "OK":
  logging.info("Checking mqtt-bridge status url: %s" % statusurl)
  reqdata = {"serverstatus":"serverstatus"}
  reqdata = json.dumps(reqdata).encode('utf8')
  req = urllib.request.Request(statusurl, data = reqdata, headers = {'content-type': 'application/json', 'user-agent': 'Linux UPnP/1.0 HomeAssistantStart'})
  response = urlopen_with_retry(req)
  currentstatus = json.loads(response.read())
  currentstatus = currentstatus["status"]
  logging.info("Current Status: %s" % currentstatus)
  time.sleep(5)


logging.info("Sending device states to url: %s" % url)
for device in data["history"].keys():
  if "cmd" not in device:
    smartthings, name, type = device.split('/')
    value = data["history"][device]
    reqdata = {"name":name, "value":value, "type":type}
    reqdata = json.dumps(reqdata).encode('utf8')
    req = urllib.request.Request(url, data = reqdata, headers = {'content-type': 'application/json', 'user-agent': 'Linux UPnP/1.0 HomeAssistantStart'})
    response = urlopen_with_retry(req)
    logging.info("Setting state on: name: %s : value: %s : type: %s" % (name, value, type))
    logging.info("Set state response: %s" % response.read())


