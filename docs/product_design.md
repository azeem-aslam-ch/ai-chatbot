# AI Customer Support Chatbot - Product Design

## 1. User Persona
**The Customer (End-User):**
- **Demographics:** Varied, looking for immediate help on the "Antigravity Services" website.
- **Pain Points:** Needs quick answers to common questions without waiting for a human agent. Wants a simple, intuitive interface that works seamlessly on mobile and desktop.
- **Goals:** Resolve issues, find information about services, or easily escalate to a human if necessary.

**The Business Owner (Admin):**
- **Goals:** Reduce support ticket volume, provide 24/7 basic support, and maintain brand voice.
- **Needs:** A system that is easy to deploy, reliable (high uptime), and secure.

## 2. Chatbot Use Cases
1. **General Inquiry:** The user asks about services, pricing, or company background. The chatbot responds using its generalized knowledge and system prompt settings.
2. **Account Assistance:** The user asks how to reset a password or update billing. The chatbot provides step-by-step generic instructions.
3. **Escalation:** The user expresses frustration or asks a complex, specific question. The chatbot apologizes and advises the user to contact the human support team via email/phone.

## 3. Functional Requirements
- **Real-time Interaction:** The chat must feel instantaneous and responsive, featuring a typing indicator when generation is in progress.
- **Aesthetics & UI:** The interface must be modern, using a dark-mode theme, smooth animations, and clear typography (Inter font).
- **Backend Processing:** The backend must efficiently proxy requests to the OpenAI API, stream or handle responses, and handle errors gracefully.
- **Resilience:** If the AI API fails, the user must receive a friendly, non-technical error message.
