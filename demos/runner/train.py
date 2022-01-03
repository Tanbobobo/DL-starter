import wandb
def learn(
        optimizer=None,
        criterion=None,
        metric=None,
        loader=None,
        model=None,
        device=None
):
    r'''

    Args:
        optimizer: a function to optimize the learning process
        criterion: a differentiable function to provide gratitude for backward
        metric: a score to save best model
        loader: a data iterator
        model: model
        device: calculation device, cpu or cuda.
    Notes:
        * :attr:`transforms`

            it must be the same with validation stage

        * :attr:`device`

            this item format is 'cpu' means do calculation on cpu device; 'cuda:0' means
            do calculation on cuda device, 0 refers to the first gpu.
    Returns:

    '''
    model.train()
    model.to(device)
    loss_value_mean = 0
    for idx, data in enumerate(loader):
        
        img = data['img'].to(device)
        gt = data['gt'].to(device)
        optimizer.zero_grad()
        pred = model(img)
        loss_value = criterion(pred, gt)
        loss_value_mean += loss_value
        metric.accumulate(pred, gt)
        loss_value.backward()
        optimizer.step()
        wandb.log({'train_loss':loss_value})
        
        
    metric_value = metric.value
    loss_value_mean = loss_value_mean / len(loader)
    return model, metric_value, loss_value_mean
