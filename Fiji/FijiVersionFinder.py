#!/usr/local/autopkg/python
#
# Refactoring 2018 Michal Moravec
# Copyright 2015 Greg Neagle
# Based on URLTextSearcher.py, Copyright 2014 Jesse Peterson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for FijiVersionFinder class"""

import re

from autopkglib import ProcessorError
from autopkglib.URLGetter import URLGetter

MATCH_MESSAGE = "Found matching text"
NO_MATCH_MESSAGE = "No match found on URL"

__all__ = ["FijiVersionFinder"]


class FijiVersionFinder(URLGetter):
    """Downloads a URL using curl and performs a regular expression match
    on the text.
    Requires version 1.4."""

    input_variables = {
        "url": {"description": "URL to download", "required": True},
        "request_headers": {
            "description": (
                "Optional dictionary of headers to include with "
                "the download request."
            ),
            "required": False,
        },
        "curl_opts": {
            "description": (
                "Optional array of curl options to include with "
                "the download request."
            ),
            "required": False,
        },
    }
    output_variables = {
        "version": {
            "description": (
                "Highest version Number found on the url"
                            )
        }
    }

    description = __doc__

    def prepare_curl_cmd(self):
        """Assemble curl command and return it."""
        curl_cmd = super().prepare_curl_cmd()
        self.add_curl_common_opts(curl_cmd)
        curl_cmd.append(self.env["url"])
        return curl_cmd



    def get_max_version(self, content):
        """Find all version numbers and return the highest"""

        re_pattern = re.compile('\d+\.\d+\.\d+/')
        matches = re_pattern.findall(content)

        if not matches:
            raise ProcessorError(f"{NO_MATCH_MESSAGE}: {self.env['url']}")

        max_version = "0.0.0"
        for match in matches:
            parts = match[:-1].split('.')
            for i, p, in enumerate(parts):
                # If Newer version set max as this version and don't look at subversions
                if int(p) > int(max_version.split('.')[i]):
                    max_version = match[:-1]
                    break
                # If Lower version don't look at subversions
                elif int(p) < int(max_version.split('.')[i]):
                    break


        return max_version

    def main(self):
        # Prepare curl command
        curl_cmd = self.prepare_curl_cmd()

        # Execute curl command and search in content
        content = self.download_with_curl(curl_cmd)
        max_version = self.get_max_version(content)

        self.output(f"{MATCH_MESSAGE} {max_version}")
        self.env["version"] = max_version


if __name__ == "__main__":
    PROCESSOR = FijiVersionFinder()
    PROCESSOR.execute_shell()