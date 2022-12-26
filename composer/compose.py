# %%
import os
import sys
from vscepackmaker import ExtensionPackMetadata

HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(HERE))

# %%
if __name__ == "__main__":
    PROJECT_ROOT = os.path.dirname(HERE)  # type: ignore
    sys.path.append(PROJECT_ROOT)
    # read sample metadata, downloaded from marketplace
    # datapath = os.path.join(PROJECT_ROOT, ".vscode", "lab", "extn_metadata.json")
    # extension_metadata = get_extension_metadata_from_marketplace_dump(datapath)
    # print(json.dumps(extension_metadata, indent=2))

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
