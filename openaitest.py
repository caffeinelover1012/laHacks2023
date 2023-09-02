import os
import openai
import json
openai.api_key = "YOUR_API_KEY_HERE"

text = """In computer science, binary search, also known as half-interval search,[1] logarithmic search,[2] or binary chop,[3] is a search algorithm that finds the position of a target value within a sorted array.[4][5] Binary search compares the target value to the middle element of the array. If they are not equal, the half in which the target cannot lie is eliminated and the search continues on the remaining half, again taking the middle element to compare to the target value, and repeating this until the target value is found. If the search ends with the remaining half being empty, the target is not in the array.

Binary search runs in logarithmic time in the worst case, making 
(
log
)
O(\log n) comparisons, where 
n is the number of elements in the array.[a][6] Binary search is faster than linear search except for small arrays. However, the array must be sorted first to be able to apply binary search. There are specialized data structures designed for fast searching, such as hash tables, that can be searched more efficiently than binary search. However, binary search can be used to solve a wider range of problems, such as finding the next-smallest or next-largest element in the array relative to the target even if it is absent from the array.

There are numerous variations of binary search. In particular, fractional cascading speeds up binary searches for the same value in multiple arrays. Fractional cascading efficiently solves a number of search problems in computational geometry and in numerous other fields. Exponential search extends binary search to unbounded lists. The binary search tree and B-tree data structures are based on binary search.
"""
num_questions=3
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-16k",
  messages=[
    {
      "role": "user",
      "content": f"Given the following text: {text}, generate {num_questions} multiple choice questions in a json format with the following keys: question_text, correct_answer, incorrect_answers. There should only be 3 incorrect answers and one correct answer. Return only the valid json response. "
    }
  ],
  temperature=0.5,
  max_tokens=1024,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

y= (response.choices[0].message.content)

x = json.loads(y)['questions']
for question in x:
    print(question['question_text'])
    print(question['correct_answer'])
    for i in question['incorrect_answers']:
        print(i)
    print()
