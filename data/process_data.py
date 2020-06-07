import os
from sklearn.model_selection import train_test_split
import shutil
import cv2
import numpy as np
import json

def initialize_folders():
    os.makedirs('images', exist_ok=True)
    os.makedirs('labels', exist_ok=True)
    print('Folders initialized for images and labels')
    os.makedirs('images/test', exist_ok=True)
    os.makedirs('images/train', exist_ok=True)
    os.makedirs('labels/test', exist_ok=True)
    os.makedirs('labels/train', exist_ok=True)
    print(f'initialized folders for train/test split')
        

def csv_to_darknet(filename):
    knife_class_id = 43
    with open(filename, 'r') as file:
        for index, line in enumerate(file):
            print(f'on line: {index}')
            line = line.split(',')
            if index == 0:
                continue
            else:
                image_name = line[9]
                img_width = int(line[7])
                img_height = int(line[8])
                width = int(line[26])
                height = int(line[27])
                x = (int(line[24]) + (width//2))/img_width
                y = (int(line[25]) + (height//2))/img_height
                width /= img_width
                height /= img_height
                img_folder_name = image_name[:-3] + "txt"
                if image_name == '91303750_222109369133602_1482966226358501376_n.jpg':
                    print(line[7:9], line[24:28])
                    print(img_width, img_height, x, y, width, height)
                # with open(f'labels/{img_folder_name}', 'w') as label_file:
                #     label_file.write(f'{knife_class_id} {x} {y} {width} {height}')


def rename_files():
    for image in os.listdir('labels'):
        if "'" in image:
            new_image = image.replace("'", "_")
            os.rename(f'labels/{image}', f'labels/{new_image}')

def ensure_similar(labels, images):
    # assert len(labels) == len(images), f'len(labels) {len(labels)} != len(images) {len(images)}'
    failed = False
    missing_labels = []
    for i in range(len(labels)):
        if failed or not labels[i][:-3] == images[i][:-3]:
            missing_labels.append(labels[i])
            failed = True
            
    if failed: 
        raise Exception(f"Image does not exist for these {missing_labels}")
    else:
        print('test passed')

def data_split(val_amount=0, test_amount=0.1): 
    labels = [label for label in os.listdir('labels') if '.txt' in label.lower()]
    images = [image for image in os.listdir('images') if '.jpg' in image.lower() and image[:-3] + 'txt' in labels]
    images.sort()
    labels.sort()
    ensure_similar(labels, images)
    x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=test_amount)
    # print(f'x_train: {x_train}')
    # print(f'x_test: {x_test}')
    print(f'len(images): {len(images)}, split_total: {(len(x_train), len(x_test), len(x_train) + len(x_test))}')
    same = 0
    wrong = 0
    print('Moving same training data')
    # Split the training labels
    for i in range(len(x_train)):
        image = x_train[i]
        label = y_train[i]
        shutil.move(f'images/{image}', f'images/train/{image}')
        shutil.move(f'labels/{label}', f'labels/train/{label}')
    print('Finished moving training data')
    print('Moving Test Data')
    # Split the test labels
    for i in range(len(x_test)):
        image = x_test[i]
        label = y_test[i]
        shutil.move(f'images/{image}', f'images/test/{image}')
        shutil.move(f'labels/{label}', f'labels/test/{label}')
    print('Finished moving test data')


def create_train_test_txt():
    base_train_path = 'images/train/'
    base_test_path = 'images/test/'
    print('Creating Train data file')
    with open('knife_only_train.txt', 'w') as train_data_file:
        train_images = os.listdir(base_train_path)
        for image in train_images:
            train_data_file.write(f'data/knife_only/images/train/{image}\n')
    print('Done')
    print('Creating Test data file')
    with open('knife_only_test.txt', 'w') as test_data_file:
        test_images = os.listdir(base_test_path)
        for image in test_images:
            test_data_file.write(f'data/knife_only/images/test/{image}\n')
    print('Done')

def demo_data(csv_file_name):
    limit = float('inf')
    with open(csv_file_name, 'r') as csv_file:
        for index, line in enumerate(csv_file):
            line = line.strip().split(',')
            line = list(map(lambda x: x.replace('"', ''),line))
            if index == 0:
                continue
            elif index >= limit:
                break
            else:
                image_name = line[9]
                img_width = int(line[7])
                img_height = int(line[8])
                x = int(line[24])#/img_width
                y = int(line[25])#/img_height
                width = int(line[26])#/img_width
                height = int(line[27])#/img_height
                img_folder_name = image_name[:-3] + "txt"
                image = cv2.imread(f'images/{image_name}')
                x1 = x
                x2 = x + (width)
                y1 = y 
                y2 = y + (height)
                start = (int(x1), int(y1))
                end = (int(x2),int(y2))
                color = (0, 0, 255)
                if True:#'img' in image_name.lower():
                    image = cv2.rectangle(image, start, end, color, 2)
                    center = (int(x + width//2), int(y + height//2))
                    image = cv2.circle(image, center, radius=0, color=color, thickness=-1)
                    cv2.imwrite(f'nigel_only_images/{image_name}', image)
                    # image = cv2.resize(image, (608, 608))
                    # cv2.imshow(image_name, image)
                    # key = cv2.waitKey(0)
                    # # If esc(27) key
                    # # If space(32)
                    # if key == 32:
                    #     break

def parse_json(json_file_name):
    with open(json_file_name, 'r') as json_file:
        data = json.load(json_file)
    image_list = data['images']
    annot_list = data['annotations']
    annot_index = 0
    for index, image_details in enumerate(image_list):
        image_read = False
        # Gather image related stuffs
        image_name = image_details['file_name']
        if "'" in image_name:
            image_name = image_name.replace("'", "_")
        image_width = image_details['width']
        image_height = image_details['height']
        image_id = int(image_details['id'])
        image_label_name = image_name[:-3] + 'txt'
        # img = cv2.imread(f'images/{image_name}')
        # Gather segmentations stuffs
        # print(index, annot_list[annot_index]['image_id'], image_id)
        # print(int(annot_list[annot_index]['image_id']) == image_id)
        try:
            with open(f'labels/{image_label_name}', 'w') as label_file:
                while int(annot_list[annot_index]['image_id']) == image_id:
                    annotation_details = annot_list[annot_index]
                    bbox = annotation_details['bbox']
                    class_id = 0
                    x, y, width, height = bbox
                    img_folder_name = image_name[:-3] + "txt"
                    if not image_read:
                        image = cv2.imread(f'images/{image_name}')
                        image_read = True
                    x_center = x  + (width//2)
                    x_center /= image_width
                    width /= image_width

                    y_center = y + (height//2)
                    y_center /= image_height
                    height /= image_height

                    label_file.write(f'{class_id} {x_center} {y_center} {width} {height}\n')

                    # x1 = x
                    # x2 = x + (width)
                    # y1 = y 
                    # y2 = y + (height)
                    # start = (int(x1), int(y1))
                    # end = (int(x2),int(y2))
                    # color = (0, 0, 255)
                    # image = cv2.rectangle(image, start, end, color, 2)
                    # center = (int(x + width//2), int(y + height//2))

                    annot_index += 1
        except IndexError:
            print(f'finished {json_file_name}')
            pass
        # cv2.imwrite(f'labeled_images/{image_name}', image)
            
def parse_all_jsons():
    json_files = os.listdir()
    for json_file in json_files:
        if 'json' in json_file:
            print(f'on file: {json_file}')
            parse_json(json_file)
    

if __name__ == "__main__":
    initialize_folders()
    csv_file_name = "via_export.csv"#"coco-knife-524-images-annots.csv"
    # json_file = 'via_export_coco.json'
    # csv_to_darknet(csv_file_name)
    # parse_json(json_file)
    parse_all_jsons()
    rename_files()
    data_split()
    create_train_test_txt()
    # demo_data(csv_file_name)