from apps.reviews.models import PullRequest
from apps.ai.prompts import (system_prompt, build_review_prompt)
from apps.ai.services.llm import call_llm
from apps.ai.services.github import get_pr_files


def review_pull_request(pr: PullRequest):
    diff = ...
    user_prompt = build_review_prompt(diff)
    files = get_pr_files(pr)
    diff_parts = []
    for file in files:
        patch = file.get("patch")
        if not patch:
            continue
        diff_parts.append(
                        f"""
        File: {file["filename"]}
        Status: {file["status"]}

        Diff:
        {patch}
        """
        )
    diff = "\n\n".join(diff_parts)
    user_prompt = build_review_prompt(diff)
    res = call_llm(system_prompt,user_prompt)
    return res
