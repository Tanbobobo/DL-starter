import torch


def val(
        criterion=None,
        metric=None,
        loader=None,
        model=None,
        device=None
):
    r'''

    Args:
        criterion: a differentiable function to provide gratitude for backward
        metric: a score to save best model
        loader: a data iterator
        model: model
        device: calculation device, cpu or cuda.

    Returns:
        a metric socre on behalf of the accuracy on unseen dataset of the prediction of the model

    '''
    model.eval()
    model.to(device)
    loss_value_mean = 0
    with torch.no_grad():
        for idx, data in enumerate(loader):
            img = data['img'].to(device)
            gt = data['gt'].to(device)

            pred = model(img)
            loss_value = criterion(pred, gt)
            loss_value_mean += loss_value
            metric.accumulate(pred, gt)

        metric_value = metric.value
        loss_value_mean = loss_value_mean / len(loader)
        return model, metric_value, loss_value_mean
