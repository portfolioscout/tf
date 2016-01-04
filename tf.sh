#docker run -v /home/ruslan/tf:/tf -p 8888:8888 -it b.gcr.io/tensorflow/tensorflow /bin/sh -c 'cd /tf/nb;ipython notebook'
docker run -v /home/ruslan/tf:/tf -p 8888:8888 -it fa491baf16ec /bin/sh -c 'cd /tf/nb;ipython notebook --no-browser --ip="*"'

