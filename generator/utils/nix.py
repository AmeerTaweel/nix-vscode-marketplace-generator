import string

def convert_to_valid_nix_identifier(s: str) -> str:
    """Convert string to a valid Nix identifier."""
    valid_first = string.ascii_letters + "_"
    valid_rest = valid_first + string.digits + "-"

    # remove invalid characters
    identifier = "".join([c for c in s if c in valid_rest])
    # add padding in the beginning if needed
    if s[0] not in valid_first:
        identifier = "_" + identifier

    return identifier

def get_nix_package_name(extension: dict) -> str:
    name = convert_to_valid_nix_identifier(extension["name"])
    publisher = convert_to_valid_nix_identifier(extension["publisher"])
    return f"{name}.{publisher}"

def get_derivation(e: dict) -> list[str]:
    return [
        f"{get_nix_package_name(e)} = buildVscodeMarketplaceExtension " + "{",
        "\tmktplcRef = {",
        f"\t\tpublisher = \"{e['publisher']}\";",
        f"\t\tname = \"{e['name']}\";",
        f"\t\tversion = \"{e['version']}\";",
        f"\t\tsha256 = \"{e['sha256']}\";",
        "\t};",
        "};"
    ]

def output_flake(extensions: list[dict]):
    with open("flake.tmp.nix", "r") as template:
        template_split = template.read().split("\t\t\t###")
    with open("flake.out.nix", "w") as flake:
        derivations_text = "".join(["".join(["\t\t\t" + l + "\n" for l in get_derivation(e)]) for e in extensions])
        flake.writelines([
            template_split[0],
            derivations_text,
            template_split[1]
        ])