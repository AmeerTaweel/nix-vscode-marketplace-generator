{
	description = "Nix VSCode Marketplace";

	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
		flake-utils.url = "github:numtide/flake-utils";
	};

	outputs = { self, nixpkgs, mach-nix, flake-utils }:
	flake-utils.lib.eachDefaultSystem (system: let
		pkgs = nixpkgs.legacyPackages.${system};
	in {
		packages = with pkgs.vscode-utils; {
			###
		};
	});
}
