import xmltodict
import json
import os
import pdb
from jcsclient import requestify 
from jcsclient import config 

class FlowLogsManager():
    
    def __init__(self):
        self.url = config.get_service_url('vpc')
        self.headers = {}
        self.version = '2016-03-01'
        self.verb = 'GET'

    def show_vpc_flow_logs_admin(self, start_time, end_time, 
                          admin_pass=None, account_id=None,
                                       direction_ing=None):
        params = {}
        params['Version']= self.version
        params['Action'] = 'DescribeFlowLog'
        if (admin_pass is not None) :
           params['admin_password'] = admin_pass
        if (direction_ing is not None):
           params['direction_ing'] = direction_ing
        params['start_time'] = start_time
        params['end_time']   = end_time
        if account_id is not None:
           params['account'] = 'acc-'+account_id
        resp = requestify.make_request(self.url, self.verb,
                self.headers, params)
        if resp is not None:
            try:
                resp_dict = json.loads(resp.content)
            except:
                resp_dict = xmltodict.parse(resp.content)
                resp_json = json.dumps(resp_dict, indent=4, sort_keys=True)
                #resp_dict = json.loads(resp_json)
            return resp_json
        return 'FAIL'

