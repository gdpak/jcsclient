#!/usr/bin/env python

import flow_logs_manager
import logging
import sys
import os
import time
import getopt
import sys
from datetime import datetime
from datetime import timedelta

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger('Flow Logs UT')

def help_display():
    print "Usage: vpc_flow_logs_ut.py -s <start_time> -e <end_time>"
    print "Example - ./vpc_flow_logs_ut.py"+ " -s "+"\"08-11-2016 11:30:00\""+" -e "+ "\"08-11-2016 11:31:00\""
    print "\n-h or --help\t\thelp"
    print "\nMandatory parameters:"
    print "-s\t\tstart_time\t\t start_time in IST timezone format 'dd-mm-yyyy hh:mm:ss'"
    print "-e\t\tend_time\t\t end_time   in IST timezone format 'dd-mm-yyyy hh:mm:ss'"
    print "\nOptional parameters:"
    print "-a\t\tAccount id "
    print "-d\t\tSelect direction. Options are 1 for ingress 0 for egress.Required for query on account_id"
    print "-o\t\tSelect Output file"
    print "\n"


step_time_sec = 30
out_file_def  = "my_vpc_flow_log.txt"

def test_check_flow_logs_admin_all(start_time, end_time, admin_password,
                                      account_id, direction_ing, output_file):
    flow_manager = flow_logs_manager.FlowLogsManager()
    if (not output_file):
       output_file = out_file_def
    s_struct_time = time.struct_time
    s_struct_time = time.strptime(start_time, "%d-%m-%Y %H:%M:%S");
    e_struct_time = time.struct_time
    e_struct_time = time.strptime(end_time, "%d-%m-%Y %H:%M:%S");

    t_delta_sec = time.mktime(e_struct_time) - time.mktime(s_struct_time)
    t_delta_sec_orig = t_delta_sec

    if (t_delta_sec < 0 ):
        print "End time should be greater than start time"
        print "Usage: vpc_flow_logs_ut.py start_time end_time"
        return

    if (t_delta_sec > 7200) :
        print "Max time interval for query is 2 hours. Please try again"
        print "with lesser time interval"
        return

    curr_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    with open(output_file, "w") as text_file:
         text_file.write("\n VPC Flow Logs Start write at "+curr_time+"\n")
         print "\n VPC Flow Logs Collection Starting at "+curr_time+" Local\n"
         text_file.write("================= START ================ \n")

    new_start_time = datetime.fromtimestamp(time.mktime(s_struct_time))
    tdelta = timedelta(seconds=step_time_sec)
    steps_completed = step_time_sec
    percent_collection = (step_time_sec * 100) / t_delta_sec
    while (t_delta_sec >= step_time_sec):
         new_end_time = new_start_time + tdelta
         new_e_time_str = new_end_time.strftime("%d-%m-%Y %H:%M:%S")
         new_s_time_str = new_start_time.strftime("%d-%m-%Y %H:%M:%S")

         resp = flow_manager.show_vpc_flow_logs_admin(new_s_time_str,
                                                 new_e_time_str,
                                                 admin_password,
                                                 account_id,
                                                 direction_ing)
         with open(output_file, "a") as text_file:
              text_file.write(resp)
        
         percent_collection = (steps_completed * 100 )/t_delta_sec_orig
         print "{}% percent completed ".format(int(percent_collection))
         steps_completed = steps_completed + step_time_sec
         new_start_time = new_end_time
         t_delta_sec = t_delta_sec - step_time_sec

    curr_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    with open(output_file, "a") as text_file:
         text_file.write("\n VPC Flow Logs end write at "+curr_time+"\n")
         print("VPC Flow Logs collection Finished at "+curr_time+" Local \n")
         print "Results are stored at - "+output_file+"\n"
         text_file.write("================= END ================ \n")

def main(argv):
    account_id=None
    direction_ing=None
    start_time=None
    end_time=None
    output_file=None

    admin_password = os.environ.get('VPC_FLOW_LOGS_ADMIN_PASS')
    if (not admin_password) :
        print "Warning: Admin password is not set in config file\n"
        print "Displaying only VPC flow logs which are created by your account"

    try:
        opts, args = getopt.getopt(argv, "h:s:e:a:d:o", ["help"])
    except getopt.GetoptError:
        help_display()
        sys.exit(2)

    for opt, arg in opts:
        
        if opt in ("-h"):
            help_display()
            sys.exit()
        elif opt in ("-s"):
            start_time=arg
        elif opt in ("-e"):
            end_time=arg
        elif opt in ("-a"):
            account_id=arg
        elif opt in ("-d"):
            direction_ing=arg
        elif opt in ("-o"):
            output_file=arg

    if (not start_time) or (not end_time) :
        print "Usage: start_time and end_time should be specified"
        help_display()
        sys_exit()
    if (account_id is not None) and (not direction_ing) :
        print "Usage: direction_ing is manadatory when account_id is specified"
        help_display()
        sys_exit()
    if (account_id is not None) and (not admin_password) :
        print "Usage: admin_password should be set when account_id is specified"
        help_display()
        sys_exit()

    test_check_flow_logs_admin_all(start_time, end_time,
                                   admin_password, account_id,
                                   direction_ing, output_file)

if __name__ == "__main__":
    main(sys.argv[1:])

