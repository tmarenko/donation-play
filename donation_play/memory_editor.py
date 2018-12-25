import ctypes
import pymem
from ctypes import wintypes

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
PROCESS_ALL_ACCESS = 0x1F0FFF

SIZE_T = ctypes.c_size_t
PSIZE_T = ctypes.POINTER(SIZE_T)


def _check_zero(result, func, args):
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


kernel32.OpenProcess.errcheck = _check_zero
kernel32.OpenProcess.restype = wintypes.HANDLE
kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)

kernel32.ReadProcessMemory.errcheck = _check_zero
kernel32.ReadProcessMemory.argtypes = (wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID, SIZE_T, PSIZE_T)

kernel32.WriteProcessMemory.restype = wintypes.BOOL
kernel32.WriteProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, ctypes.c_size_t,
                                        ctypes.POINTER(ctypes.c_size_t)]

kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)


def read_process_memory(pid, address, size=4):
    """Read process memory by address.

    :param pid: process id.
    :param address: address of memory.
    :param size: number of bytes to read.

    :return: bytes from the process memory.
    """
    buffer = (ctypes.c_char * size)()
    n_read = SIZE_T()
    process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    try:
        kernel32.ReadProcessMemory(process, address, buffer, size, ctypes.byref(n_read))
    except WindowsError as e:
        raise e
    finally:
        kernel32.CloseHandle(process)
    return buffer[:n_read.value]


def write_process_memory(pid, address, data, size=4):
    """Write bytes to process memory.

    :param pid: process id.
    :param address: address of memory.
    :param data: bytes to write.
    :param size: number of bytes to write.
    """
    bytes_data = data.to_bytes(length=size, byteorder='little')
    process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    try:
        kernel32.WriteProcessMemory(process, address, bytes_data, len(bytes_data), None)
    except WindowsError as e:
        raise e
    finally:
        kernel32.CloseHandle(process)


class MemoryEditor:
    """Class for editing process memory."""

    def __init__(self, process_name):
        """Class initialization.

        :param process_name: process name.
        """
        self.process = pymem.Pymem(process_name)
        self.base_address = self.process.process_base.lpBaseOfDll

    def _read_int_from_memory(self, address):
        """Read 4-bytes integer from memory.

        :param address: address of memory.

        :return: bytes from the process memory.
        """
        value = read_process_memory(self.process.process_id, address)
        return int.from_bytes(value, byteorder='little')

    def _write_int_to_memory(self, address, value):
        """Write 4-bytes integer to memory.

        :param address: address of memory.
        :param value: value to write.
        """
        write_process_memory(self.process.process_id, address, value)

    def get_value_from_pointer(self, pointer_offset=0, value_offset=0):
        """Get value from memory pointer.

        :param pointer_offset: pointer offset from base process address.
        :param value_offset: value offset from pointer.

        :return: value from the process memory.
        """
        pointer_address = self.base_address + pointer_offset
        pointer = self._read_int_from_memory(address=pointer_address)
        return self._read_int_from_memory(address=pointer + value_offset)

    def put_value_into_pointer(self, value, pointer_offset=0, value_offset=0):
        """Out value into the pointer.

        :param value: value to put.
        :param pointer_offset: pointer offset from base process address.
        :param value_offset: value offset from pointer.
        """
        pointer_address = self.base_address + pointer_offset
        pointer = self._read_int_from_memory(address=pointer_address)
        self._write_int_to_memory(address=pointer + value_offset, value=value)
