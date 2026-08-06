from apps.reviews.models import PullRequest
from apps.ai.models import AIReview
from apps.ai.services.github import get_pr_files
from apps.ai.services.llm import call_llm
from apps.ai.services.parser import parser_ai_response
from apps.ai.prompts import system_prompt, build_review_prompt


def review_pull_request(pr: PullRequest):
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
    print("RAW GEMINI RESPONSE:")
    print(repr(res))
    result = parser_ai_response(res)
    print(result, "RESULT...............")
    review, created = AIReview.objects.update_or_create(
        pull_request=pr,
        defaults={
            "summary": result["summary"],
            "strengths": result["strengths"],
            "issues": result["issues"],
            "suggestions": result["suggestions"],
            "score": result["score"],
            "status": "completed",
            "model_name": "gemini-3.5-flash-lite",
        },
    )
    return review
