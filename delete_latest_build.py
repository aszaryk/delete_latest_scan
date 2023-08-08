import sys
import requests
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py import VeracodeAPI
api_target = "https://analysiscenter.veracode.com/api/5.0/deletebuild.do"
headers = {"User-Agent": "Veracode Python Script"}



def getBuilds():
    data = []
    with open(sys.argv[1], "r") as application_input:
        applications = application_input.readlines()
    for build_candidates in applications:
        app_id,sandbox_id = build_candidates.split(':')
        app_id = app_id.strip()
        sandbox_id = sandbox_id.strip()
        
        #Determine if only app_id provided or sandbox_id was provided
        if sandbox_id == "":
            print("Processing APP ID: " + app_id + ". No Sandbox ID specified. The latest Policy Scan will be deleted")
            try:
                response = requests.get(api_target, auth=RequestsAuthPluginVeracodeHMAC(), headers={"User-Agent": "api.py"}, params={'app_id': app_id})
            except requests.RequestException as e:
                print("API Request Error occured")
                print(e)
            if response.ok:
                responsetree = ET.fromstring(response.content)

                if responsetree.text != None:
                    print("There was an Error deleting the build. Detailed Reponse from API:", end = " ")
                    print(responsetree.text)

                msg = responsetree.find('{https://analysiscenter.veracode.com/schema/deletebuildresult}result')
                if msg != None:
                    print("Result Received. Detailed Response from API:", end = " ")
                    print(msg.text)
            else:
                print(response.status_code)

        else:
            print("Processing APP ID: " + app_id + " and Sandbox ID " + sandbox_id + " for deletion")
            try:
                response = requests.get(api_target, auth=RequestsAuthPluginVeracodeHMAC(), headers={"User-Agent": "api.py"}, params={'app_id': app_id, 'sandbox_id': sandbox_id})
            except requests.RequestException as e:
                print("API Request Error occured")
                print(e)
            if response.ok:
                responsetree = ET.fromstring(response.content)

                if responsetree.text != None:
                    print("There was an Error deleting the build. Detailed Reponse from API:", end = " ")
                    print(responsetree.text)

                msg = responsetree.find('{https://analysiscenter.veracode.com/schema/deletebuildresult}result')
                if msg != None:
                    print("Result Received. Detailed Response from API:", end = " ")
                    print(msg.text)
            else:
                print(response.status_code)



def main():

    getBuilds()


if __name__ == "__main__":
    main()