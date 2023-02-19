from typing import Mapping, Any#, Dict
from typing import List
import numpy as np
import eatpy.filter
import logging
from my_plugins.IO import readtxt
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
        # self.slices = {} dict() OrderedDict()
        self.slices: Mapping[str,List[]] = OrderedDict()
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
        MAX_N_CHL = 150.
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
        

        for name in self.nitvars:
            start,stop=self.slices[name]
            Vv_p[start:stop] 
        
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

    def cvt_ens(self, iter: int, state: np.ndarray, v_p: np.ndarray) -> np.ndarray:
        """Forward covariance transformation for ensemble 3D-Var"""
        if iter == 1:
            Vcv_p = state.mean(axis=0)
            self.Vmat_ens_p = np.repeat((state - Vcv_p) / np.sqrt(v_p.size - 1), mcols_cvec_ens, axis=0)
        return self.Vmat_ens_p @ v_p

    def cvt_adj_ens(self, iter: int, state: np.ndarray, Vv_p: np.ndarray) -> np.ndarray:
        """Adjoint covariance transformation for ensemble 3D-Var"""
        return self.Vmat_ens_p.T @ Vv_p 
    
    
class Chl(eatpy.filter.CvtHandler):
    
    def __init__(self, eofs_file: str = 'data/init/eof.txt', z_file: str = 'data/init/z.txt', name: str = 'OGS-3Dvar'):
        self.logger = logging.getLogger(name)
        self.eofs_file=eofs_file
        self.z_file=z_file

    def initialize(self, variables: Mapping[str, Any], ensemble_size: int):
        # Here you might add routines that read the square root of the error covariance matrix (Vmat_p) from file
        
        self.logger.info('Initialization')
        self.dim_cvec=26
        self.npft = 4
        
        self.logger.info('Available variables: {}'.format(', '.join(variables)))
        
        self.variables = variables
        self.pvars = [variable for variable in variables.keys() if variable[0]=='P']
        self.chlvars = [variable for variable in self.pvars if variable[-3:]=='Chl']
        self.allvars = self.pvars

        # self.nitvars = [variable for variable in self.pvars if variable[-2:]=='_n']
        # self.phovars = [variable for variable in self.pvars if variable[-2:]=='_p']
        # self.carvars = [variable for variable in self.pvars if variable[-2:]=='_c']

        self.pftvars = {}
        for ii in range(4):
            strpft = np.str(ii+1)
            self.pftvars[ii] = [variable for variable in self.pvars if variable[1]==strpft]

            
        self.logger.info('Reading z levels from file: {}'.format(self.z_file))
        self.z=np.loadtxt(self.z_file)
        self.nz=self.z.size
        
        self.logger.info('Reading EOFs from file: {}'.format(self.eofs_file))
        self.Vmat_p = readtxt(self.eofs_file, [self.dim_cvec, self.nz])
        self.Vmat_p = self.Vmat_p[:,::-1]
        
        self.logger.info('Initialized')

    def cvt(self, iter: int, state: np.ndarray, v_p: np.ndarray) -> np.ndarray:
        """Forward covariance transformation for parameterized 3D-Var"""
        
        #self.logger.info('cvt state shape: {}'.format(state.shape))
        
        if True: #iter==1:
            self.totchl=np.zeros(self.nz)
            start = self.variables['total_chlorophyll_calculator_result']['start']
            stop = start + self.variables['total_chlorophyll_calculator_result']['length']
            self.totchl = state[start:stop]
            
        #if abs(iter)<10:    
        #    self.logger.info('cvt: state = {}'.format(state[:10]))
        #    self.logger.info('cvt: chl = {}'.format(self.totchl))
            
        
        #Vertical operator:
        Mv=np.matmul(v_p, self.Vmat_p)
        
        #Biogeochemical operator:
        Vv_p=np.zeros([state.size])
        Vv_p[start:stop] = Mv
        for name in self.pvars:
            start = self.variables[name]['start']
            stop = start + self.variables[name]['length']
            
            MvOverChl=Mv/self.totchl
            Vv_p[start:stop]=np.where(MvOverChl<-0.99, -0.99, MvOverChl)*state[start:stop]

        for ii in range(self.npft):


        return Vv_p

    def cvt_adj(self, iter: int, state: np.ndarray, Vv_p: np.ndarray) -> np.ndarray:
        """Adjoint covariance transformation for parameterized 3D-Var"""
        
        #Biogeochemical operator:
        Mv=np.zeros([self.nz])
        for name in self.pvars:
            start = self.variables[name]['start']
            stop = start + self.variables[name]['length']
            
            Mv+=Vv_p[start:stop]*state[start:stop]
            Mv/=self.totchl
            
        if True: #iter==1:
            self.totchl=np.zeros(self.nz)
            start = self.variables['total_chlorophyll_calculator_result']['start']
            stop = start + self.variables['total_chlorophyll_calculator_result']['length']
            self.totchl = state[start:stop]
            
        #if abs(iter)<10:    
        #    self.logger.info('cvt_adj: state = {}'.format(state[:10]))
        #    self.logger.info('cvt_adj: chl = {}'.format(self.totchl))
        
        Mv+=Vv_p[start:stop]
        
        #Vertical operator:
        v_p=np.matmul(self.Vmat_p, Mv)
        
        return v_p

    def cvt_ens(self, iter: int, state: np.ndarray, v_p: np.ndarray) -> np.ndarray:
        """Forward covariance transformation for ensemble 3D-Var"""
        
        #self.logger.info('cvt_ens state shape: {}'.format(state.shape))
        
        #if abs(iter)<10:
        #    self.logger.info('cvt_ens: iter = {}'.format(iter))
        #    self.logger.info('cvt_ens: v_p = {}'.format(v_p))
        #    self.logger.info('cvt_ens: state = {}'.format(state.mean(axis=0)))
        #    self.logger.info('cvt_ens: state = {}'.format(state[:,:10]))
        #    self.logger.info('cvt_ens: state = {}'.format(state[:,-10:]))
        
        if True: #iter == 1: #can be decommented  iter==1
            Vcv_p = state.mean(axis=0)
            #self.Vmat_ens_p = np.repeat((state - Vcv_p) / np.sqrt(v_p.size - 1), mcols_cvec_ens, axis=0)
            self.Vmat_ens_p = (state - Vcv_p) / np.sqrt(v_p.size - 1)
        
        Vv_p=np.matmul(v_p, self.Vmat_ens_p)
        
        #if abs(iter)<10:
        #    self.logger.info('cvt_ens: iter = {}'.format(iter))
        #    self.logger.info('cvt_ens: Vv_p = {}'.format(Vv_p))
        
        return Vv_p

    def cvt_adj_ens(self, iter: int, state: np.ndarray, Vv_p: np.ndarray) -> np.ndarray:
        """Adjoint covariance transformation for ensemble 3D-Var"""
        
        #if abs(iter)<10:
        #    self.logger.info('cvt_adj_ens: iter = {}'.format(iter))
        #    self.logger.info('cvt_adj_ens: Vv_p = {}'.format(Vv_p))
        #    self.logger.info('cvt_adj_ens: state = {}'.format(state.mean(axis=0)))
        #    self.logger.info('cvt_adj_ens: state = {}'.format(state[:,:10]))
        #    self.logger.info('cvt_adj_ens: state = {}'.format(state[:,-10:]))
        
        if True: #iter == 1:
            Vcv_p = state.mean(axis=0)
            self.Vmat_ens_p = (state - Vcv_p) / np.sqrt(state.shape[0] - 1)
        
        v_p=np.matmul(self.Vmat_ens_p, Vv_p)
        
        #if abs(iter)<10:
        #    self.logger.info('cvt_adj_ens: iter = {}'.format(iter))
        #    self.logger.info('cvt_adj_ens: v_p = {}'.format(v_p))
        
        return v_p

