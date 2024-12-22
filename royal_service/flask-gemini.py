from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gemini_logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model to log Gemini responses
class GeminiLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response_content = db.Column(db.Text, nullable=False)
    finish_reason = db.Column(db.String(20), nullable=False)
    avg_logprobs = db.Column(db.Float, nullable=True)
    prompt_token_count = db.Column(db.Integer, nullable=False)
    candidates_token_count = db.Column(db.Integer, nullable=False)
    total_token_count = db.Column(db.Integer, nullable=False)
    model_version = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize the database
db.create_all()

# 1. Handler to process the response and forward it to Flutter
@app.route('/process_response', methods=['POST'])
def process_response():
    data = request.get_json()

    # Log the response to the database
    log = GeminiLog(
        response_content=str(data['candidates'][0]['content']['parts'][0]['text']),
        finish_reason=data['candidates'][0]['finishReason'],
        avg_logprobs=data['candidates'][0].get('avgLogprobs'),
        prompt_token_count=data['usageMetadata']['promptTokenCount'],
        candidates_token_count=data['usageMetadata']['candidatesTokenCount'],
        total_token_count=data['usageMetadata']['totalTokenCount'],
        model_version=data['modelVersion']
    )
    db.session.add(log)
    db.session.commit()

    # Forward the relevant data to Flutter
    return jsonify({
        "response": data['candidates'][0]['content']['parts'][0]['text'],
        "model_version": data['modelVersion']
    }), 200

# 2. Handler to fetch Gemini logs for the dashboard
@app.route('/get_logs', methods=['GET'])
def get_logs():
    logs = GeminiLog.query.order_by(GeminiLog.timestamp.desc()).all()
    logs_data = [
        {
            "id": log.id,
            "response_content": log.response_content,
            "finish_reason": log.finish_reason,
            "avg_logprobs": log.avg_logprobs,
            "prompt_token_count": log.prompt_token_count,
            "candidates_token_count": log.candidates_token_count,
            "total_token_count": log.total_token_count,
            "model_version": log.model_version,
            "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for log in logs
    ]
    return jsonify(logs_data), 200

# 3. Handler for aggregated log statistics
@app.route('/get_aggregates', methods=['GET'])
def get_aggregates():
    total_logs = GeminiLog.query.count()
    avg_prompt_tokens = db.session.query(db.func.avg(GeminiLog.prompt_token_count)).scalar()
    avg_candidates_tokens = db.session.query(db.func.avg(GeminiLog.candidates_token_count)).scalar()
    total_tokens_used = db.session.query(db.func.sum(GeminiLog.total_token_count)).scalar()

    aggregates = {
        "total_logs": total_logs,
        "avg_prompt_tokens": round(avg_prompt_tokens, 2) if avg_prompt_tokens else 0,
        "avg_candidates_tokens": round(avg_candidates_tokens, 2) if avg_candidates_tokens else 0,
        "total_tokens_used": total_tokens_used if total_tokens_used else 0
    }
    return jsonify(aggregates), 200

# 4. Recommendation: Add a handler to limit usage
@app.route('/check_usage_limit', methods=['GET'])
def check_usage_limit():
    limit = 100000  # Example token limit
    total_tokens_used = db.session.query(db.func.sum(GeminiLog.total_token_count)).scalar()
    total_tokens_used = total_tokens_used if total_tokens_used else 0

    if total_tokens_used > limit:
        return jsonify({"message": "Usage limit exceeded", "tokens_used": total_tokens_used, "limit": limit}), 403
    else:
        return jsonify({"message": "Within usage limit", "tokens_used": total_tokens_used, "limit": limit}), 200

if __name__ == '__main__':
    app.run(debug=True)
