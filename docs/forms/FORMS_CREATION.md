# Agent Tasks,  Forms
This document describes how to set up a new form for an agent-service.

## Prerequisites
Be sure to have full agent-service's file structure:
* /<agent_name>_service
    * __init__.py
    * <agent_name>_service.py
    * settings.conf
    * /agent_tasks


## Basic Form's Structure
First of all, you need to add a new form (.json file) to `agent_tasks` folder.
Please, name it adequate: if it is going to conquer the world name it `world_conquer_task.json`.

The next thing is the file's content.
It consist of:
* **description** that appears in the list of tasks for an element,
* and the **input** form
    * **title** that appears in the form's header
    * **indexed input fields**, a list of fields to fill in by a user
        * **index** that defines the order for the input field, [1..n]
        * **input element**, question or textbox data (will be described later)

Here's an example:
```
{
  "agentTask": {
    "description": str,
    "input":
    {
      "title": str,
      "indexedInputFields": [
        {
          "index": int
          "inputElement":
          {
            // <input_field_specific_data>
          }
        },
        // ...
      ]
    }
  }
}
```

### Input-fields
For now, there are 2 arch-types of input fields:
1. Question tat can be:
    * single choice
```
"inputElement": {
  "question": {
    "text": "*whispering* What's the colour of night?",
    "questionType": "SINGLE_CHOICE",
    "questionAnswers": [
      {
        "answer": "Sanguine, my brother!",
        "isGolden": true
      },
      {
        "answer": "RGB: #030112",
        "isGolden": false
      },
      // ...
    ]
  }
}
```
    * dropdown
```
"inputElement": {
  "question": {
    "text": "Choose for whom will you draw a sword of yours?"
    "questionType": "DROPDOWN",
    "questionAnswers": [
      {
        "answer": "The King of Kings, The God of Men!",
        "isGolden": false
      },
      {
        "answer": "The Darkness that shall not end!",
        "isGolden": false
      },
      {
        "answer": "The Nothingness, The Time, The Space!",
        "isGolden": true
      },
      {
        "answer": "The No-And-Any-One, Its Face!",
        "isGolden": false
      }
    ]
  }
}
```
    * multiple choice
```
"inputElement": {
  "question": {
    "text": "What is/are the thing(s) a human can have?",
    "questionType": "MULTIPLE_CHOICE",
    "questionAnswers": [
      {
        "answer": "a body",
        "isGolden": true
      },
      {
        "answer": "a life",
        "isGolden": false
      },
      {
        "answer": "a choice",
        "isGolden": true
      },
      // ...
    ]
  }
}
```
2. Textbox
```
"inputElement": {
  "textbox": {
    "placeholder": "Once you have everything this world can suggest, what else will you do?",
    "goldenText": "To live a life; once more, once more...",
    "isMultiline": true
  }
}
```

## Form's submission
After you've done with the template, you want to have your form on the site.
For his you need to upload it to the back-end, just send a [POST-request](https://apiary.com/agentdata/<AgentDataID>).
It can be done however you want, but preferable method is to use Agents->Add option from `agents_platform/cli.py`
**IMPORTANT** note is that you need to get **AgentData's ID**.
If you don't have one, use GET-request to retrieve, but here you will need **Agent's UID** (user ID).
You can find it <the method how to find agent's UID>.
