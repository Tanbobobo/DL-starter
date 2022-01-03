from pipelines.loading import *
from criterions import crossentropy
from metrics import kappa
from runner import learn, val, infer
from optimizers import adam_optim

from albumentations import *
from models import resnet
from datetime import datetime

import wandb
def run():
    r'''

    This is a deep learning glaucoma classification demo for new hand.
    In this demo, based on the glaucoma datasets of :attr:`MICCAI 2021 GAMMA challenge`,
    the deep learning process is divided into :attr:`7` modules to enable the classification and grading of glaucoma
    for the convolutional neural network.

    * :attr:`preprocess`

        contains the customized method to organize the dataset in your type
        such as KFold

    * :attr:`pipelines`

        contains the data loading process based on pytorch, in this process
        you can load the image with corresponding label and make some transforms to enrich your
        image types

    * :attr:`optimizers`

        contains the optimization method for better model parameters

    * :attr:`criterions`

        contains the loss function that produce the gratitudes for deep learning back-propagation

    * :attr:`metrics`

        contains the evaluating indicator to quantify the robustness of the neural network

    * :attr:`models`

        contains the topological structure and forward logic of the networks

    * :attr:`runer`

        contains 3 deep learning process including `train`,`validate` and `inferrence`




    Returns: Happiness :)

    '''
    wandb.init(project='demo')
    config = wandb.config
    time_info = str(datetime.now()).replace(' ', '_').replace(':', '_').split('.')[0]
    SAVE_DIR = "./work_dirs/" + f"{time_info}/"
    os.makedirs(SAVE_DIR, exist_ok=True)
    weight_name = 'epoch_{}.pth'
    log_name = 'log.txt'
    config.epochs = 10
    device = 'cpu'  # 'cuda:0'
    fold_num = 1
    config.data_seed = 2021
    config.data_root = './data/fundus_data/'
    img_folder = 'imgs'
    anns_folder = f'split_seed_{data_seed}/fold_{fold_num}'
    anns_name_train = 'train_gt.csv'
    anns_name_val = 'eval_gt.csv'
    config.anns_dict = {'non': 0, 'early': 1, 'mid_advanced': 2}
    config.depth = 18
    pretrained = False
    config.cls_num = len(anns_dict)
    config.mean = (0.485, 0.456, 0.406)  # RGB
    config.std = (0.229, 0.224, 0.225)
    config.img_h = 512
    config.img_w = 512
    config.lr = 1e-4
    config.batch_size = 4
    shuffle = True
    pin_memory = True
    num_workers = 0
    weight_decay = 1e-5
    model = resnet(
        depth=config.depth,
        cls_num=config.cls_num,
        pretrained=pretrained
    )
    config.model = model.__class__.__name__
    optim = adam_optim(lr=config.lr, params=model.parameters(), weight_decay=weight_decay)
    config.optimizer = optim.__class__.__name__
    crit = crossentropy
    config.loss = crit.__class__.__name__
    metric = kappa()
    config.metric = metric.__class__.__name__
    transforms = Compose(
        [
            Resize(config.img_h, config.img_w)
        ]
    )
    dataset_train = GAMMADataset(
        anns_file=os.path.join(
            data_root,
            anns_folder,
            anns_name_train
        ),
        img_path=os.path.join(
            data_root,
            img_folder
        ),
        transforms=transforms,
        anns_dict=config.anns_dict,
        mean=config.mean,
        std=config.std
    )
    data_loader_train = GAMMALodaer(
        dataset=dataset_train,
        batch_size=config.batch_size,
        shuffle=shuffle,
        pin_memory=pin_memory,
        num_workers=num_workers
    )
    dataset_val = GAMMADataset(
        anns_file=os.path.join(
            data_root,
            anns_folder,
            anns_name_val
        ),
        img_path=os.path.join(
            data_root,
            img_folder
        ),
        transforms=transforms,
        anns_dict=config.anns_dict,
        mean=config.mean,
        std=config.std
    )
    data_loader_val = GAMMALodaer(
        dataset=dataset_val,
        batch_size=config.batch_size,
        shuffle=shuffle,
        pin_memory=pin_memory,
        num_workers=num_workers
    )
    best_metric_value = 0
    log_format = "epoch: {}, train loss: {}, val loss: {}, train score: {}, val score: {}\n"

    for epoch in range(1, config.epochs + 1):

        model, \
        metric_value_train, \
        loss_value_train = learn(optimizer=optim, criterion=crit, metric=metric,
                                 loader=data_loader_train,
                                 model=model, device=device,

                                 )
        model, \
        metric_value_val, \
        loss_value_val = val(criterion=crit, metric=metric,
                             loader=data_loader_val, model=model,
                             device=device)

        wandb.log({'train_loss_epoch':loss_value_train,
                   'train_score_epoch':metric_value_train,
                   'val_loss_epoch':loss_value_train,
                   'val_score_epoch':metric_value_val})
        if 1:  # metric_value_val > best_metric_value:
            best_metric_value = metric_value_val
            torch.save(
                {
                    'state_dict': model.state_dict(),
                    'epoch': epoch,
                    'score': best_metric_value
                },
                SAVE_DIR + weight_name.format(epoch)

            )
        with open(os.path.join(SAVE_DIR, log_name), 'a') as f:
            f.writelines(log_format.format(
                epoch, loss_value_train, loss_value_val,
                metric_value_train, metric_value_val
            ))


if __name__ == '__main__':
    run()
