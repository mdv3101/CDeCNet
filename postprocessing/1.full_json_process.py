import json
import os
import shutil

list_name = os.listdir("path_of_gt_text_files/")
gt_json = "path_of_gt_json_file/instances_val2014.json"
output_json = "path_of_CdeCNet_output_json_file/output_1.0x.bbox.json"
output_txt_path = "path_to_write_text_file_using_json/output_text/"

if not os.path.exists(output_txt_path):
    os.mkdir(output_txt_path)
id_name_mapping = {}
category_id_name_mapping = {}
with open(gt_json) as f:
    data = json.load(f)
    for q in data['images']:
        q_image_id = q['id']
        image_name = q['file_name']
        file_basename = os.path.basename(image_name)
        filename, file_extension = os.path.splitext(file_basename)
        id_name_mapping[q_image_id] = filename
    for c in data["categories"]:
        category_id = c['id']
        category_name = c['name']
        category_id_name_mapping[category_id] = category_name
#print(id_name_mapping)
#print(category_id_name_mapping)
f.close()
with open(output_json) as f2:
    data_json = json.load(f2)
    for data in data_json:
        image_id = data["image_id"]
        category_id = int(data["category_id"])
        bbox = data["bbox"]
        score = data["score"]
        try:
            image_name = id_name_mapping[image_id]
            caption = category_id_name_mapping[category_id]
            f = open(output_txt_path+image_name+".txt","a")
            if score >= 0.95:
                x_min = bbox[0]
                y_min = bbox[1]
                width = bbox[2]
                height = bbox[3]
                x_max = x_min + width
                y_max = y_min + height
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
            else:
                print("Score Less:",score,image_name)
            f.close()
        except Exception as e:
            print("--",e)
files_detection = len(os.listdir(output_txt_path))
for file in list_name:
    filename, fileextension = os.path.splitext(file)
    if filename+".txt" not in os.listdir(output_txt_path):
        #print(file)
        f = open(output_txt_path+filename+".txt","a")
        f.close()
print("Total files created",len(list_name),"--",files_detection,"--",len(os.listdir(output_txt_path)))
