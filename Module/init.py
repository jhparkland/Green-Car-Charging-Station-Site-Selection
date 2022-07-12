import os

from isort import file

def getdir(filename):
    '''
    요청한 데이터 경로 반환
    :param filename: 접근할 데이터 이름 
    :return: 데이터 경로
    '''
    cwd = os.chdir(
        '..')
    cwd = os.getcwd()  # 현재 경로
    file_list = []
    idx = 0
    print("##############################################################################################")
    print("현재", cwd)

    if not (os.path.isdir(cwd + '\Data')):
        raise IOError("해당 경로가 바른지 확인해 주세요")
    else:
        os.chdir(cwd + '\Data')  # 디렉터리 이동
        cwd = os.getcwd()  # 현재 위치 갱신
        
        file_list = os.listdir()  # 하위 목록 리스트

    idx = file_list.index(filename)

    if not (os.path.isfile(f'{cwd}\{file_list[idx]}')):
        raise IOError("해당 파일이 존재 하는지 확인해 주세요")
    else:
        print(f"{file_list[idx]}에 접근합니다.")
        reuslt = f'{cwd}\{file_list[idx]}'
        #cwd = os.chdir('../')

    return reuslt

