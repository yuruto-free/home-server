#!/usr/bin/python3
#coding: utf-8
#
# preparation: sudo apt-get install python3-smbus

import smbus

class Adrsir():
    def __init__(self):
        # I2C address of ADRSIR
        self.__ADDR = 0x52
        # command group
        self.__R1_memo_no_write  = 0x15
        self.__R2_data_num_read  = 0x25
        self.__R3_data_read      = 0x35
        self.__W2_data_num_write = 0x29
        self.__W3_data_write     = 0x39
        self.__T1_trans_start    = 0x59
        self.__bus = smbus.SMBus(1)

    def get(self, no):
        # ==================================== #
        # procedure of reading infrared length #
        # ==================================== #
        send_data = [no]
        self.__bus.write_i2c_block_data(self.__ADDR, self.__R1_memo_no_write, send_data)
        data = self.__bus.read_i2c_block_data(self.__ADDR, self.__R2_data_num_read, 3)
        # data = [0, data length High, data length Low]
        read_length = (data[1] << 8) + data[2] # Byte size of data is read_length * 4.

        if read_length == 0xffff:
            return []

        # Throw away after a signal reading becase the data of 1st byte is zero.
        data = self.__bus.read_i2c_block_data(self.__ADDR, self.__R3_data_read, 1)
        # repeate read_length
        ir_data = []
        for _ in range(read_length):
            # read by 4 byte
            data = self.__bus.read_i2c_block_data(self.__ADDR, self.__R3_data_read, 4)
            ir_data.extend(data)

        ir_str_data = ''.join(['{:02x}'.format(val) for val in ir_data])

        return ir_str_data

    def send(self, ir_str_data):
        # ==================================== #
        # procedure of writing infrared length #
        # ==================================== #
        ir_data = [int(ir_str_data[idx:idx+2], 16) for idx in range(0, len(ir_str_data), 2)]
        data_length = len(ir_data)
        send_data = [data_length >> 8, data_length & 0xff]
        self.__bus.write_i2c_block_data(self.__ADDR, self.__W2_data_num_write, send_data)

        # repeate read_length
        for idx in range(0, data_length, 4):
            # write by 4 byte
            self.__bus.write_i2c_block_data(self.__ADDR, self.__W3_data_write, ir_data[idx:idx+4])
        self.__bus.write_i2c_block_data(self.__ADDR, self.__T1_trans_start, [0])

if __name__ == '__main__':
    model = Adrsir()
    gotten_data = model.get(0)
    print(gotten_data)
