import torch.nn as nn
import torch
def crossentropy(pred=None,gt=None):
    r"""A loss function to handle the classification problems in image domain.

    Args:
        pred: The output of the model. A tensor with shape :attr:`(B,C)`
            where B is the batch size used in training process and C is the number of classes
        gt: Gound truth. A tensor with shape :attr:`(B,)`
            where each value is the class index ranging from :attr:`0 to C-1` or
            with shape :attr:`(B,C)` in one-hot encoding type

    Returns:
        a scalar tensor value to make backward

    Note:
        The standard input shape of the gt in nn.CrossEntropyLoss is (B,) and the data type is long

    Examples:
        >>> loss = nn.CrossEntropyLoss()
        >>> input = torch.randn(3, 5, requires_grad=True)
        >>> target = torch.empty(3, dtype=torch.long).random_(5)
        >>> output = loss(input, target)
        >>> output.backward()
    """
    func = nn.CrossEntropyLoss()
    if gt.dtype != torch.long:
        gt = gt.long()
    gt_shape = gt.shape
    if len(gt_shape) == 2:
        if gt_shape[1] == 1:
            gt = gt.squeeze()
        else:
            gt = gt.argmax(dim=1)
    return func(pred,gt)
