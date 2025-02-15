from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Path to the JSON file
WORDS_JSON_FILE = '/Users/ricoxu/Desktop/webTest/words.json'

# Load existing data from the JSON file
def load_data():
    if os.path.exists(WORDS_JSON_FILE):
        with open(WORDS_JSON_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save data to the JSON file
def save_data(data):
    with open(WORDS_JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Remove a word from the specified period in the JSON data
def remove_data(data, period, word):
    if period in data and word in data[period]:
        del data[period][word]  # Remove the word
        return True  # Indicate success
    return False  # Indicate failure (word or period not found)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', periods=data.keys(), data=data)

@app.route('/add', methods=['POST'])
def add_word():
    period = request.form.get('period')  # Selected period
    word = request.form.get('word')     # Word input
    definition = request.form.get('definition')  # Definition input
    date = request.form.get('date')     # Date input
    types = request.form.get('types')   # Types input (as a JSON string)

    if period and word and definition and date and types:
        data = load_data()
        if period in data:
            # Convert types from JSON string to a Python list
            types_list = json.loads(types)

            # Add the word with its definition, date, and types list to the selected period
            data[period][word] = [definition, int(date), types_list]
            save_data(data)  # Save the updated data
    return jsonify({"status": "success", "message": f"Added '{word}' to '{period}'."})

@app.route('/remove', methods=['POST'])
def remove_word():
    period = request.form.get('period')  # Selected period
    word = request.form.get('word')     # Word to remove

    if period and word:
        data = load_data()
        if remove_data(data, period, word):  # Remove the word
            save_data(data)  # Save the updated data
            return jsonify({"status": "success", "message": f"Removed '{word}' from '{period}'."})
        else:
            return jsonify({"status": "error", "message": f"Word '{word}' not found in '{period}'."}), 404
    return jsonify({"status": "error", "message": "Invalid input."}), 400

if __name__ == '__main__':
    app.run(debug=True)