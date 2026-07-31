from apps.reviews.models import PullRequest
from apps.ai.prompts import (system_prompt, build_review_prompt)


def review_pull_request(pull_request: PullRequest):
    diff = ...
    user_prompt = build_review_prompt(diff)
