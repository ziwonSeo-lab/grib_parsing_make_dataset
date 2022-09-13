### 샘플파일 기준으로 테스트 진행


import os 

# import pandas as pd
import pygrib
import numpy as np
import os, sys
from datetime import datetime, timedelta


#파일 탐색
def find_files(root_dir:str):
    '''
        파일을 탐색하여 파일명 리스트 생성
        root_dir :: [str] root directory path
    '''
    filelist = []
    file_path_list = []
    folders =[]
    subdirs = []
    for folder, subdir, files in os.walk(root_dir):
        
        if files:
            for file in files:
                path = folder +'/'+ file
                file_path_list.append(path)
                filelist.append(file)
        folders.append(folder)
    return filelist, file_path_list, folders



def make_data(path, features, feature_list):
    filelist, file_path_list, folders = find_files(path)
    for folder in folders :
        try :
            for day in range(1,32):
                filelist, file_path_list, folders = find_files(folder+"/"+ f'{day}') # -> 일별 파일 시간.
                file_path_list.sort()
                for i, feature_name in enumerate(features):
                    for j, file in enumerate(file_path_list):
                        ## data parsing
                        filepaths = file.split('/')
                        file_name = filepaths[-1]
                        time_temp = file_name.split('_')
                        time = time_temp[4].split('.')
                        ym = time[1][:6]
                        ymd = time[1][:8]
                        predict_time = time[1][-2:]
                    
                        grbs = pygrib.open(file)
                        temp = grbs.select(name=feature_name)[0]
                        feature = temp.value()

                        if j == 0:
                            total_npy = feature.reshape(839, 1049, 1)
                        else:
                            total_npy = np.append(total_npy,feature.reshape(839, 1049, 1),axis=-1)
                    
                    # 저장경로 설정 필요
                    ## feature_list = ['temperature', 'humidity', 'Uwind', 'Vwind', 'pressure']
                    ## predict_time = 예측시간
                    ## 디렉토리 경로가 없으면 생성하고, npy 형태로 데이터 저장.
                    dir_path = f'/home/szw001/development/2022/data_ana/sample_parsing/{feature_list[i]}/{predict_time}/{ym}'
                    os.makedirs(dir_path, exist_ok=True)
                    np.save(f"{dir_path}/{ymd}.npy",total_npy)
                    print(f'{dir_path}/{ymd}.npy')
                        
        except Exception as e:
            print(e)



if __name__ == "__main__": 

    # 파일 탐색 경로 설정 필요.
    path = '/home/szw001/development/2022/data_ana/sample_data'
    features = ['2 metre temperature', '2 metre relative humidity', '10 metre U wind component', '10 metre V wind component', 'Mean sea level pressure']
    # 저장할 파일에 들어갈 요소 이름.
    feature_list=['temperature', 'humidity', 'Uwind', 'Vwind', 'pressure']
    make_data(path, features, feature_list)

    