"""Recorded answers for replay mode, one per notebook step (the label passed to llm.ask).

They're typical of what a model says at each step. A live model's words will differ.
A list means several answers: replay returns them in turn.
"""

RECORDED = {
    # Lesson 4 · a first call, with no rules
    "l4-no-rules": "Hi! Full stack development courses usually cost between ₹50,000 and ₹2,00,000, depending on "
                   "the institute. And yes, with hard work and the right skills, you're sure to get a good job! 😊",

    # Lesson 4 · the same message, with a system prompt
    "l4-with-rules": "Hi! Full Stack Web Development (MERN) is ₹1,35,000, with EMI from ₹11,300 a month. We don't "
                     "promise jobs, but our placement team helps every student prepare and apply. Would you like a "
                     "free counselling call?",

    # Lesson 4 · answers in a fixed shape (JSON)
    "l4-classify-0": '{"intent": "fees", "course": "Full Stack Web Development (MERN)", "needs_human": false}',
    "l4-classify-1": '{"intent": "booking", "course": null, "needs_human": false}',
    "l4-classify-2": '{"intent": "scholarship", "course": null, "needs_human": true}',
    "l4-classify-3": '{"intent": "refund", "course": null, "needs_human": true}',
    "l4-classify-4": '```json\n{"intent": "course_info", "course": "Digital Marketing", "needs_human": false}\n```',

    # Lesson 4 · tools
    "l4-sat-0": '{"tool": "find_slots", "args": {"day": "2026-11-21", "part": "morning"}}',
    "l4-sat-1": '{"reply": "Yes! On Saturday 21 Nov there are free calls at 10:00 and 11:00. Which time suits you?"}',
    "l4-py-0": '{"tool": "get_fee", "args": {"course": "Python & AI"}}',
    "l4-py-1": '{"reply": "Python & AI is ₹1,65,000 for 11 months, with EMI from ₹13,800 a month. '
               'Would you like a free counselling call?"}',
    "l4-both-0": '{"tool": "get_fee", "args": {"course": "Python & AI"}}',
    "l4-both-1": '{"tool": "find_slots", "args": {"day": "2026-11-23", "part": "any"}}',
    "l4-both-2": '{"reply": "Python & AI is ₹1,65,000, with EMI from ₹13,800 a month. On Monday 23 Nov '
                 'there are free calls at 11:00, 15:00 and 18:00. Which suits you?"}',

    # Lesson 4 · temperature
    "l4-temp-low": ["Full Stack is ₹1,35,000, with EMI available.",
                    "Full Stack is ₹1,35,000, with EMI available.",
                    "Full Stack is ₹1,35,000, with EMI available."],
    "l4-temp-high": ["The Full Stack course costs ₹1,35,000, and you can pay in monthly EMIs!",
                     "It's ₹1,35,000 for Full Stack 🎉 EMI is possible too.",
                     "Full Stack is around 1.35 lakh, with easy EMI options."],
}
