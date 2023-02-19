from typing import Mapping, Any
import datetime
import numpy
import seawater
import eatpy.shared

class NitDens(eatpy.shared.Plugin):
    def initialize(self, variables: Mapping[str, Any], ensemble_size: int):
        self.logger.info('The model state consists of the following variables: {}'.format(', '.join(variables)))
        self.salt = variables['salt']
        self.temp = variables['temp']
        self.nit = variables['N3_n']
        self.pho = variables['N1_p']
        self.z = variables['z']

    def before_analysis(self, time: datetime.datetime, state: numpy.ndarray, iobs: numpy.ndarray, obs: numpy.ndarray, obs_sds: numpy.ndarray, filter: eatpy.shared.Filter):
        self.logger.info('{} before analysis:'.format(time))
        self.rho_before = seawater.dens(self.salt["data"],self.temp["data"],self.z["data"]).mean(axis=0)
        #self.nit_before = self.nit["data"].mean(axis=0)
        #self.pho_before = self.pho["data"].mean(axis=0)
        #self.z_before_mean = self.z["data"].mean(axis=0)
        self.nit_before = self.nit["data"].copy()
        self.pho_before = self.pho["data"].copy()
        self.z_before = self.z["data"].copy()

    def after_analysis(self, state: numpy.ndarray):
        self.logger.info('after analysis:')
        rho_after = seawater.dens(self.salt["data"],self.temp["data"],self.z["data"]).mean(axis=0)
        deltarho = rho_after - self.rho_before
        zmean = self.z_before.mean(axis=0)
        coeff = numpy.zeros_like(zmean,dtype=float)
        zlim = [0,-200,-250,-400,-800]
        coefval = [.1,4,8,7,.3]
        #for iiz,zz in enumerate(zlim[1:-1]):
        for iiz,zz in enumerate(zlim[:-1]):
            maskz = ((zmean<=zlim[iiz]) & (zmean>zlim[iiz+1]))
            nz = numpy.sum(maskz)
            coeff[maskz] = numpy.linspace(coefval[iiz],coefval[iiz+1],nz)
        #coeff[zmean>zlim[1]] = coefval[0]
        coeff[zmean<zlim[-1]] = coefval[-1]
        deltanit = deltarho * coeff
        self.nit["data"][:] = self.nit_before + deltanit
        rationit = self.nit["data"][:]/self.nit_before
        self.pho["data"][:] = self.pho_before * rationit
        #self.nit["data"][:] = self.nit_before
        self.z["data"][:] = self.z_before





