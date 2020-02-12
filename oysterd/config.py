import os
from enum import Enum
import datetime
from os.path import join
import logging
import json

class InputType(Enum):
    labelme = 0
    makesense = 1


class Config:
    folders = dict(
        data="/home/bsadrfa/behzad/projects/data_oyster/data/",
        save="/home/bsadrfa/behzad/projects/data_oyster/img_poly/",
        # img="/home/bsadrfa/behzad/projects/data_oyster/img/",
        # json="/home/bsadrfa/behzad/projects/data_oyster/json/",
        makesense="/home/bsadrfa/behzad/projects/data_oyster/database/",
        pred="/home/bsadrfa/behzad/projects/data_oyster/img_pred/",
        model="/home/bsadrfa/behzad/projects/data_oyster/model/",
        # output="/home/bsadrfa/behzad/projects/output_oyster/"
        output="../output/"
    )
    SOLVER_IMS_PER_BATCH = 2
    SOLVER_BASE_LR = 0.00025
    SOLVER_MAX_ITER = 100
    config_file = [
        "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml",
        "COCO-InstanceSegmentation/mask_rcnn_R_101_FPN_3x.yaml",
        "COCO-Detection/retinanet_R_101_FPN_3x.yaml",
        "COCO-Detection/rpn_R_50_FPN_1x.yaml"
    ]
    MODEL_WEIGHTS = ["model_final.pth"]
    resume = True
    thresh_percent = 25
    input = InputType.labelme

    def __init__(self, cfg_id=0):
        self.cfg_id = cfg_id
        self.datetime = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M")
        print('summary log @ ')
        print(self.logname())
        for f in self.folders.values():
            try:
                os.makedirs(f, exist_ok=True)
            except OSError:
                print("Error creating {}".format(f))

    def log_model(self):
        data = dict(
            SOLVER_BASE_LR=self.SOLVER_BASE_LR,
            SOLVER_MAX_ITER=self.SOLVER_MAX_ITER,
            config_file=self.config_file[self.cfg_id],
            resume=self.resume,
            thresh_percent=self.thresh_percent,
            id=self.cfg_id,
            datetime=self.datetime,
        )
        self.log(data, 'w')

    def logname(self):
        return join(join(self.folders['output'], '{:02d}'.format(self.cfg_id)), 'log_{}.json'.format(self.datetime))

    def log(self, data, access_mode='a'):
        try:
            with open(self.logname(), access_mode) as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Error dumping json file {}".format(self.logname()))
