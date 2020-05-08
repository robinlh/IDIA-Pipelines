import sys
import subprocess


def read_jobs(file):
    job_ids = []
    with open(file, "r") as job_list:
        for line in job_list:
            job_ids.append(eval(line))

    return job_ids


def parse_data(line):
    data = line.split(' ')
    return data


def sacct_diagnostics(job_ids, file_to_write, *args):
    intermediate_file = 'run_times.txt'
    data = []
    for job in job_ids:
        time_cmd = 'sacct --format="NCPUS,MaxRSS,Submit,Start,End,JobID" | grep {} >> {}'.format(job, intermediate_file)
        proc = subprocess.Popen(time_cmd, shell=True, stdout=subprocess.PIPE)
        proc.wait()
        print(proc.returncode)

    with open(intermediate_file, 'r') as sacct_results:
        for line in sacct_results:
            if not line.endswith('.bat+'):
                data.append(parse_data(line))

    return data


def main(job_list_file):
    jobs = read_jobs(job_list_file)
    print(sacct_diagnostics(jobs, 'nada'))


if __name__ == '__main__':
    main(sys.argv[1])
