#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/opt/anaconda3/envs/pcn_crash_course/lib/python3.12/site-packages
/opt/anaconda3/envs/pcn_crash_course/bin/python /opt/anaconda3/envs/pcn_crash_course/lib/python3.12/site-packages/pcntoolkit/util/runner.py /Users/stijndeboer/Projects/PCN/Crash course/resources/hbr_runner_sandbox/temp_dir/python_callable_0.pkl /Users/stijndeboer/Projects/PCN/Crash course/resources/hbr_runner_sandbox/temp_dir/data_0.pkl > /Users/stijndeboer/Projects/PCN/Crash course/resources/hbr_runner_sandbox/log_dir/0.out 2> /Users/stijndeboer/Projects/PCN/Crash course/resources/hbr_runner_sandbox/log_dir/0.err
exit_code=$?
if [ $exit_code -eq 0 ]; then
    touch /Users/stijndeboer/Projects/PCN/Crash course/resources/hbr_runner_sandbox/log_dir/0.success
fi
exit $exit_code
