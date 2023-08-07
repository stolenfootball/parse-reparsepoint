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
        
        with open(file_name, 'rb') as file:

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

        return int.from_bytes(data, byteorder=byteorder, signed=signed)
    

    def __applyFixup(self, data: bytes) -> bytes:
        """
        Applies the NTFS fixup to the given data.  

        :param data: The data to apply the fixup to

        :return:     The data with the fixup applied
        """

        offset_to_fixup = self.__unpack(data[4:6])
        num_fixup_entries = self.__unpack(data[6:8])

        fixup = data[offset_to_fixup + 2 : offset_to_fixup + 2 * num_fixup_entries]

        data_bytes = bytearray(data)
        for i in range(num_fixup_entries):
            data_bytes[(512 * i) - 2 : (512 * i)] = fixup[(2 * i) : (2 * i) + 2]

        return bytes(data)
    

    def __parseRunlist(self, runlist: bytes) -> list[int]:
        """
        Parses the runlist of a non-resident file and returns a list of the sectors that the file spans.

        :param runlist: The runlist to parse

        :return:        A list of sectors that the file spans
        """

        sector_list = []
        offset = 0

        # Continue processing until 0x00 is reached.  This marks the end of the runlist.
        while runlist[0] != 0x00:

            # The number of bytes in the offset and length fields are stored in the first byte. The
            # upper 4 bits are the number of bytes in the offset and the lower 4 bits are the number
            # of bytes in the length.
            offset_length = runlist[0] >> 4
            length_length = runlist[0] & 0x0F

            # The number of conseutive sectors in the run
            length = self.__unpack(runlist[1 : length_length + 1], signed=True)

            # The offset of the start of the current run from the start of the previous run.  Since
            # the start of the current run can be before than the start of the previous run, the offset
            # is signed.
            offset = offset + self.__unpack(
                runlist[length_length + 1 : length_length + 1 + offset_length], signed=True
            )

            # Add the sectors in the current run to the list of sectors
            for i in range(length):
                sector_list.append(offset + i)
            runlist = runlist[length_length + 1 + offset_length :]

        return sector_list
    

    def __getMFTSectors(self, file: BinaryIO) -> list[int]:
        """
        Gets the sectors that the MFT spans

        :param file: The file to read from

        :return:     A list of sectors that the MFT spans
        """

        file.seek(self.mft_byte_offset)
        raw_mft_entry = file.read(self.bytes_per_entry)

        # The first 4 bytes of the MFT entry are the signature.  If the signature is not 'FILE', then
        # the MFT is corrupt.
        if raw_mft_entry[0:4] != b'FILE':
            raise Exception('MFT is corrupt')
        
        mft_entry = self.__applyFixup(raw_mft_entry)

        # The runlist is contained in the data attribute.  The data attribute has an ID of 0x80.
        data_attribute = self.__getRawAttribute(mft_entry, 0x80)

        # The sectors that the MFT spans are stored in the runlist.  The offset to the runlist is stored
        # at offset 0x20 in the MFT entry.
        offset_to_runlist = self.__unpack(data_attribute[0x20:0x22])
        return self.__parseRunlist(data_attribute[offset_to_runlist:])


    def __getRawMFTEntry(self, file: BinaryIO, entry: int) -> bytes:
        """
        Gets the raw MFT entry bytes from the file.  Performs no processing.

        :param file:  The file to read from
        :param entry: The entry to read

        :return:      The raw MFT entry
        """

        entries_per_cluster = self.bytes_per_cluster // self.bytes_per_entry

        # The cluster number the entry is in, and the byte offset of the entry in the cluster
        # print(entry, entries_per_cluster)
        cluster_number = self.mft_sectors[entry // entries_per_cluster]
        cluster_offset = (entry % entries_per_cluster) * self.bytes_per_entry

        # The byte offset of the MFT entry from the beginning of the file
        byte_offset = (cluster_number * self.bytes_per_cluster) + cluster_offset

        file.seek(byte_offset)
        return file.read(self.bytes_per_entry)



    def __getRawAttribute(self, data: bytes, attribute: int) -> bytes:
        """
        Loops through each attribute in the MFT entry and returns the raw bytes 
        of the attribute with the given ID.

        :param data:       The MFT entry to parse
        :param attribute:  The ID of the attribute to get

        :return:           The raw bytes of the attribute
        """
        
        # The offset to the first attribute is stored at offset 0x14 in the MFT entry.
        attr_start = self.__unpack(data[0x14:0x16])

        # Loop through each attribute until either the end of the MFT entry is reached or the
        # attribute with the given ID is found.
        while attr_start < self.bytes_per_entry:

            attr_end = attr_start + self.__unpack(data[attr_start + 4:attr_start + 8])

            attr = data[attr_start:attr_end]

            if self.__unpack(attr[0:4]) ==  0xFFFFFFFF: break
            if self.__unpack(attr[0:4]) == attribute: return attr

            attr_start = attr_end    

        raise Exception('Attribute not found')


    def __parseFileNameAttribute(self, data: bytes) -> str:
        """
        Retrieves the file name from the file name attribute.

        :param data: The file name attribute to parse

        :return:     The file name
        """

        content_offset = self.__unpack(data[0x14:0x16])
        attribute_content = data[content_offset:]
        
        return bytes.decode(attribute_content[66 : 66 + (attribute_content[64] * 2)], "utf-16-le")


    def __parseReparseAttribute(self, data: bytes) -> dict[str, bytes]:
        """
        Parses and returns the reparse data and the reparse tag from the reparse attribute.

        :param data: The reparse attribute to parse

        :return:     A dictionary containing the reparse tag and the reparse data
        """

        content_offset = self.__unpack(data[0x14:0x16])
        attribute_content = data[content_offset:]

        reparse_data_length = self.__unpack(attribute_content[4:8])

        return {
            "reparse_tag": attribute_content[0:4],
            "reparse_data": attribute_content[8:8 + reparse_data_length]
        }

    
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
    

