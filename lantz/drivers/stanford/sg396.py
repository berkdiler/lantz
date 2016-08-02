# -*- coding: utf-8 -*-
"""
    lantz.drivers.stanford.sg396
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation of SG396 signal generator

    Author: Kevin Miao
    Date: 12/15/2015
"""

import numpy as np
from lantz import Action, Feat, DictFeat, ureg
from lantz.messagebased import MessageBasedDriver

class SG396(MessageBasedDriver):

        DEFAULTS = {
            'COMMON': {
                'write_termination': '\r\n',
                'read_termination': '\r\n',
            }
        }

    @Feat()
    def idn(self):
        """Identification.
        """
        return self.query('*IDN?')

        # Signal synthesis commands
        @Feat
        def lf_amplitude(self):
            """
            low frequency amplitude (BNC output)
            """
            return float(self.query('AMPL?'))

        @lf_amplitude.setter
        def lf_amplitude(self, value):
            self.write('AMPL{:.2f}'.format(value))

        @Feat
        def rf_amplitude(self):
            """
            RF amplitude (Type N output)
            """
            return float(self.query('AMPR?'))

        @rf_amplitude.setter
        def rf_amplitude(self, value):
            self.write('AMPR{:.2f}'.format(value))

        @Feat(values={True: '1', False: '0'})
        def lf_toggle(self):
            """
            low frequency output state
            """
            return self.query('ENBL?')

        @lf_toggle.setter
        def lf_toggle(self, value):
            self.write('ENBL{:s}'.format(value))

        @Feat(values={True: '1', False: '0'})
        def rf_toggle(self):
            """
            RF output state
            """
            return self.query('ENBR?')

        @rf_toggle.setter
        def rf_toggle(self, value):
            self.write('ENBR{:s}'.format(value))

        @Feat(units='Hz',limits=(1, 6.075e+9))
        def frequency(self):
            """
            signal frequency
            """
            return self.query('FREQ?')

# Can only set frequency up to a Hz
        @frequency.setter
        def frequency(self, value):
            self.write('FREQ{:.0f}'.format(value))

# Not needed?
'''
        @Feat()
        def rf_pll_loop_filter_mode(self):
            raise NotImplementedError

        @rf_pll_loop_filter_mode.setter
        def rf_pll_loop_filter_mode(self, value):
            raise NotImplementedError
'''

        @Feat()
        def lf_offset(self):
            """
            low frequency offset voltage
            """
            return self.query('OFSL?')

        @lf_offset.setter
        def lf_offset(self, value):
            self.write('OFSL{:.2f}'.format(value))

        @Feat(units='degrees')
        def phase(self):
            """
            carrier phase
            """
            return self.query('PHAS?')

        @phase.setter
        def phase(self, value):
            self.write('PHAS{:.2f}'.format(value))

        @Action()
        def rel_phase(self):
            """
            sets carrier phase to 0 degrees
            """
            self.write('RPHS')

        @Feat(values={True: 1, False: 0})
        def mod_toggle(self):
            """
            Modulation State
            """
            return self.query('MODL?')

        @mod_toggle.setter
        def mod_toggle(self, value):
            self.write('MODL {}'.format(value))

        @Feat(values={'AM': 0, 'FM': 1, 'Phase':2, 'Sweep':3, 'Pulse':4, 'Blank':5, 'QAM':7,'CPM':8, 'VSB':9})
        def mod_type(self):
            """
            Modulation State
            """
            return self.query('TYPE?')

        @mod_type.setter
        def mod_type(self, value):
            self.write('TYPE {}'.format(value))

# Set the modulation function for Sine\Ramp\Tri\Sq\noise\Ext
    @Feat(values={'sine': 0, 'ramp': 1, 'triangle': 2, 'square': 3, 'noise': 4, 'external':5})
    def modulation_function(self):
        """Modulation_Function.
        """
        return int(self.query('MFNC?'))

    @modulation_function.setter
    def modulation_function(self, value):
        self.write('MFNC {}'.format(value))

# Set the Modulation Rate for AM/FM/Phase
    @Feat(units='Hz', limits=(0, 93.75e6)) # This means 0 to 93.75e6
    def modulation_rate(self):
        """Modulation_Frequency.
        """
        return float(self.query('RATE?'))

# Can only set frequency up to a Hz
    @modulation_rate.setter
    def modulation_rate(self, value):
        self.write('RATE {:.0f}'.format(value))

# Set AM modulation depth
    @Feat(limits=(0, 100)) # The percentage depth
    def am_depth(self):
        """Amplitude Modulation Depth.
        """
        return float(self.query('ADEP?'))

    @am_depth.setter
    def am_depth(self, value):
        self.write('ADEP {:.2f}'.format(value))
        
# Set FM modulation depth - assuming above 500MHZ
    @Feat(units='Hz', limits=(0, 8e6))
    def fm_dev(self):
        """Frequency Modulation Difference
        """
        return float(self.query('FDEV?'))

    @fm_dev.setter
    def fm_dev(self, value):
        self.write('FDEV {:0f}'.format(value))

# Set phase modulation angle
    @Feat(units="degrees", limits=(-180,180))
    def phase_modulation(self):
        """Modulated Phase
        """
        return float(self.query('PDEV?'))

    @phase_modulation.setter
    def phase_modulation(self,value):
        self.write('PDEV {:1f}'.format(value))
        
# Set sweep modulation function
    @Feat(values={'sine': 0, 'ramp': 1, 'triangle': 2,'external':3})
    def sweep_function(self):
        """Sweep Function
        """
        return float(self.query('SFNC?'))

    @sweep_function.setter
    def sweep_function(self,value):
        self.write('SFNC {}'.format(value))
        
# Set sweep modulation rate
    @Feat(units="Hz", limits=(0,120))
    def sweep_modulation(self):
        """Sweep Modulation Rate.
        """
        return float(self.query('SRAT?'))

    @sweep_modulation.setter
    def sweep_modulation(self,value):
        self.write('SFNC {:1.f}'.format(value))
        
### Actions
    @Action()
    def calibrate(self):
        self.query('*CAL?')

    @Action()
    def clear_status(self):
        self.write("*CLS")

    @Action()
    def reset(self):
        self.write("*RST")
