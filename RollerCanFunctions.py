from machine import Pin, I2C
from time import sleep
import struct

class RollerCan:
    """Class to control the RollerCAN device."""
    def __init__(self, i2c, address=0x64):
        self.i2c = i2c
        self.address = address
        self.initialized = False
        
        #Register motor enable
        self.REG_ENABLE = 0x00
        
        # Mode definitions (from the M5Unit-Roller library)
        self.REG_MODE = 0x01
        self.MODE_OFF = 0
        self.MODE_SPEED = 1
        self.MODE_POSITION = 2
        self.MODE_CURRENT = 3
        self.MODE_ENCODER = 4
        
        #Position readback register
        self.REG_POSITION_READBACK = 0x90
        #Position register
        self.REG_POSITION = 0x80
        #Speed register
        self.REG_SPEED = 0x40
        #Speed readback register
        self.REG_SPEED_READBACK = 0x60
  
    def init(self):
        """Initialize the RollerCAN device."""
        try:
            # Check if the device responds.  A simple way is to try to read a register.
            self.i2c.readfrom_mem(self.address, self.REG_MODE, 1)
            self.initialized = True
            return True
        except:
            self.initialized = False
            return False

    def _write_register(self, register, data):
        """Write data to a register."""
        self.i2c.writeto_mem(self.address, register, data)

    def _read_register(self, register, num_bytes):
        """Read data from a register."""
        return self.i2c.readfrom_mem(self.address, register, num_bytes)
    
    def get_speed(self):
        """Get the current speed."""
        return struct.unpack("<i",self._read_register(self.REG_SPEED_READBACK, 4))[0] // 100

    def set_speed(self, speed):
        """Set the home offset."""
        
        speed_bytes = struct.pack("<i", int(speed))
        
        self._write_register(self.REG_SPEED,speed_bytes)
    
    def set_mode(self, mode):
        """Set the operating mode."""
        self._write_register(self.REG_MODE, bytes([mode]))
        
    def set_position(self, position):
        """Set the target position."""
        # Convert the position to 4 bytes
        pos_bytes = struct.pack("<i", int(position))  # Changed to signed integer
        
        # Write the 4 bytes to the registers
        self._write_register(self.REG_POSITION, pos_bytes)

    def get_position(self):
        """Get the current position."""
        #read the 4 bytes of the position
        pos_bytes = self._read_register(self.REG_POSITION,4)
        #convert the bytes to an integer
        position = struct.unpack("<i", pos_bytes)[0]  # Changed to signed integer
        return int(position)
    
    def get_position_readback(self):
        """Get the current position."""
        #read the 4 bytes of the position
        pos_bytes = self._read_register(self.REG_POSITION_READBACK,4)
        #convert the bytes to an integer
        position = struct.unpack("<I", pos_bytes)[0]  # Changed to signed integer
        return position
    
    def enable_motor(self):
        """Enable the motor."""
        self._write_register(self.REG_ENABLE, bytes([1]))

    def disable_motor(self):
        """Disable the motor."""
        self._write_register(self.REG_ENABLE, bytes([0]))

i2c = I2C(0, scl=Pin(41), sda=Pin(40), freq=100000)  # Use I2C0 on Presto, adjust pins if needed.

class FilterMove:
    def __init__(self):
        
        self.i2c = I2C(0, scl=Pin(41), sda=Pin(40), freq=100000)
        self.roller = RollerCan(self.i2c)
        self.roller.set_mode(self.roller.MODE_POSITION) 
     
class DiskRotate:
    def __init__(self):

        self.i2c = I2C(0, scl=Pin(41), sda=Pin(40), freq=100000)
        self.roller = RollerCan(self.i2c)
        self.roller.set_mode(self.roller.MODE_SPEED)
    
    def start(self):
        self.roller.enable_motor()
        
    def stop(self):
        self.roller.disable_motor()