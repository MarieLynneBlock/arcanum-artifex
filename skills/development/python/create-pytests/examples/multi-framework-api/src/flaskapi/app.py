from __future__ import annotations

import logging

from flask import Flask, jsonify, request

from flaskapi.models import Item, _items


def _configure_logging(app: Flask) -> None:
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)


def create_app() -> Flask:
    app = Flask(__name__)
    _configure_logging(app)

    @app.errorhandler(404)
    def not_found(e):  # noqa: ANN001
        return jsonify({"error": "not found"}), 404

    @app.route("/items", methods=["GET"])
    def list_items():
        return jsonify([item.to_dict() for item in _items.values()])

    @app.route("/items/<int:item_id>", methods=["GET"])
    def get_item(item_id: int):
        item = _items.get(item_id)
        if item is None:
            return jsonify({"error": "not found"}), 404
        return jsonify(item.to_dict())

    @app.route("/items", methods=["POST"])
    def create_item():
        data = request.get_json(force=True, silent=True) or {}
        try:
            item = Item.from_dict(data)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        item.save()
        return jsonify(item.to_dict()), 201

    @app.route("/items/<int:item_id>", methods=["DELETE"])
    def delete_item(item_id: int):
        item = _items.pop(item_id, None)
        if item is None:
            return jsonify({"error": "not found"}), 404
        return "", 204

    return app
