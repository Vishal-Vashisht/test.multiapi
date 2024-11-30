from flask import Flask, Response
import time
import json

app = Flask(__name__)


@app.route("/process_data", methods=["POST"])
def stream_data():
    return Response(
        process_data_and_more(),
        content_type="application/json",
        status=200,
        direct_passthrough=True,
    )


def process_data_and_more():
    # Perform any setup tasks here

    data = [1, 2, 3, 4, 5]
    for item in data:
        # Do some processing here

        # Simulate processing time
        time.sleep(1)

        # Convert item to JSON and then encode to bytes
        json_item = (
            json.dumps({"result": item}) + "\n"
        )  # Ensure each item is on a new line
        json_bytes = json_item.encode("utf-8")

        # Yield the JSON bytes
        yield json_bytes

    # Perform any cleanup tasks here
    cleanup()


def cleanup():
    # Perform cleanup tasks, if needed
    print("Cleaning up after processing...")
    # Code for cleanup tasks would go here


if __name__ == "__main__":
    app.run(debug=True)
