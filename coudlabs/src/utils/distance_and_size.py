"""
File name: distance_and_size.py
Author: Ehsan Kazemi
Date created: Apr 2023
Date last modified: 05/06/2023
-------------------------------------------------------------------------\
This code calculates the size ratios, distances, and real sizes of       /
objects based on the reference object's height and the camera's focal    \
length.                                                                  /
-------------------------------------------------------------------------\
"""

def distsize_I(data_ref, data_other, real_size_ref, focal_length):
    """
    Parameters:
    - data_ref: The data of the reference object.
    - data_other: The data of the other object.
    - real_size_ref: The real size of the reference object in meters.
    - focal_length: The focal length of the camera in pixels.

    Returns:
    - distance_ref_list: A list of estimated distances of the reference object to the camera.
    - distance_other_list: A list of estimated distances of the other object to the camera.
    - real_size_other_list: A list of estimated real sizes of the other object.
    - common_frame_numbers: A list of frame numbers where both objects are present.
    """
    # Initialize lists to store the calculated values
    distance_ref_list = []
    distance_other_list = []
    real_size_other_list = []
    common_frame_numbers = []

    # Iterate over the data rows
    for i, row_ref in enumerate(data_ref):
        # Get the frame number and the reference object's height
        frame_number_ref = int(row_ref[0])
        height_ref = float(row_ref[4])

        # Search for the corresponding row in the other object's data
        for j, row_other in enumerate(data_other):
            frame_number_other = int(row_other[0])

            # If the frame numbers match, calculate the size ratios, distances, and real sizes
            if frame_number_ref == frame_number_other:
                height_other = float(row_other[4])
                size_ratio = height_other / height_ref
                distance_ref = real_size_ref * focal_length / height_ref
                distance_other = distance_ref * size_ratio
                real_size_other = real_size_ref * size_ratio

                distance_ref_list.append(distance_ref)
                distance_other_list.append(distance_other)
                real_size_other_list.append(real_size_other)
                common_frame_numbers.append(frame_number_ref)

                break

    return distance_ref_list, distance_other_list, real_size_other_list, common_frame_numbers