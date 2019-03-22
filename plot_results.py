import pickle
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import argparse

data_path = ""
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', type=str, default=data_path, help='the path for training dictionary')
args = parser.parse_args()

if args.data_path:
    data_path = args.data_path


with open(data_path,"rb") as f:
	data = pickle.load(f)

name = data_path.split("_")[1]

# summarize history for accuracy
plt.plot(data['categorical_accuracy'])
plt.plot(data['val_categorical_accuracy'])
plt.title('{} accuracy'.format(name))
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(data['loss'])
plt.plot(data['val_loss'])
plt.title('{} loss'.format(name))
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


