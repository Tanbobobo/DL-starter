import os

import numpy as np
import pandas as pd

from torch.utils.data import Dataset as torch_Dataset
from torch.utils.data import DataLoader as torch_DataLoader
import torch
from PIL import Image


class GAMMADataset(torch_Dataset):
    r'''

            Combines the image files and annotations for train/val/test in a unified torch form

            Args:
                anns_file: a absolute path for the annotation file
                img_path: a path for loading image
                transforms: augment and transform the images to the unified size
                anns_dict: a dict map the category names to the digit number, start at 0
                mean: the image mean value of the whole dataset
                std: the standard deviation value of the whole dataset

    '''
    def __init__(self,
                 anns_file=None,
                 img_path=None,
                 transforms=None,
                 anns_dict=None,
                 mean=None,
                 std=None
                 ):

        self.mean = mean
        self.std = std
        self.anns = pd.read_csv(anns_file)
        self.img_path = img_path

        self.transforms = transforms

        self.anns_dict = anns_dict

    def load_img(self, item=None, mode='RGB'):
        _case = str(self.anns.iloc[item, 0]).split('.')[0].zfill(4)

        path = os.path.join(f'{self.img_path}', '{}.jpg'.format(_case))
        img_pil = Image.open(path).convert(mode)
        img_np = np.array(img_pil)
        return img_np, path

    def transform_img(self, img=None):
        img_trans = self.transforms(image=img)["image"]

        return img_trans

    def load_label(self, index=None):

        return self.anns.iloc[index, 1:].values.astype(np.int64)

    def transform_label(self, label_idx=None):

        return torch.tensor(label_idx).long()

    def get_data(self, item):

        r'''

        Load the image and corresponding classification label

        Args:
            item: A random number range from ``0`` to ``data length - 1``

        Returns: customized output for iteration

        '''
        label_idx = self.load_label(index=item)
        img_np, img_path = self.load_img(item=item)

        img_trans = self.transform_img(img=img_np)
        label_t = self.transform_label(label_idx=label_idx)
        img_t = self.img2tensor(img=img_trans / 255)
        return img_t, label_t, img_path

    def img2tensor(self, img):

        r'''

        This func normalize images and covert the numpy format to the torch tensor format
        B,H,W,C -> B,C,H,W for the calculation in cuda device

        Args:

            img: A numpy array with the shape (H,W,C) where H is the image height,
                W is the image width and C is the image channel

        Returns: a tensor value

        '''
        assert img.max() <= 1

        if img.ndim == 3:
            img = (img - self.mean) / self.std

        elif img.ndim == 2:
            img = img[..., None]
        img = np.transpose(img, (2, 0, 1))
        return torch.from_numpy(img.astype(np.float32, copy=False))

    def __getitem__(self, item):

        r'''

        Iterable process to organize the data

        Args:
            item: A random number range from 0 to data length - 1

        Returns: customized output for iteration

        '''
        img_t, label_t, img_path = self.get_data(item)

        return {'img': img_t, 'gt': label_t}

    def __len__(self, ):
        return len(self.anns)


def GAMMALodaer(dataset=None,
                batch_size=None,
                shuffle=None,
                pin_memory=None,
                num_workers=None,
                ):
    r'''

    Combines a dataset and provides an iterable over the given dataset.

    Args:
        dataset: An object of a class: torch Dataset
        batch_size: The number of image during one forward and one backward process
        shuffle: set to ``True`` to have the data reshuffled at every epoch (default: ``False``).
        pin_memory:  If ``True``, the data loader will copy Tensors
        num_workers: how many subprocesses to use for data
            loading. ``0`` means that the data will be loaded in the main process.
            (default: ``0``)

    Returns: An object of a class: torch DataLoader

    '''
    return torch_DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        pin_memory=pin_memory,
        num_workers=num_workers,
    )
