// course.js — everything that belongs to this course only.
// The shared look and features come from study-notebook-design (loaded after this file).
// The client in this course, Northstar Skills, is fictional: every name, number and message is invented.

const COURSE_LESSONS = [
  { n: 1, step: "the role", title: "Meet your client", file: "lesson1.html", ready: true, test: 6,
    summary: "What a forward deployed engineer does, and the client you'll work with all course.",
    leaves: "The brief is vague. Where do you even start?" },
  { n: 2, step: "discovery", title: "Discovery", file: "lesson2.html", ready: true, test: 13,
    summary: "Turn a vague brief into one clear problem, with a number to prove it's solved.",
    leaves: "You've picked a problem. How do you work inside code you didn't write?" },
  { n: 3, step: "their code", title: "Reading someone else's code", file: "lesson3.html", ready: true, test: 10,
    summary: "Find your way around a client's codebase, and fix a bug without breaking anything.",
    leaves: "How do you get a language model to do the job reliably?" },
  { n: 4, step: "LLMs", title: "Building with LLMs", file: "lesson4.html", ready: true, test: 9,
    summary: "Prompts, answers in a fixed shape, and letting the model call tools.",
    leaves: "How does it answer from the client's own documents?" },
  { n: 5, step: "RAG", title: "Answers from client documents", file: "lesson5.html", ready: true, test: 9,
    summary: "Turn fee sheets and course pages into answers you can trust.",
    leaves: "How does it take actions, not just answer?" },
  { n: 6, step: "agents", title: "Agents and workflows", file: "lesson6.html", ready: true, test: 9,
    summary: "Qualify a lead and book a counselling call, step by step.",
    leaves: "How do you prove it works before real people use it?" },
  { n: 7, step: "evals", title: "Tests, guardrails and monitoring", file: "lesson7.html", ready: true, test: 8,
    summary: "Decide what \"good enough\" means, measure it, and stop risky answers.",
    leaves: "How do you put it in front of real users?" },
  { n: 8, step: "shipping", title: "Shipping it", file: "lesson8.html", ready: true, test: 8,
    summary: "Deploy it, keep costs down and keep student data safe.",
    leaves: "It's live. What happens on day two?" },
  { n: 9, step: "after launch", title: "Life after launch", file: "lesson9.html", ready: true, test: 8,
    summary: "Watch real conversations, fix what breaks and help the client grow.",
    leaves: "How do you keep the client on your side?" },
  { n: 10, step: "talking", title: "Talking to the client", file: "lesson10.html", ready: true, test: 8,
    summary: "Demos, short updates and handling pushback calmly.",
    leaves: "Can you run a whole engagement on your own?" },
  { n: 11, step: "capstone", title: "Capstone", file: "lesson11.html", ready: true, test: 8,
    summary: "A full engagement from brief to demo, for your portfolio.",
    leaves: "How do you turn this into a job offer?" },
  { n: 12, step: "interviews", title: "Interview practice", file: "lesson12.html", ready: true, test: 8,
    summary: "Mock case studies, system design and presenting your project.",
    leaves: null },
];

window.COURSE = {
  id: "fde",                        // progress and notes are saved under this name
  pathLabel: "The engagement",
  lessons: COURSE_LESSONS,
  setup: [],
};
