sudo apt-get update
sudo apt-get upgrade
sudo apt-get install rpi.gpio

python3 -m venv venv
source venv/bin/activate

pip --version
python -V

sudo apt-get install pigpiod -y
pip install pigpio

sudo apt install libwebp6 libtiff5 libjbig0 liblcms2-2 libwebpmux3 libopenjp2-7 libzstd1 libwebpdemux2 libjpeg-dev -y

sudo apt-get install python-dev python-setuptools -y
pip install pillow

sudo apt install libatlas3-base libgfortran5 -y
pip install numpy

sudo apt-get install git -y

pip install tqdm readchar

git clone https://github.com/evildmp/BrachioGraph.git

cd BrachioGraph && sudo pigpiod && source venv/bin/activate && python