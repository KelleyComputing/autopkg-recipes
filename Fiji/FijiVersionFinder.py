#!/usr/local/autopkg/python

"""See docstring for FijiVersionFinder class"""

import re
import os

from autopkglib import Processor, ProcessorError

MATCH_MESSAGE = "Found fiji version"
NO_MATCH_MESSAGE = "No match found"

__all__ = ["FijiVersionFinder"]


class FijiVersionFinder(Processor):
    """Searches the fiji jars folder to find the fiji jar, and extracts
    the version number from the file name."""

    input_variables = {
        "jars_folder": {"description": "Fiji jars folder", "required": True},
    }
    output_variables = {
        "version": {
            "description": (
                "The version number of fiji.jar"
                            )
        }
    }

    description = __doc__

    def main(self):
        pattern = re.compile('fiji-(?P<ver>\d*\.\d*\.\d*)\.jar')
        for f in os.listdir(self.env["jars_folder"]):
            m = re.match(pattern, f)
            if m:
                self.output(f"{MATCH_MESSAGE} {m.group('ver')}")
                self.env["version"] = m.group('ver')
                break

if __name__ == "__main__":
    PROCESSOR = FijiVersionFinder()
    PROCESSOR.execute_shell()
