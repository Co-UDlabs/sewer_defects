'''
The code reads the data from the text files, compares the sizes of the 
two objects in each frame (where both objects are present), calculates 
the distance of the reference object (usually a joint) from it's real 
size (m) and its size on the image (pixels), then calculates change in 
the image sizes of both objects, calculates the ratio between the change
in the image sizes, an finally estimates the distance of the second 
object from the camera as well as its size.
'''

def distsize(data_ref, data_other, real_size_ref, focal_length):

    # Extract the frame numbers from each file
    frame_numbers_ref = set(int(row[0]) for row in data_ref)
    frame_numbers_other = set(int(row[0]) for row in data_other)

    # initialise
    image_size_other_prev = None
    image_size_ref_prev = None
    distance_ref_list = []
    distance_other_list = []
    real_size_other_list = []
    
    # Find the common frame numbers
    common_frame_numbers = frame_numbers_ref.intersection(frame_numbers_other)
    
    # Iterate over the common frame numbers
    for frame_number in common_frame_numbers:
        # Find the rows with the matching frame number in each file
        matching_rows_ref = [row for row in data_ref if int(row[0]) == frame_number]
        matching_rows_other = [row for row in data_other if int(row[0]) == frame_number]

        # Perform operations on the matching rows
        for ref, other in zip(matching_rows_ref, matching_rows_other):
            
            # Extract the relevant information from the rows and perform operations
            image_size_ref = float(ref[4])
            image_size_other = float(other[4])

            # ref real distance
            distance_ref = (real_size_ref * focal_length) / image_size_ref
            distance_ref_list.append(distance_ref)

            if image_size_ref_prev is not None and image_size_other_prev is not None:

                # image size change for ref and other object
                image_size_change_ref = image_size_ref - image_size_ref_prev
                image_size_change_other = image_size_other - image_size_other_prev
            
                if image_size_change_ref != 0 and image_size_change_other != 0:
                    # ratio of image size change
                    image_size_change_ratio = image_size_change_ref / image_size_change_other
            
                    # estimate distance of other object to camera
                    distance_other = distance_ref * image_size_change_ratio
                    distance_other_list.append(distance_other)
            
                    # estimate real size of other object
                    real_size_other = distance_other * image_size_other / focal_length
                    real_size_other_list.append(real_size_other)

            # set current as prev for next interation
            image_size_ref_prev = image_size_ref
            image_size_other_prev = image_size_other

    return distance_ref_list, distance_other_list, real_size_other_list, common_frame_numbers