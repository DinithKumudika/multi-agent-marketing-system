# Automated Agentic Marketing System


### Example Usage

The Goal: A user provides a simple product description and a budget (e.g., "A new AI-powered hiking boot recommendation app, $1000 budget"). 

The system will:

1. Perform market research.

2. Write a professional blog post and a landing page.

3. Generate the code for the landing page.

4. Securely publish the new ad campaign to Google Ads.


### Agents Overview

Here is the breakdown of each agent, the framework it's built on, and its specific role.

#### 1. Agent: **`CampaignOrchestrator`**
- **Framework**: LangGraph

- **Why this Framework?**: LangGraph's unique strength is creating stateful, cyclical graphs. A marketing campaign is not a simple linear (A -> B -> C) process. It involves loops, like Draft -> Review -> Edits -> Draft Again. LangGraph is built to manage this exact kind of stateful, non-linear workflow.

- **Role**: This is the "project manager" and the user's primary contact. It manages the overall state of the campaign (e.g., `RESEARCHING`, ``DRAFTING``, ``IN_REVIEW``, ``CODING``, ``PUBLISHING``). It calls the other agents as "tools" or sub-tasks and manages the flow, especially the review/edit cycles.

- **Tool Integrations**: Its tools are the other agents. It doesn't need external tools itself; its job is to orchestrate.

- **A2A & Authentication**: Acts as the primary A2A "client." It initiates Task requests to the other three agents. It would use simple A2A authentication (like a JWT) to prove to the other agents that its requests are valid.

#### 2. Agent: **``ContentCreationCrew``**
- **Framework**: CrewAI
- **Why this Framework?**: crewAI's superpower is its role-based abstraction. It's designed to make agents collaborate like a real team with defined roles (e.g., Researcher, Writer, Editor). This is perfect for content creation.
- **Role**: This agent is a "sub-team" that, when activated by the `Orchestrator`, produces the final blog post and landing page copy. Internally, it runs its own crew:
  - `MarketResearcher` Agent: Uses a Google Search tool to find keywords, target audience pain points, and competitor articles.

  - `Copywriter` Agent: Takes the research and writes the first draft of the blog post and landing page.

  - `SEO_Editor` Agent: Reviews the draft for tone, clarity, and SEO alignment, sending it back to the Copywriter for revisions.
  
- **Tool Integrations**: Google Search Tool: (Used by the MarketResearcher).
- **A2A & Authentication**: This agent acts as an A2A "server." The `CampaignOrchestrator` sends it a single task (e.g., "Create content for product X"). The ContentCrew handles its internal collaboration and, once its process is complete, returns the final text artifacts.

#### 3. Agent: **`LandingPageDeveloper`**
- **Framework**: Autogen
- **Why this Framework?**: Autogen's key differentiator is its powerful code execution and conversational-coding loop. It excels at tasks involving a `UserProxyAgent` (or a proxy) that can execute code (Python, shell scripts) in a secure Docker environment and report back the results.
- **Role**: This agent's job is to write, execute, and validate code. The `Orchestrator` passes it the final landing page copy from the ContentCrew. This agent (likely a pair of `AssistantAgent` and `UserProxyAgent`):

  1. Writes the HTML, CSS, and basic JS for the landing page.

  2. Executes the code (e.g., runs a Python script to validate the HTML or check for broken links).

  3. If there's an error, it "converses" with itself to fix the bug and re-executes, all within its own loop.
   
- **Tool Integrations**: 

  - **Code Executor**: (Autogen's built-in capability, configured to run in Docker for safety).
  - **File System Tool**: To save the final index.html and style.css files.

- **A2A & Authentication**: Acts as an A2A "server" that exposes a single capability: "CreateWebpage." The `Orchestrator` calls it, and it returns the final, validated code files or a URL to a staging environment.

#### 4. Agent: **`ApiPlatformGateway`**
- **Framework**: ADK
- **Why this Framework?**: The ADK is Google's open-source framework, optimized for the Google ecosystem (Vertex AI, Gemini models) and built for production-ready, secure agents. Its strength is acting as the native, secure bridge to other A2A-compliant services, especially other Google APIs.
- **Role**: This is the most sensitive agent. It is the only one with the credentials to act on the user's behalf. Its job is to take the final landing page URL, the ad copy, and the budget, and create the ad campaign.

- **Tool Integrations**: 
  - **Google Ads API**: To create the campaign, ad group, and ads.
  - **Google Analytics API**: (Optional) To set up a new property or goal for the landing page.
- **A2A & Authentication**: This ADK agent would handle the OAuth 2.0 flow for the user, allowing the user to grant it permission to manage their Google Ads account. The A2A protocol facilitates this. When the `Orchestrator` sends its final Task ("Publish Campaign"), this agent uses its delegated OAuth token to securely create the ad. This demonstrates true agent authentication: the agent isn't just internally authenticated, it is externally authorized to act on a user's behalf.


### Workflow

1. User: "Create a campaign for my AI hiking boot app."

2. `Orchestrator` **(LangGraph)**: Receives request, moves state to `RESEARCHING`. It makes an A2A Task call to the `ContentCrew`.

3. `ContentCrew` **(crewAI)**: (Internal) `Researcher` -> `Writer` -> `Editor`. Process completes. It returns the final text artifacts to the `Orchestrator`.

4. `Orchestrator` **(LangGraph)**: Receives text. Moves state to `IN_REVIEW`. (It could pause here for human-in-the-loop approval). User approves.

5. `Orchestrator` **(LangGraph)**: Moves state to `CODING`. It makes an A2A `Task` call to the `LandingPageDeveloper`, passing the approved copy.

6. `LandingPageDeveloper` **(Autogen)**: (Internal) Writes HTML/CSS -> Executes/Tests -> Fixes Bugs -> Executes/Tests. Process completes. It returns the final code files.

7. `Orchestrator` **(LangGraph)**: Receives code. Moves state to `PUBLISHING`. It makes a final A2A `Task` call to the `AdPlatformGateway`, passing the code, budget, and ad copy.

8. `AdPlatformGateway` **(ADK)**: Receives the task. It uses its pre-authorized OAuth 2.0 token to make a secure API call to the Google Ads API, creating the campaign. It returns the campaign ID.

9. `Orchestrator` **(LangGraph)**: Receives the ID. Moves state to `DONE` and reports the success and campaign ID to the user.

