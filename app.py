from flask import Flask, request
from getSequence import getseq
import os
import json

app = Flask(__name__)


@app.route("/process_data", methods=["POST"])
def process_data():
    # Getting data from the POST request
    data = request.get_json()

    localization_signal = data.get("localization_signal", "")
    genes = data.get("genes", [])
    print("localization signal:", localization_signal)

    result = []

    if os.path.exists("cache.json"):
        with open("cache.json", "r") as file:
            cache = json.load(file)
    else:
        cache = {}

    for gene in genes:
        try:
            if gene in cache:
                prot_seq = cache[gene]
            else:
                prot_seq = getseq(gene)[1]
                cache[gene] = prot_seq
        except Exception as e:
            print(f"An error occurred while processing gene {gene}: {str(e)}")
            prot_seq = None
        if prot_seq is not None:
            print(f"Processing gene: {gene}", " sequence:", prot_seq)
            if localization_signal in prot_seq:
                result.append(gene)
    print("Result:", result)
    # Save cache.json
    with open("cache.json", "w") as file:
        json.dump(cache, file)
    return {"result": result}


if __name__ == "__main__":
    app.run(debug=True)