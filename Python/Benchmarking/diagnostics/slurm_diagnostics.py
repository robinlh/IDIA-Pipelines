import sys
from subprocess import Popen, PIPE
from datetime import datetime

SACCT_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def read_jobs(file):
    job_ids = []
    with open(file, "r") as job_list:
        for line in job_list:
            job_ids.append(line.strip())
    return job_ids


def read_sacct(file):
    sacct_list = []
    with open(file, 'r') as sacct_lines:
        for line in sacct_lines:
            stripped = line.strip()
            if '.bat+' not in stripped:
                sacct_list.append(stripped.split())

    return sacct_list


def run_command(command):
    proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    proc.wait()
    if proc.returncode != 0:
        raise Exception(
            'Error {} running command: {}:\n{}'.format(proc.returncode, command, proc.stderr)
        )
    return proc.returncode, proc.stdout, proc.stderr


def get_sacct_output_as_list():
    cmd = 'sacct --format="JobID,ReqMem,Submit,Start,End,Elapsed,TotalCPU"'
    exit_status, stdout, stderr = run_command(cmd)
    sacct_list = []
    for line in stdout:
        stripped = line.strip()
        if '.bat+' not in stripped:
            sacct_list.append(stripped.split())
    return sacct_list


def get_sacct_diagnostics(job_list, sacct_list):
    data = []
    for item in sacct_list:
        for job_id in job_list:
            if job_id in item:
                data.append(item)
    return data


def compile_data(data):
    service_times = []
    arrival_times = []
    time_dict = {}

    for item in data:
        submit_time = datetime.strptime(item[2], SACCT_DATE_FORMAT)
        start_time = datetime.strptime(item[3], SACCT_DATE_FORMAT)
        end_time = datetime.strptime(item[4], SACCT_DATE_FORMAT)

        service_time = end_time - start_time
        arrival_time = start_time - submit_time

        service_times.append(service_time.total_seconds())
        arrival_times.append(arrival_time.total_seconds())

    time_dict['service_times'] = service_times
    time_dict['arrival_times'] = arrival_times
    return time_dict


def main(job_list_file, *args):
    job_list = read_jobs(job_list_file)
    # sacct_list = read_sacct(args[0])
    sacct_list = get_sacct_output_as_list()
    data = get_sacct_diagnostics(job_list, sacct_list)
    print(compile_data(data))
    # service, arrival = get_queue_times(data)
    # for ser, arr in zip(service, arrival):
    #     print('service time: {}'.format(ser.total_seconds()))
    #     print('arrival time: {}'.format(arr.total_seconds()))


if __name__ == '__main__':
    main(job_list_file='job_ids.txt', sacct_file='sample_sacct.txt')
