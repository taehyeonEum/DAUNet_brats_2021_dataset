import torch
import torch.nn as nn

def customLoss(pred, mask, pos_weight, device, smooth):
    pw = torch.Tensor([pos_weight]).to(device)
    bce_lossFunc = nn.BCEWithLogitsLoss(pos_weight=pw)
    bce_loss = bce_lossFunc(pred, mask)

    pred = torch.sigmoid(pred)

    mask_inverse = (mask -1)*(-1)
    new_loss = pred*mask_inverse
    
    pred_thres = (pred > 0.5).type(torch.uint8)


    intersection = (pred * mask).sum(dim=(2, 3))

    pred_fn = (intersection*pred_thres).sum(dim=(2, 3))
    fn_loss = ((pred_fn + smooth)/ (intersection + smooth)).sum(dim=(2, 3))

    union = pred.sum(dim=(2,3)) + mask.sum(dim=(2, 3))
    dice_loss = 1 - ( ((2*intersection + smooth) / (union + smooth)) )

    return (new_loss.mean(), fn_loss.mean(), bce_loss.mean(), dice_loss.mean())
