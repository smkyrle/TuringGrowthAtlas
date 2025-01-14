import numpy as np
import pandas as pd

class LHS: # Defines parameter sampling

    def __init__(self, nsamples = 1, params = None):
        self.nsamples = nsamples
        self.params = {
            'production_x'  :  [0.1],#[0.1, 100],    # Production rate.
            'production_y'  :  [0.1],#[0.1, 100],
            'degradation_x' :  [0.01],#[0.01,1],      # Degradation rate.
            'degradation_y' :  [0.1],#[0.01,1],
            'max_conc_x'    :  [3.1623],#[0.1, 100],    # Saturation.
            'max_conc_y'    :  [100],#[0.1, 100],
            'k_xx'          :  [100],#[0.1, 100],    # Reaction rates.
            'k_xy'          :  [3.1623],#[0.1, 100],
            'k_yy'          :  [100],#[0.1, 100],
            'k_yx'          :  [3.1623],#[0.1, 100],
            'diffusion_x'   :  [1.],           # Diffusion constants.
            'diffusion_y'   :  [1000],#[0.001, 1000],
            'n_xx'          :  [2],          # Hill coefficients.
            'n_xy'          :  [2],
            'n_yy'          :  [2],
            'n_yx'          :  [2], 
            }

    # Function generates value from log distribution (0.001 to 1000).
    def loguniform(self,low=-3, high=3, size=None):
        return (10) ** (np.random.uniform(low, high, size))

    # Function generates non-overlapping samples from a distribution (latin hypercube sampling).
    # (data = distribution, nsample = number of desired samples)

    def lhs(self,data):
         P = 100*(np.random.permutation(self.nsamples) + 1 - np.random.uniform(size=(self.nsamples)))/self.nsamples
         s = np.percentile(data, P)
         return s

    # Function generates distribution range for each parameter and performs latin hypercube sampling.
    def sample_parameters(self):

        # def loguniform(low=-3, high=3, size=None):
        #     return (10) ** (np.random.uniform(low, high, size))

        param_sample_dict = {}

        for p in self.params:

            if len(self.params[p]) == 2: # If 2 numbers in parameter range we do sampling.

                distribution = []

                # Sample from log distribution until reaching 1000 points within the specified range.
                while len(distribution) < 1000:
                    point = self.loguniform()
                    if self.params[p][0] <= point <= self.params[p][1]:
                        distribution.append(point)

                # Perform lhs using the resulting distribution.
                samples = self.lhs(distribution)

                param_sample_dict[p] = samples.tolist()

            elif len(self.params[p]) == 1: # If one number in parameter range it is constant.

                param_sample_dict[p] = [self.params[p][0] for i in range(self.nsamples)]

        # Convert dictionary of lists into dictionary of dictionaries
        samples = {count: dict(zip(param_sample_dict, i)) for count, i in enumerate(zip(*param_sample_dict.values()))}

        return samples
