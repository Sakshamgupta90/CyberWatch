from json import loads, JSONDecodeError
from io import StringIO
from requests import post, exceptions
from pandas import DataFrame, read_csv
from flask import Flask, request, render_template, url_for, redirect,jsonify

app = Flask(__name__)

@app.route('/results', methods=['GET'])
def results():
    predicted_data = request.args.get('predicted')

    try:
        # Attempt to load JSON data
        predicted = DataFrame.from_dict(loads(predicted_data))
        print(f"Predicted data received: {predicted}")  # Add this line for debugging
    except JSONDecodeError as e:
        # Handle JSON decoding error
        print(f"Error decoding JSON: {e}")
        predicted = DataFrame()

    return render_template('results.html', predicted=predicted)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            file = request.files['log_file'].read()
            df = read_csv(StringIO(file.decode('utf-8')), sep=',')

            # Debug print statement to check the data being sent
            print(f"Data sent to /predict: {df}")

            response = post("http://localhost:5000/predict", json={"features": df.to_json(orient='records')})

            # Debug print statement to check the response
            print(f"Response from /predict: {response.status_code} - {response.text}")

            # Check if the response is successful (status code 200)
            if response.status_code == 200:
                predicted = response.json()
                print(f"Received predicted data: {predicted}")

                # Debug print statement to check the redirect URL
                redirect_url = url_for('results', predicted=predicted)
                print(f"Redirect URL: {redirect_url}")

                return redirect(redirect_url)
            else:
                print(f"Unexpected response status code: {response.status_code}")

        except exceptions.RequestException as e:
            # Handle request exception
            print(f"Request exception: {e}")

    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    print("Reached /predict route")
    try:
        data = request.get_json()

        # Assuming 'data' is a list of dictionaries, each representing a row of your DataFrame
        df = DataFrame.from_records(data)
        print(f"Data received for prediction: {df}")  # Add this line for debugging

        # Perform your prediction logic here using the received data
        # Replace the following line with your actual prediction code
        predicted_result = {"example_key": "example_value"}

        return jsonify(predicted_result)
    except Exception as e:
        # Handle exceptions appropriately, e.g., log the error
        print(f"Error during prediction: {e}")
        return jsonify({"error": "An error occurred during prediction"}), 500  # HTTP status code 500 for internal server error

if __name__ == '__main__':
    app.run(debug=True, port=3000)
