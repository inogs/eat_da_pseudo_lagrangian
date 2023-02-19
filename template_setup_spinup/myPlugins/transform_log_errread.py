from typing import Mapping, Any, List
import eatpy.shared
import datetime
import numpy as np
import logging



class LogErr(eatpy.shared.Plugin):
    def __init__(self, *variable_names):
        self.logger = logging.getLogger('transform log')
        self.variable_names = frozenset(variable_names)
        self.variable_metadata: List[Any] = []

    def initialize(self, variables: Mapping[str, Any], ensemble_size: int):
        for name in self.variable_names:
            self.variable_metadata.append(variables[name])

    def before_analysis(
        self,
        time: datetime.datetime,
        state: np.ndarray,
        iobs: np.ndarray,
        obs: np.ndarray,
        obs_sds: np.ndarray,
        filter: eatpy.shared.Filter
    ):
        small = 1.e-6
        verysmall = 1.e-20
        for metadata in self.variable_metadata:
            affected_obs = (iobs >= metadata["start"]) & (iobs < metadata["stop"])
            if affected_obs.any():
                nobs = affected_obs.sum()
                #self.logger.info(np.sum(obs[affected_obs] <= small))
                ppobs = obs[affected_obs]
                ppobs[ppobs <= small] = small
                obs[affected_obs] = ppobs
                #varM = (np.log(1.2))**2
                #varA = (np.log(1+.02/obs[affected_obs]))**2
                #obs_sds[affected_obs] = np.sqrt((varM + varA)*nobs)
                ppsds = obs_sds[affected_obs]
                pvarM = ((ppsds-1.e+12).astype(int)/1.e+6).astype(int)/1.e+3
                dvarA = (ppsds-1.e+12-pvarM*1.e+9)/1.e+3
                # pvarM = 1.2
                # dvarA = .02
                varM = (np.log(pvarM))**2
                varA = (np.log(1+dvarA/obs[affected_obs]))**2
                self.logger = logging.getLogger('transform ERR read')
                self.logger.info(dvarA)
                self.logger.info(pvarM)
                obs_sds[affected_obs] = np.sqrt((varM + varA)*nobs)
                obs[affected_obs] = np.log(obs[affected_obs])
            masksmall = metadata["data"] < small
            maskverysmall = metadata["data"] < verysmall
            if np.any(metadata["data"]==0):
                self.logger = logging.getLogger('ZERO')
                self.logger.info(metadata['long_name'])
                vsmetadata = metadata["data"]
                vsmetadata[maskverysmall] = verysmall
                metadata["data"][...] = vsmetadata
            if np.any(np.isfinite(np.log(metadata["data"]))==False):
                masknonfin = np.isfinite(np.log(metadata["data"]))==False
                self.logger = logging.getLogger('non fin')
                self.logger.info(metadata['long_name'])
                self.logger.info(metadata["data"][masknonfin])
            ppmetadata = np.log(metadata["data"])
            mean_notlimited = np.mean(ppmetadata,axis=0)
            #self.logger.info(mean_notlimited)
            ppmetadata[masksmall] = np.log(small)
            mean_limited = np.mean(ppmetadata,axis=0)
            #self.logger.info(mean_limited)
            metadata["data"][...] = ppmetadata + ( mean_notlimited - mean_limited )
            #metadata["data"][...] = np.log(metadata["data"])

    def after_analysis(self, state: np.ndarray):
        for metadata in self.variable_metadata:
            metadata["data"][...] = np.exp(metadata["data"])
