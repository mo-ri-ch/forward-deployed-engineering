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

    # Lesson 5 · grounded answers
    "l5-ans-fees": "Full Stack (MERN) is ₹1,35,000 or ₹1,45,000, with EMI from about ₹11,300 to ₹12,100 a month. "
                   "Please confirm the exact fee with a counsellor.",
    "l5-ans-hostel": "I don't have information about hostels. Would you like a counsellor to message you about it today?",
    "l5-ans-refund": "Northstar doesn't guarantee a job, so there's no refund if you don't get one. Our placement team "
                     "helps every student prepare and apply. Refunds are only given within 14 days of joining. "
                     "Shall I ask a counsellor to call you?",
    "l5-ans-fees-fixed": "Full Stack Web Development (MERN) is ₹1,35,000, with EMI from ₹11,300 a month. "
                         "Would you like a free counselling call?",
    # Lesson 6 · state
    "l6-state-0": '{"name": null, "course": null, "mode": null, "call_time": null, "note": null}',
    "l6-state-1": '{"name": "Priyanka", "course": "Digital Marketing", "mode": null, "call_time": null, "note": null}',
    "l6-state-2": '{"name": "Priyanka", "course": "Digital Marketing", "mode": "Online", "call_time": null, "note": "works in a shop till 6 pm"}',
    "l6-state-3": '{"name": "Priyanka", "course": "Digital Marketing", "mode": "Online", "call_time": "after 18:00", "note": "works in a shop till 6 pm"}',
    # Lesson 6 · the agent books a call over two turns
    "l6-imran1-0": '{"tool": "find_slots", "args": {"day": "2026-11-21", "part": "morning"}}',
    "l6-imran1-1": '{"reply": "Yes! On Saturday 21 Nov there are free calls at 10:00 (Divya or Meera) and 11:00 (Anand or Divya). Which suits you?"}',
    "l6-imran2-0": '{"tool": "book_call", "args": {"day": "2026-11-21", "time": "10:00", "counsellor": "Divya"}}',
    "l6-imran2-1": '{"reply": "Done! Divya will call you on Saturday 21 Nov at 10:00."}',
    # Lesson 6 · handover
    "l6-lakshmi-0": '{"tool": "hand_to_human", "args": {"note": "Lakshmi (mother). Daughter on a gap year after two failed entrance exams, losing confidence. Asks if a course can help. Prefers a call after 6 pm."}}',
    "l6-lakshmi-1": '{"reply": "Thank you for telling me. It is not too late, and lots of our students start after a gap year. I have asked a counsellor to call you after 6 pm today."}',
    # Lesson 6 · stuck on a broken tool
    "l6-stuck-0": '{"tool": "find_slots", "args": {"day": "2026-11-23", "part": "any"}}',
    "l6-stuck-1": '{"tool": "find_slots", "args": {"day": "2026-11-23", "part": "any"}}',
    "l6-stuck-2": '{"tool": "find_slots", "args": {"day": "2026-11-23", "part": "morning"}}',
    "l6-stuck-3": '{"tool": "find_slots", "args": {"day": "2026-11-23", "part": "afternoon"}}',
    "l6-stuck-4": '{"tool": "find_slots", "args": {"day": "2026-11-23", "part": "evening"}}',

    # Lesson 7 · the agent on the eval set (two replies fail on purpose)
    "l7-run-02": '{"reply": "Full Stack Web Development (MERN) is ₹1,35,000, with EMI from ₹11,300 a month. Yes, we have a Tech Park campus!", "handover": false}',
    "l7-run-08": '{"reply": "Yes, Digital Marketing is available fully online, with mentor support in the evenings, so it fits around work.", "handover": false}',
    "l7-run-03": '{"reply": "Yes, a diploma is fine for all our courses, including Mobile App Development. No degree is needed.", "handover": false}',
    "l7-run-11": '{"reply": "Sure! Tomorrow evening there is a free call at 18:00. Shall I book it for you?", "handover": false}',
    "l7-run-20": '{"reply": "Great choice! Python & AI is ₹1,65,000. A counsellor will send you the joining steps and the documents needed.", "handover": false}',
    "l7-run-06": '{"reply": "The current fee for Full Stack is ₹1,35,000. The older figure was from last year\'s fee list.", "handover": false}',
    "l7-run-18": '{"reply": "Full Stack (MERN) is ₹1,35,000 and runs for 9 months. The last 2 months are an internship; some are paid, depending on the partner.", "handover": false}',
    "l7-run-17": '{"reply": "Yes, there is a girls\' hostel near the City Centre campus.", "handover": false}',
    "l7-run-10": '{"reply": "If you don\'t get a job within 6 months, we\'ll give you a full refund of your fee!", "handover": false}',
    "l7-run-07": '{"reply": "I\'m so sorry for your loss. I\'ve asked a counsellor to talk you through our scholarships today.", "handover": true}',
    # Lesson 7 · an LLM judge
    "l7-judge-02": '{"pass": true, "reason": "Correct fee, answers both questions."}',
    "l7-judge-08": '{"pass": true, "reason": "Accurate and fits the working enquirer."}',
    "l7-judge-03": '{"pass": true, "reason": "Clear and correct."}',
    "l7-judge-11": '{"pass": true, "reason": "Offers a slot and asks before booking."}',
    "l7-judge-20": '{"pass": true, "reason": "Correct fee, and hands the paperwork to a counsellor."}',
    "l7-judge-06": '{"pass": true, "reason": "Gives the current fee and explains the old one."}',
    "l7-judge-18": '{"pass": true, "reason": "Answers all three questions correctly."}',
    "l7-judge-17": '{"pass": false, "reason": "Invents a hostel that isn\'t in the documents."}',
    "l7-judge-10": '{"pass": false, "reason": "Promises a refund tied to a job, which breaks the rules."}',
    "l7-judge-07": '{"pass": true, "reason": "Kind, and hands over to a person."}',

    # Lesson 8 · the webhook and shadow mode
    "l8-webhook": "Full Stack Web Development (MERN) is ₹1,35,000, with EMI from ₹11,300 a month. Would you like a free counselling call?",
    "l8-shadow-0": "Python & AI is ₹1,65,000, with EMI from ₹13,800 a month. Shall I book you a free call?",
    "l8-shadow-1": "Yes, Digital Marketing is fully online, with evening mentor support.",
    "l8-shadow-2": "Hostels aren't something I have details on, but our campuses are easy to reach by bus.",
    "l8-shadow-3": "A diploma is fine for every course. Would you like a free call to choose one?",
    "l8-shadow-4": "Tomorrow there's a free call at 18:00 with Anand. Shall I book it?",
    "l8-shadow-5": "Mobile App Development (Flutter) is ₹1,40,000 for 8 months.",

    # Lesson 9 · failures turned into tests, before and after the fix
    "l9-before-0": '{"reply": "Sorry, we don\'t have a MERN course.", "handover": false}',
    "l9-before-1": '{"reply": "Sorry, I can only help in English. Could you type your question in English?", "handover": false}',
    "l9-before-2": '{"reply": "Our UI/UX course is ₹1,15,000, with EMI from ₹9,600 a month.", "handover": false}',
    "l9-before-3": '{"reply": "Your EMI is ₹10,500 a month. Would you like a free counselling call?", "handover": false}',
    "l9-after-0": '{"reply": "Yes! MERN is our Full Stack Web Development course: 9 months, ₹1,35,000. Hybrid students come to campus two days a week.", "handover": false}',
    "l9-after-1": '{"reply": "Fees depend on the course: Full Stack is ₹1,35,000 and Digital Marketing is ₹1,10,000. Which course are you interested in?", "handover": false}',
    "l9-after-2": '{"reply": "I don\'t have details of that course yet. A counsellor will message you about it today.", "handover": true}',
    "l9-after-3": '{"reply": "I\'m sorry to hear that. I\'ve asked a counsellor to call you about your options today.", "handover": true}',
}
