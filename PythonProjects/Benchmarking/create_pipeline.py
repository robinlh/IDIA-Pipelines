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
    sbatch_file.close()


def write_batch_all(scripts, script_args, container_path, *args):
    """
    :param scripts: list of scripts
    :param script_args: list or arguments
    :param container_path: path to container to be used
    :param args: sbatch arguments
    :return:
    """
    script_list = []
    for i, script in enumerate(scripts):
        filename = str(script).replace('.py', '') + '_sbatch.sh'
        script_list.append(filename)
        write_batch(filename, script, script_args[i], container_path, args[0], args[1])

    return script_list


def write_pipeline(script_list, filename):
    """
    :param script_list: list of batch scripts (returned by write_batch_all() function)
    :param filename: name of file to be written
    :return:
    """
    pipeline_script = open(filename, 'a')
    pipeline_script.write('#!/bin/bash\n')
    pipeline_script.write('\n')
    pipeline_script.write('jid0=$(sbatch ' + script_list[0] + ')\n')
    pipeline_script.write('jid0=${jid0##* }\n')
    for i, script in enumerate(script_list):
        pipeline_script.write('jid' + str(i + 1) + '=$(sbatch --dependency=afterok:$jid' + str(i) + ' ' +
                              script_list[i + 1] + ')\n')
        pipeline_script.write('jid' + str(i + 1) + '=${jid' + str(i + 1) + '##* }\n')


if __name__ == '__main__':
    scripts = ['script1.py', 'script2.py', 'script3.py', 'script4.py']
    script_args = ['32 test_script_creation.log', '32 test_script_creation.log', '32 test_script_creation.log',
                   '32 test_script_creation.log']
    container_path = '/some/path/container.simg'

    batch_list = write_batch_all(scripts, script_args, container_path, 32, 'test_func')
    write_pipeline(batch_list, 'pipeline.sh')
