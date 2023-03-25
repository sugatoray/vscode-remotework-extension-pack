# %%
import glob
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from collections import OrderedDict
from textwrap import dedent
from typing import Dict, List, Optional

import fire

__all__ = ["ExtensionPackMetadata", "main"]

HERE = os.path.dirname(os.path.abspath(__file__))  # type: ignore
DUMP_METADATA_FILENAME_PATTERN: str = "dump_{extension_id}_metadata.json"
README_TEMPLATE_FILENAME: str = "README_TEMPLATE.md"

MD_TABLE_TEMPLATE: Dict[str, str] = dict(
    header=dedent(
        """\
        | SL# | Extension |
        |:---:|:---|
    """
    ),
    rowdata=dedent(
        """\
        | `{idx}` | 🎁 [{label}](https://marketplace.visualstudio.com/items?itemName={extension_id}) <br/> <p><ul> {description}. </ul></p> |
    """
    ),
)


def get_extension_metadata_from_marketplace_dump(filepath: str) -> dict:
    """Get extension metadata from the json file.

    Usage:

        ```python
        extension_metadata = get_extension_metadata_from_marketplace_dump(filepath)
        print(json.dumps(extension_metadata, indent=2))
        ```

    """

    with open(filepath, "r") as f:
        data = json.load(f)
    return dict(
        publisherName=data.get("publisher", {}).get("publisherName", ""),
        extensionName=data.get("extensionName", ""),
        displayName=data.get("displayName", ""),
        shortDescription=data.get("shortDescription", ""),
        latestVersion=data.get("versions", [])[0].get("version", ""),
    )


def dump_extension_metadata(extension_id: str, output_folder: str) -> None:
    """Dump extension metadata to a json file."""
    os.makedirs(output_folder, exist_ok=True)
    filename = DUMP_METADATA_FILENAME_PATTERN.format(extension_id=extension_id)
    output_filepath = os.path.join(output_folder, filename)
    command = f"vsce show --json {extension_id}"
    with open(output_filepath, "w") as f:
        subprocess.run(shlex.split(command), stdout=f)


def get_dumped_metadata_files(
    output_folder: str, extensions: List[str], pattern: str = "dump_*_metadata.json"
) -> list:
    """Get dumped metadata files."""
    dumped_metadata_filepaths = glob.glob(os.path.join(output_folder, pattern))
    metadata_filenames = [pattern.replace("*", f"{e}") for e in extensions]
    filepaths = dict()
    for dmf in dumped_metadata_filepaths:
        basename = os.path.basename(dmf)
        if basename in metadata_filenames:
            filepaths[metadata_filenames.index(basename)] = dmf
    # filepaths = dict(
    #     (metadata_filenames.index(os.path.basename(dmf)), dmf)
    #     for dmf in dumped_metadata_filepaths
    #     if os.path.basename(dmf) in metadata_filenames
    # )
    dumped_metadata_filepaths = OrderedDict(sorted(filepaths.items())).values()

    return dumped_metadata_filepaths


def prepare_table(
    dumped_metadata_files: list,
    extensions: list,
    template: dict,
    enforce_lowercase_extension_id: bool = True,
) -> list:
    """Prepare the table."""
    table = []
    table.append(template.get("header"))
    extensions = [e.lower() for e in extensions]
    num_extensions = len(dumped_metadata_files)
    ndigits = len(str(num_extensions))
    for idx, filepath in enumerate(dumped_metadata_files):
        metadata = get_extension_metadata_from_marketplace_dump(filepath)
        extension_id = (
            f"{metadata.get('publisherName')}.{metadata.get('extensionName')}"
        )
        label = metadata.get("displayName")
        description = metadata.get("shortDescription")
        idx_text = f"{idx+1}".zfill(ndigits)
        if extension_id.lower() in extensions:
            # only include the extensions that are in the extension pack
            if enforce_lowercase_extension_id:
                extension_id = extension_id.lower()
            rowdata = template.get("rowdata").format(
                label=label,
                extension_id=extension_id,
                description=description,
                idx=idx_text,
            )
            table.append(rowdata)
    return table


