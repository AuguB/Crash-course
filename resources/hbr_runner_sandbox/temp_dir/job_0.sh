#!/bin/bash
    
#SBATCH --job-name=normative_job_0
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=15:00:00
#SBATCH --mem=5GB
#SBATCH --error=/Users/stijndeboer/Projects/PCN/Crash course/resources/hbr_runner_sandbox/log_dir/job_0.err
#SBATCH --output=/Users/stijndeboer/Projects/PCN/Crash course/resources/hbr_runner_sandbox/log_dir/job_0.out

/opt/anaconda3/envs/pcn_crash_course/bin/python /opt/anaconda3/envs/pcn_crash_course/lib/python3.12/site-packages/pcntoolkit/util/runner.py /Users/stijndeboer/Projects/PCN/Crash course/resources/hbr_runner_sandbox/temp_dir/python_callable_0.pkl /Users/stijndeboer/Projects/PCN/Crash course/resources/hbr_runner_sandbox/temp_dir/data_0.pkl
exit_code=$?
if [ $exit_code -eq 0 ]; then
    touch /Users/stijndeboer/Projects/PCN/Crash course/resources/hbr_runner_sandbox/log_dir/job_0.success
fi
exit $exit_code
