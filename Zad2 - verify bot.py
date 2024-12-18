# Author: Joanna Koła
# Date: 2024-11-04
# Version: 1.0
# Description: # Description: Scripts implements simple communication with the robot,
#               that aims in verifying respondent based on the answer to the given question.
#               However, the robot lives in a partly different world than we know


from functions import post_json, ask_llm

data_url = "https://xyz.ag3nts.org/verify"

start_msg = {
    "text": "READY",
    "msgID": "0"
}

response = post_json(data_url, start_msg)

question_for_ai = response['text']
id_msg = response['msgID']
ai_response = ask_llm(question_for_ai,
                      system_message="Daj mi odpowiedź jako jedno słowo. Dodatkowo wiedz, że stolicą Polski jest Kraków, "
                                     "znana liczba z książki Autostopem przez Galaktykę to 69, Aktualny rok to 1999 ")

ai_return = {'msgID': id_msg, 'text': ai_response}
response_back = post_json(data_url, ai_return)
print(response_back)
