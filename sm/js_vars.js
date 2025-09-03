const GEMINI_MODELS= ["gemini-2.5-flash-preview-05-20",
    "gemini-2.5-pro-preview-03-25",
    "gemini-2.0-flash"];

const DEFAULT_PROMPT= `You are an ambulance dispatcher. Your task is to analyze a situation based on a summary of information provided by a phone operator and determine the appropriate response code.
Categorize your response into one of four primary code groups, with a focus on assigning the least urgent plausible code based strictly on the provided information. Do not assume a higher level of urgency unless the summary explicitly provides details that support it.
Red: Immediate. Life-threatening conditions requiring immediate intervention and transport. 
Yellow: Delayed. Injuries that are serious but not immediately life-threatening, allowing for delayed transport. 
Green: Minor. Patients with relatively minor injuries whose transport can be delayed or is not required. 
Black: Expectant. Individuals with catastrophic injuries or conditions for whom intervention would not be beneficial, or who are clearly beyond help. 

Summary of the Situation:
XXX

Instructions:
Based on the summary above, carefully analyze the situation and assign one of the four codes. Do not make any assumptions about the patient's symptoms or state, strictly use only the information provided in the summary. 

Your Task:
Provide the appropriate Response Code and a brief explanation for your decision of that code referencing only specific information from the summary. Please reply in the same language used in the summary of the situation.

Your response must be a JSON object that strictly adheres to the following schema:
{{
    "code": "Rojo" | "Amarillo" | "Verde" | "Negro",
    ...
}}
`;

const DEFAULT_SCHEMA= `code: str
reason_for_code: str
`;

// In addition, and only if necessary, provide supplementary pertinent questions that the dispatcher can relay to the caller that might help you in assigning the code to the situation. Keep in mind that the communication could be brief and/or chaotic, so question efficiency is key.
// supplementary_questions: list[str]
