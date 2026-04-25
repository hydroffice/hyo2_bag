import argparse
import shutil

import h5py
import numpy as np


def is_zero_attr(value) -> bool:
    try:
        return float(value) == 0.0
    except Exception:
        return False


def clone_bag_and_fix_zero_resolution_attrs(src_path: str, dst_path: str) -> None:
    shutil.copy2(src_path, dst_path)

    with h5py.File(dst_path, "r+") as f:
        ds = f["/BAG_root/varres_metadata"]

        resolution_x = np.asarray(ds["resolution_x"], dtype=np.float64)
        resolution_y = np.asarray(ds["resolution_y"], dtype=np.float64)

        # Ignore NaN, inf, and -1 nodata
        valid_x = resolution_x[np.isfinite(resolution_x) & (resolution_x != -1)]
        valid_y = resolution_y[np.isfinite(resolution_y) & (resolution_y != -1)]

        if valid_x.size == 0:
            raise ValueError("No valid values found in resolution_x")

        if valid_y.size == 0:
            raise ValueError("No valid values found in resolution_y")

        computed = {
            "min_resolution_x": float(valid_x.min()),
            "max_resolution_x": float(valid_x.max()),
            "min_resolution_y": float(valid_y.min()),
            "max_resolution_y": float(valid_y.max()),
        }

        print(f"Created clone: {dst_path}")
        print("Checking attributes on /BAG_root/varres_metadata:")

        for attr_name, new_value in computed.items():
            current_value = ds.attrs.get(attr_name, 0.0)

            if is_zero_attr(current_value):
                ds.attrs[attr_name] = new_value
                print(f"  updated {attr_name}: {current_value} -> {new_value}")
            else:
                print(f"  kept {attr_name}: {current_value}")


def main():
    parser = argparse.ArgumentParser(
        description="Clone a BAG file and fix resolution attributes only when currently 0"
    )
    parser.add_argument("input_bag", nargs="?", help="Path to input BAG file")
    parser.add_argument("output_bag", nargs="?", help="Path to output BAG file")
    args = parser.parse_args()

    if not args.input_bag or not args.output_bag:
        raise SystemExit("Please provide input_bag and output_bag, or set them in __main__.")

    clone_bag_and_fix_zero_resolution_attrs(args.input_bag, args.output_bag)


if __name__ == "__main__":
    # Option 1: write file paths here and run the script directly
    input_bag = r"G:\My Drive\_ccom\QC Tools\data\survey\QC Tools 4\BAG_Checks\VR_resolution_is_zero\H11694_MB_VR_MLLW_1of2.bag"
    output_bag = r"G:\My Drive\_ccom\QC Tools\data\survey\QC Tools 4\BAG_Checks\VR_resolution_is_zero\H11694_MB_VR_MLLW_1of2_fixed.bag"

    use_hardcoded_paths = True

    if use_hardcoded_paths:
        clone_bag_and_fix_zero_resolution_attrs(input_bag, output_bag)
    else:
        # Option 2: use command-line arguments
        # Example:
        #   python clone_fix_bag.py input.bag output_fixed.bag
        main()
