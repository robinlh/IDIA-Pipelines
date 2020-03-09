#!/bin/bash

jid0=$(sbatch benchmarks_c_1.sh)
jid0=${jid0##* }
jid1=$(sbatch --dependency=afterok:$jid0 benchmarks_c_4.sh)
jid1=${jid1##* }
jid2=$(sbatch --dependency=afterok:$jid1 benchmarks_c_8.sh)
jid2=${jid2##* }
jid3=$(sbatch --dependency=afterok:$jid2 benchmarks_c_16.sh)
jid3=${jid3##* }
jid4=$(sbatch --dependency=afterok:$jid3 benchmarks_c_32.sh)
jid4=${jid4##* }
