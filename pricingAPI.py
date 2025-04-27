from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/pricing', methods=['GET'])
def get_pricing():
    drug = request.args.get('drug')
    city = request.args.get('city')
    results = find_top_cheapest_drugs(drug, city)
    return jsonify(results)

if __name__ == '__main__':
    app.run()
