## Remove overlapping bounding boxes
import os
import math

threshold = 0.5
overlap_threshold = 0.05

base_path = 'root_directory_containing_the_multiscale_folders/'
input_path = base_path+"multiscale_output/"
output_path = base_path+"multiscale_nms/"
if not os.path.exists(output_path):
    os.mkdir(output_path)

def read_file_return_bbox_dict(read_text_path):
    bbox_dict = {}
    idx =0
    with open(read_text_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            data = line.split()
            caption = data[0]
            confidence = float(data[1])
            if confidence<=threshold:
                continue
            x1 = int(float(data[2]))
            y1 = int(float(data[3]))
            x2 = int (float(data[4]))
            y2 = int(float(data[5]))
            bbox_dict[idx] = [(x1,y1),(x2,y2)]
            idx = idx+1
    return bbox_dict

def write_file(text_file,bbox):
    caption = 'table'
    score = 0.99
    f = open(output_path+text_file,"a")
    x_min = bbox[0][0]
    y_min = bbox[0][1]
    x_max = bbox[1][0]
    y_max = bbox[1][1]
    f.write(caption)
    f.write(" ")
    f.write(str(score))
    f.write(" ")
    f.write(str(x_min))
    f.write(" ")
    f.write(str(y_min))
    f.write(" ")
    f.write(str(x_max))
    f.write(" ")
    f.write(str(y_max))
    f.write("\n")
    f.close()

def Overlap_percentage(l1, r1, l2, r2):
    x_left = max(l1[0], l2[0])
    y_top = max(l1[1], l2[1])
    x_right = min(r1[0], r2[0])
    y_bottom = min(r1[1], r2[1])
    if x_right < x_left or y_bottom < y_top:
        return 0.0,0,0
    within_box = 0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    bb1_area = (r1[0] - l1[0]) * (r1[1] - l1[1])
    bb2_area = (r2[0] - l2[0]) * (r2[1] - l2[1])
    if bb2_area>bb1_area:
        greater_area =2
        if intersection_area >=(0.9*bb1_area) and intersection_area<=(1.1*bb1_area):
            within_box = 1
    else:
        greater_area =1
        if intersection_area >= (0.9*bb2_area) and intersection_area<=(1.1*bb2_area):
            within_box = 1
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    return iou, greater_area, within_box

def check_overlap(bbox_1,bbox_2):
    l1 = bbox_1[0]
    r1 = bbox_1[1]
    l2 = bbox_2[0]
    r2 = bbox_2[1]
    overlap_per,greater_area, within_box = Overlap_percentage(l1, r1, l2, r2)
    if overlap_per>overlap_threshold and within_box==1:
        #print(bbox_1,bbox_2)
        print("Rectangle within")
        d1 = math.sqrt(((l1[0]-l2[0])**2)+((l1[1]-l2[1])**2))
        d2 = math.sqrt(((r1[0]-r2[0])**2)+((r1[1]-r2[1])**2))
        if greater_area == 1:
            thrs = 0.2*r1[0]
        else:
            thrs = 0.2*r2[0]


    return overlap_per,greater_area,within_box

for text_file in os.listdir(input_path):
    if text_file.endswith('txt'):
        keep_bbox = {}
        change_bbox = {}
        bbox_dict_org = read_file_return_bbox_dict(input_path+text_file)
        if not bbox_dict_org:
            f = open(output_path+text_file,"a")
            f.close()
            continue
        keep_bbox = bbox_dict_org.copy()
        box_to_remove = []
        for i in range(0,len(bbox_dict_org)):
            for j in range(i+1,len(bbox_dict_org)):
                overlap_per,greater_area,within_box = check_overlap(bbox_dict_org[i],bbox_dict_org[j])
                if within_box==1:
                    print(text_file,bbox_dict_org[i],bbox_dict_org[j])
                    if greater_area ==1:
                        box_to_remove.append(j)
                    else:
                        box_to_remove.append(i)
        for key, value in bbox_dict_org.items():
            if key  in box_to_remove:
                continue
            write_file(text_file,bbox_dict_org[key])
