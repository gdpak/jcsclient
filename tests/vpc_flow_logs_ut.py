#!/usr/bin/env python

import flow_logs_manager
import logging
import sys
import os

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('Flow Logs UT')

def test_check_flow_logs_admin_all(start_time, end_time, admin_password,
                                      account_id, direction_ing):
    flow_manager = flow_logs_manager.FlowLogsManager()
    resp = flow_manager.show_vpc_flow_logs_admin(start_time,
                                                 end_time,
                                                 admin_password,
                                                 account_id,
                                                 direction_ing)
    print resp

def main():
    account_id=None
    direction_ing=None
    start_time = sys.argv[1]
    end_time   = sys.argv[2]
    if (len(sys.argv) > 3):
       account_id = sys.argv[3]
    if (len(sys.argv) > 4):
       direction_ing = sys.argv[4]
    admin_password = os.environ.get('VPC_FLOW_LOGS_ADMIN_PASS')
    if (not start_time) or (not end_time) :
        print "Usage: start_time and end_time should be specified"
        return 0
    if (account_id is not None) and (not direction_ing) :
        print "Usage: direction_ing is manadatory when account_id is specified"
        return 0
    if (account_id is not None) and (not admin_password) :
        print "Usage: admin_password should be set when account_id is specified"
        return 0
    if (not admin_password) :
        print "Warning: Admin password is not set in config file\n"
        print "Displaying only VPC flow logs which are created by your account"

    test_check_flow_logs_admin_all(start_time, end_time,
                                   admin_password, account_id,
                                                direction_ing)

main()