def table_as_markdown(table: list, insert_line_break: bool = False) -> str:
    """Convert the table to markdown."""
    if insert_line_break:
        return "\n".join(table)
    return "".join(table)


class ExtensionPackMetadata:
    """Extension pack metadata."""

    package_json_path: str
    package_data: str
    extensions: str
    num_extensions: int
    extension_id: str
    extension_label: str
    extension_publisher: str
    extension_name: str
    output_folder: str
    table_template: dict = MD_TABLE_TEMPLATE
    table: List[str]

    def __init__(
        self,
        package_json_path: str,
        output_folder: str,
        table_template: Optional[dict] = None,
        readme_path: Optional[str] = None,
    ) -> None:
        self.package_json_path = package_json_path
        self.output_folder = output_folder
        if readme_path is None:
            readme_path = os.path.join(os.path.dirname(package_json_path), "README.md")
        self.readme_path = readme_path
        if table_template is not None:
            self.table_template = table_template
        self._update()

    def get_package_data(self) -> dict:
        """Get package.json data."""
        with open(self.package_json_path, "r") as f:
            package_data = json.load(f)
        if package_data:
            return package_data
        else:
            raise ValueError("Empty package.json")

    def _update(self) -> None:
        """Update package.json data."""
        self.package_data = self.get_package_data()
        self.extensions = self.get_extensions()
        self.num_extensions = len(self.extensions)

        self.extension_label = self._get_extension_label()
        self.extension_publisher = self._get_extension_publisher()
        self.extension_name = self._get_extension_name()
        self.extension_id = f"{self.extension_publisher}.{self.extension_name}"

    def process_data(self, insert_line_break: bool = False) -> None:
        """Process data."""

        self.download_all_extensions_metadata()
        dumped_metadata_files = get_dumped_metadata_files(
            self.output_folder, self.extensions
        )

        self.table = prepare_table(
            dumped_metadata_files, self.extensions, self.table_template
        )
        self.table_md = table_as_markdown(
            self.table, insert_line_break=insert_line_break
        )

    def save_table_output(
        self,
        output_filepath: Optional[str] = None,
        header: Optional[str] = None,
    ) -> None:
        """Save table output."""
        if output_filepath is None:
            output_filepath = os.path.join(self.output_folder, "table.md")
        if header is None:
            header = "# Table Output\n\n"
        with open(output_filepath, "w") as f:
            f.write(header + self.table_md)

    def get_extensions(self) -> list:
        """Get extension list from package.json."""
        return self.package_data.get("extensionPack", [])

    def _get_extension_name(self) -> str:
        """Get extension id (field: ``name``) from package.json."""
        try:
            return self.package_data.get("name")
        except KeyError:
            raise KeyError("Missing 'name' field in package.json")

    def _get_extension_label(self) -> str:
        """Get extension label (field: ``displayName``) from package.json."""
        try:
            return self.package_data.get("displayName")
        except KeyError:
            raise KeyError("Missing 'displayName' field in package.json")

    def _get_extension_publisher(self) -> str:
        """Get extension publisher (field: ``publisher``) from package.json."""
        try:
            return self.package_data.get("publisher")
        except KeyError:
            raise KeyError("Missing 'publisher' field in package.json")

    def download_all_extensions_metadata(self) -> None:
        """Download all extensions metadata."""
        for extension_id in self.extensions:
            dump_extension_metadata(extension_id, self.output_folder)

    def process_readme(self, readme_template_path: Optional[str] = None) -> str:
        """Process template README and create the content of the README file.

        Args:
            readme_template_path (Optional[str], optional): Path to the
                README template file. Defaults to None.

        Returns:
            str: Contents of the README file.
        """
        if readme_template_path is None:
            readme_template_path = os.path.join(
                self.output_folder, README_TEMPLATE_FILENAME
            )

        with open(readme_template_path, "r") as f:
            readme = f.read()

        readme = re.sub("{{ extension_label }}", self.extension_label, readme)
        readme = re.sub("{{ extension_id }}", self.extension_id, readme)
        readme = re.sub("{{ extension_publisher }}", self.extension_publisher, readme)
        readme = re.sub("{{ extension_name }}", self.extension_name, readme)
        readme = re.sub("{{ INSERT_TABLE_HERE }}", self.table_md, readme)

        return readme

    def create_readme(self, output_filepath: Optional[str] = None, **kwargs) -> None:
        """Create README.md."""
        if output_filepath is None:
            output_filepath = os.path.join(self.output_folder, "README.md")
        self.readme = self.process_readme(**kwargs)
        with open(output_filepath, "w") as f:
            f.write(self.readme)

    def cleanup(
        self,
        output_folder: Optional[str] = None,
        filename: str = "dump_*_metadata.json",
        verbose: bool = False,
    ) -> None:
        """Cleanup temporary files."""
        if output_folder is None:
            output_folder = self.output_folder
        if filename is None:
            filename = DUMP_METADATA_FILENAME_PATTERN.replace("{extension_id}", "*")
        elif filename in ["*.*", "all", "*"]:
            filename = "*.*"
        output_filepath = os.path.join(self.output_folder, filename)
        for f in glob.glob(output_filepath):
            os.remove(f)
            if verbose:
                print(f"Removed {f}")

    def replace_readme(
        self,
        target_filepath: Optional[str] = None,
        source_filepath: Optional[str] = None,
        backup_prefix: str = "backup_",
        backup_suffix: str = "",
        verbose: bool = False,
    ) -> None:
        """Replace README.md (target) with the new one (source)."""
        if source_filepath is None:
            source_filepath = os.path.join(self.output_folder, "README.md")
        if target_filepath is None:
            target_filepath = os.path.join(self.readme_path)
        target_filename = os.path.basename(target_filepath)
        backup_filepath = os.path.join(
            os.path.dirname(source_filepath),
            f"{backup_prefix}{target_filename}{backup_suffix}",
        )
        # create backup copy of target README file
        shutil.copyfile(src=target_filepath, dst=backup_filepath)
        # replace target README file with generated README file (source)
        shutil.copyfile(source_filepath, target_filepath)

        if verbose:
            print(
                dedent(
                    f"""\
                Updated README: 
                  source: {os.path.relpath(source_filepath)}
                  target: {os.path.relpath(target_filepath)}
                
                >> NOTE: 
                >> A backup copy of the target README file is available at:
                >> {os.path.relpath(backup_filepath)}
                """
                )
            )


