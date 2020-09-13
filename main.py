import argparse

from cpu import CPU
from memory import Memory
from ppu import PPU
from rom import ROM

HEADER_SIZE = 16
KB_SIZE = 16384


def main():
    parser = argparse.ArgumentParser(description='NES Emulator.')

    parser.add_argument('rom_path',
                        metavar='R',
                        type=str,
                        help='path to the nes rom')

    args = parser.parse_args()

    print(args.rom_path)

    with open(args.rom_path, 'rb') as file:
        rom_bytes = file.read()

    rom = ROM(rom_bytes)

    memory = Memory()
    ppu = PPU()

    cpu = CPU(memory, ppu)

    cpu.initialization()
    cpu.load_rom(rom)


if __name__ == '__main__':
    main()
