import sys
import requests
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py import VeracodeAPI
api_target = "https://analysiscenter.veracode.com/api/5.0/deletebuild.do"
headers = {"User-Agent": "Veracode Python Script"}



def deleteBuilds():
    data = []
    with open(sys.argv[1], "r") as application_input:
        applications = application_input.readlines()
    for build_candidates in applications:
        app_id,sandbox_name = build_candidates.split(',') 
        app_id = app_id.strip()
        sandbox_name = sandbox_name.strip()
        
        #If no sandbox name provided, the latest policy scan will be deleted
        if sandbox_name == "":
            print("Processing APP ID: " + app_id + ". No Sandbox ID specified. The latest Policy Scan will be deleted")
            try:
                response = requests.get(api_target, auth=RequestsAuthPluginVeracodeHMAC(), headers={"User-Agent": "Veracode Python Script"}, params={'app_id': app_id})
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

        #If sandbox name provided, find the corresponding sandbox ID and delete the latest build from the sandbox
        else:
            print("Processing APP ID: " + app_id + " and searching for sandbox name: '" + sandbox_name + "'")
            sandbox_list = VeracodeAPI().get_sandbox_list(app_id)
            
            sandbox_tree = ET.fromstring(sandbox_list)
            for sanbox_ids in sandbox_tree.iter('{https://analysiscenter.veracode.com/schema/4.0/sandboxlist}sandbox'):
                if sanbox_ids.attrib['sandbox_name'] == sandbox_name:
                    sandbox_id = sanbox_ids.attrib['sandbox_id']

                    print("Sandbox Found. Processing APP ID: " + app_id + " and Sandbox Name '" + sandbox_name + "' (Sandbox ID: " + sandbox_id + ") for deletion")
                    try:
                        response = requests.get(api_target, auth=RequestsAuthPluginVeracodeHMAC(), headers={"User-Agent": "Veracode Python Scripts"}, params={'app_id': app_id, 'sandbox_id': sandbox_id})
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
                    break
            else:
                print("No sandbox with name '" + sandbox_name + "' found in app " + app_id)


def main():

    deleteBuilds()


if __name__ == "__main__":
    main()