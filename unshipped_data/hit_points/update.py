import csv
import os
import yaml


def update_yaml(file: str, hit_points: int) -> None:
    with open(file, "r") as f:
        data = f.readlines()

    # strip trailing whitespace
    while not len(data[-1]) and len(data) > 0:
        data = data[0:-1]

    # append trailing newline
    if data[-1][-1] != "\n":
        data[-1] += "\n"

    # update, ignore existing hit_points settings
    found = False
    key = "hit_points"
    for line in data:
        if line[0 : len(key) + 1] == f"{key}:":
            line = f"{key}: {hit_points}\n"
            found = True
    if not found:
        data.append(f"{key}: {hit_points}\n")

    with open(file, "w") as f:
        f.writelines(data)


if __name__ == "__main__":
    hit_points_file = os.path.join(os.path.dirname(__file__), "hit_points_data.csv")

    resources_path = os.path.join(os.path.dirname(__file__), "..", "..", "resources")
    resource_type_paths = {
        "ship": "units\\ships",
        "helicopter": "units\\aircraft",
        "plane": "units\\aircraft",
        "vehicle": "units\\ground_units",
    }

    with open(hit_points_file, "r") as file:
        reader = csv.DictReader(file, fieldnames=["type", "name", "hit_points"])
        for line in reader:
            if line["type"] not in resource_type_paths:
                continue
            yaml_file = os.path.join(
                resources_path,
                resource_type_paths[line["type"]],
                f"{line['name']}.yaml",
            )
            if not os.path.exists(yaml_file):
                print(f"Skipping {line['name']} as YAML file could not be found")
                continue
            update_yaml(yaml_file, int(float(line["hit_points"])))
