import timm

def resnet(depth=None,cls_num=None,pretrained=None):

    r'''

    This function utilize the timm package to construct the model

    Args:
        depth: the levels of the res block, such as 50,101
        cls_num: the number of the categories
        pretrained: a bool value to decide wether load the weight of the imagenet

    Returns: a ready-made model

    '''
    model = timm.create_model(model_name=f'resnet{depth}',pretrained=pretrained)
    model.reset_classifier(cls_num)
    return model