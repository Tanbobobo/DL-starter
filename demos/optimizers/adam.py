from torch.optim import Adam

def adam_optim(lr=None,params=None,weight_decay=None):
    r'''

    an optimization method to assist the network to converge to the global minimum

    Args:
        lr: learning rate
        params: the parameters of the model
        weight_decay: weight decay (L2 penalty)

    Returns: an object of the class: Adam

    '''
    return Adam(params=params,lr=lr,weight_decay=weight_decay)