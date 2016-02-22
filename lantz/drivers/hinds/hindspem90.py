from lantz import Feat, DictFeat, Action
from lantz.messagebased import MessageBasedDriver
from pyvisa import constants

from numpy import ceil

from time import sleep

from lantz.log import log_to_screen, DEBUG


class HindsPEM90(MessageBasedDriver):
    """

    """

    # Set paramters here
    off_on = {'off': 1, 'on': 0}
    waves_limits = (0.0, 19999.9)
    retardation_limits = (0.0, 1.0)

    DEFAULTS = {'ASRL': {'write_termination': '\r',
                         'read_termination': '\r\n',
                         'baud_rate': 9600,
                         'data_bits': 8,
                         'parity': constants.Parity.none,
                         'stop_bits': constants.StopBits.one,
                         'encoding': 'utf-8',
                         'timeout': 3000}}

    def initialize(self):
        """
        """
        super().initialize()
        self.reset()
        self.echo = 'off'

    @Feat(values=off_on)
    def echo(self):
        """
        Checks to see if ECHO mode is enabled. Note that the code in this
        driver assumes that the command echo is disabled.
        """

        print('Can\'t read this, can only set.')
        return 0

    @echo.setter
    def echo(self, status):
        """
        Sets echo mode to be controlled by on_off.
        """
        self.clear_buffer()
        result = self.write('E:{}'.format(status))
        self.read()
        return result


    @Feat(limits=waves_limits)
    def wavelength(self):
        """
        Reads out current wavelength in nm
        """
        self.clear_buffer()
        self.write('W')
        self.read()
        return float(self.read())/10.0

    @wavelength.setter
    def wavelength(self, nm):
        """
        Sets wavelength in nm.
        """
        result = self.write('W:{0:0>6.0f}'.format(nm*10.0))
        self.read()
        return result

    @Feat(limits=retardation_limits)
    def retardation(self):
        """
        Reads out current retardation in wave units
        """
        self.clear_buffer()
        self.write('R')
        self.read()
        return float(self.read())/1000.0

    @retardation.setter
    def retardation(self, wave_units):
        """
        Sets retardation in wave units.
        """
        return self.write('R:{0:04.0f}'.format(ceil(wave_units*1000)))

    @Feat()
    def frequency(self):
        """
        Reads out the reference frequency in hertz
        """
        self.clear_buffer()
        self.write('F')
        self.read()
        return float(self.read())

    @Feat()
    def frequency2(self):
        """
        Reads out the reference frequency2 in hertz
        """
        self.clear_buffer()
        self.query('2F')
        return float(self.read())

    @Feat(values=off_on)
    def inhibitor(self):
        """
        Returns 0 for the retardation inhibitor
        """
        return 0

    @inhibitor.setter
    def inhibitor(self, status):
        """
        Sets the mode to be controlled by on_off.
        """
        print('I:{}'.format(status))
        return self.query('I:{}'.format(status))

    @Action()
    def reset(self):
        """
        Resets PEM-90 to default factory settings.
        """
        print('Resetting PEM90...')
        self.clear_buffer()
        return self.write('Z')

    def clear_buffer(self):
        """
        Clears the buffer of PEM-90.
        """
        while True:
            try:
                self.read()
            except:
                print('Timeout?')
                return



if __name__ == '__main__':
    print('Hi')
    log_to_screen(DEBUG)
    with HindsPEM90.via_serial(12) as inst:
        for a in range(0, 100):
            print('Frequency:{}Hz'.format(inst.frequency))
            print('Wavelength:{}nm'.format(inst.wavelength))
            print('Retardation:{}'.format(inst.retardation))

            inst.wavelength = 500.0
            print('Wavelength:{}nm'.format(inst.wavelength))

            inst.retardation = 0.5
            print('Retardation:{}'.format(inst.retardation))

            inst.wavelength = 400.0
            print('Wavelength:{}nm'.format(inst.wavelength))

            inst.retardation = 0.25
            print('Retardation:{}'.format(inst.retardation))
