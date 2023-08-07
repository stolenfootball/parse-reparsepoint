from typing import BinaryIO

class Navigator:

    def __init__(self, file_name: str):
        """
        Reads the boot sector of the NTFS file system and extracts the following information:
        - Bytes per cluster
        - Bytes per entry
        - The offset of the MFT in bytes

        :param file_name: The name of the file to parse
        """
        
        with open(file_name, 'r') as file:

            self.file_name = file_name

            file.seek(0)
            boot = file.read(512)

            bytes_per_sector = self.__unpack(boot[11:13])
            sectors_per_cluster = self.__unpack(boot[13:14])
            mft_starting_cluster = self.__unpack(boot[48:56])

            self.bytes_per_cluster = bytes_per_sector * sectors_per_cluster
            self.bytes_per_entry = 1024
            self.mft_byte_offset = mft_starting_cluster * sectors_per_cluster * bytes_per_sector

            self.mft_sectors = self.__getMFTSectors(file)

    
    def __unpack(self, data: bytes, byteorder='little', signed=False) -> int:
        """
        Unpacks the given bytes into an integer.  This is a wrapper for the int.from_bytes() method
        with default values for byteorder and signed.

        :param data:      The bytes to unpack
        :param byteorder: The byte order to use
        :param signed:    Whether or not the bytes are signed

        :return:          The unpacked integer
        """

        pass
    

    def __applyFixup(self, data: bytes) -> bytes:
        """
        Applies the NTFS fixup to the given data.  

        :param data: The data to apply the fixup to

        :return:     The data with the fixup applied
        """

        pass
    

    def __parseRunlist(self, runlist: bytes) -> list[int]:
        """
        Parses the runlist of a non-resident file and returns a list of the sectors that the file spans.

        :param runlist: The runlist to parse

        :return:        A list of sectors that the file spans
        """

        pass
    

    def __getMFTSectors(self, file: BinaryIO) -> list[int]:
        """
        Gets the sectors that the MFT spans

        :param file: The file to read from

        :return:     A list of sectors that the MFT spans
        """

        pass


    def __getRawMFTEntry(self, file: BinaryIO, entry: int) -> bytes:
        """
        Gets the raw MFT entry bytes from the file.  Performs no processing.

        :param file:  The file to read from
        :param entry: The entry to read

        :return:      The raw MFT entry
        """

        pass


    def __getRawAttribute(self, data: bytes, attribute: int) -> bytes:
        """
        Loops through each attribute in the MFT entry and returns the raw bytes 
        of the attribute with the given ID.

        :param data:       The MFT entry to parse
        :param attribute:  The ID of the attribute to get

        :return:           The raw bytes of the attribute
        """
            
        pass


    def __parseFileNameAttribute(self, data: bytes) -> str:
        """
        Retrieves the file name from the file name attribute.

        :param data: The file name attribute to parse

        :return:     The file name
        """

        pass


    def __parseReparseAttribute(self, data: bytes) -> dict[str, bytes]:
        """
        Parses and returns the reparse data and the reparse tag from the reparse attribute.

        :param data: The reparse attribute to parse

        :return:     A dictionary containing the reparse tag and the reparse data
        """

        pass

    
    def getEntry(self, entry: int) -> dict[str, bytes]:
        """
        Gets the entry from the MFT and parses attribute agnostic information from it.
        Returns a dictionary of the following:
        - The entry name
        - The reparse tag
        - The reparse data

        :param entry: The MFT entry number of the entry to get

        :return:      The data obtained from the entry
        """

        pass
    

