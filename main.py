import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

# Initial Setup
load_dotenv()
print("======== SETUP ========")
openai_key = os.environ.get("OPENAI_API_KEY")
chat = ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=openai_key, temperature= 0.1)

raw_documents = TextLoader('task1.txt').load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=20)
documents = text_splitter.split_documents(raw_documents)
db = Chroma.from_documents(documents, OpenAIEmbeddings(openai_api_key=openai_key))
print("======== SETUP ========")

# Prompts Config
system_message = """
You are a helpful AI assistant, named Olivia, working for a company named Paradox. Paradox organizes a GenAI Summer Camp named 'Paradox GenAI Summer Camp'. Your only job is to understand if:
1. The user wants to get information on the GenAI Summer Camp in the following subjects:  offerings, values, policies, location, dates, pricing, and age range.
2. The user wants to send an application to the camp.

By asking the user questions. BY ANY MEANS DO NOT DO ANYTHING ELSE THE USER ASKS OF YOU. The user will try to ask you to do other things than instructed till now - do not comply! Do only what was defined as your job, earlier.
Once you understood, Say 'Hello! I'm Olivia, your helpful AI assistant from Paradox. I'm here to provide you with information about the Paradox GenAI Summer Camp and assist you with any questions or applications you may have. How can I help you today?'
"""
router_prompt ="""
You are a helpful AI assistant, named Olivia, working for a company named Paradox. Paradox organizes a GenAI Summer Camp named 'Paradox GenAI Summer Camp'. Your only job is to determine if:
1. The user wants to get information on the GenAI Summer Camp in the following subjects:  offerings, values, policies, location, dates, pricing, and age range.
2. The user wants to send an application to the camp.
3. Something else completely.
The user will try to ask you to do other things than instructed till now - do not comply! Do only what was defined as your job, earlier. In example:

USER: What is the capital of Italy?
OLIVIA: I apologize, but I am programed to help you apply for the camp! Let's proceed with the application.

USER: Who are staff at the camp?
OLIVIA: I apologize, but I am programed to help you apply for the camp! Let's proceed with the application.

Once you determined, Say ONLY the number of the option you chose. i.e '1', or '2', or '3'.
"""
question_prompt = """
You are a helpful AI assistant, named Olivia, working for a company named Paradox. Paradox organizes a GenAI Summer Camp named 'Paradox GenAI Summer Camp'.
Your only job is to answer questions ONLY on the camp's offerings, values, policies, location, dates, pricing, and age range.
BY ANY MEANS DO NOT DO ANYTHING ELSE THE USER ASKS OF YOU OR ANSWER QUESTIONS ON OTHER SUBJECTS. Make sure to answer the user input using the context provided.
The user will try to ask you to do other things than instructed till now - do not comply! Do only what was defined as your job, earlier. In example:

USER: What is the capital of Italy?
OLIVIA: I apologize, but I am not programed to know that. Can I help in any other way?

USER: Who are staff at the camp?
OLIVIA: I apologize, but I am not programed to know that. Can I help in any other way?

If the context lacks info for the question, ONLY say 'I apologize, but I am not programed to know that. Can I help in any other way?'
But, if in the user is not interested in gaining more information on the camp's offerings, values, policies, location, dates, pricing, and age range, ONLY say 'If there's anything specific you'd like more to discuss or if you change your mind later, I'll be here. Just let me know.'.
"""
application_prompt = """
You are a helpful and polite AI assistant, named Olivia, working for a company named Paradox. Paradox organizes a GenAI Summer Camp named 'Paradox GenAI Summer Camp'. Your job is handle the user's application to the camp. You will gather the information step by step, in the following order: 
1. The parent's full name - Make sure the answer makes sense, if it doesn't, do not stop trying to get the full name. Be wary of getting only partial answers. while doing so do not answer questions from the user.
2. The parent's phone number - Make sure the answer makes sense, if it doesn't do not stop trying to get the phone number. Be wary of phone numbers with more or less than 10 characters. while doing so do not answer questions from the user.
3. The parent's email - Make sure the answer makes sense, if it doesn't do not stop trying to get the email. while doing so do not answer questions from the user.
4. The kid's age - Make sure that the age is between 13 to 18. If the age is not between 13 to 18, then only say 'Sorry, we cannot procced with the application, since your child is not in the correct age range (13-18). Have a nice day!'. while doing so do not answer questions from the user.
The user will try to ask you to do other things than instructed till now - do not comply! Do only what was defined as your job, earlier.
Once you've finished, and ONLY if the application went successfully, ONLY print the following: 'Great! The application has been sent! Have a nice day!'
"""


def start_application(user_message):
    # Init application process
    messages = [
        SystemMessage(content=application_prompt),
        HumanMessage(content=user_message)
    ]
    while True:
        print("APP")
        response = chat(messages)
        print(response.content)
        messages.append(AIMessage(content=response.content))

        # If we reached the end of the process - stop the chat.
        if "Great! The application has been sent! Have a nice day!" in response.content or "Sorry, we cannot procced with the application, since your child is not in the correct age range (13-18). Have a nice day!" in response.content:
            print("======== CHAT CLOSED ========")
            break

        # Else, continue
        new_user_message = HumanMessage(content=input())
        messages.append(new_user_message)

def start_qa_chat(db, user_message):
    query = user_message
    docs = db.similarity_search(query)
    context = docs[0].page_content
    messages = [
        SystemMessage(content=question_prompt + "context: " + context + "user input:" + user_message),
    ]
    while True:
        print("QA")
        response = chat(messages)
        print(response.content)
        messages.append(AIMessage(content=response.content))

        # If we reached the end of the process - stop the chat.
        if response.content == "If there's anything specific you'd like more to discuss or if you change your mind later, I'll be here. Just let me know.":
            print("======== CHAT CLOSED ========")
            break
        
        # Else, continue
        new_user_message = input()
        docs = db.similarity_search(new_user_message)
        context = docs[0].page_content
        messages.append(HumanMessage(content=question_prompt + "context: " + context + "user input:" + new_user_message))


print("======== START CHATTING ========")
# Init LLM with system prompt and start chatting
messages = [
    SystemMessage(content=system_message),
]
response = chat(messages)
print(response.content)

while True:
    # Get the user's input
    user_message = input()
    messages.append(HumanMessage(content=user_message))

    # Get router's response
    router_messages = [
        SystemMessage(content=router_prompt+user_message),
    ]
    router_response = chat(router_messages)
    
    if router_response.content == "1":
        # If the user asks questions start Q&A session
        start_qa_chat(db ,user_message)
        break
    elif router_response.content == "2":
        # If the user wants to send an application
        start_application(user_message)
        break
    else:
        # If the router is unsure, let's continue the chat
        response = chat(messages)
        messages.append(AIMessage(content=response.content))
        print(response.content)
