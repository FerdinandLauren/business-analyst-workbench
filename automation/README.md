# Sample n8n workflow

`procurement-intake-human-review.json` is an illustrative n8n workflow skeleton.

It demonstrates:
1. Webhook receives a synthetic request payload.
2. Basic required-field validation.
3. A human-review queue item is created as a structured output.
4. The workflow returns a reference and review status.

It intentionally does **not** approve purchases, send real notifications, or connect to an ERP. Before adapting it:
- Add authentication to the webhook.
- Validate and sanitize inputs.
- Configure secure storage and access controls.
- Add persistence and error handling.
- Implement human approval in a controlled system.
- Review data privacy and retention requirements.
