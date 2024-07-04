# Deploying the Telegram Bot on Google Colab

This guide provides step-by-step instructions to set up and run the Telegram bot on Google Colab.

## Steps

### 1. Create a New Notebook in Google Colab

1. Go to [Google Colab](https://colab.research.google.com/).
2. Click on **"New Notebook"**.

### 2. Install the Necessary Libraries

Run the following command to install the required libraries:

```python
!pip install python-telegram-bot nest_asyncio
```

### 3. Copy and Paste the Code

Copy the code commented in your chosen language from the repository and paste it into a code cell in Google Colab.

### 4. Replace the Token

Replace `'your-key'` with your bot token provided by BotFather.

### 5. Run the Notebook

Click on **"Runtime"** in the menu and select **"Run all"**.

---

This will start the Telegram bot, which will be ready to respond to the `/start` and `/time` commands.
