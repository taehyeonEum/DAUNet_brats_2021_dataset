from torch.utils.data import Dataset
import numpy as np
import os
from . import config as cf

class DukeDataset(Dataset): 

    def __init__(self, mode=None, transform=None):
        self.transform =transform
        self.mode = mode
     
        if self.mode =='train':
            self.image_path = os.path.join(cf.TRAIN_IMAGE_PATH)  
            self.label_path = os.path.join(cf.TRAIN_MASK_PATH)
     
        elif self.mode == 'test':
            self.image_path = os.path.join(cf.VALID_IMAGE_PATH)
            self.label_path = os.path.join(cf.VALID_MASK_PATH)

        lst_data_image = os.listdir(self.image_path) #list of train image paths
        lst_data_label = os.listdir(self.label_path) #list of Mask paths
        
        # making only tumor dataset!

        tumor_imgs = []
        tumor_msks = []
        for idx in range(len(lst_data_image)):
            temp = lst_data_image[idx]
            flag = temp.split('_')[-1]
            if flag == 'T.npy':
                tumor_imgs.append(lst_data_image[idx])
                tumor_msks.append(lst_data_label[idx])

        # print(tumor_img)
 
        self.lst_input = tumor_imgs 
        self.lst_label = tumor_msks

    def __len__(self): #Dataset 상속
        return len(self.lst_label)

    def __getitem__(self,index):

        image = np.load(os.path.join(self.image_path,self.lst_input[index])).astype('float32')
        label = (np.load(os.path.join(self.label_path,self.lst_label[index])) > 0).astype('uint8')

        image = image.transpose(1, 2, 0) # image.shape = channels, height, width


        ## 둘 다 16bit 이지만 mr영상은 max 값 편차가 크고 대부분 65535보다 훨씬 작은 값
        # if not image.sum() == 0:
        #     image = image/image.max() #0~1 사이 값으로 변환해줌!
        # label = (label > 0).astype(float)   #마찬가지로 0~1사이 값으로 변환해줌!
        
        if image.ndim == 2:
            image = image[:,:,np.newaxis] #(x, y) --> (x, y, 1)
        if label.ndim == 2:
            label = label[:,:,np.newaxis] 

        # data = {'input':image, 'label': label}
        
        if self.transform is not None:
            data = self.transform(image = image, mask = label)
            
            # image의 값을 0-1 사이로 
            # data_img = (data["image"]*0.4)+(1-0.4) # 아직 어두운 것 같아서 0.5 / 0.5 에서 바꿈!
            '''
            THUM 지성씨 코드에서 수정한 부분: 뿌옇게 나오는 것이 안좋을 것이라 판단!
            다시 해보니 저렇게 처리해주지 않으면 너무 검게 나와서 데이터가 거의 확인이 되지 않음..!
            normalization하는 과정(zscore을 구하는 과정)에서 다시 검게 변하는 것 같음..!
            '''
            data_lab = data["mask"]
            data_lab = data_lab.permute(2,0,1) #출력해보고... 수정.

        return data['image'], data_lab