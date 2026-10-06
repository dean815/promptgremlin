---
family: jev
kind: tool
last_verified: 2026-10-05
sources: [models, primitives]
---
## All models
- A Jev "prompt" is not prose. It is a JSON request body with `model`, `state` (the material to judge), and `questions` (a map of id to question). Output that JSON, not a chat message. (primitives#Define a question, #Ask multiple questions together)
- Question ids are not sent to the model. Put the complete meaning in `instructions`. (primitives#Define a question)
- Each question has `type`, `instructions`, and usually `criteria`. `choice`: one of an unordered set (criteria is an object of option to meaning). `score`: position on ordered levels (criteria is an ordered list, each level self-explanatory). `noul`: clean yes/no (criteria optional). (primitives#Define a question, #Choose a question type)
- Always include an `other` or `none` option in a choice; answers can only be supplied options. (primitives#Choose a question type, #What comes back)
- One snap judgment per question, one a person makes in a second. Split anything needing analysis into small questions; the calling code combines and weights them. (primitives#Ask for one snap judgment per question, #Split a complex judgment into several questions)
- Questions run in parallel and cannot see each other. Never write one that depends on another; a truly dependent one is a second request, noted outside the JSON. (primitives#When one question depends on another)
- Extra questions are nearly free; include ones that matter only for some inputs. Use one `noul` per label when several can apply. (primitives#Ask speculative questions, #Choose a question type)
- Every question carries `instructions` and `criteria`; a `noul`'s criteria defines yes; use a `score` with defined levels for degree. (primitives#Choose a question type)
- Point at parts of a structured state with backticked dot-paths such as `ticket.messages[0].text` inside `instructions`. (primitives#Reference specific fields)
- State is text only (string, JSON object, or array of text); convert images and audio to text first. English works best. (models#Current models, #Language support)
- Worked shape (invented):
```json
{
  "model": "jev-latest",
  "state": { "review": "Arrived late, box crushed, works fine." },
  "questions": {
    "topic": {
      "type": "choice",
      "instructions": "What is the main complaint in `review`?",
      "criteria": {
        "shipping": "Delivery or packaging",
        "product": "The item is faulty",
        "other": "Neither"
      }
    },
    "wants_refund": {
      "type": "noul",
      "instructions": "Does `review` ask for a refund?",
      "criteria": "Yes if it asks for money back"
    },
    "anger": {
      "type": "score",
      "instructions": "How angry does the writer sound in `review`?",
      "criteria": ["Neutral", "Mildly irritated", "Clearly upset", "Furious"]
    }
  }
}
```

## jev-1-13-0
- Send it as `"model": "jev-1.13.0"` (dots) to pin this version, or `jev-latest` to follow the newest stable release; the alias can change answers when a release ships. `jev-preview` can run ahead of `jev-latest`; it is the same model for now. (models#Aliases)
- Budget: 64k tokens per request covering `state` plus all questions, and 32k for `state` plus the single longest question, so keep state and each question's `instructions` compact. (models#Current models)
