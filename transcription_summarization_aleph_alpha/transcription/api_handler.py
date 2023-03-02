from aleph_alpha_client import Client, CompletionRequest, Prompt
import re


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
    """Wrapper for the Aleph Alpha Client.
    """
    def __init__(self, token=""):
        self.token = token

    def initialize_client(self, token):
        """Initializes the Aleph Alpha Client with a JWT.

        :param token: Token from Aleph Alpha Account
        :type token: str
        """
        self.client = Client(token=token)

    def complete(self, prompt, model="luminous-extended"):
        request = CompletionRequest(
            prompt=Prompt.from_text(prompt),
            maximum_tokens=200,
        )
        response = self.client.complete(request, model=model)

        return response.completions[0].completion



def summarize_text_using_summarize(client_wrapper: ClientWrapper, text: str):
    """_summary_

    :param text: _description_
    :type text: str
    """
    multiple_splits = False
    # if the text is longer than 400 words we need to split it into multiple prompts
    if len(text.split(" ")) > 400:
        # use the sliding window method.
        # split the text into 5 sentences
        text_split = sliding_window_text(text, amount_of_sentences=5)
        multiple_splits = True

    # first generate the prompt
    text_prompt = (
        """This app gives a short summary from a narrative perspective in German.
        ###Text: Weil wenn der Wind einmal untergreift, du hast keine Chance dagegen. Das geht nicht. Bei dem Sturm sowieso nicht. Wenn man dann so eine Platte trägt und nach oben reichen möchte und so eine Windhöhe kommt, dann haut es einen halt regelmäßig um. What's the plan? Ich guck erst mal, wie das passt, die ersten. Ich weiß auch nicht. Wenn das zu windig ist, dann warten wir auf besseres Wetter.Narrative: Es ist sehr windig, weshalb die Protagonisten überlegen, ob sie mit ihrer Aktivität weitermachen sollen.
        ###Text: Ernst. Da bist du ja. Na endlich. Ernst. Guck mal. Guck mal, ich habe eine Banane. Wo warst du denn? Ich habe dich überall gesucht. Was jetzt folgt, ist das typisch pädagogische Mutter-Kind-Gespräch. Einsicht beim Pubertier, die Puppe, die Mutter, die Mutter. Das ist das typische Mutter-Kind-Gespräch. Einsicht beim Pubertier sollte man aber auch hier nicht erwarten. Ernst, mein Schatz, ich muss dir was sagen. Ernst, du darfst heute nicht mehr auf der Terrasse schlafen. Aber du bist selber schuld. Du hast die ganze Terrasse vollgekackt.
        Narrative: Ernst wurde gesucht von seiner Mutter und es folgt ein typisches Mutter-Kind-Gespräch. Einsicht beim Kind gibt es aber nicht.
        ###
        Text: """
    )
    client_wrapper.initialize_client(token=client_wrapper.token)

    if multiple_splits:
        results = []
        for split in text_split:
            text_prompt += text
            text_prompt += split
            text_prompt +=  """
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

