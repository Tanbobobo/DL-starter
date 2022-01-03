#### Key process
This section lists some vital code snippets corresponding to the data process
and model forward.
* preprocess.py
```angular2html
    # 设定折数
    kf = KFold(n_splits=5, random_state=seed, shuffle=True) 
    # 按类别取出对应索引
    img_non = gt[gt['non'].isin([1])] 
    img_early = gt[gt['early'].isin([1])]
    img_mid_advanced = gt[gt['mid_advanced'].isin([1])]

    #迭代过程，迭代次数为折数大小
    #得到不同折的训练集和验证集
    for (n_train, n_test), (e_train, e_test), (ma_train, ma_test) in zip(kf.split(img_non),
                                                                         kf.split(img_early),
                                                                         kf.split(img_mid_advanced)
                                                                         ):
        
        n_train, n_test = img_non.iloc[n_train, :].reset_index(drop=True), \
                          img_non.iloc[n_test, :].reset_index(drop=True)
        ...
```
* pipelines.loading.GAMMADataset.get_data
```angular2html
    # 读取数据
    # 变换数据
    label_idx = self.load_label(index=item)
    img_np, img_path = self.load_img(item=item)
    img_trans = self.transform_img(img=img_np)
    label_t = self.transform_label(label_idx=label_idx)
    img_t = self.img2tensor(img=img_trans / 255)
    return img_t, label_t, img_path
```
* runner.train.learn
```angular2html
    # 每次计算新的梯度时,要把原来的梯度清0
    optimizer.zero_grad()
    # 前向传播
    pred = model(img)
    # 损失函数计算
    loss_value = criterion(pred, gt)
    # 计算梯度
    loss_value.backward()
    # 更新参数
    optimizer.step()
```
* main
```angular2html
    # 训练过程记录
    wandb.log({'train_loss_epoch':loss_value_train,
                   'train_score_epoch':metric_value_train,
                   'val_loss_epoch':loss_value_train,
                   'val_score_epoch':metric_value_val})
    # 模型存储
    torch.save(
        {
            'state_dict': model.state_dict(),
            'epoch': epoch,
            'score': best_metric_value
        },
        SAVE_DIR + weight_name.format(epoch)

    )
```
