from gpt_tool.gpt_tool import ConwayGPTTool 

if __name__ == "__main__":
    tool = ConwayGPTTool()

    prompts = [
        "How many generations will the word ‘brayden’ return from the Conway tool?",
        "How many generations will the word ‘Brayden’ return from the Conway tool?",
        "Generate 3 random words and tell me the highest Conway score.",
        "What is the meaning of life?"
    ]
    for prompt in prompts:
        response = tool.handle_prompt(prompt)
        print(f"Prompt: {prompt}\nResponse: {response}\n")
        print("\n\n\n\n\n\n")