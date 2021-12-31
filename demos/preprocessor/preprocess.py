import os
import pandas as pd
from sklearn.model_selection import KFold


def prepare_img_data(seed=2021, gt=None):
    r'''

    This function split the datasets into k folds which means k pairs of training sets and validation sets
    

    Args:
        seed: this parameter is magic for your model preference when generate different sets and `seed` affects the ordering of the
        indices, which controls the randomness of each fold.
        gt: this parameter contains whole indexs of the ground truth

    Returns: K folds indexs or the customized outputs

    '''
    data_train = []
    data_eval = []
    kf = KFold(n_splits=5, random_state=seed, shuffle=True)
    img_non = gt[gt['non'].isin([1])]
    img_early = gt[gt['early'].isin([1])]
    img_mid_advanced = gt[gt['mid_advanced'].isin([1])]

    for (n_train, n_test), (e_train, e_test), (ma_train, ma_test) in zip(kf.split(img_non),
                                                                         kf.split(img_early),
                                                                         kf.split(img_mid_advanced)
                                                                         ):
        import pdb
        # pdb.set_trace()
        n_train, n_test = img_non.iloc[n_train, :].reset_index(drop=True), \
                          img_non.iloc[n_test, :].reset_index(drop=True)
        e_train, e_test = img_early.iloc[e_train, :].reset_index(drop=True), \
                          img_early.iloc[e_test, :].reset_index(drop=True)
        ma_train, ma_test = img_mid_advanced.iloc[ma_train, :].reset_index(drop=True), \
                            img_mid_advanced.iloc[ma_test, :].reset_index(drop=True)

        _train = pd.concat([n_train, e_train, ma_train], axis=0, ignore_index=True)
        _test = pd.concat([n_test, e_test, ma_test], axis=0, ignore_index=True)
        data_train.append(_train)
        data_eval.append(_test)

    return data_train, data_eval


if __name__ == '__main__':

    data_seed = 2021
    data_root = '../data/fundus_data/'
    img_folder = 'imgs'
    anns_folder = 'anns'
    anns_name = 'glaucoma_grading_training_GT.xlsx'

    anns_ori = pd.read_excel(
        os.path.join(
            data_root,
            anns_folder,
            anns_name
        )
    )

    save_dir = f'{data_root}' + 'split_seed_{}/'.format(data_seed)
    data_para = dict(seed=data_seed, gt=anns_ori)
    train_folds, eval_folds = prepare_img_data(**data_para)

    for fold, _folds in enumerate(zip(train_folds, eval_folds)):
        fold += 1
        train_fold, eval_fold = _folds
        save_gt_dir = save_dir + 'fold_{}/'.format(fold)
        os.makedirs(save_gt_dir, exist_ok=True)
        print(fold, len(train_fold), len(eval_fold))

        train_fold.to_csv(save_gt_dir + 'train_gt.csv', index=False)

        eval_fold.to_csv(save_gt_dir + 'eval_gt.csv', index=False)

        print(fold, len(train_fold), len(eval_fold))
