# pip install --upgrade ultralytics
# pip install -r path/to/sewer_defects/ultralytics/requirements.txt

import ultralytics
ultralytics.checks()
from ultralytics import YOLO
import os
import datetime
    
def train(model_name, project_root, **kwargs):
    
    # Get data file path
    current_directory = os.getcwd()
    coudlabs_directory = os.path.abspath(os.path.join(current_directory, "../..")) # two levels up
    yaml_file_path = os.path.join(coudlabs_directory, "data/data.yaml")
    
    # Check if the yaml file exists
    if not os.path.exists(yaml_file_path):
        raise FileNotFoundError("The data yaml file does not exist.")

    # Load a model
    model = YOLO(model_name)

    # Save the results to the trained_models folder
    trained_models_folder = os.path.join(project_root, 'coudlabs/trained_models')  # specify the base folder where trained models are saved
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")   # generate a subfolder name based on the current date and time
    subfolder_name = f"model_{current_datetime}"
    results_path = os.path.join(trained_models_folder, subfolder_name)  # create the full path to the subfolder
    os.makedirs(results_path, exist_ok=True)  # make sure the subfolder exists, or create it if necessary
    
    # Train model with user-specified arguments
    results = model.train(data=yaml_file_path, project=trained_models_folder, name=subfolder_name, **kwargs)

    # Evaluate model performance on the validation set
    val_metrics = model.val(project=trained_models_folder, name=subfolder_name)

    # Export model
    model.export(format="onnx")

    print("\nResults saved to ", results_path)
    
    return results_path, results, val_metrics