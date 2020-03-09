def write_batch(filename, script, script_args, container_path, *args):
    """
    :param filename: name of file to write to
    :param script: python script to be run in sbatch file
    :param script_args: any arguments the script requires as string with items separated by space
    :param container_path: path to container to use
    :param args: parameters for the cluster
    :return: sbatch file
    """
    params = {'script': script,
              'script_args': script_args,
              'container_path': container_path,
              'cpus': args[0],
              'job_name': args[1]}

    content = """#!/bin/bash\n
    #SBATCH --job-name={job_name}
    #SBATCH --cpus-per-task={cpus}
    #SBATCH --mem=16GB
    #SBATCH --output=logs/bench-%j-stdout.log
    #SBATCH --error=logs/bench-%j-stderr.log
    
    echo "Submitting SLURM job: {script} using {cpus} cores"
    singularity exec {container_path} python {script} {script_args}
    """

    # insert arguments and remove whitespace
    content = content.format(**params).replace("    ", "")
    sbatch_file = open(filename, 'a')
    sbatch_file.write(content)


def write_batch_all(scripts, script_args, container_path, *args):
    """
    :param scripts: list of scripts
    :param script_args: list or arguments
    :param container_path: path to container to be used
    :param args: sbatch arguments
    :return:
    """
    for i, script in enumerate(scripts):
        filename = script + '_sbatch.sh'
        write_batch(filename, script, script_args[i], container_path, args[0], args[1])


scripts = ['script1.py', 'script2.py', 'script3.py', 'script4.py']
script_args = ['32 test_script_creation.log', '32 test_script_creation.log', '32 test_script_creation.log', '32 test_script_creation.log']
container_path = '/some/path/container.simg'

write_batch_all(scripts, script_args, container_path, 32, 'test_func')
