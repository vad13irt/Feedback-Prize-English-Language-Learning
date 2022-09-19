import torch
from typing import Optional, Tuple, Union


def column_wise_rmse_loss(
    input: torch.Tensor, 
    target: torch.Tensor, 
    return_column_wise: bool = False, 
    reduction: str = "mean", 
    column_weight: Optional[torch.Tensor] = None, 
    sample_weight: Optional[torch.Tenosr] = None,
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
    """
    Mean Column-wise Root Mean Squared Error
    https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/348985
    """
    
    # compute column-wise RMSE
    squared_error = torch.square(target - input)
    
    # sample weightning
    if sample_weight is not None:
        squared_error = (squared_error * sample_weight)
    
    column_wise_mse = torch.mean(squared_error, dim=0)
    column_wise_rmse = torch.sqrt(column_wise_mse)
    
    # column weightning
    if column_weight is not None:
        column_wise_rmse = (column_wise_rmse * column_weight)
    
    # reduction
    if reduction == "mean":
        loss = torch.mean(column_wise_rmse, dim=0)
    elif reduction == "max":
        loss = torch.max(column_wise_rmse, dim=0)
    else:
        loss = column_wise_rmse
        
    if return_column_wise:
        return loss, column_wise_rmse
    
    return loss