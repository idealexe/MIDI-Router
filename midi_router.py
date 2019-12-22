import rtmidi2
import time

MIDI_IN = "EWI-USB"
MIDI_OUT = "SD-90 PART A"


class MidiRouter:
    """ MIDI Router
    """
    def __init__(self, midi_in: str, midi_out: str):
        self.presets = [
            [0xF0, 0x41, 0x10, 0x00, 0x48, 0x12, 0x10, 0x00, 0x20, 0x04, 0x51, 0x00, 0x28, 0x53, 0xF7],  # Reed Romance
            [0xF0, 0x41, 0x10, 0x00, 0x48, 0x12, 0x10, 0x00, 0x20, 0x04, 0x62, 0x00, 0x38, 0x32, 0xF7],  # Romantic Tp
            [0xF0, 0x41, 0x10, 0x00, 0x48, 0x12, 0x10, 0x00, 0x20, 0x04, 0x50, 0x00, 0x0D, 0x6F, 0xF7],  # Mariachi Tp
            [0xF0, 0x41, 0x10, 0x00, 0x48, 0x12, 0x10, 0x00, 0x20, 0x04, 0x51, 0x00, 0x1F, 0x5C, 0xF7],  # Loose Lips
            [0xF0, 0x41, 0x10, 0x00, 0x48, 0x12, 0x10, 0x00, 0x20, 0x04, 0x62, 0x00, 0x3D, 0x2D, 0xF7],  # St.Brass
            [0xF0, 0x41, 0x10, 0x00, 0x48, 0x12, 0x10, 0x00, 0x20, 0x04, 0x62, 0x00, 0x51, 0x19, 0xF7],  # Oct.JP Saw
            [0xF0, 0x41, 0x10, 0x00, 0x48, 0x12, 0x10, 0x00, 0x20, 0x04, 0x62, 0x00, 0x49, 0x21, 0xF7],  # Flute vib
            [0xF0, 0x41, 0x10, 0x00, 0x48, 0x12, 0x10, 0x00, 0x20, 0x04, 0x62, 0x03, 0x10, 0x57, 0xF7],  # Full Stops
            [0xF0, 0x41, 0x10, 0x00, 0x48, 0x12, 0x10, 0x00, 0x20, 0x04, 0x51, 0x00, 0x33, 0x48, 0xF7],  # Celtic Ens
        ]
        """ initialize
        """
        print("available MIDI IN:\t" + str(rtmidi2.get_in_ports()))
        print("available MIDI OUT:\t" + str(rtmidi2.get_out_ports()))

        self.midi_in = rtmidi2.MidiIn()
        self.midi_out = rtmidi2.MidiOut()

        self.midi_in.open_port(midi_in + "*")
        self.midi_out.open_port("*" + midi_out + "*")

        self.midi_in.callback = self.midi_in_callback
        self.current_preset = 0
        self.midi_out.send_sysex(*self.presets[self.current_preset])

    def midi_in_callback(self, msg, timestamp):
        # print(msg)

        """ filters
        """
        if msg[0] == rtmidi2.CC and msg[1] == 96 and msg[2] == 127:
            self.increment_preset()
            return
        if msg[0] == rtmidi2.CC and msg[1] == 97 and msg[2] == 127:
            self.decrement_preset()
            return
        self.midi_out.send_raw(*msg)

    def increment_preset(self):
        """ 次のプリセットに変更する
        """
        self.current_preset = self.current_preset + 1 if self.current_preset < len(self.presets) - 1 else 0
        self.midi_out.send_sysex(*self.presets[self.current_preset])

    def decrement_preset(self):
        """ 前のプリセットに変更する
        """
        self.current_preset = self.current_preset - 1 if self.current_preset > 0 else len(self.presets) - 1
        self.midi_out.send_sysex(*self.presets[self.current_preset])

    def start_performance(self):
        """ start performance
        """
        while KeyboardInterrupt:
            time.sleep(0.01)
        self.end_performance()

    def end_performance(self):
        """ end performance
        """
        self.midi_in.close_port()
        self.midi_out.close_port()


if __name__ == '__main__':
    midi_router = MidiRouter(MIDI_IN, MIDI_OUT)
    midi_router.start_performance()
