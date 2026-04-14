from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal, Optional

load_dotenv()

model = ChatOpenAI(model = "gpt-4o-mini")

class Review(BaseModel):
    key_themes: list[str] = Field(description="write down all the key themes discussed in the review in a list")
    summary: str = Field(description="A concise summary of the review, no more than 50 words")
    sentiment: Literal["pos", "neg", "neu"] = Field(description="The overall sentiment of the review, either positive, negative, or neutral")
    pros: Optional[list[str]] = Field(default=None, description="The pros of the product mentioned in the review, if any")
    cons: Optional[list[str]] = Field(default=None, description="The cons of the product mentioned in the review, if any")
    name: Optional[str] = Field(default=None, description="The name of the reviewer, if mentioned in the review")

structured_output = model.with_structured_output(Review)

result = structured_output.invoke(
    "I recently purchased the XYZ headphones and I am really impressed with the sound quality. The bass is deep and the highs are clear. However, I found the ear cushions to be a bit uncomfortable after long listening sessions. Overall, I would recommend these headphones for their excellent sound quality, but be aware of the comfort issue."
)

print(result.name)