#!/bin/bash

beginning='#--------------------------------------------------------------------------------'
end='END OF VARIABLES SECTION'
pattern='TRITON (TRIANGLE TRANS-OCEAN BUOY NETWORK)'

# make it so they're all numbered
mv "MRB_CSV/ocldb1526349572.28401.MRB.csv" "MRB_CSV/ocldb1526349572.28401.MRB1.csv"

for i in {1..7}
    do
        file_in="MRB_CSV/ocldb1526349572.28401.MRB${i}.csv"
        file_out="MRB_CSV/triton_data.${i}.txt"

        # modify random MONTEREY seabird entries
        sed -z -i.bak 's/MicroCAT (Sea-Bird Electronics, Inc.),\n#--------------/MicroCAT (Sea-Bird Electronics, Inc.),\nEND OF VARIABLES SECTION,\n#--------------/g' ${file_in}

        # now pull the tao array data
        sed -n "/${beginning}/!b;:a;/${end}/!{$!{N;ba}};{/${pattern}/p}" ${file_in} > ${file_out}
        echo " --- Done with i = ${i}"
    done
