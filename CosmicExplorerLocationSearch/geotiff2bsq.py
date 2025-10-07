# Distributed under the MIT License.
# See LICENSE for details.

import argparse
import sys

from CosmicExplorerLocationSearch import Geotiff


def main():
    """Convert a geotiff file to BSQ format."""
    helptext = """Convert a geotiff file to BSQ (Band Sequential) binary format.
    
    This tool converts geotiff files to BSQ format, which is suitable for
    direct reading into memory without the overhead of geotiff metadata.
    """
    
    p = argparse.ArgumentParser(prog='geotiff2bsq', description=helptext)
    p.add_argument('input', help="Path to input geotiff file")
    p.add_argument('output', help="Path to output BSQ file")
    
    args = p.parse_args()
    
    try:
        Geotiff.geotiff_to_bsq(args.input, args.output)
        print(f"Successfully converted {args.input} to {args.output}")
    except Exception as e:
        print(f"Error converting file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main() 