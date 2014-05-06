 #!/bin/bash
if [ -f "simple-cpu-sensor.zip" ]; then
    rm simple-cpu-sensor.zip
fi;

mkdir build
rsync -r --exclude .git --exclude *.pyc --exclude build --exclude .plasmateprojectrc . build
cd build

zip -r  ../simple-cpu-sensor.zip .
cd ..
rm -rf ./build
