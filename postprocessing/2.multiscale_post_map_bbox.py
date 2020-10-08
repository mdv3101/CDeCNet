## It will help in creating a single file by merging the multiscale outputs and voting out those boxes which are present in less than 4 scales.

import os

threshold = 0.5
overlap_threshold = 0.8
count_threshold = 4
base_path = 'root_directory_containing_the_multiscale_folders/'
scales = ['0.7x','0.8x','0.9x','1.0x','1.1x','1.2x','1.3x']
original_scale = base_path+'1.0x/output_text/'
if not os.path.exists(base_path+"multiscale_output/"):
    os.mkdir(base_path+"multiscale_output/")
def read_file_return_bbox_dict(read_text_path):
    bbox_dict = {}
    idx =0
    with open(read_text_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            data = line.split()
            caption = data[0]
            if caption != 'table':
                continue
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
    f = open(base_path+"multiscale_output/"+text_file,"a")
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
    #print(l1,r1,l2,r2)
    # determine the coordinates of the intersection rectangle
    x_left = max(l1[0], l2[0])
    y_top = max(l1[1], l2[1])
    x_right = min(r1[0], r2[0])
    y_bottom = min(r1[1], r2[1])

    if x_right < x_left or y_bottom < y_top:
        return 0.0,0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (r1[0] - l1[0]) * (r1[1] - l1[1])
    bb2_area = (r2[0] - l2[0]) * (r2[1] - l2[1])
    if bb2_area>bb1_area:
        greater_area =2
    else:
        greater_area =1
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    return iou, greater_area


def check_overlap(bbox_1,bbox_2):
    #print(bbox_1,"\n",bbox_2)
    vote_dict = {}
    bbox_dict = {}
    counted_key2 = []
    if not bbox_1:
        for key2, value2 in bbox_2.items():
            vote_dict[key2] = 1
            bbox_dict[key2] = bbox_2[key2]
    else:
        for key1,value1 in bbox_1.items():
             l1 =  value1[0]
             r1 =  value1[1]
             vote_dict[key1] = 1
             for key2, value2 in bbox_2.items():
                 l2 = value2[0]
                 r2 = value2[1]
                 overlap_per,greater_area = Overlap_percentage(l1, r1, l2, r2)
                 #print(overlap_per)
                 if overlap_per > overlap_threshold:
                     vote_dict[key1] = vote_dict[key1]+1
                     if greater_area ==2:
                        bbox_dict[key1] = bbox_2[key2]
                     else:
                         bbox_dict[key1] = bbox_1[key1]
                     counted_key2.append(key2)
                     continue
             #print(counted_key2)
             if vote_dict[key1]==1:
                 bbox_dict[key1] = bbox_1[key1]
        new_detections = list(set(bbox_2.keys())-set(counted_key2))
        #print(new_detections)
        last_idx = len(bbox_dict.keys())
        for i in new_detections:
             bbox_dict[last_idx] = bbox_2[i]
             vote_dict[last_idx] = 1
             last_idx = last_idx +1
    return vote_dict, bbox_dict


for text_file in os.listdir(original_scale):
    if text_file.endswith('txt'):
        bbox_dict_org = {}
        vote_dict_main ={}
        file_written = 0
        file_prefix = text_file.split(".txt")[0]
        read_text_path = original_scale+text_file
        bbox_dict_org = read_file_return_bbox_dict(read_text_path)

        #print(bbox_dict_org)
        for i in scales:
            read_text_path = base_path+str(i)+'/output_text/'+text_file
            bbox_dict_2 ={}
            bbox_dict_2 = read_file_return_bbox_dict(read_text_path)

            #print(bbox_dict_2)
            vote_dict, bbox_dict = check_overlap(bbox_dict_org,bbox_dict_2)
            #print(vote_dict)
            for key,value in vote_dict.items():
                if key in vote_dict_main:
                    vote_dict_main[key] = vote_dict_main[key]+vote_dict[key]-1
                else:
                    vote_dict_main[key] = vote_dict[key]
            for key,value in bbox_dict.items():
                bbox_dict_org[key] = bbox_dict[key]
        if text_file == 'POD_2285.txt':
            print(text_file)
            print(vote_dict_main)
            print(bbox_dict_org)
        for key, value in vote_dict_main.items():
            if vote_dict_main[key]>=count_threshold:
                write_file(text_file,bbox_dict_org[key])
                file_written =1
        if file_written ==0:
            f = open(base_path+"multiscale_output/"+text_file,"a")
            f.close()
