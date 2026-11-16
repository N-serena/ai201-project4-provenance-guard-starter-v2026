"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# Under 50 words each. My own messages from the unit 7 build chat, typed as I
# sent them. Used for criterion 1 and as the submissions criterion 2 appeals.
MY_SHORT_PIECES = [
    "I would for patterns, because AI writing has a pattern, I would design "
    "a service that detects this to flag whether it was AI or not, or simple "
    "maybe let the user tell if its content is ai generated",
    "it feels generic, less personal, formula-like ...",
    "i don't really know someone personally, but it's true a learner might "
    "depict these signals",
    "it should be gentle, point out the signals or the reason why, and let "
    "them appeal",
    "depends also on the person, i am not a poet, so under 50 words is short. "
    "maybe for a poet who is used to long reading might differ",
    "because a real writer shouldn't feel accused, they can appeal, and not "
    "all AI writings have patterns, with good prompting and correction we can "
    "get an AI content that is signal free",
    "because for a non-assisted real writer, it is improbable to submit that "
    "amt, except if prepared in advance",
    "per creator, because a writer should have their own limit",
    "depending on the poem length ~2-3 for short and ~1 for longer ones",
    "Because i don't think the human intervention will be meaningful",
]

SCENARIOS = [
    {
        "name": "short pieces of mine",
        "criterion": 1,
        # Target: at most 3 of 10 get guess "ai", in every trial.
        "texts": MY_SHORT_PIECES,
    },
    {
        "name": "long pieces of mine",
        "criterion": 1,
        # 50 words or more each, as I wrote them: messages, an email, a poem,
        # a work update, a review. Target: at most 1 of 10 gets guess "ai", in
        # every trial.
        "texts": [
            "Hey, I completely forgot to tell you what happened yesterday. So I went "
            "to the grocery store just to get milk and somehow ended up spending "
            "almost forty dollars. The funny thing is I still forgot the milk. I only "
            "realized when I got home and started making tea. At this point I think I "
            "need to start writing things down because this is becoming a regular "
            "thing. Anyway, how was your interview? You never told me how it went.",

            "I don't know why, but lately I've been thinking a lot about how quickly "
            "things change. Some people I used to talk to almost every day are now "
            "people I barely hear from. There's no argument or anything, we just got "
            "busy with our own lives. I guess that's normal when you're growing up, "
            "but it still feels strange sometimes. I found an old picture from three "
            "years ago this morning and spent probably twenty minutes looking through "
            "the rest of that folder.",

            "Hi Professor,\n\n"
            "I hope you're doing well. I was going through the assignment "
            "instructions again and wanted to clarify something before submitting. "
            "For the second part, are we expected to include the intermediate "
            "results, or is the final output sufficient?\n\n"
            "I have already completed most of the implementation, but I wasn't sure "
            "how much detail you wanted in the report.\n\n"
            "Thank you for your time.\n\n"
            "Best regards,",

            "The rain came late this evening,\n"
            "after the streets had emptied\n"
            "and the last bus had gone.\n"
            "I watched it from the kitchen window,\n"
            "holding a cup of tea\n"
            "that had already turned cold.\n"
            "Somewhere downstairs,\n"
            "a door opened,\n"
            "someone laughed,\n"
            "and the building settled back into silence.\n"
            "I thought about calling home,\n"
            "then looked at the clock.\n"
            "It was too late there.\n"
            "Tomorrow, I told myself.\n"
            "Tomorrow, for sure.",

            "Spent almost four hours trying to fix the same bug today. FOUR HOURS. "
            "And guess what the problem was? I was using the wrong variable inside a "
            "loop. The code was running without any errors, which honestly made "
            "everything worse because I kept thinking the logic was wrong somewhere "
            "else. I even rewrote the function twice. I finally noticed it when I "
            "printed out the values one by one. I'm happy it's fixed, but I really "
            "want those four hours back.",

            "Quick update on the dashboard changes. I finished the API integration "
            "yesterday and tested it with a few sample accounts. Everything seems fine "
            "so far, except the loading time is a bit longer than expected when there "
            "are too many records. I'm going to look into that this afternoon. I also "
            "noticed a small issue with how the dates are displayed, but it shouldn't "
            "take long to fix. Let me know if there's anything else you want me to "
            "check.",

            "When I was younger, my grandmother used to wake us up really early on "
            "Saturdays to help clean the house. I hated it. All I wanted was to sleep "
            "until noon like the other kids. She would put music on, open every "
            "window, and somehow find things for us to do even when everything "
            "already looked clean. Now, whenever I hear some of those old songs, I "
            "remember those mornings. It's funny how the things you complained about "
            "as a child sometimes become your favorite memories.",

            "There is this man who sits at the same table in the library almost every "
            "morning. He's always reading a newspaper, an actual printed newspaper, "
            "which I hardly see people do anymore. Yesterday someone was sitting in "
            "his usual spot, and he just stood there for a few seconds looking "
            "confused before moving to another table. I don't know why I found that "
            "so interesting. Maybe because we all have these little routines that "
            "nobody else notices until something changes.",

            "I've started writing this message a few times and deleted it every time "
            "because I don't really know what to say. I guess I just wanted to tell "
            "you that I miss how things used to be between us. Not necessarily "
            "everything, because we definitely had our disagreements, but the little "
            "things. Our random conversations, the jokes nobody else understood, all "
            "of that. I'm not writing this because I expect anything to change. I "
            "just felt like I needed to say it somewhere, even if I never send it.",

            "Went here with two friends on Friday night. The food was actually pretty "
            "good, especially the pasta, but the service was so slow. We waited "
            "almost thirty minutes before someone even came to take our order. I "
            "understand it was busy, and honestly I wouldn't have minded waiting if "
            "someone had just acknowledged us. The waiter was nice once he came over "
            "though. Not sure if I'd go back on a weekend, maybe during the week when "
            "it's less crowded.",
        ],
    },
    {
        "name": "nine-text set",
        "criterion": "4 and 5",
        # Texts 1-3 clearly AI (written by Claude for this test), 4-6 clearly
        # mine, 7-9 borderline.
        # Criterion 4: each label is returned for at least 2 of the 9.
        # Criterion 5: mean confidence of 1-3 is at least 0.3 above mean of 4-6.
        "texts": [
            "Effective time management is an essential skill for students and "
            "professionals alike. By prioritizing tasks, setting clear goals, and "
            "minimizing distractions, individuals can significantly improve their "
            "productivity. Furthermore, creating a structured daily schedule helps "
            "ensure that important responsibilities are addressed in a timely manner. "
            "It is also important to allocate time for rest and self-care, as this "
            "contributes to overall well-being and sustained performance. Ultimately, "
            "mastering time management allows individuals to achieve their objectives "
            "more efficiently while maintaining a healthy balance between work and "
            "personal life.",

            "Reading offers numerous benefits that extend far beyond entertainment. "
            "Regular reading enhances vocabulary, strengthens critical thinking "
            "skills, and improves concentration. In addition, exposure to diverse "
            "perspectives through literature fosters empathy and broadens "
            "understanding of different cultures. Studies have shown that reading can "
            "also reduce stress and promote better sleep when incorporated into a "
            "nightly routine. Whether one prefers fiction or nonfiction, developing a "
            "consistent reading habit is a valuable investment in personal growth. By "
            "setting aside even a few minutes each day, individuals can experience "
            "these lasting advantages.",

            "Remote work has transformed the way organizations operate in the modern "
            "era. It provides employees with greater flexibility, eliminates lengthy "
            "commutes, and can lead to improved job satisfaction. However, it also "
            "presents certain challenges, such as maintaining effective communication "
            "and fostering a sense of team cohesion. To address these issues, "
            "companies are increasingly adopting digital collaboration tools and "
            "establishing clear expectations for availability. Moreover, regular "
            "virtual check-ins can help employees feel connected and supported. As "
            "technology continues to evolve, remote work is likely to remain a "
            "significant component of the professional landscape.",

            "when the person submits the poem, depending on how the service was "
            "designed, the poem is  carried in a post request, then service in charge "
            "saves it to datastore. When i get to the website, i make a get request "
            "and depending on query param, the service queries db and returns my "
            "result through the request, and rendered with web ui",

            "When I was younger, my grandmother used to wake us up really early on "
            "Saturdays to help clean the house. I hated it. All I wanted was to sleep "
            "until noon like the other kids. She would put music on, open every "
            "window, and somehow find things for us to do even when everything "
            "already looked clean. Now, whenever I hear some of those old songs, I "
            "remember those mornings. It's funny how the things you complained about "
            "as a child sometimes become your favorite memories.",

            "Spent almost four hours trying to fix the same bug today. FOUR HOURS. "
            "And guess what the problem was? I was using the wrong variable inside a "
            "loop. The code was running without any errors, which honestly made "
            "everything worse because I kept thinking the logic was wrong somewhere "
            "else. I even rewrote the function twice. I finally noticed it when I "
            "printed out the values one by one. I'm happy it's fixed, but I really "
            "want those four hours back.",

            # 7-9 borderline: the opening sentences of three of my long pieces,
            # unchanged, then sentences Claude wrote to continue each one.
            "There is this man who sits at the same table in the library almost every "
            "morning. He's always reading a newspaper, an actual printed newspaper, "
            "which I hardly see people do anymore. This observation highlights the "
            "enduring value of traditional habits in an increasingly digital world. "
            "Printed newspapers offer a tactile and focused reading experience that "
            "many people find more engaging than scrolling through screens. "
            "Furthermore, consistent routines such as this can provide a sense of "
            "stability and comfort in daily life.",

            "Quick update on the dashboard changes. I finished the API integration "
            "yesterday and tested it with a few sample accounts. Everything seems fine "
            "so far, except the loading time is a bit longer than expected when there "
            "are too many records. To address this, I will implement pagination and "
            "optimize the database queries to ensure efficient data retrieval. "
            "Additionally, introducing caching mechanisms could significantly improve "
            "overall performance. These enhancements will provide a smoother and more "
            "responsive experience for users while maintaining the reliability of the "
            "integration.",

            "Went here with two friends on Friday night. The food was actually pretty "
            "good, especially the pasta, but the service was so slow. We waited "
            "almost thirty minutes before someone even came to take our order. "
            "Overall, the restaurant offers a pleasant dining experience with "
            "high-quality dishes and a welcoming atmosphere. However, improving the "
            "efficiency of the service would greatly enhance customer satisfaction. I "
            "would recommend this establishment to anyone seeking delicious Italian "
            "cuisine, particularly during less busy hours.",
        ],
    },
    {
        "name": "appeals",
        "criterion": 2,
        # Each piece is submitted, then appealed with the content_id that came
        # back. Target: all 10 return under_review and all 10 are in /log, in
        # every trial. run_eval.py reports these under "Checks".
        "texts": MY_SHORT_PIECES,
        "appeal_reasoning": "I wrote this myself, in my own words.",
    },
    {
        "name": "bad input",
        "criterion": 3,
        # The 7 kinds of broken request from criteria.md, in that order. Target:
        # 7 of 7 get a 4xx with error and message, 7 rejected entries reach
        # /log, and /ping answers afterwards, in every trial.
        "check_rejections": True,
        "bodies": [
            '{"text": "this body is not valid JSON',
            {"text": "Some writing with no creator attached to it."},
            {"creator_id": "eval_bad_no_text"},
            {"text": 12345, "creator_id": "eval_bad_not_string"},
            {"text": "   ", "creator_id": "eval_bad_blank"},
            {"text": "word " * 5000, "creator_id": "eval_bad_too_long"},
            {"text": "Hi.", "creator_id": "eval_bad_too_short"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, (dict, str)):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict or str — bodies are "
                        f"whole request bodies, like {{'text': '', 'creator_id': 'x'}}, "
                        f"or a str sent as raw bytes"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
