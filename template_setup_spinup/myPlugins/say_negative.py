from typing import Mapping, Any, Union, Iterable
import fnmatch
import numpy as np
import logging
import eatpy.shared

import sys

class SayNegative(eatpy.shared.Plugin):
    def __init__(self, include: Union[Iterable, str]='*', exclude: Union[Iterable, str]=(), name: str = 'Say negative'):
        self.logger = logging.getLogger(name)
        self.include = include if not isinstance(include, str) else (include,)
        self.exclude = exclude if not isinstance(exclude, str) else (exclude,)

    def initialize(self, variables: Mapping[str, Any], ensemble_size: int):
        self.vars=variables
        
        self.positive = set()
        for name in variables:
            
            use = False
            for include_pattern in self.include:
                if fnmatch.fnmatch(name, include_pattern):
                    use = True
            for exclude_pattern in self.exclude:
                if fnmatch.fnmatch(name, exclude_pattern):
                    use = False
            if use:
                self.positive.add(name)
                
    def after_analysis(self, state: np.ndarray):
        SMALL=1.0e-8
        self.logger.info('after analysis:')
        
        NegVars=[]
        for name in self.vars:
            if name in self.positive:
                start=self.vars[name]['start']
                stop=start + self.vars[name]['length']
                var = state[:, start:stop]  # note: the first axis is for the ensemble members
                if var.min() < 0:
                    NegVars.append(name)
                #var[:,:] = np.where(var<SMALL, SMALL, var)
                self.logger.info(name + ': Min ' + np.str(var.min()) + ', Max ' + np.str(var.max())) 
    
        self.logger.info('Corrected negative variables: {}'.format(', '.join(NegVars)))
        
