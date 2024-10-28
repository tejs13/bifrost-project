# main.py
import os
from flask import Flask, request, send_file, jsonify
from PIL import Image
import matplotlib.pyplot as plt
from constants import OUTPUT_DIR
from segment import segment_image
from tracking import track_objects_in_stack
from export import export_tracking_data

# Create the output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = Flask(__name__)

@app.route('/segment', methods=['POST'])
def segment_images():
    file = request.files['image']
    image = Image.open(file.stream)
    colored_image = segment_image(image)
    # Save the segmented image
    segmented_image_path = os.path.join(OUTPUT_DIR, 'segmented_image.png')
    plt.imsave(segmented_image_path, colored_image)
    return send_file(segmented_image_path, mimetype='image/png')

@app.route('/track', methods=['POST'])
def track_objects():
    file = request.files['image']
    image_stack = Image.open(file.stream)
    tracking_data = track_objects_in_stack(image_stack)
    tracking_csv_path = export_tracking_data(tracking_data)
    return jsonify({"msg": f"Tracking completed Image saved at: {OUTPUT_DIR}"})

@app.route('/export', methods=['GET'])
def export_data():
    tracking_csv_path = os.path.join(OUTPUT_DIR, 'tracking_data.csv')
    if os.path.exists(tracking_csv_path):
        return jsonify({"msg": f"Exported data successfully: {tracking_csv_path}"})
    else:
        return jsonify({"error": "No tracking data available."}), 404

if __name__ == '__main__':

    # app = create_app()
    app.run(debug=True)
