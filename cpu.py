from collections import defaultdict
from typing import List

from instruction import *
from memory import Memory
from memory_owner import MemoryOwnerMixin
from ppu import PPU
from rom import ROM
from status import Status


class CPU(object):
    def __init__(self, memory: Memory, ppu: PPU):
        self.memory = memory
        self.ppu = ppu
        self.rom = None

        self.memory_owners = [  # type: List[MemoryOwnerMixin]
            self.memory,
            self.ppu
        ]

        self.status_reg = None  # type: Status

        self.pc_reg = None
        self.sp_reg = None

        self.x_reg = None
        self.y_reg = None
        self.a_reg = None

        self.running = True

        self.instructions = [
            SEIInstruction(),
            CLDInstruction(),
            LoadAccumulatorInstruction(),
            StoreAccumulatorAbsoluteInstruction()
        ]

        self.instructions_mapping = defaultdict()
        for instruction in self.instructions:
            self.instructions_mapping[instruction.identifier_byte] = instruction

    def initialization(self):
        self.pc_reg = 0
        self.status_reg = Status()
        self.sp_reg = bytes.fromhex('FD')

        self.x_reg = 0
        self.y_reg = 0
        self.a_reg = 0

    def get_memory_owner(self, location: int) -> MemoryOwnerMixin:
        if self.rom.memory_start_location <= location <= self.rom.memory_end_location:
            return self.rom

        for memory_owner in self.memory_owners:
            if memory_owner.memory_start_location <= location <= memory_owner.memory_end_location:
                return memory_owner

        raise Exception('Cannot find memory owner')

    def load_rom(self, rom: ROM):
        self.rom = rom
        self.pc_reg = self.rom.header_size

        self.running = True

        while self.running:
            identifier_byte = self.rom.get(self.pc_reg)

            instruction = self.instructions_mapping.get(identifier_byte, None)

            if instruction is None:
                raise Exception('Instruction {} not found.'.format(identifier_byte))

            num_data_bytes = instruction.instruction_length - 1

            data_bytes = self.rom.get(self.pc_reg + 1, num_data_bytes)

            instruction.execute(self, data_bytes)

            self.pc_reg += instruction.instruction_length
