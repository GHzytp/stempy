import numpy as np


def convert_data_format(data, scan_positions, scan_shape, frame_shape,
                        from_version, to_version):
    """Convert the data and return new (data, scan_positions) as a tuple"""
    if from_version == to_version:
        return data, scan_positions

    if from_version == 1 and to_version == 2:
        return convert_data_v1_to_v2(data, scan_positions, scan_shape)

    msg = f'Conversion not implemented: {from_version} => {to_version}'
    raise NotImplementedError(msg)


def convert_data_v1_to_v2(data, scan_positions, scan_shape):
    if not is_data_v1_format(data, scan_shape):
        # This means there are no duplicate values in the frames and
        # therefore no difference between the versions.
        return data, scan_positions

    # Remove any duplicates and place them in their own rows.
    scan_positions = np.arange(len(data))
    ret = np.empty(len(scan_positions), dtype=object)

    # Place duplicates in separate frames
    extra_rows = []
    extra_scan_positions = []
    for i, row in enumerate(data):
        unique, counts = np.unique(row, return_counts=True)
        ret[i] = unique

        # Ensure counts can be negative
        counts = counts.astype(np.int64) - 1
        while np.any(counts > 0):
            extra_rows.append(unique[counts > 0])
            extra_scan_positions.append(scan_positions[i])
            counts -= 1

    if extra_rows:
        # Resize the data and add on the extra rows
        new_size = ret.shape[0] + len(extra_rows)
        new_data = np.empty(new_size, dtype=object)
        new_data[:ret.shape[0]] = ret
        new_data[ret.shape[0]:] = extra_rows
        new_scan_positions = np.append(scan_positions,
                                       extra_scan_positions)

        ret = new_data
        scan_positions = new_scan_positions

    return ret, scan_positions


def is_data_v1_format(data, scan_shape):
    # If the data array is longer than the number of scan positions,
    # it must be v2 format or greater.
    if len(data) > np.prod(scan_shape):
        return False

    # Check if any rows contain duplicates. If so, it must be v1 format.
    # If not, then there is no difference between the v1 and v2 formats.
    return any(len(np.unique(x)) != len(x) for x in data)
