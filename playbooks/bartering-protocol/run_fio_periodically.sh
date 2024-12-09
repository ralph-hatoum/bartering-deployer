#!/bin/bash

# Set the interval in seconds (e.g., 3600 seconds for 1 hour)
INTERVAL=3600

# Set the duration for the entire run (e.g., 14400 seconds for 4 hours)
TOTAL_DURATION=14400

# List of filenames to test
files=("fio_test_file1" "fio_test_file2" "fio_test_file3")

# Calculate the end time
END_TIME=$(( $(date +%s) + TOTAL_DURATION ))

# Loop until the total duration is reached
while [ $(date +%s) -lt $END_TIME ]; do
  for file in "${files[@]}"; do
    echo "Running fio on $file..."

    # Create a temporary fio job file for the current file
    cat <<EOT > temp_fio_job_${file}.fio
[global]
ioengine=libaio
direct=1
size=10M
runtime=60
time_based
iodepth=32
directory=./data
filename=$file

[job_read]
bs=4k
rw=read

[job_write]
bs=4k
rw=write

[job_randread]
bs=4k
rw=randread

[job_randwrite]
bs=4k
rw=randwrite
EOT

    # Run fio with the temporary job file in the background
    fio temp_fio_job_${file}.fio > fio_${file}_stdout.log 2> fio_${file}_stderr.log &
  done

  # Wait for all background jobs to finish
  wait

  # Wait for the specified interval before running again
  sleep $INTERVAL
done
