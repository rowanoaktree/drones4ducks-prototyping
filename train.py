#load the modules
import os
import time
import numpy as np
from deepforest import main 
from deepforest import get_data
from deepforest import utilities
from deepforest import preprocess

from torch.utils.data import DataLoader
from dataset import BirdsDataset

#Prepare training and validation data
# trainimg_dir = r"/datadrive/Data/train/"
# valimg_dir = r"/datadrive/Data/val/"

# annotations_file = r"/datadrive/Data/train_filter3.csv"
# validation_file = r"/datadrive/Data/val_filter3.csv"

label_dict = {"Duck":0, "Goose":1, "Crane":2}

#initial the model 
m = main.deepforest(num_classes=3, label_dict=label_dict, config_file="config.yml")

#for scratch training my own model, comment out these four lines and save the checkpoint into a different directory
deepforest_release_model = main.deepforest()
deepforest_release_model.use_bird_release()
m.model.backbone.load_state_dict(deepforest_release_model.model.backbone.state_dict())
m.model.head.regression_head.load_state_dict(deepforest_release_model.model.head.regression_head.state_dict())


#change the corresponding config file
m.config['gpus'] = None #'1' #move to GPU and use all the GPU resources
# m.config["train"]["csv_file"] = annotations_file
# m.config["train"]["root_dir"] = trainimg_dir
# m.config["train"]["fast_dev_run"] = True
# m.config["train"]["batch_size"] = 2

# m.config["score_thresh"] = 0.4
# m.config['epochs'] = 100

# m.config["validation"]["csv_file"] = validation_file
# m.config["validation"]["root_dir"] = valimg_dir
# m.config["validation"]["val_accuracy_interval"] = 1

#create a pytorch lighting trainer used to training 
m.create_trainer(**{
    'num_sanity_val_steps': 0,
    'check_val_every_n_epoch': 1,
    'devices': 1
})

# dataset_val = BirdsDataset(
#     data_root='/datadrive/Data/val',
#     csv_file='/datadrive/Data/val_filter4.csv',
#     label_dict=label_dict
# )
# dl_val = DataLoader(dataset_val, batch_size=m.config['batch_size'], num_workers=m.config['workers'])
# dataset_val = m.load_dataset('/datadrive/Data/val_filter4.csv', '/datadrive/Data/val', train=False)
# m.trainer.validate(m, dataset_val)

# m.trainer.validate(m, dl_val)
# #use Bird Detector
# m.use_bird_release()

#Start training
start_time = time.time()
m.trainer.fit(m)
m.trainer.save_checkpoint("{}/checkpoint.pl".format("modelstates"))
assert m.num_classes == 3
print(f"--- Training on GPU: {(time.time() - start_time):.2f} seconds ---")