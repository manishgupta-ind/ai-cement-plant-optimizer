import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import aiplatform

# --- 1. CONFIGURATION ---
# IMPORTANT: Replace these with your actual values from the Vertex AI console
PROJECT_ID = "astute-cumulus-472318-v4"
LOCATION = "us-central1" # Or your region, e.g., 'asia-south1'

# A dictionary mapping KPI names to their respective Vertex AI Endpoint IDs
MODEL_ENDPOINT_IDS = {
    "clinker_free_lime_%": "5608840810238836736",
    # You must update the values with the correct Endpoint IDs after adding them.
    "raw_meal_lsf_ratio": "your-raw-meal-lsf-deployed-model-id",
    "kiln_specific_thermal_energy_Kcal/kg_clinker": "your-kiln-thermal-energy-deployed-model-id",
    "kiln_exit_nox_emissions_mg/Nm3": "your-kiln-nox-deployed-model-id",
    "mill_motor_power_draw_kW": "your-mill-motor-power-deployed-model-id",
    "mill_specific_electrical_energy_kWh/ton_cement": "your-mill-specific-electrical-energy-deployed-model-id",
    "cement_fineness_blaine_cm2/g": "your-cement-fineness-deployed-model-id"
}

# Define the features required for each model, based on the provided documentation
MODEL_FEATURES = {
    "clinker_free_lime_%": [
        "raw_meal_lsf_ratio", "limestone_feed_rate_pct", "clay_feed_rate_pct", 
        "iron_ore_feed_rate_pct", "bauxite_feed_rate_pct", "raw_meal_feed_rate_tph", 
        "fuel_feed_rate_tph", "fuel_alt_substitution_rate_pct", 
        "kiln_hood_pressure_mmH2O", "kiln_burner_air_flow_m3_hr",
        "kiln_main_drive_current_amp"
    ],
    "raw_meal_lsf_ratio": [
        "limestone_feed_rate_pct", "clay_feed_rate_pct", "iron_ore_feed_rate_pct", 
        "bauxite_feed_rate_pct", "raw_meal_feed_rate_tph"
    ],
    "kiln_specific_thermal_energy_Kcal/kg_clinker": [
        "raw_meal_feed_rate_tph", "fuel_feed_rate_tph", "fuel_alt_substitution_rate_pct", 
        "kiln_hood_pressure_mmH2O", "kiln_burner_air_flow_m3_hr", "clinker_feed_rate_tph"
    ],
    "kiln_exit_nox_emissions_mg/Nm3": [
        "fuel_feed_rate_tph", "fuel_alt_substitution_rate_pct", "kiln_burner_air_flow_m3_hr"
    ],
    "mill_motor_power_draw_kW": [
        "clinker_feed_rate_tph", "gypsum_feed_rate_tph", "mill_recirculation_ratio_%"
    ],
    "mill_specific_electrical_energy_kWh/ton_cement": [
        "clinker_feed_rate_tph", "gypsum_feed_rate_tph", "mill_recirculation_ratio_%",
        "mill_motor_power_draw_kW"
    ],
    "cement_fineness_blaine_cm2/g": [
        "mill_recirculation_ratio_%", "mill_motor_power_draw_kW", 
        "clinker_feed_rate_tph", "gypsum_feed_rate_tph"
    ]
}

# --- 2. GLOBAL INITIALIZATION (Best Practice) ---
# Initialize the Vertex AI client once at the global scope.
aiplatform.init(project=PROJECT_ID, location=LOCATION)

# Initialize all required Vertex AI Endpoint objects once at the global scope.
# This prevents the overhead of creating a new object on every request.
global_endpoints = {}
for kpi, endpoint_id in MODEL_ENDPOINT_IDS.items():
    if endpoint_id and not endpoint_id.startswith("your-"):
        global_endpoints[kpi] = aiplatform.Endpoint(endpoint_name=endpoint_id)

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for the frontend to access the API
CORS(app)

def get_vertex_prediction(endpoint: aiplatform.Endpoint, input_data: dict) -> float:
    """
    Sends input data to a specified Vertex AI deployed model and returns the prediction.
    
    Args:
        endpoint (aiplatform.Endpoint): The pre-initialized Vertex AI Endpoint object.
        input_data (dict): The feature-value pairs for the prediction instance.
        
    Returns:
        float: The predicted value, or None if an error occurs.
    """
    try:
        # Format the data for the API request.
        instance = [{key: value for key, value in input_data.items()}]
        
        # The 'predict' method automatically routes the request to the correct model
        response = endpoint.predict(instances=instance)
        
        if response and response.predictions and response.predictions[0] and 'value' in response.predictions[0]:
            prediction = response.predictions[0]['value']
            return prediction
        else:
            print("Vertex AI prediction response was not in the expected format.")
            return None

    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return None

@app.route('/', methods=['POST'])
def predict(request):
    """
    This function handles the HTTP request for the Cloud Run service.
    It takes JSON data, gets predictions, and returns a JSON response.
    """
    try:
        request_json = request.get_json(silent=False)
        if request_json is None:
            raise ValueError("The request body is empty or not a valid JSON.")
        
        predictions = {}
        for kpi in MODEL_ENDPOINT_IDS:
            predictions[kpi] = "N/A"
        
        kpi_to_predict = "clinker_free_lime_%"
        
        # Now, we get the pre-initialized endpoint object from the global dictionary.
        endpoint = global_endpoints.get(kpi_to_predict)
        
        if not endpoint:
            print(f"WARNING: The endpoint for '{kpi_to_predict}' is not configured or initialized. Skipping prediction.")
            predictions[kpi_to_predict] = None
        else:
            required_features = MODEL_FEATURES.get(kpi_to_predict, [])
            input_data = {
                feature: request_json.get(feature) for feature in required_features
            }

            if all(v is not None for v in input_data.values()):
                print(f"Input data to be sent for {kpi_to_predict}: {input_data}")
                # Pass the endpoint object, not the ID string
                predicted_value = get_vertex_prediction(endpoint, input_data)
                predictions[kpi_to_predict] = predicted_value
            else:
                print(f"WARNING: Missing data for KPI '{kpi_to_predict}'. Skipping prediction.")
                predictions[kpi_to_predict] = None
                
        return jsonify(predictions), 200

    except ValueError as ve:
        print(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    # Best practice for Cloud Run: `debug=False` for production deployments.
    # The debug server is not meant for production traffic.
    app.run(host='0.0.0.0', port=port)
