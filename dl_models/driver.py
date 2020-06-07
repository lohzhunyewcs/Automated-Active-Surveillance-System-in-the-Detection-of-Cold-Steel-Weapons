import sys
import os
import cv2
import torch
import random

# CenterNet
def getCenterNetModel(linux):
    if linux:
        CENTERNET_PATH = '/home/student/Desktop/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/models/CenterNet/src/lib'
    else:
        CENTERNET_PATH = 'D:\GitLab_respos\Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons\models\CenterNet\src\lib'
    sys.path.insert(0, CENTERNET_PATH)
    if linux:
        src_path = '/home/student/Desktop/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/models/CenterNet/src'
    else:
        src_path = 'D:\GitLab_respos\Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons\models\CenterNet\src'
    sys.path.insert(0, src_path)
    print(os.listdir(CENTERNET_PATH))
    from detectors.detector_factory import detector_factory
    from opts import opts

    MODEL_PATH = '/home/student/Desktop/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/models/CenterNet/models/ctdet_coco_dla_2x.pth'

    TASK = 'ctdet' # or 'multi_pose' for human pose estimation

    """
    help='level of visualization.'
        '1: only show the final detection results'
        '2: show the network output features'
        '3: use matplot to display' # useful when lunching training with ipython notebook
        '4: save all visualizations to disk')
    """
    opt = opts().init('{} --load_model {} --debug 4'.format(TASK, MODEL_PATH).split(' '))
    detector = detector_factory[opt.task](opt)

    return detector

def centerNetPredict(detector, img):
    return detector.run(img)#['results']

# CenterNet Done

class YoloConfig:
    def __init__(self, linux, coco=False):
        cfg = 'yolov3/cfg/yolov3-spp.cfg'
        if linux:
            raise Exception('TODO!')
            self.cfg = 'D:/GitLab_respos/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/models/yolov3/cfg/yolov3-spp.cfg'
            self.names = 'yolov3/data/coco.names'
            self.weights = "yolov3/yolov3-spp.pt"
            self.source = 'data/samples'#raise Exception # prob not needed
            self.output = "yolov3/output"
        else:
            if coco:
                base_path = 'D:/GitLab_respos/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/dl_models/'
                self.cfg = base_path + 'yolov3/cfg/yolov3-spp.cfg'
                self.names = base_path + 'yolov3/data/coco.names'
                self.weights = base_path + "yolov3/yolov3-spp.pt"
                self.source = base_path +'yolov3/data/samples'#raise Exception # prob not needed
                self.output = base_path + "yolov3/output"
            else:
                base_path = 'D:/GitLab_respos/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/dl_models/'
                self.cfg = base_path + 'yolov3/cfg/yolov3-spp-knife.cfg'
                self.names = base_path + 'yolov3/data/knife_only.names'
                self.weights = base_path + "yolov3/weights/best_knife_only_spp_pretrained_cls_00001_2.pt"
                self.source = base_path +'yolov3/data/samples'#raise Exception # prob not needed
                self.output = base_path + "yolov3/output"
        self.img_size = 416
        self.conf_thres = 0.3
        self.iou_thres = 0.6
        self.fourcc = 'mp4v'
        self.half = False
        self.device = ''
        self.view_image = False
        self.save_txt = False
        self.classes = None
        self.agnostic_nms = False
        self.view_img = False

# YOLOV3
def yolov3(linux):
    # image_path = "/home/student/Desktop/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/models/yolov3/meme.jpg"
    # # os.system(f"cd yolov3")
    # os.chdir("yolov3")
    # os.system(f"python3 detect.py --source {image_path} --cfg cfg/yolov3-spp.cfg --weights yolov3-spp.pt")
    # os.chdir("..")
    # YOLOV3_PATH = '/home/student/Desktop/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/models/yolov3'
    # sys.path.insert(0, YOLOV3_PATH)

    # Code
    if linux:
        YOLO_PATH= '/home/student/Desktop/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/dl_models/yolov3'
    else:
        YOLO_PATH = 'D:\GitLab_respos\Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons\dl_models\yolov3'
    sys.path.insert(0, YOLO_PATH)
    from models import Darknet
    opt = YoloConfig(linux)
    img_size= opt.img_size
    out, source, weights, half, view_img, save_txt = opt.output, opt.source, opt.weights, opt.half, opt.view_img, opt.save_txt
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    
    model = Darknet(opt.cfg, img_size)
    model.load_state_dict(torch.load(weights)['model'])
    return model, opt
    

def yolo_predict(model, opt, image=None, to_read_img=True):
    from dl_models.yolov3.detect import detect_mod as yolo_detect
    if image is not None:
        opt.source = image
    if to_read_img:
        img0 = cv2.imread(image)
    else:
        img0 = image
    detected_classes, img = yolo_detect(opt, model, img0, img_size=416)
    result = (img, 'knife' in detected_classes)
    # cv2.imshow('window', img)
    # cv2.waitKey(0)
    # print(result)
    return result

if __name__ == "__main__":
    # # CenterNeeet
    # centerNet = getCenterNetModel()
    linux = False
    image_name = 'meme.jpg'
    if linux:
        img = f'/home/student/Desktop/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/test_images/{image_name}'
    else:
        img = f'D:/GitLab_respos/Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons/test_images/{image_name}'
    # cv2_img = cv2.imread(img)
    # print(cv2_img)
    # print(img)
    # result = centerNetPredict(centerNet, img)
    # print('done')

    # YOLO
    yolo_model, opt = yolov3(linux=linux)
    yolo_predict(yolo_model, opt, img)
    # YOLO DONE

