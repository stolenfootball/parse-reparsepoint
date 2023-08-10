import re
import string


class Interpreter:

    # Info can be found in Microsoft's documentation:
    # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fscc/c8e77b37-3909-4fe6-a4ea-2b9d423b1ee4
    REPARSE_TAG_INFO = {
        0x00000000: (
            "IO_REPARSE_TAG_RESERVED_ZERO",
            "Reserved reparse tag value"
        ),
        0x00000001: (
            "IO_REPARSE_TAG_RESERVED_ONE",
            "Reserved reparse tag value"
        ),
        0x00000002: (
            "IO_REPARSE_TAG_RESERVED_TWO",
            "Reserved reparse tag value"
        ),
        0xA0000003: (
            "IO_REPARSE_TAG_MOUNT_POINT",
            "Contains information about mount point reparse points",
        ),
        0xC0000004: (
            "IO_REPARSE_TAG_HSM",
            "Obsolete. Used by legacy Hierarchical Storage Manager Product",
        ),
        0x80000005: (
            "IO_REPARSE_TAG_DRIVE_EXTENDER",
            "Home server drive extender"
        ),
        0x80000006: (
            "IO_REPARSE_TAG_HSM2",
            "Obsolete. Used by legacy Hierarchical Storage Manager Product",
        ),
        0x80000007: (
            "IO_REPARSE_TAG_SIS",
            "Used by single-instance storage (SIS) filter driver",
        ),
        0x80000008: (
            "IO_REPARSE_TAG_WIM",
            "Used by the WIM Mount filter"
        ),
        0x80000009: (
            "IO_REPARSE_TAG_CSV",
            "Obsolete. Used by Clustered Shared Volumes (CSV) version 1 in Windows Server 2008 R2",
        ),
        0x8000000A: (
            "IO_REPARSE_TAG_DFS",
            "Used by the DFS filter. DFS is described in the Distributed File System (DFS): Referral Protocol Specification [MS-DFSC]",
        ),
        0x8000000B: (
            "IO_REPARSE_TAG_FILTER_MANAGER",
            "Used by filter manager test harness",
        ),
        0xA000000C: (
            "IO_REPARSE_TAG_SYMLINK",
            "Used for symbolic link support. Contains information on symbolic link reparse points",
        ),
        0xA0000010: (
            "IO_REPARSE_TAG_IIS_CACHE",
            "Used by Microsoft Internet Information Services (IIS) caching",
        ),
        0x80000012: (
            "IO_REPARSE_TAG_DFS",
            "Used by the DFS filter. DFS is described in the Distributed File System (DFS): Referral Protocol Specification [MS-DFSC]",
        ),
        0x80000013: (
            "IO_REPARSE_TAG_DEDUP",
            "Used by the Data Deduplication (Dedup) filter",
        ),
        0xC0000014: (
            "IO_REPARSE_TAG_APPXSTRM",
            "Not used"
        ),
        0x80000014: (
            "IO_REPARSE_TAG_NFS",
            "Used by the Network File System (NFS) component",
        ),
        0x80000015: (
            "IO_REPARSE_TAG_FILE_PLACEHOLDER",
            "Obsolete. Used by Windows Shell for legacy placeholder files in Windows 8.1",
        ),
        0x80000016: (
            "IO_REPARSE_TAG_DFM",
            "Used by the Dynamic File filter"
        ),
        0x80000017: (
            "IO_REPARSE_TAG_WOF",
            "Used by the Windows Overlay filter, for either WIMBoot or single-file compression",
        ),
        0x80000018: (
            "IO_REPARSE_TAG_WCI",
            "Used by the Windows Container Isolation filter",
        ),
        0x90001018: (
            "IO_REPARSE_TAG_WCI_1",
            "Used by the Windows Container Isolation filter",
        ),
        0xA0000019: (
            "IO_REPARSE_TAG_GLOBAL_REPARSE",
            "Used by NPFS to indicate a named pipe symbolic link from a server silo into the host silo",
        ),
        0x9000001A: (
            "IO_REPARSE_TAG_CLOUD",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000101A: (
            "IO_REPARSE_TAG_CLOUD_1",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000201A: (
            "IO_REPARSE_TAG_CLOUD_2",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000301A: (
            "IO_REPARSE_TAG_CLOUD_3",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000401A: (
            "IO_REPARSE_TAG_CLOUD_4",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000501A: (
            "IO_REPARSE_TAG_CLOUD_5",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000601A: (
            "IO_REPARSE_TAG_CLOUD_6",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000701A: (
            "IO_REPARSE_TAG_CLOUD_7",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000801A: (
            "IO_REPARSE_TAG_CLOUD_8",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000901A: (
            "IO_REPARSE_TAG_CLOUD_9",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000A01A: (
            "IO_REPARSE_TAG_CLOUD_A",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000B01A: (
            "IO_REPARSE_TAG_CLOUD_B",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000C01A: (
            "IO_REPARSE_TAG_CLOUD_C",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000D01A: (
            "IO_REPARSE_TAG_CLOUD_D",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000E01A: (
            "IO_REPARSE_TAG_CLOUD_E",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x9000F01A: (
            "IO_REPARSE_TAG_CLOUD_F",
            "Used by the Cloud Files filter, for files managed by a sync engine such as Microsoft OneDrive",
        ),
        0x8000001B: (
            "IO_REPARSE_TAG_APPEXECLINK",
            "Used by Universal Windows Platform (UWP) packages to encode information that allows the application to be launched by CreateProcess",
        ),
        0x9000001C: (
            "IO_REPARSE_TAG_PROJFS",
            "Used by the Windows Projected File System filter, for files managed by a user mode provider such as VFS for Git",
        ),
        0xA000001D: (
            "IO_REPARSE_TAG_LX_SYMLINK",
            "Used by the Windows Subsystem for Linux (WSL) to represent a UNIX symbolic link",
        ),
        0x8000001E: (
            "IO_REPARSE_TAG_STORAGE_SYNC",
            "Used by the Azure File Sync (AFS) filter",
        ),
        0xA000001F: (
            "IO_REPARSE_TAG_WCI_TOMBSTONE",
            "Used by the Windows Container Isolation filter",
        ),
        0x80000020: (
            "IO_REPARSE_TAG_UNHANDLED",
            "Used by the Windows Container Isolation filter",
        ),
        0x80000021: (
            "IO_REPARSE_TAG_ONEDRIVE",
            "Not used"
        ),
        0xA0000022: (
            "IO_REPARSE_TAG_PROJFS_TOMBSTONE",
            "Used by the Windows Projected File System filter, for files managed by a user mode provider such as VFS for Git",
        ),
        0x80000023: (
            "IO_REPARSE_TAG_AF_UNIX",
            "Used by the Windows Subsystem for Linux (WSL) to represent a UNIX domain socket",
        ),
        0x80000024: (
            "IO_REPARSE_TAG_LX_FIFO",
            "Used by the Windows Subsystem for Linux (WSL) to represent a UNIX FIFO (named pipe)",
        ),
        0x80000025: (
            "IO_REPARSE_TAG_LX_CHR",
            "Used by the Windows Subsystem for Linux (WSL) to represent a UNIX character special file",
        ),
        0x80000026: (
            "IO_REPARSE_TAG_LX_BLK",
            "Used by the Windows Subsystem for Linux (WSL) to represent a UNIX block special file",
        ),
        0xA0000027: (
            "IO_REPARSE_TAG_WCI_LINK",
            "Used by the Windows Container Isolation filter",
        ),
        0xA0001027: (
            "IO_REPARSE_TAG_WCI_LINK_1",
            "Used by the Windows Container Isolation filter",
        ),
    }

    def __init__(self, reparse_data: dict[str, bytes]):
        """
        Initializes a new instance of the Interpreter class.

        :param reparse_data: The reparse data to interpret
        """

        self.reparse_data = reparse_data
        self.tag = int.from_bytes(reparse_data["reparse_tag"], "little")


    def __pull_regex(self, raw_data: bytes, regex_str: str) -> str:
        """
        Take a raw byte string and return anything that matches the compiled regex string.
        Ignore all non-printable characters and whitespace.

        :param raw_data: The raw byte string to convert
        :param regex_str: The regex string to use

        :return: A string with the regex match
        """

        # Convert bytes to string and remove all non-printable characters
        str_raw = raw_data.decode("utf-8", "ignore")
        all_ascii = "".join(filter(lambda x: x in string.printable, str_raw))

        # Remove all whitespace
        str = "".join(all_ascii.split())

        # Search for the regex
        regex = re.compile(regex_str)
        res = re.search(regex, str)

        if not res:
            raise ValueError("Regex not found in byte string")

        return res.group()


    def resolveReparseTag(self) -> str:
        """
        Takes the reparse tag and looks it up in a dict of info tag taken from the Microsoft learning
        website.  Formats them and returns a string for processing.

        :return: A human-readable string with the tag and the description.
        """

        try:
            return {
                "Tag Value": f"0x{self.tag:08X}",
                "Tag Identity": self.REPARSE_TAG_INFO[self.tag][0],
                "Tag Desctiption": self.REPARSE_TAG_INFO[self.tag][1],
            }

        except KeyError:
            return {
                "Tag Value": f"0x{self.tag:08X}",
                "Tag Identity": "UNKNOWN",
                "Tag Description": "No description available.",
            }


    def resolveOneDriveInfo(self) -> str:
        """
        Takes the reparse data, and returns a human-readable string with the OneDrive CID.

        :return: A human-readable string with the OneDrive CID.
        """

        if self.tag & 0xFFFF0FFF != 0x9000001A:
            raise ValueError("[-] ERROR: Not a OneDrive reparse point")

        # Check to see if it's a OneDrive Buisiness account.  These use GUIDs as CIDs
        try:
            guid_regex = "[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"

            return {
                "OneDrive CID": self.__pull_regex(self.reparse_data["reparse_data"], guid_regex),
                "OneDrive Account Type": "OneDrive Business",
            }

        except:
            pass

        # Check to see if it's a OneDrive Personal account.  These use 16 digit alphanum as CIDs.
        try:
            pers_regex = "[0-9A-F]{16}!"

            return {
                "OneDrive CID": self.__pull_regex(self.reparse_data["reparse_data"], pers_regex)[:-1],
                "OneDrive Account Type": "OneDrive Personal",
            }

        # It's a OneDrive account, but doesn't match any known pattern
        except:
            return {
                "OneDrive CID": "Unable to resolve OneDrive CID",
                "OneDrive Account Type": "Unknown",
            }


    def resolveSymLinkInfo(self) -> str:
        """
        Takes the reparse data, and returns a human-readable string with the symlink target.

        :return: A human-readable string with the symlink target.
        """

        if self.tag != 0xA000000C:
            raise ValueError("[-] ERROR: Not a symbolic link reparse point")

        try:
            # The substitute name is the computer readable target of the symlink
            substitute_name_offset = int.from_bytes(self.reparse_data["reparse_data"][0:2], "little") + 12
            substitute_name_length = int.from_bytes(self.reparse_data["reparse_data"][2:4], "little")

            substitute_name = self.reparse_data["reparse_data"][
                substitute_name_offset : substitute_name_offset + substitute_name_length
            ].decode("utf-16")
        
        except:
            substitute_name = "Unable to parse subsitiute name"

        try:
            # The print name is the human readable target of the symlink
            print_name_offset = int.from_bytes(self.reparse_data["reparse_data"][4:6], "little") + 12
            print_name_length = int.from_bytes(self.reparse_data["reparse_data"][6:8], "little")

            print_name = self.reparse_data["reparse_data"][
                print_name_offset : print_name_offset + print_name_length
            ].decode("utf-16")

        except:
            print_name = "Unable to parse print name"    

        try:
            # The flag is a boolean value that determines if the substitute name is an absolute or relative path
            flag = int.from_bytes(self.reparse_data["reparse_data"][8:12], "little")
            flag_value = "Substitute name is an absolute path name"
            if flag:
                flag_value = "Substitute name is a relative path name"

        except:
            flag_value = "Unable to parse flags"

        return {
            "Substitute Name": substitute_name,
            "Print Name": print_name,
            "Flag Info": flag_value,
        }


    def resolveMountPointInfo(self) -> str:
        """
        Takes the reparse data, and returns a human-readable string with the mount point.

        :return: A human-readable string with the mount point.
        """

        if self.tag != 0xA0000003:
            raise ValueError("[-] ERROR: Not a mount point reparse point")

        try:
            # The substitute name is the computer readable target of the mount point
            substitute_name_offset = int.from_bytes(self.reparse_data["reparse_data"][0:2], "little") + 8
            substitute_name_length = int.from_bytes(self.reparse_data["reparse_data"][2:4], "little")

            substitute_name = self.reparse_data["reparse_data"][
                substitute_name_offset : substitute_name_offset + substitute_name_length
            ].decode("utf-16")

        except:
            substitute_name = "Unable to parse subsitiute name"

        try:
            # The print name is the human readable target of the mount point
            print_name_offset = int.from_bytes(self.reparse_data["reparse_data"][4:6], "little") + 8
            print_name_length = int.from_bytes(self.reparse_data["reparse_data"][6:8], "little")

            print_name = self.reparse_data["reparse_data"][
                print_name_offset : print_name_offset + print_name_length
            ].decode("utf-16")
        
        except:
            print_name = "Unable to parse print name"

        return {
            "Substitute Name": substitute_name,
            "Print Name": print_name
        }


    def resolveAllInfo(self) -> str:
        """
        Takes the reparse data, and returns a human-readable string with all information
        able to be processed by this class.

        :return: A human-readable string with all processed information.
        """

        info = self.resolveReparseTag()

        info.update({"File Name": self.reparse_data["file_name"]})

        if self.tag & 0xFFFF0FFF == 0x9000001A:
            info.update(self.resolveOneDriveInfo())
        if self.tag == 0xA000000C:
            info.update(self.resolveSymLinkInfo())
        if self.tag == 0xA0000003:
            info.update(self.resolveMountPointInfo())

        return info


    def printAllInfo(self) -> None:
        """
        Takes the reparse data, and prints a human-readable string with all information
        able to be processed by this class.

        :return: None
        """

        buf = 25

        info = self.resolveAllInfo()
        print("Gathered reparse info:")
        for key in info:
            print(f"[+] {key + ':' :<{buf}} {info[key]}")
