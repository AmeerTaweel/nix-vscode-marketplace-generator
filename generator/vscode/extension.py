from utils import nix

class VSCodeExtension():
    ZIP_DIR = "zip"

    def __init__(self, publisher: str, name: str):
        self._publisher = publisher
        self._name = name
        self._version = ""
        self._sha256 = ""

    @property
    def name(self) -> str:
        return self._name

    @property
    def publisher(self) -> str:
        return self._publisher

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, version) -> None:
        self._version = version

    @property
    def sha256(self) -> str:
        return self._sha256

    @sha256.setter
    def sha256(self, sha256) -> None:
        self._sha256 = sha256.replace("\n", "")

    # Computed Properties

    @property
    def nix_package_name(self) -> str:
        name = nix_utils.convert_to_valid_nix_identifier(self._name)
        publisher = nix_utils.convert_to_valid_nix_identifier(self._publisher)
        return f"{publisher}.{name}"

    @property
    def download_url(self):
        return f"https://{self.publisher}.gallery.vsassets.io/_apis/public/gallery/publisher/{self.publisher}/extension/{self.name}/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage"

    @property
    def zip_file(self) -> str:
        return f"{VSCodeExtension.ZIP_DIR}/{self.nix_identifier}.zip"

    @property
    def derivation(self) -> list[str]:
        return [
            f"{self.nix_identifier} = buildVscodeMarketplaceExtension " + "{",
            "\tmktplcRef = {",
            f"\t\tpublisher = \"{self.publisher}\";",
            f"\t\tname = \"{self.name}\";",
            f"\t\tversion = \"{self.version}\";",
            f"\t\tsha256 = \"{self.sha256}\";",
            "\t};",
            "};"
        ]
