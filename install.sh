 #!/bin/bash
 
if plasmapkg -l |  grep -q "simple-cpu-sensor"
    then plasmapkg -u .
    else plasmapkg -i .
fi;