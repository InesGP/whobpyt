import torch


class CostsMean():
    '''
    Target Mean Value of a Variable
    
    This loss function calculates the mean value of a particular variable for every node across time, and then takes the Mean Squared Error of those means with the target value. 
    
    Attributes
    -----------------
    num_regions : Int
        The number of reagons in the model beign fit
    simKey : String 
        The name of the variable for which the mean is calculated
    targetValue : Tensor
        The target value either as single number or vector
    '''
        
    def __init__(self, num_regions, simKey, targetValue = None, empiricalData = None):
        '''
        Parameters
        -----------------
        num_regions : Int
            The number of regions in the model being fit
        simKey : String 
            The name of the variable for which the mean is calculated
        targetValue : Tensor
            The target value either as single number or vector
        '''
        
        self.num_regions = num_regions
        self.simKey = simKey # This is the key from the numerical simulation used to select the time series
        
        # Target can be specific to each region, or can have a single number that is repeated for each region
        if torch.numel(targetValue) == 1:
            self.targetValue = targetValue.repeat(num_regions)
        else:
            self.targetValue = targetValue
            
        if empiricalData != None:
            # In the future, if given empiricalData then will calculate the target value in this initialization function. 
            # That will possibly involve a time series of targets, for which then the calcLoss would need a parameter to identify
            # which one to fit to.
            pass
        
    def calcLoss(self, simData):
        '''
        Method to calculate the loss
        
        Parmeters
        --------------
        simData: Tensor[ Nodes x Time ]
            The time series used by the loss function 
            
        Returns
        --------------
        Tensor
            The loss value 
        
        '''
        meanVar = torch.mean(simData[:,:], 1)
        
        return torch.nn.functional.mse_loss(meanVar, self.targetValue)
        