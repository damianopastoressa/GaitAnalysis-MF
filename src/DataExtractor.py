import cv2
import os
import json
from DataStorage import DataStorage

class DataExtractor:
    
    def __init__(self, sub_folder):
        #folder with video recorded by camera
        self.videos_dir = '../videos/'+sub_folder
        
        

    #function to extract frames from the selected video and to store json files with walking data
    def extraction(self, video_path, frames_dir, json_dir):
        openpose_command = './../openpose/build/examples/openpose/openpose.bin --video ' + video_path
        openpose_command += ' --write_json ' + json_dir + ' --write_images ' + frames_dir
        os.system(openpose_command)



    #function to read walking data from json files
    def getDataByJson(self, json_dir, width, height, fps):
        #array in which to store x and y coordinates of each body part (0 if a specific body part isn't visible in a specific frame)
        pose2d = []
        #array in which to store visibilities of each body part 
        visibilities = []
        #array in which to store beginning time of each frame
        time = []        
        #list of json files
        json_files = os.listdir(json_dir)
        #sorting list of json files
        json_files.sort()
        #for each json file
        for j in range(0, len(json_files)):
            #loading json file
            with open(json_dir +json_files[j], 'r') as f:
                loaded_json = json.load(f)
            #array in which to store x and y coordinates of each body part of person in the frame
            frame_coords = []
            #array in which to store visibilities of each body part of person in the frame
            frame_visib = []
            #storing data of the person in the frame
            if len(loaded_json['people']) > 0:
                coords = loaded_json['people'][0]['pose_keypoints_2d']
                #cycle to analize each information of interest in data array
                i = 0
                while(i < 75):
                    #storing x and y coordinates and visibilities of each body part, avoiding the coordinates of middle hip
                    if((i != 45) and (i != 48) and (i != 51) and (i != 54) and (i != 60) and (i != 69)):
                        frame_coords.append([int(coords[i]), int(coords[i+1])])
                        if coords[i] == 0:
                            frame_visib.append(False)
                        else:
                            frame_visib.append(True)
                    i = i+3                
            else:
                #cycle to analize each information of interest in data array
                i = 0
                while(i < 75):
                    #storing x and y coordinates and visibilities of each body part, avoiding the coordinates of middle hip
                    if((i != 45) and (i != 48) and (i != 51) and (i != 54) and (i != 60) and (i != 69)):
                        frame_coords.append([0, 0])
                        frame_visib.append(False)
                    i = i+3                
            pose2d.append(frame_coords)
            visibilities.append(frame_visib)
            time.append(j/fps)                
        #creation of the record in which to store data of walking
        pose_estimation = {}
        pose_estimation['pose2d'] = pose2d
        pose_estimation['visibilities'] = visibilities
        pose_estimation['time'] = time
        pose_estimation['width'] = width
        pose_estimation['height'] = height
        return pose_estimation           
            
        
    #function to extract frames from videos and to create txt files with data of interest from each video
    def extractor(self):
        #list of videos to analize
        videos_list = os.listdir(self.videos_dir)
        #sorting list of videos
        videos_list.sort()
        #array in which to store videos name
        video_name_list = []
        #for each video
        for i in range (0, len(videos_list)):
            #video name
            video_name = videos_list[i].split(".")[0]
            #adding video name to list
            video_name_list.append(video_name)
            #video path
            video_path = self.videos_dir + '/' + videos_list[i]
            #creation of frames folder, if it doesn't already exist
            frames_dir = '../frames/' + video_name
            if not os.path.exists(frames_dir):
                os.mkdir(frames_dir)
                print("Directory " , frames_dir ,  " Created ")
            frames_dir += '/'
            #creation of jsons folder, if it doesn't already exist
            json_dir = '../json_files/' + video_name
            if not os.path.exists(json_dir):
                os.mkdir(json_dir)
                print("Directory " , json_dir ,  " Created ")
            json_dir += '/'        
            #function to extract frames from the selected video and to store json files with walking data
#            self.extraction(video_path, frames_dir, json_dir)
            #initialization of cv2 to extract informations from the selected video (width, height, fps, number of frames)
            cap = cv2.VideoCapture(video_path)
            #width (in pixel) of selected video
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            #height (in pixel) of selected video
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))        
            #frame per second
            fps = cap.get(cv2.CAP_PROP_FPS)
            #termination of cv2
            cap.release()
            cv2.destroyAllWindows()
            #function to read walking data from json files
            pose_estimation = self.getDataByJson(json_dir, width, height, fps)
            #function to create txt files with data of interest extracted from each json file                
            ds = DataStorage(video_name, pose_estimation)
            ds.storage()
        return video_name_list