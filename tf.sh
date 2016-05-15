#docker run -v /home/ruslan/tf:/tf -p 8888:8888 -it b.gcr.io/tensorflow/tensorflow /bin/sh -c 'cd /tf/nb;ipython notebook'
docker run -v ~/tf:/conda -p 8888:8888 -it $1 /bin/sh -c 'cd /conda/nb;ipython notebook --no-browser --ip="*"'

