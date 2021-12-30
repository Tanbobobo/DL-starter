import numpy as np
from sklearn.metrics import cohen_kappa_score


class kappa(object):
    r"""
    Cohen's kappa: a statistic that measures inter-annotator agreement.
    This function computes Cohen's kappa, a score that expresses the level
    of agreement between two annotators on a classification problem.
    """

    def __init__(self, ):
        self.reset()

    def reset(self, ):
        r'''
        initialize the list variable

        Returns: a list variable

        '''
        self.cache = []

    def accumulate(self, pred=None, gt=None):

        r'''
        A accumulate function to save the batch results of prediction and ground turth
        for final kappa score calculation.

        Args:
            pred: The output of the model.
            gt: Gound truth.

        Returns: a list containing a pair of labels with prediction and ground truth

        '''

        pred = pred.cpu().detach().numpy().argmax(1)
        gt_shape = gt.shape
        if len(gt_shape) == 2:
            if gt_shape[1] == 1:
                gt = gt.squeeze()
            else:
                gt = gt.argmax(dim=1)
        gt = gt.cpu().detach().numpy()

        for _pred, _gt in zip(pred, gt):
            self.cache.append([_pred, _gt])

    @property
    def value(self, ):
        r'''
        calculate the kappa score between predictions and ground turth

        Returns: kappa score

        '''
        cache = np.array(self.cache)
        kappa = cohen_kappa_score(cache[:, 0], cache[:, 1], weights='quadratic')
        return kappa
