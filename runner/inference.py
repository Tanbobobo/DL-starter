import numpy as np
import torch
from PIL import Image


def img2tensor(img=None, mean=None, std=None):
    r'''
    This func normalize images and covert the numpy format to the torch tensor format
    | B,H,W,C -> B,C,H,W for the calculation in cuda device
    | :param img: A numpy array with the shape (H,W,C) where H is the image height,
    | W is the image width and C is the image channel
    | :return: a tensor value
    '''
    assert img.max() <= 1

    if img.ndim == 3:
        img = (img - mean) / std

    elif img.ndim == 2:
        img = img[..., None]
    img = np.transpose(img, (2, 0, 1))
    return torch.from_numpy(img.astype(np.float32, copy=False))


def infer(
        model=None,
        device=None,
        transforms=None,
        img_paths=None,
        mean=None,
        std=None,
):
    r'''

    an inference stage using the model owing best validation metric

    Args:
        model: convergent model
        device: calculation device, cpu or cuda.
        transforms: augment and transform the images to the unified size
        img_paths: a list of test image paths
        mean: image channels mean value
        std: image channels standard deviation value
    Notes:
        * :attr:`transforms`

            it must be the same with validation stage

        * :attr:`device`

            this item format is 'cpu' means do calculation on cpu device; 'cuda:0' means
            do calculation on cuda device, 0 refers to the first gpu.
    Returns:
        the inference results
    '''
    model.eval()
    model.to(device)
    with torch.no_grad():
        for img_path in img_paths:
            img = np.array(Image.open(img_path))
            img = transforms(image=img)['image']
            img_t = img2tensor(img=img, mean=mean, std=std)
            img_t = img_t.to(device)
            pred = model(img_t)
            pred_idx = pred.argmax(1)
            print(pred_idx)