def main():
    """Main function to run the package maker with defaults."""
    # %%
    PROJECT_ROOT = os.path.dirname(HERE)  # type: ignore
    if os.path.basename(PROJECT_ROOT) == "composer":
        PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)  # type: ignore
    sys.path.append(PROJECT_ROOT)
    # %%
    # read sample package.json
    package_json_path = os.path.join(PROJECT_ROOT, "package.json")
    readme_path = os.path.join(PROJECT_ROOT, "README.md")
    output_folder = os.path.join(PROJECT_ROOT, "composer", "staging", "dump")
    readme_template_path = os.path.join(
        PROJECT_ROOT, "composer", "template", "README_TEMPLATE.md"
    )

    # %%
    # create an instance of ExtensionPackMetadata
    epm = ExtensionPackMetadata(package_json_path, output_folder)
    # process data and create markdown table
    epm.process_data(insert_line_break=False)
    epm.save_table_output()

    # %%
    # create README.md
    epm.create_readme(
        output_filepath=os.path.join(output_folder, "README.md"),
        readme_template_path=readme_template_path,
    )

    # cleanup
    epm.cleanup(filename="*.json")
    epm.cleanup(filename="table.md")
    epm.replace_readme(target_filepath=readme_path, verbose=True)
    epm.cleanup(filename="README.md")

    print("DONE!")


# %%
if __name__ == "__main__":
    fire.Fire(
        {
            "epm": ExtensionPackMetadata,
            "genpack": main,
        }
    )
    # fire.Fire()
    # main()

    # %%
