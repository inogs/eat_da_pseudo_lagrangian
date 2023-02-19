import eatpy.filter
import numpy as np
import logging
from my_plugins.IO import readtxt
from typing import Mapping, Any#, Dict
from collections import OrderedDict

import sys

class P1l(eatpy.filter.CvtHandler):
    
    def __init__(self, eofs_file: str = 'data/init/eof.txt', z_file: str = 'data/init/z.txt', name: str = 'OGS-3Dvar'):
        self.logger = logging.getLogger(name)
        self.eofs_file=eofs_file
        self.z_file=z_file

    def initialize(self, variables: Mapping[str, Any], ensemble_size: int):
        # Here you might add routines that read the square root of the error covariance matrix (Vmat_p) from file
        
        self.logger.info('Initialization')
        self.dim_cvec=26
        
        self.logger.info('Available variables: {}'.format(', '.join(variables)))
        
        self.pvars = [variable for variable in variables.keys() if variable[0]=='P']
        self.chlvars = [variable for variable in self.pvars if variable[-3:]=='Chl']
        self.allvars = self.pvars
        
        self.logger.info('Finding indexes for relevant 3dvar variables: {}'.format(', '.join(self.allvars)))
        self.slices: Mapping[str,Tuple[int, int]] = OrderedDict()
        
        for name in self.allvars:
            info = variables[name]
            self.slices[name]=(info['start'], info['start'] + info['length'])
            
        self.logger.info('Reading z levels from file: {}'.format(self.z_file))
        self.z=np.loadtxt(self.z_file)
        self.nz=self.z.size
        
        self.logger.info('Reading EOFs from file: {}'.format(self.eofs_file))
        self.Vmat_p = readtxt(self.eofs_file, [self.dim_cvec, self.nz])
        self.Vmat_p = self.Vmat_p[:,::-1]
        
        self.logger.info('Initialized')

    def cvt(self, iter: int, state: np.ndarray, v_p: np.ndarray) -> np.ndarray:
        """Forward covariance transformation for parameterized 3D-Var"""
        
        if iter==1:
            self.totchl=np.zeros(self.nz)
            for name in self.chlvars:
                start,stop=self.slices[name]
                self.totchl += state[start:stop]
            
        
        #Vertical operator:
        Mv=np.matmul(v_p, self.Vmat_p)
        
        #Biogeochemical operator:
        Vv_p=np.zeros([state.size])
        for name in self.pvars:
            start,stop=self.slices[name]
            MvOverChl=Mv/self.totchl
            Vv_p[start:stop]=np.where(MvOverChl<-0.99, -0.99, MvOverChl)*state[start:stop]
        
        return Vv_p

    def cvt_adj(self, iter: int, state: np.ndarray, Vv_p: np.ndarray) -> np.ndarray:
        """Adjoint covariance transformation for parameterized 3D-Var"""
        
        if iter==1:
            self.totchl=np.zeros(self.nz)
            for name in self.chlvars:
                start,stop=self.slices[name]
                self.totchl += state[start:stop]
        
        #Biogeochemical operator:
        Mv=np.zeros([self.nz])
        for name in self.pvars:
            start,stop=self.slices[name]
            Mv+=Vv_p[start:stop]*state[start:stop]
        
        Mv/=self.totchl
        
        #Vertical operator:
        v_p=np.matmul(self.Vmat_p, Mv)
        
        return v_p

    
    

