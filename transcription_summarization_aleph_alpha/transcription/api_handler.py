from aleph_alpha_client import (
    Client,
    CompletionRequest,
    Document,
    Prompt,
    SummarizationRequest,
)


def sliding_window_text(text, amount_of_sentences=10):
    results = []
    # loop over the text
    # take the length of the text and divide it by the amount of sentences
    amount = int(len(text) / amount_of_sentences)
    for i in range(0, amount_of_sentences):
        # select the amount of sentences but include the last three sentences then move the window
        # make sure that the last sentence is not cut off

        if i == amount_of_sentences - 1:
            selected_texts = text[i * amount :]
        else:
            print(i * amount, (i + 1) * amount + 5)
            selected_texts = text[i * amount : (i + 1) * amount + 5]

        # join the selected texts into a single string
        selected_texts = "".join(selected_texts)

        results.append(selected_texts)

    return results


# initialize the client
class ClientWrapper:
    """Wrapper for the Aleph Alpha Client."""

    def __init__(self, token=None):
        self.token = token

    def initialize_client(self, token):
        """Initializes the Aleph Alpha Client with a JWT.

        :param token: Token from Aleph Alpha Account
        :type token: str
        """
        self.client = Client(token=token)

    def complete(self, prompt, model="luminous-extended"):
        request = CompletionRequest(prompt=Prompt.from_text(prompt), maximum_tokens=200, stop_sequences=["\n", "###"])
        response = self.client.complete(request, model=model)

        return response.completions[0].completion

    def summarize(self, prompt, model="luminous-extended"):
        document = Document.from_text(prompt)
        request = SummarizationRequest(document)
        response = self.client.summarize(request=request, model="luminous-extended")
        summary = response.summary
        return summary


def summarize_text_using_summarize(client_wrapper: ClientWrapper, text: str):
    """Summarizes the Text using the Summarize Endpoint from Aleph Alpha Luminous

    :param client_wrapper
    :type ClientWrapper
    :param text: Text to summarize
    :type text: str
    """
    multiple_splits = False
    # if the text is longer than 400 words we need to split it into multiple prompts
    if len(text.split(" ")) > 400:
        # use the sliding window method.
        # split the text into 5 sentences
        text_split = sliding_window_text(text, amount_of_sentences=5)
        multiple_splits = True

    client_wrapper.initialize_client(token=client_wrapper.token)

    if multiple_splits:
        results = []
        for split in text_split:
            answer = client_wrapper.summarize(split)
            results.append(answer)
        # combine the results
        answer = "\n".join(results)
    else:
        # initialize the client
        answer = client_wrapper.summarize(text)

    return answer


def summarize_text_using_completion(client_wrapper: ClientWrapper, text: str):
    """_summary_

    :param text: _description_
    :type text: str
    """
    multiple_splits = False
    # if the text is longer than 400 words we need to split it into multiple prompts
    if len(text.split(" ")) > 200:
        # use the sliding window method.
        # split the text into 5 sentences
        text_split = sliding_window_text(text, amount_of_sentences=5)
        multiple_splits = True

    # load the prompt from the text file
    with open("prompt.txt") as f:
        text_prompt = f.read()

    client_wrapper.initialize_client(token=client_wrapper.token)

    if multiple_splits:
        results = []
        for split in text_split:
            text_prompt += text
            text_prompt += split
            text_prompt += """
                            Narrative: """
            answer = client_wrapper.complete(text_prompt)
            results.append(answer)
        # combine the results
        answer = "\n".join(results)
    else:
        text_prompt += text
        text_prompt += """
        Narrative: """
        # initialize the client

        answer = client_wrapper.complete(text_prompt)

    return answer
