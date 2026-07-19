from outliner import outline_create
from writter import writter
from editer import Editer
from analyzer import Analyzer
import json


async def pipeline(topic):

    print("Starting async pipeline...")

    # ---------------- OUTLINE ----------------
    outline = await outline_create(topic)
    print("Outline done")

    outline_analyzer = await Analyzer(outline)
    print("outline_analyzer", outline_analyzer)
    analysis = json.loads(outline_analyzer)

    while not analysis["Approved"]:

        print("analysis:", analysis["Approved"])
        print("Need better outline...")

        outline = await outline_create(analysis["Feedback"])
        outline_analyzer = await Analyzer(outline)
        analysis = json.loads(outline_analyzer)

    # ---------------- ARTICLE ----------------
    article = await writter(outline)
    print("Writing done")

    article_analysis = await Analyzer(article)
    analysis = json.loads(article_analysis)

    while not analysis["Approved"]:

        print("Article needs improvement...")
        article = await writter(analysis["Feedback"])

        article_analysis = await Analyzer(article)
        analysis = json.loads(article_analysis)

    # ---------------- EDITING ----------------
    final = await Editer(article)
    print("Editing done")

    final_analysis = await Analyzer(final)
    analysis = json.loads(final_analysis)

    while not analysis["Approved"]:

        print("Final edit needed...")

        final = await Editer(analysis["Feedback"])
        final_analysis = await Analyzer(final)
        analysis = json.loads(final_analysis)

    # ---------------- FINAL RETURN ----------------
    return final
