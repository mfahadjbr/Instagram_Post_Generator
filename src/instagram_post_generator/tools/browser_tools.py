import json
import os
import requests
from crewai import Agent, Task
from langchain.tools import tool
from bs4 import BeautifulSoup
from crewai.llm import LLM

class BrowserTools:

    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content. Pass a full URL like 'https://google.com'."""
        url = f"https://chrome.browserless.io/content?token={os.getenv('BROWSERLESS_API_KEY')}"
        payload = json.dumps({"url": website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}

        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code != 200 or not response.text:
            return "Failed to retrieve content. Please check the URL or API key."

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text(separator='\n\n')

        content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []

        for chunk in content_chunks:
            agent = Agent(
                role='Principal Researcher',
                goal='Analyze and summarize the given content accurately.',
                backstory="You're a researcher summarizing web content.",
                llm=LLM(model=os.getenv('MODEL', 'gpt-4')),
                allow_delegation=False
            )

            task = Task(
                description=f'Analyze and summarize the following content:\n\n{chunk}',
                expected_output="A concise summary including all key points.",
                agent=agent
            )

            summary = task.execute()
            summaries.append(summary)

        final_summary = "\n\n".join(summaries)
        return f"\nScraped Content:\n{final_summary}\n"
