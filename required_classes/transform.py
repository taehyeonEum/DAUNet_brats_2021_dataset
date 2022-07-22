import albumentations.augmentations as AA
import albumentations as A
import albumentations.pytorch as Ap
from albumentations.core.composition import Compose, OneOf

meanFour = (0.5, 0.5, 0.5, 0.5)

def transform_js(mode,resol):
    if mode == 'train':
        train_transform = Compose([
            # AA.Resize(height = resol, width = resol),
            # AA.Normalize(meanFour, meanFour, max_pixel_value=1.0), #normalize 방식을 바꿔볼 수도 있겠음!
            
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.5),
            A.RandomRotate90(p=0.5),
            A.ShiftScaleRotate(shift_limit=0.01, scale_limit=0.04, rotate_limit=0, p=0.25),           
            A.OneOf([
                A.RandomBrightnessContrast(brightness_limit=.2, contrast_limit=.2, p=0.4),
                # A.CLAHE(p=0.25),
                A.Blur(blur_limit=7, p=0.4) ], p=0.5), 
            Ap.transforms.ToTensorV2()
             ])        
        return train_transform
    
    elif mode == 'test':
        test_transform = Compose([
            # AA.Resize(height = resol, width = resol),
            # AA.Normalize(meanFour, meanFour, max_pixel_value=1.0),

            Ap.transforms.ToTensorV2()
             ])
        return test_transform