# Paradox-HA

## How Can I Run the Assignment?

1. Enter your OpenAI key in the `.env` file.
2. Install dependencies: `pip install -r requirements.txt` (This make take 1-2 mins, due to LangChain).
3. Execute the `main.py` file: `python main.py`
4. Profit.

## Documentation

### Generation of GenAI Summer Camp Details

The generated information can be found in the `task1.txt` file.

### Creating the Assistant with LLM

You can locate all the prompts within the `main.py` file, spanning from lines 26 to 73.

As I approached the assignment, my objectives were to develop a solution that is not only straightforward but also highly scalable. Consequently, I chose to build the assistant using LangChain, widely recognized as the top tool for AI engineering.

The user initiates a conversation with a chatbot that focuses solely on recognizing the user's intent, disregarding unrelated requests. Once the router identifies the relevant intent, it triggers the appropriate function, activating another chatbot equipped with the right prompt, either for a Q&A session or the application process. When either of these processes is completed, providing the necessary assistance, the chat session ends.

Additionally, the Q&A session utilizes Retrieval Augmented Generation (RAG). This approach involves retrieving external data, in this case from `Task1.txt`, and incorporating it into the generation step, allowing for the handling of extensive datasets that may exceed the contextual length of the LLM.

Moreover, the application process is segmented into individual steps for a smoother user experience. The application prompt manages this procedure, ensuring a user-friendly interaction.

### Techniques Used

- [Formalizing Prompts](https://learnprompting.org/docs/basics/formalizing)
- [Generated Knowledge](https://learnprompting.org/docs/intermediate/generated_knowledge)
- [Instruction Defense](https://learnprompting.org/docs/prompt_hacking/defensive_measures/instruction)

## Open Questions

### How Would You Optimize the Process if You Had More Time?

**Short-term:**

1. Integrate the router into the end of the Q&A and Application process for fluidity between user requests.
2. Implement more anti-prompt hacking techniques such as the ["Separate LLM Evaluation"](https://learnprompting.org/docs/prompt_hacking/defensive_measures/llm_eval) technique.
3. Enhance the consistency of the assistant using techniques such as the ["Prompt Ensembling"](https://learnprompting.org/docs/reliability/ensembling) technique, as it is still susceptible to jailbreaks.

**Long-term:**

Introduce "prompt tuning" by using soft prompts and continuous prompts to go beyond what is possible with human-created prompts. For more information, refer to the following recent research papers on the subject:
1. ["PROMPT WAYWARDNESS: The Curious Case of Discretized Interpretation of Continuous Prompts"](https://arxiv.org/pdf/2112.08348.pdf)
2. ["The Power of Scale for Parameter-Efficient Prompt Tuning"](https://arxiv.org/pdf/2104.08691.pdf)

### How Would You Test the Prompts' Performance?

I would create as many edge cases as possible to be automatically checked each time a prompt is updated, similar to the way traditional QA automation teams in tech companies work today.

### What Edge Cases Do You Think Are Not Handled Currently That You Would Add?

**Edge cases:**
1. Switching between Q&A and the application process mid-process.
2. Handling "trolling" or jailbreaking - a simple "unsubscribe" method might have solved this issue (similarly, this was handled in the Olivia chatbot - image attached below!). 
3. In the application process, allowing users to go backward to "update" information.


!["unsubscribe" method](https://i.imgur.com/oODjatf.jpeg)
