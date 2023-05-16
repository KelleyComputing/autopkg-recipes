
from autopkglib import ProcessorError, Processor

__all__ = ["WebExURLProvider"]

class WebExURLProvider(Processor):
    """Provides an architecture specific download URL for the latest WebEx Version"""

    input_variables = {
        "architecture": {
            "required": False,
            "description": "Architecture of the WebEx package to download. "
            "Possible values are 'x86_64' (Intel) or 'arm64' (Apple Silicon). "
            "Defaults to 'x86_64' (Intel).",
        },
    }
    output_variables = {
        "url": {"description": "URL to the latest WebEx Connect release."},
    }
    description = __doc__

    def main(self):
        """Main process."""

        # Set Base Url
        url_base = "https://binaries.webex.com/"

        # Read and validate input variables
        arch = self.env.get("architecture", "x86_64")
        if arch not in ("x86_64", "arm64"):
            raise ProcessorError("Architecture must be one of: x86_64, arm64")

        # Set url in environment
        if arch == "x86_64":
            self.env["url"] = url_base + "WebexTeamsDesktop-MACOS-Gold/Webex.dmg"
        elif arch == "arm64":
            self.env["url"] = url_base + "WebexDesktop-MACOS-Apple-Silicon-Gold/Webex.dmg"

        self.output("Found url: %s" % self.env["url"])


if __name__ == "__main__":
    PROCESSOR = WebExURLProvider()
    PROCESSOR.execute_shell()
